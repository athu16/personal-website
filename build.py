"""
build.py

Usage:
    python build.py
"""

import argparse
from datetime import datetime
import re
import shutil
import sys
from pathlib import Path
import markdown
import frontmatter

MARKDOWN_EXTENSIONS = [
    "extra", "codehilite", "toc", "sane_lists", "admonition", "smarty", "markdown_katex", "pymdownx.details",
]
MARKDOWN_EXTENSION_CONFIGS = {
    "codehilite": {"guess_lang": False},
    "toc": {"permalink": False},
    "katex": {
        "no_subtitles": True,
        "insert_fonts_css": True, # Ensures math symbols render perfectly
    },
}

def convert_markdown(md_text: str) -> str:
    md = markdown.Markdown(
        extensions=MARKDOWN_EXTENSIONS,
        extension_configs=MARKDOWN_EXTENSION_CONFIGS,
        output_format="html5",
    )
    return md.convert(md_text)

def render_template(text: str, context: dict) -> str:
    def replacer(match):
        key = match.group(1).strip()
        if key in context:
            return str(context[key])
        return match.group(0)

    return re.sub(r'\{\{\s*([a-zA-Z0-9_]+)\s*\}\}', replacer, text)

def format_date(date_val) -> str:
    """Helper to convert dates into standard 'Nov 22, 2025' string format."""
    if isinstance(date_val, (datetime, str)):
        try:
            if isinstance(date_val, str):
                dt = datetime.fromisoformat(date_val)
            else:
                dt = date_val
            return dt.strftime("%b %d, %Y")
        except ValueError:
            return str(date_val)
    return ""

def process_file(input_path: Path, output_dir: Path, content_dir: Path, template_dir: Path) -> dict:
    post = frontmatter.load(input_path)
    metadata = post.metadata
    raw_content = post.content

    # Defaults
    metadata.setdefault("title", input_path.stem.replace("-", " ").title())
    metadata.setdefault("lang", "en")
    metadata.setdefault("theme", "brutalist")
    metadata.setdefault("category", "General")
    metadata.setdefault("tags", [])
    metadata.setdefault("date", "")
    metadata.setdefault("summary", "")

    layout_name = metadata.get("layout", "base.html")

    # Relative path calculations for working links
    rel_path = input_path.relative_to(content_dir)
    out_path = output_dir / rel_path.with_suffix('.html')
    web_link = "/" + str(rel_path.with_suffix('.html')).replace("\\", "/")

    # Extract tags list or format if string
    tags = metadata.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",")]

    tags_html = "".join([f'<span class="tag-pill">#{t.lstrip("#")}</span>' for t in tags])
    metadata["tags_html"] = tags_html

    # Substitute content variables
    rendered_content = render_template(raw_content, metadata)

    # Markdown -> HTML conversion
    if input_path.suffix == '.md':
        content_html = convert_markdown(rendered_content)
    else:
        content_html = rendered_content

    # Inject into layout template
    layout_path = template_dir / layout_name
    if not layout_path.exists():
        print(f"Warning: Template '{layout_name}' not found. Falling back to raw content.", file=sys.stderr)
        final_html = content_html
    else:
        layout_text = layout_path.read_text(encoding="utf-8")
        metadata["content"] = content_html
        final_html = render_template(layout_text, metadata)

    # Write output file
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(final_html, encoding="utf-8")
    print(f"Built post: {out_path}")

    # Return article info for the homepage index builder
    return {
        "title": metadata["title"],
        "category": metadata["category"],
        "date": metadata["date"],
        "date_str": format_date(metadata["date"]),
        "summary": metadata["summary"],
        "tags": tags,
        "url": web_link,
        "file_path": input_path
    }

