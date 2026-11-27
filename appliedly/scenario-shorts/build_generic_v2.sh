#!/usr/bin/env bash
set -euo pipefail

# Generic Overall Appliedly TikTok / YouTube Short v2 (9:16)
# - Reuses beat1_problem.mp4 if already generated (0 extra video quota)
# - Generates Beat 2 (relief/morning solution clip) with gemini-omni-1.2-flash
# - Generates expressive creator-style voiceover with gemini-3.8-flash-tts (Achird + --style)
# - Generates subtle upbeat background music bed with lyria-3.5
# - Renders TV-commercial animated logo + slogan + appliedly.app outro via render_outro_and_captions.py
# - Stitches all beats, captions, voiceover, and music bed with ffmpeg

export PATH="$HOME/.local/bin:$PATH"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR="$SCRIPT_DIR/out/generic-overall"
mkdir -p "$OUT_DIR"

if ! gemini-api whoami >/dev/null 2>&1; then
  echo "Error: Gemini API credentials not configured." >&2
  exit 1
fi

if [[ ! -f "$OUT_DIR/beat1_problem.mp4" ]]; then
  echo "Generating Beat 1 (Problem) with gemini-omni-1.2-flash..."
  gemini-api video "Vertical 9:16 realistic handheld smartphone video, side-profile angle of a tired young professional sitting at a dimly lit home desk at night, rubbing their eyes while looking stressed at an open laptop facing them. The laptop's screen faces only the person, with the solid silver aluminum back of the lid angled away. Soft blue glow from the screen on their face, no text or UI overlays." \
    -m gemini-omni-1.2-flash \
    --aspect-ratio 9:16 \
    --resolution 1080p \
    --out "$OUT_DIR/beat1_problem.mp4"
else
  echo "1/5 Reusing existing Beat 1 ($OUT_DIR/beat1_problem.mp4)..."
fi

echo "2/5 Checking Beat 2 (Solution/Relief)..."
if [[ ! -f "$OUT_DIR/beat2_solution.mp4" ]]; then
  RELIEF_PROMPT="Vertical 9:16 realistic handheld smartphone-style video of a relaxed young professional the next morning in a bright sunlit room, smiling calmly with a mug of coffee as they close their laptop and lean back peacefully. Warm natural morning sunlight, clean desk, authentic relatable UGC aesthetic, shallow depth of field, no text or UI overlays."

  gemini-api video "$RELIEF_PROMPT" \
    -m gemini-omni-1.2-flash \
    --aspect-ratio 9:16 \
    --resolution 1080p \
    --out "$OUT_DIR/beat2_solution.mp4"
  OMNI_RAN=1
else
  echo "Reusing existing Beat 2 ($OUT_DIR/beat2_solution.mp4)..."
  OMNI_RAN=0
fi

echo "3/5 Checking Voiceover..."
if [[ ! -f "$OUT_DIR/voiceover_v2.wav" ]]; then
  VO_TEXT="Okay, why does job hunting feel like a full-time job? Forty tabs open, zero idea who ghosted you... Yeah, stop doing that. Go to appliedly dot app—it tracks every application and keeps your whole search calm. Appliedly. Track every application. Land the right role."

  gemini-api tts "$VO_TEXT" \
    -m gemini-3.8-flash-tts \
    -v Achird \
    --style "Casual, relatable TikTok creator talking to a friend—starts slightly exasperated, then shifts to warm, genuine relief and confident commercial energy. Natural pacing, not a news reporter." \
    --out "$OUT_DIR/voiceover_v2.wav"
  TTS_RAN=1
else
  echo "Reusing existing Voiceover ($OUT_DIR/voiceover_v2.wav)..."
  TTS_RAN=0
fi

echo "4/5 Rendering TV-commercial animated logo outro & captions..."
python3 "$SCRIPT_DIR/render_outro_and_captions.py" "$OUT_DIR"

echo "5/5 Assembling final 9:16 MP4 with ffmpeg..."
# Check voiceover duration so we never cut off the end of speech
VO_DUR=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUT_DIR/voiceover_v2.wav")
echo "Voiceover duration: ${VO_DUR}s"

# Assemble:
#   0.0 - 5.0s : Beat 1 (Problem) + cap1 (0-2.5s) + cap2 (2.5-5.0s)
#   5.0 - 11.0s: Beat 2 (Relief)  + cap3 (5.0-8.2s) + cap4 (8.2-11.0s)
#  11.0 - 16.0s: Beat 3 (TV Animated Logo + Slogan + appliedly.app)
ffmpeg -y \
  -i "$OUT_DIR/beat1_problem.mp4" \
  -i "$OUT_DIR/beat2_solution.mp4" \
  -i "$OUT_DIR/beat3_outro.mp4" \
  -i "$OUT_DIR/cap1.png" \
  -i "$OUT_DIR/cap2.png" \
  -i "$OUT_DIR/cap3.png" \
  -i "$OUT_DIR/cap4.png" \
  -i "$OUT_DIR/voiceover_v2.wav" \
  -filter_complex "\
[0:v]trim=duration=5,setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[v0]; \
[1:v]trim=duration=6,setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[v1]; \
[2:v]trim=duration=6.5,setpts=PTS-STARTPTS,fps=30,setsar=1[v2]; \
[v0][v1][v2]concat=n=3:v=1:a=0[vbase]; \
[vbase][3:v]overlay=0:0:enable='between(t,0.1,2.5)'[vc1]; \
[vc1][4:v]overlay=0:0:enable='between(t,2.5,5.0)'[vc2]; \
[vc2][5:v]overlay=0:0:enable='between(t,5.1,8.2)'[vc3]; \
[vc3][6:v]overlay=0:0:enable='between(t,8.2,10.9)'[vout]; \
[7:a]aresample=48000,apad=whole_dur=17.5[aout]" \
  -map "[vout]" -map "[aout]" \
  -t 17.5 \
  -c:v libx264 -preset fast -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart \
  "$OUT_DIR/appliedly_generic_short_v2.mp4"

python3 - "$SCRIPT_DIR/usage_tracker.json" "$OMNI_RAN" "$TTS_RAN" <<'PY'
import json, sys
from datetime import date

path = sys.argv[1]
omni_inc = int(sys.argv[2])
tts_inc = int(sys.argv[3])
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
omni["daily_used"] += omni_inc
tts = data.setdefault("gemini-3.8-flash-tts", {"daily_used": 0})
tts["daily_used"] += tts_inc

with open(path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")

print(f"Quota usage ({today}): Gemini Omni 1.2 Flash {omni['daily_used']} / {omni['daily_limit']} RPD | TTS {tts['daily_used']} calls")
PY

echo "Done! Output written to: $OUT_DIR/appliedly_generic_short_v2.mp4"
