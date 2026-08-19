#!/usr/bin/env python3
"""Build a local sample TikTok video without Runway (for previewing the format)."""

from __future__ import annotations

import argparse
import subprocess
import textwrap
from pathlib import Path

import requests

from lib.presets import app_info_from_preset, get_preset, script_from_preset


def _escape_drawtext(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace(":", "\\:")
        .replace("'", "\\'")
        .replace("%", "\\%")
    )


def _lines(text: str, width: int = 20) -> str:
    wrapped = textwrap.wrap(text, width=width) or [text]
    return "\\n".join(_escape_drawtext(line) for line in wrapped[:3])


def _download_store_screenshots(product_id: str, output_dir: Path, limit: int = 3) -> list[Path]:
    response = requests.get(
        f"https://displaycatalog.mp.microsoft.com/v7.0/products/{product_id}",
        params={"market": "US", "languages": "en-US", "moId": "Public"},
        timeout=20,
    )
    response.raise_for_status()
    images = response.json()["Product"]["LocalizedProperties"][0].get("Images") or []
    screenshots = [
        img for img in images if img.get("ImagePurpose") == "Screenshot" and img.get("Uri")
    ]
    paths: list[Path] = []
    for index, image in enumerate(screenshots[:limit], start=1):
        url = "https:" + image["Uri"] if image["Uri"].startswith("//") else image["Uri"]
        path = output_dir / f"screen{index}.png"
        path.write_bytes(requests.get(url, timeout=30).content)
        paths.append(path)
    if not paths:
        raise RuntimeError("No Microsoft Store screenshots found.")
    return paths


def _card_clip(text: str, output: Path, color: str = "0x101820", duration: float = 3.5, subtitle: str = "") -> None:
    caption = _escape_drawtext(text)
    if subtitle:
        sub = _escape_drawtext(subtitle)
        vf = (
            f"drawtext=text='{caption}':fontcolor=white:fontsize=56:"
            "borderw=4:bordercolor=black@0.85:x=(w-text_w)/2:y=(h-text_h)/2-40:line_spacing=12,"
            f"drawtext=text='{sub}':fontcolor=white:fontsize=40:"
            "borderw=3:bordercolor=black@0.85:x=(w-text_w)/2:y=(h-text_h)/2+40"
        )
    else:
        vf = (
            f"drawtext=text='{caption}':fontcolor=white:fontsize=56:"
            "borderw=4:bordercolor=black@0.85:x=(w-text_w)/2:y=(h-text_h)/2:line_spacing=12"
        )
    command = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        f"color=c={color}:s=1080x1920:d={duration}",
        "-vf",
        vf,
        "-an",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-r",
        "30",
        str(output),
    ]
    subprocess.run(command, check=True, capture_output=True, text=True)


def _screenshot_clip(image: Path, text: str, output: Path, duration: float = 3.5) -> None:
    caption = _escape_drawtext(text)
    command = [
        "ffmpeg",
        "-y",
        "-loop",
        "1",
        "-i",
        str(image),
        "-vf",
        (
            "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            "zoompan=z='min(zoom+0.0015,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f"d={int(duration * 30)}:s=1080x1920:fps=30,"
            "drawbox=x=0:y=ih*0.70:w=iw:h=ih*0.30:color=black@0.50:t=fill,"
            f"drawtext=text='{caption}':fontcolor=white:fontsize=50:"
            "borderw=3:bordercolor=black@0.85:x=(w-text_w)/2:y=h*0.76:line_spacing=10"
        ),
        "-t",
        str(duration),
        "-an",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        str(output),
    ]
    subprocess.run(command, check=True, capture_output=True, text=True)


def build_sample(preset_name: str, output_dir: Path) -> Path:
    preset = get_preset(preset_name)
    app = app_info_from_preset(preset)
    script = script_from_preset(preset, app)
    output_dir.mkdir(parents=True, exist_ok=True)

    product_id = preset.store_url.rstrip("/").split("/")[-1]
    screenshots = _download_store_screenshots(product_id, output_dir)

    raw_dir = output_dir / "raw_clips"
    raw_dir.mkdir(parents=True, exist_ok=True)
    beats = script.beats()
    clips: list[Path] = []

    for index, beat in enumerate(beats, start=1):
        clip = raw_dir / f"{index:02d}_{beat.kind}.mp4"
        if beat.kind == "hook":
            _card_clip(beat.on_screen, clip)
        elif beat.kind == "cta":
            _card_clip(beat.on_screen, clip, color="0x005FB8", subtitle="Microsoft Store")
        elif beat.kind == "problem":
            _screenshot_clip(screenshots[0], beat.on_screen, clip)
        elif beat.kind == "solution":
            _screenshot_clip(screenshots[min(1, len(screenshots) - 1)], beat.on_screen, clip)
        else:
            _screenshot_clip(screenshots[min(2, len(screenshots) - 1)], beat.on_screen, clip)
        clips.append(clip)

    list_file = output_dir / "concat.txt"
    with list_file.open("w", encoding="utf-8") as handle:
        for clip in clips:
            handle.write(f"file '{clip.resolve()}'\n")

    final_path = output_dir / f"{preset_name}-sample.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(list_file),
            "-c",
            "copy",
            str(final_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    list_file.unlink(missing_ok=True)
    return final_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a local sample TikTok video without Runway.")
    parser.add_argument(
        "--preset",
        default="work-time-tracker-pro",
        choices=["work-time-tracker-pro", "draft-pal"],
    )
    parser.add_argument("--output-dir", default="./out/sample")
    args = parser.parse_args()

    final_path = build_sample(args.preset, Path(args.output_dir).resolve())
    print(final_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
