"""Assemble Runway clips into one TikTok-ready vertical video."""

from __future__ import annotations

import subprocess
import textwrap
from pathlib import Path

from lib.script import ScriptBeat


def _escape_drawtext(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace(":", "\\:")
        .replace("'", "\\'")
        .replace("%", "\\%")
        .replace("\n", " ")
    )


def _wrap_on_screen(text: str, width: int = 24) -> str:
    lines = textwrap.wrap(text, width=width) or [text]
    return "\\n".join(lines[:3])


def _segment_with_caption(input_clip: Path, beat: ScriptBeat, output_clip: Path) -> None:
    caption = _escape_drawtext(_wrap_on_screen(beat.on_screen))
    output_clip.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_clip),
        "-vf",
        (
            "scale=1080:1920:force_original_aspect_ratio=decrease,"
            "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,"
            f"drawtext=text='{caption}':fontcolor=white:fontsize=54:"
            "borderw=3:bordercolor=black@0.8:"
            "x=(w-text_w)/2:y=h*0.78:line_spacing=8"
        ),
        "-an",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-r",
        "30",
        str(output_clip),
    ]
    subprocess.run(command, check=True, capture_output=True, text=True)


def concat_clips(clips: list[Path], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    list_file = output_path.with_suffix(".txt")
    with list_file.open("w", encoding="utf-8") as handle:
        for clip in clips:
            handle.write(f"file '{clip.resolve()}'\n")

    command = [
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
        str(output_path),
    ]
    subprocess.run(command, check=True, capture_output=True, text=True)
    list_file.unlink(missing_ok=True)
    return output_path


def build_final_video(
    raw_clips: list[Path],
    beats: list[ScriptBeat],
    output_path: Path,
) -> Path:
    if len(raw_clips) != len(beats):
        raise ValueError("Each clip needs a matching script beat.")

    captioned_dir = output_path.parent / "captioned"
    captioned_clips: list[Path] = []
    for index, (clip, beat) in enumerate(zip(raw_clips, beats, strict=True), start=1):
        captioned = captioned_dir / f"{index:02d}_{beat.kind}.mp4"
        _segment_with_caption(clip, beat, captioned)
        captioned_clips.append(captioned)

    return concat_clips(captioned_clips, output_path)
