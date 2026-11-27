#!/usr/bin/env bash
set -euo pipefail

# Generic Overall Appliedly TikTok / YouTube Short (9:16) Generator
# Requires:
#   - gemini-api CLI (~/.local/bin/gemini-api or on PATH)
#   - GEMINI_API_KEY (or configured via `gemini-api configure --api-key "..."`)
#   - ffmpeg

export PATH="$HOME/.local/bin:$PATH"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APPLIEDLY_DIR="$(dirname "$SCRIPT_DIR")"
OUT_DIR="$SCRIPT_DIR/out/generic-overall"
mkdir -p "$OUT_DIR"

EXISTING_DEMO="$APPLIEDLY_DIR/videos/appliedly_tiktok_reels_shorts_9x16_1080x1920.mp4"
if [[ ! -f "$EXISTING_DEMO" ]]; then
  echo "Error: Expected demo video not found at $EXISTING_DEMO" >&2
  exit 1
fi

if ! command -v gemini-api >/dev/null 2>&1; then
  echo "Error: gemini-api CLI not found on PATH." >&2
  exit 1
fi

echo "1/4 Checking Gemini API auth..."
if ! gemini-api whoami >/dev/null 2>&1; then
  echo "Error: Gemini API credentials not configured." >&2
  echo "Run: export GEMINI_API_KEY=\"your-key\"  OR  gemini-api configure --api-key \"your-key\"" >&2
  exit 1
fi

echo "2/4 Generating Problem Scenario clip (Beat 1) with gemini-omni-1.2-flash..."
PROBLEM_PROMPT="Vertical 9:16 realistic handheld smartphone-style video of a tired young professional sitting at a dimly lit home desk at night, illuminated by a laptop screen. They sigh and rub their eyes while looking stressed at dozens of cluttered browser tabs and a messy spreadsheet. Authentic relatable UGC aesthetic, natural indoor lighting, shallow depth of field, no text or UI overlays."

gemini-api video "$PROBLEM_PROMPT" \
  -m gemini-omni-1.2-flash \
  --aspect-ratio 9:16 \
  --resolution 1080p \
  --out "$OUT_DIR/beat1_problem.mp4"

echo "3/4 Generating Voiceover with gemini-3.8-flash-tts..."
VO_TEXT="Job hunting shouldn't feel like a second full-time job. Appliedly tracks every application, blocks the roles you don't want, and keeps your entire pipeline calm. Take back your search—try Appliedly."

gemini-api tts "$VO_TEXT" \
  -m gemini-3.8-flash-tts \
  -v Kore \
  --out "$OUT_DIR/voiceover.wav"

echo "4/4 Assembling 9:16 Short with ffmpeg..."
# Normalize Beat 1 (first 5s, 1080x1920, 30fps, silent video) and Beat 2 (8s slice of real Appliedly demo)
ffmpeg -y \
  -i "$OUT_DIR/beat1_problem.mp4" \
  -ss 2 -t 8 -i "$EXISTING_DEMO" \
  -i "$OUT_DIR/voiceover.wav" \
  -filter_complex "\
[0:v]trim=duration=5,setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[v0]; \
[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[v1]; \
[v0][v1]concat=n=2:v=1:a=0[vout]; \
[2:a]apad=whole_dur=13[aout]" \
  -map "[vout]" -map "[aout]" \
  -t 13 \
  -c:v libx264 -preset fast -crf 22 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart \
  "$OUT_DIR/appliedly_generic_short_test.mp4"

echo "Done! Output written to: $OUT_DIR/appliedly_generic_short_test.mp4"

python3 - "$SCRIPT_DIR/usage_tracker.json" <<'PY'
import json, sys
from datetime import date

path = sys.argv[1]
today = date.today().isoformat()
try:
    with open(path) as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}

if data.get("date") != today:
    data = {
        "date": today,
        "gemini-omni-1.2-flash": {"daily_used": 0, "daily_limit": 40, "rpm_limit": 8},
        "gemini-3.8-flash-tts": {"daily_used": 0},
    }

omni = data.setdefault("gemini-omni-1.2-flash", {"daily_used": 0, "daily_limit": 40, "rpm_limit": 8})
omni["daily_used"] += 1
tts = data.setdefault("gemini-3.8-flash-tts", {"daily_used": 0})
tts["daily_used"] += 1

with open(path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")

print(f"Quota usage ({today}): Gemini Omni 1.2 Flash {omni['daily_used']} / {omni['daily_limit']} RPD | TTS {tts['daily_used']} calls")
PY
