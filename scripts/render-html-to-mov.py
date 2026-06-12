#!/usr/bin/env python3
"""
Render a standalone HTML animation to a transparent ProRes 4444 MOV.

Usage:
    python3 render-html-to-mov.py \
        --input  animations/MyAnim.html \
        --output animations/out/MyAnim.mov \
        --duration 8.0 \
        --fps 30 \
        --width 1920 \
        --height 1080
"""

import argparse
import asyncio
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from playwright.async_api import async_playwright


async def render(html_path: Path, output_path: Path, duration: float, fps: int,
                 width: int, height: int, bg_color: str) -> None:
    frames_dir = Path(tempfile.mkdtemp(prefix="anim_frames_"))
    frame_ms = 1000 / fps
    total_frames = int(duration * fps)

    print(f"Input:    {html_path}")
    print(f"Output:   {output_path}")
    print(f"Size:     {width}×{height}  |  {fps}fps  |  {duration}s  |  {total_frames} frames")

    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--disable-web-security"])
        context = await browser.new_context(viewport={"width": width, "height": height})
        page = await context.new_page()

        await page.goto(f"file://{html_path.resolve()}", wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)

        # Strip page background so Playwright omit_background works correctly
        await page.evaluate(f"""
            () => {{
                document.body.style.background = 'transparent';
                document.documentElement.style.background = 'transparent';
                const viewport = document.getElementById('viewport');
                if (viewport) viewport.style.background = 'transparent';

                const target = '{bg_color}'.toLowerCase();
                if (target) {{
                    for (const el of document.querySelectorAll('*')) {{
                        const bg = window.getComputedStyle(el).backgroundColor;
                        // Convert hex to rgb for comparison — simple approach
                        const r = parseInt(target.slice(1,3),16);
                        const g = parseInt(target.slice(3,5),16);
                        const b = parseInt(target.slice(5,7),16);
                        if (bg === `rgb(${{r}}, ${{g}}, ${{b}})` || bg === `rgba(${{r}}, ${{g}}, ${{b}}, 1)`) {{
                            el.style.backgroundColor = 'transparent';
                        }}
                    }}
                }}

                // Hide play/start overlays and controls
                for (const id of ['start', 'controls', '__bundler_thumbnail', '__bundler_loading']) {{
                    const el = document.getElementById(id);
                    if (el) el.style.display = 'none';
                }}
            }}
        """)

        # Silence audio to avoid AudioContext errors in headless mode
        await page.evaluate("""
            () => {
                const noop = () => ({});
                const noopPromise = () => Promise.resolve();
                const fakeNode = () => ({
                    connect: noop, start: noop, stop: noop,
                    frequency: { setValueAtTime: noop, exponentialRampToValueAtTime: noop },
                    gain: { setValueAtTime: noop, exponentialRampToValueAtTime: noop },
                    Q: { value: 0 }, type: '',
                });
                const fakeCtx = {
                    createBufferSource: () => ({ ...fakeNode(), buffer: null }),
                    createBuffer: (ch, len, sr) => ({ getChannelData: () => new Float32Array(len) }),
                    createBiquadFilter: fakeNode,
                    createGain: fakeNode,
                    createOscillator: fakeNode,
                    destination: {},
                    currentTime: 0,
                    sampleRate: 44100,
                    state: 'running',
                    resume: noopPromise,
                };
                window.AudioContext = function() { return fakeCtx; };
                window.webkitAudioContext = window.AudioContext;
            }
        """)

        # Start the animation
        await page.evaluate("""
            () => {
                // Try the most common trigger function names
                if (typeof run === 'function') { run(); return; }
                if (typeof start === 'function') { start(); return; }
                if (typeof play === 'function') { play(); return; }
                // Fallback: click the first button or play element
                const btn = document.querySelector('#start, button, [class*="play"]');
                if (btn) btn.click();
            }
        """)

        print(f"Capturing frames...")
        for i in range(total_frames):
            frame_path = frames_dir / f"frame_{i:05d}.png"
            await page.screenshot(
                path=str(frame_path),
                omit_background=True,
                clip={"x": 0, "y": 0, "width": width, "height": height},
            )
            if i % fps == 0:
                print(f"  {i}/{total_frames} frames ({i / fps:.1f}s)")
            await page.wait_for_timeout(frame_ms)

        await browser.close()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("Encoding ProRes 4444 MOV...")
    result = subprocess.run([
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", str(frames_dir / "frame_%05d.png"),
        "-c:v", "prores_ks",
        "-profile:v", "4444",
        "-pix_fmt", "yuva444p10le",
        "-vendor", "apl0",
        "-bits_per_mb", "8000",
        str(output_path),
    ], capture_output=True, text=True)

    shutil.rmtree(frames_dir)

    if result.returncode != 0:
        print("ffmpeg error:\n", result.stderr[-3000:], file=sys.stderr)
        sys.exit(1)

    size_mb = output_path.stat().st_size / 1024 / 1024
    print(f"Done: {output_path}  ({size_mb:.1f} MB)")


def main():
    parser = argparse.ArgumentParser(description="Render standalone HTML animation to transparent ProRes MOV")
    parser.add_argument("--input",    required=True, help="Path to source HTML file")
    parser.add_argument("--output",   required=True, help="Path for output .mov file")
    parser.add_argument("--duration", type=float, default=16.0, help="Capture duration in seconds (default: 16.0 — always use at least 2× the calculated JS timing)")
    parser.add_argument("--fps",      type=int,   default=30,  help="Frames per second (default: 30)")
    parser.add_argument("--width",    type=int,   default=1920, help="Viewport width (default: 1920)")
    parser.add_argument("--height",   type=int,   default=1080, help="Viewport height (default: 1080)")
    parser.add_argument("--bg-color", default="faf9f5", help="Page background hex to strip, without # (default: faf9f5)")
    args = parser.parse_args()

    html_path = Path(args.input).expanduser().resolve()
    if not html_path.exists():
        print(f"Error: input file not found: {html_path}", file=sys.stderr)
        sys.exit(1)

    asyncio.run(render(
        html_path=html_path,
        output_path=Path(args.output).expanduser().resolve(),
        duration=args.duration,
        fps=args.fps,
        width=args.width,
        height=args.height,
        bg_color=args.bg_color.lstrip("#"),
    ))


if __name__ == "__main__":
    main()
