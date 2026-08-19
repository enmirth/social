#!/usr/bin/env python3
"""Generate a simple TikTok ad from an app store URL and screenshots."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from lib.assemble import build_final_video
from lib.runway_client import (
    RunwayError,
    generate_image_to_video,
    generate_text_to_video,
    get_api_key,
)
from lib.presets import app_info_from_preset, get_preset, script_from_preset
from lib.script import TikTokScript, build_script, save_script
from lib.store import fetch_app_info, save_app_info


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def _load_screenshots(screenshots_dir: Path, max_count: int) -> list[Path]:
    if not screenshots_dir.is_dir():
        raise FileNotFoundError(f"Screenshots folder not found: {screenshots_dir}")

    images = sorted(
        path
        for path in screenshots_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )
    if not images:
        raise FileNotFoundError(
            f"No screenshots found in {screenshots_dir}. Add PNG/JPG/WEBP files."
        )
    return images[:max_count]


def _map_beats_to_assets(script: TikTokScript, screenshots: list[Path]) -> list[tuple]:
    beats = script.beats()
    if len(screenshots) >= len(beats):
        return [(beat, screenshots[index]) for index, beat in enumerate(beats)]
    if len(screenshots) == 1:
        return [(beats[0], None), (beats[1], screenshots[0]), (beats[2], screenshots[0]), (beats[3], screenshots[0]), (beats[4], None)]
    mapped = []
    for index, beat in enumerate(beats):
        if index == 0 or index == len(beats) - 1:
            mapped.append((beat, None))
        else:
            mapped.append((beat, screenshots[min(index - 1, len(screenshots) - 1)]))
    return mapped


def _print_plan(app, script: TikTokScript, screenshots: list[Path], output_dir: Path) -> None:
    print("\nGenerated plan\n" + "=" * 40)
    print(f"App: {app.name} ({app.store})")
    print(f"Category: {app.category}")
    print(f"Screenshots: {len(screenshots)}")
    print(f"Output dir: {output_dir}\n")
    for beat in script.beats():
        print(f"[{beat.kind.upper()}] {beat.on_screen}")
        print(f"  Voiceover: {beat.voiceover}")
        print(f"  Runway: {beat.runway_prompt}\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a simple TikTok video from a store URL and screenshots using Runway."
    )
    parser.add_argument(
        "--store-url",
        help="App Store, Google Play, or Microsoft Store URL",
    )
    parser.add_argument(
        "--preset",
        choices=["work-time-tracker-pro", "draft-pal"],
        help="Use a built-in preset for Enmirth Microsoft Store apps",
    )
    parser.add_argument(
        "--screenshots",
        required=True,
        help="Folder containing app screenshots (PNG/JPG/WEBP)",
    )
    parser.add_argument(
        "--output-dir",
        default="./out",
        help="Directory for generated assets (default: ./out)",
    )
    parser.add_argument(
        "--max-screenshots",
        type=int,
        default=3,
        help="Maximum screenshots to use (default: 3)",
    )
    parser.add_argument(
        "--clip-seconds",
        type=int,
        default=5,
        help="Seconds per Runway clip (default: 5)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch metadata and write script/plan without calling Runway",
    )
    parser.add_argument(
        "--script-only",
        action="store_true",
        help="Only fetch metadata and generate script.json",
    )
    parser.add_argument("--app-name", help="Override app name if store lookup is wrong")
    parser.add_argument("--problem", help="Override the problem statement beat")
    parser.add_argument("--tagline", help="Override the solution/benefit beat")
    args = parser.parse_args()

    if not args.store_url and not args.preset:
        parser.error("Provide --store-url or --preset.")

    output_dir = Path(args.output_dir).resolve()
    screenshots_dir = Path(args.screenshots).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.preset:
        preset = get_preset(args.preset)
        store_url = args.store_url or preset.store_url
        app = app_info_from_preset(preset)
        app.store_url = store_url
        script = script_from_preset(preset, app)
    else:
        app = fetch_app_info(args.store_url)
        script = build_script(app)

    if args.app_name:
        app.name = args.app_name.strip()
    if args.problem:
        script.problem.on_screen = args.problem[:90]
        script.problem.voiceover = args.problem
    if args.tagline:
        script.solution.on_screen = args.tagline[:90]
        script.solution.voiceover = args.tagline
    screenshots = _load_screenshots(screenshots_dir, args.max_screenshots)

    save_app_info(app, output_dir / "app.json")
    save_script(script, output_dir / "script.json")
    _print_plan(app, script, screenshots, output_dir)

    if args.script_only or args.dry_run:
        print("Dry run complete. Review script.json, then rerun without --dry-run.")
        return 0

    try:
        api_key = get_api_key()
    except RunwayError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    raw_dir = output_dir / "raw_clips"
    raw_dir.mkdir(parents=True, exist_ok=True)
    mapped = _map_beats_to_assets(script, screenshots)
    raw_clips: list[Path] = []
    beats: list = []

    for index, (beat, screenshot) in enumerate(mapped, start=1):
        clip_path = raw_dir / f"{index:02d}_{beat.kind}.mp4"
        print(f"\nGenerating clip {index}/{len(mapped)}: {beat.kind}", file=sys.stderr)
        if screenshot is None:
            generate_text_to_video(
                api_key,
                beat.runway_prompt,
                clip_path,
                duration=args.clip_seconds,
            )
        else:
            generate_image_to_video(
                api_key,
                screenshot,
                beat.runway_prompt,
                clip_path,
                duration=args.clip_seconds,
            )
        raw_clips.append(clip_path)
        beats.append(beat)

    final_path = output_dir / "tiktok_final.mp4"
    build_final_video(raw_clips, beats, final_path)

    caption_lines = [
        f"{script.hook.on_screen} 👇",
        script.problem.on_screen,
        script.solution.on_screen,
        f"Download {app.name} on the {app.store}.",
        app.store_url,
        f"#{app.category.replace(' ', '')} #Windows #productivity #MicrosoftStore",
    ]
    (output_dir / "tiktok_caption.txt").write_text("\n\n".join(caption_lines), encoding="utf-8")

    summary = {
        "app": app.name,
        "store_url": app.store_url,
        "final_video": str(final_path),
        "caption_file": str(output_dir / "tiktok_caption.txt"),
        "script_file": str(output_dir / "script.json"),
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"\nDone. Final TikTok video: {final_path}")
    print(f"Suggested caption: {output_dir / 'tiktok_caption.txt'}")
    print("Upload manually in TikTok, or schedule with Metricool/Later.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