def generate_index_card(article: dict) -> str:
    """Generates an HTML card for an article on the homepage grid."""
    category = article["category"]

    # Pick badge colors matching your mockup's design system
    cat_lower = category.lower()
    if "programming" in cat_lower or "code" in cat_lower:
        cat_style = 'style="background: var(--text); color: var(--surface);"'
    elif "literature" in cat_lower or "analysis" in cat_lower:
        cat_style = 'style="background: var(--accent-2); color: #fff;"'
    elif "hardware" in cat_lower or "repair" in cat_lower:
        cat_style = 'style="background: var(--accent-3); color: #fff;"'
    else:
        cat_style = 'style="background: var(--accent); color: var(--text);"'

    # Format tag pills
    tags_html = "".join([f'<span>#{t.lstrip("#")}</span>' for t in article["tags"]])

    return f"""
        <a href="{article['url']}" class="article-card">
          <div class="card-top">
            <span class="category" {cat_style}>{category}</span>
            <span>{article['date_str']}</span>
          </div>
          <div class="card-body">
            <h3>{article['title']}</h3>
            <p>{article['summary']}</p>
            <div class="card-footer">
              {tags_html}
            </div>
          </div>
        </a>"""

def build_homepage(articles: list, template_dir: Path, output_dir: Path):
    """Populates index.html dynamically with generated posts and sidebar counts."""
    index_template_path = template_dir / "index.html"
    if not index_template_path.exists():
        index_template_path = Path("index.html") # Fallback to root index.html

    if not index_template_path.exists():
        print("Warning: index.html template not found. Skipping homepage generation.")
        return

    # Sort articles newest-first
    sorted_articles = sorted(
        articles,
        key=lambda x: str(x.get("date", "")),
        reverse=True
    )

    # Build Article Grid HTML
    grid_html = "\n".join([generate_index_card(art) for art in sorted_articles])

    # Count categories for sidebar
    categories_count = {}
    for art in sorted_articles:
        cat = art["category"]
        categories_count[cat] = categories_count.get(cat, 0) + 1

    # Build Sidebar Directory List HTML
    sidebar_html = f'<a href="#" class="active">All Articles <span class="count">[ {len(sorted_articles):02d} ]</span></a>\n'
    for cat, count in sorted(categories_count.items()):
        sidebar_html += f'          <a href="#">{cat} <span class="count">[ {count:02d} ]</span></a>\n'

    index_html = index_template_path.read_text(encoding="utf-8")

    # Replace the mockup placeholder elements
    # 1. Replace directory list
    index_html = re.sub(
        r'<div class="directory-list">.*?</div>',
        f'<div class="directory-list">\n          {sidebar_html.strip()}\n        </div>',
        index_html,
        flags=re.DOTALL
    )

    # 2. Replace articles grid
    index_html = re.sub(
        r'<div class="articles-grid">.*?</div>',
        f'<div class="articles-grid">\n{grid_html}\n      </div>',
        index_html,
        flags=re.DOTALL
    )

    # Save generated index.html to output/
    out_index = output_dir / "index.html"
    out_index.write_text(index_html, encoding="utf-8")
    print(f"Built Homepage: {out_index}")

def copy_static_assets(template_dir: Path, output_dir: Path):
    """Copies static files (like style.css) from templates/ to output/."""
    css_file = template_dir / "style.css"
    if css_file.exists():
        shutil.copy(css_file, output_dir / "style.css")
        print("Copied: style.css -> public/style.css")

def main() -> int:
    parser = argparse.ArgumentParser(description="Build the static site.")
    parser.add_argument("--content", type=Path, default=Path("content"), help="Content directory")
    parser.add_argument("--templates", type=Path, default=Path("templates"), help="Templates directory")
    parser.add_argument("--output", type=Path, default=Path("public"), help="Output directory")
    args = parser.parse_args()

    if not args.content.exists():
        print(f"Error: Content directory '{args.content}' not found.", file=sys.stderr)
        return 1

    args.output.mkdir(parents=True, exist_ok=True)

    # Copy CSS and assets
    copy_static_assets(args.templates, args.output)

    # Process all Markdown and HTML files
    content_files = list(args.content.rglob("*.md")) + list(args.content.rglob("*.html"))
    articles = []

    for file_path in content_files:
        # Avoid processing index.html inside content if it exists
        if file_path.name == "index.html":
            continue
        article_info = process_file(file_path, args.output, args.content, args.templates)
        articles.append(article_info)

    # Build dynamic index.html page
    build_homepage(articles, args.templates, args.output)

    print(f"\nSite built successfully in '{args.output}'!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
