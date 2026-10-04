---
title: Bluetooth Latency Test
date: 2026-10-04
category: Blogs
summary: I had Copilot make me a web app to measure bluetooth device latency.
tags: vibecoding, personal projects
---

!!! note "TLDR"
    I made a web app to measure latency of your bluetooth devices, you can try it out [here](resources/latency-test.html).

Lately I've been using VSCode and Copilot to quickly create simple apps for my specific niche use cases. Yesterday I wanted to measure the latency of my bluetooth earphones. I quickly found a bunch of websites online, but all of them rely on the user pressing a button after hearing an audio signal. While some of them perform a "calibration run" at the beginning to measure the user's reaction time so it can be subtracted from the later measurements, I still wasn't confident with the accuracy of the results, since your reaction time can vary slightly between two measurements.

My idea was to have a light that flashes at a fixed tempo along with an audio ding. Ideally, both the visual and auditory cues will be in sync. When using a bluetooth devices that introduces latency, the audio will be delayed. The user can then move a slider to offset the light flashing until the light and sound are once again in sync. The duration by which the flashing light was offset is the latency of the user's bluetooth device.

I gave this to Copilot as a prompt, and it pretty quickly created an implementation of it in a single HTML file. I had a couple of back-and-forths with the model to get it to look and behave just how I wanted, but I'm pretty happy with the result. Although I could have implemented something functionally identical without AI with my current Javascript knowledge, there's no way I could make the UI as good looking.

You can try it out [here](resources/latency-test.html). Also since it's just an HTML file, you can download it to your computer and use it completely offline (although you might want to remove the site header).
