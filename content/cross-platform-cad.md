---
title: The search for cross-platform CAD software
date: 2026-09-03
category: Blogs
summary: My opinions on the current state of parametric modelling software.
tags: CAD
---

Linux is generally a well-supported platform for technical hobby projects. For programming-related projects, the experience is first-class with an abundance of tools, utilities and frameworks sometimes exclusively supported on Linux. There's Blender for 3D modelling & sculpting, Krita, Inkscape and GIMP? for drawing, and KiCAD for PCB and schematic design. For 3D printing, all popular slicing programs are open source and cross-platform thanks to the amazing project Slic3r.

But when it comes to actually designing parametric models for 3D printing, the options are extremely limited. FreeCAD is the most popular CAD modelling tool on Linux, and while it's getting better I still don't see it becoming my daily driver any time soon, due to its relatively unintuitive interface and missing support for features I take for granted ([why is selecting the midpoint of a line while sketching so convoluted?](https://forum.freecad.org/viewtopic.php?p=722122&sid=3a13126671fa134c3e8507fc579be461#p722122)). Onshape is unique in that it offloads all calculations and complex rendering to its server with your browser acting as a remote viewer, so it can run anywhere. But this means it won't work without a stable internet connection. Also all projects you create with the free tier are public, which I don't like at all even though my designs aren't proprietary or confidential by any means and it's probably me being paranoid for no reason. I guess I just like my data to be in my control.

All other programs (except TinkerCAD I guess) are strictly Windows-only. This is most likely because their mature codebases are already waist-deep in low level Windows APIs, and making them cross-platform is too much of a hassle without breaking everything. Of course most of them have exorbitant licensing fees and no free tier, making them impractical for hobby projects.

So my current solution is running Solid Edge inside a Windows 11 VMware host. This is one of the good ones that offers a no-strings-attached Community Edition with a self-contained offline installer (although I haven't checked if it performs some sort of "community edition license check" during installation). I only encountered one major obstacle during this entire process, and it's not even the CAD program. VMware's installation procedure has been an absolute mess since it was acquired by Broadcom, and it could get worse any day. I can't ditch it yet because it's the only virtualization software that provides hardware-accelerated drivers out of the box. Since I have a laptop, I can't dedicate an entire GPU to the VM. And running Solid Edge without hardware-accelerated drivers on QEMU or VirtualBox turns it into a slideshow.

Maybe the situation will improve, maybe it won't. In the meantime, I should probably learn FreeCAD.