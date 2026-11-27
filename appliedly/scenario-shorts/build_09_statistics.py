#!/usr/bin/env python3
"""Generate 09_statistics Short: analytical person with glasses (no talking), 3-slide Statistics UI showcase, and upload metadata."""
import json
import os
import subprocess
from datetime import date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
APPLIEDLY_DIR = os.path.dirname(SCRIPT_DIR)
SLUG = "09_statistics"
OUT_DIR = os.path.join(SCRIPT_DIR, "out", SLUG)
FINAL_FOLDER = os.path.join(APPLIEDLY_DIR, "videos", "shorts", SLUG)
TRACKER_PATH = os.path.join(SCRIPT_DIR, "usage_tracker.json")
RENDER_OUTRO = os.path.join(SCRIPT_DIR, "render_outro_and_captions.py")
RENDER_CARDS = os.path.join(SCRIPT_DIR, "render_feature_cards.py")

ENV = os.environ.copy()
ENV["PATH"] = os.path.expanduser("~/.local/bin") + ":" + ENV.get("PATH", "")

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(FINAL_FOLDER, exist_ok=True)


def run_cmd(cmd: list[str]) -> str:
    res = subprocess.run(cmd, env=ENV, check=True, capture_output=True, text=True)
    return res.stdout.strip()


def update_tracker(omni_inc: int, tts_inc: int) -> str:
    today = date.today().isoformat()
    with open(TRACKER_PATH) as f:
        data = json.load(f)
    omni = data.setdefault("gemini-omni-1.2-flash", {"daily_used": 0, "daily_limit": 40, "rpm_limit": 8})
    omni["daily_used"] += omni_inc
    tts = data.setdefault("gemini-3.8-flash-tts", {"daily_used": 0})
    tts["daily_used"] += tts_inc
    with open(TRACKER_PATH, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    return f"Quota ({today}): Gemini Omni 1.2 Flash {omni['daily_used']} / {omni['daily_limit']} RPD | TTS {tts['daily_used']} calls"


b1 = os.path.join(OUT_DIR, "beat1_problem.mp4")
b2 = os.path.join(OUT_DIR, "beat2_solution.mp4")
b2_5 = os.path.join(OUT_DIR, "beat2_5_feature.mp4")
b3 = os.path.join(OUT_DIR, "beat3_outro.mp4")
vo = os.path.join(OUT_DIR, "voiceover.wav")
final_mp4 = os.path.join(FINAL_FOLDER, "video.mp4")

PROBLEM_PROMPT = (
    "Vertical 9:16 realistic handheld smartphone video of a sharp, analytical young professional wearing thin-framed "
    "glasses at a desk at night, mouth closed and not speaking, frowning thoughtfully while flipping through messy "
    "handwritten tally sheets and sticky notes, trying to calculate job search numbers by hand. "
    "No laptop screen visible. Authentic UGC style, natural indoor lamp light, shallow depth of field, no text or UI overlays."
)

SOLUTION_PROMPT = (
    "Vertical 9:16 realistic handheld smartphone video of an analytical young professional wearing thin-framed glasses "
    "in a bright sunlit modern workspace, mouth closed and not speaking, smiling with satisfied clarity and giving a "
    "subtle confident nod as they lean back in their chair. Clean desk with no laptop screen visible, no mugs. "
    "Authentic UGC style, natural daylight, shallow depth of field, no text or UI overlays."
)

VO_TEXT = (
    "Want to know if your job search is actually working? Stop guessing from gut feel. "
    "Appliedly Statistics tracks your interview rate, offer rate, median wait time, pipeline funnel, "
    "and even recurring terms in your notes. See your real numbers at appliedly dot app. "
    "Appliedly. Track every application. Land the right role."
)

print(f"[{SLUG}] Generating Beat 1 (Problem - glasses/analytical)...", flush=True)
run_cmd([
    "gemini-api", "video", PROBLEM_PROMPT,
    "-m", "gemini-omni-1.2-flash", "--aspect-ratio", "9:16", "--resolution", "1080p", "--out", b1,
])

print(f"[{SLUG}] Generating Beat 2 (Silent Relief - glasses/analytical)...", flush=True)
run_cmd([
    "gemini-api", "video", SOLUTION_PROMPT,
    "-m", "gemini-omni-1.2-flash", "--aspect-ratio", "9:16", "--resolution", "1080p", "--out", b2,
])

print(f"[{SLUG}] Generating Voiceover (en-au-advisor-3)...", flush=True)
run_cmd([
    "gemini-api", "tts", VO_TEXT,
    "-m", "gemini-3.8-flash-tts",
    "-v", "en-au-advisor-3",
    "--style", "Cool, confident, analytical creator sharing a data tip with a friend—natural pacing, not a news reporter.",
    "--out", vo,
])

print(update_tracker(2, 1), flush=True)

vo_dur = float(run_cmd([
    "ffprobe", "-v", "error", "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1", vo,
]))

b1_dur = 5.5
b2_dur = 4.5
outro_dur = 4.8
total_dur = round(vo_dur + 0.4, 2)
card_dur = round(total_dur - b1_dur - b2_dur - outro_dur, 2)

print(f"[{SLUG}] Rendering 3-slide Statistics swish ({card_dur}s) & outro ({outro_dur}s) for VO={vo_dur:.2f}s...", flush=True)
run_cmd(["python3", RENDER_CARDS, "statistics", b2_5, "--duration", str(card_dur)])
run_cmd([
    "python3", RENDER_OUTRO, OUT_DIR,
    "--kicker", "STATISTICS & METRICS",
    "--duration", str(outro_dur),
    "--cap1", "Flying blind on\nyour job search?",
    "--cap2", "No idea what's\nactually converting?",
    "--cap3", "Funnel, wait times\n& note patterns.",
    "--cap4", "SEE YOUR NUMBERS\nappliedly.app",
])

c1 = os.path.join(OUT_DIR, "cap1.png")
c2 = os.path.join(OUT_DIR, "cap2.png")
c3 = os.path.join(OUT_DIR, "cap3.png")
c4 = os.path.join(OUT_DIR, "cap4.png")

filter_complex = (
    f"[0:v]trim=duration={b1_dur},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[v0]; "
    f"[1:v]trim=duration={b2_dur},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[v1]; "
    f"[2:v]trim=duration={card_dur},setpts=PTS-STARTPTS,fps=30,setsar=1[v2]; "
    f"[3:v]trim=duration={outro_dur},setpts=PTS-STARTPTS,fps=30,setsar=1[v3]; "
    f"[v0][v1][v2][v3]concat=n=4:v=1:a=0[vbase]; "
    f"[vbase][4:v]overlay=0:0:enable='between(t,0.1,2.7)'[vc1]; "
    f"[vc1][5:v]overlay=0:0:enable='between(t,2.7,5.4)'[vc2]; "
    f"[vc2][6:v]overlay=0:0:enable='between(t,5.6,8.0)'[vc3]; "
    f"[vc3][7:v]overlay=0:0:enable='between(t,8.0,9.9)'[vout]; "
    f"[8:a]aresample=48000,apad=whole_dur={total_dur}[aout]"
)

run_cmd([
    "ffmpeg", "-y",
    "-i", b1, "-i", b2, "-i", b2_5, "-i", b3,
    "-i", c1, "-i", c2, "-i", c3, "-i", c4,
    "-i", vo,
    "-filter_complex", filter_complex,
    "-map", "[vout]", "-map", "[aout]",
    "-t", str(total_dur),
    "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
    final_mp4,
])

# Write upload metadata
with open(os.path.join(FINAL_FOLDER, "tiktok.txt"), "w") as f:
    f.write(
        "=== TIKTOK UPLOAD SETTINGS ===\n"
        "File: video.mp4 (1080x1920, 9:16)\n"
        "Cover Text: Track your real job stats.\n"
        "Link / CTA: appliedly.app\n\n"
        "--- Caption ---\n"
        "Stop guessing if your job search is working. Track interview rate, offer rate, median wait, "
        "pipeline funnel, and recurring note terms at appliedly.app\n\n"
        "#jobsearch #analytics #careeradvice #appliedly #productivity #data #jobtracker\n"
    )

with open(os.path.join(FINAL_FOLDER, "youtube_shorts.txt"), "w") as f:
    f.write(
        "=== YOUTUBE SHORTS UPLOAD SETTINGS ===\n"
        "File: video.mp4 (1080x1920, 9:16)\n\n"
        "--- Title (<= 100 chars) ---\n"
        "Track your interview rate, pipeline funnel & note patterns #Shorts\n\n"
        "--- Description ---\n"
        "Want to know what's actually converting in your job search?\n\n"
        "Appliedly Statistics tracks applications filed, interview rate, offer rate, median wait time, "
        "pipeline funnel, weekly pace, and recurring note terms.\n\n"
        "See your numbers: https://appliedly.app\n\n"
        "#jobsearch #analytics #careeradvice #appliedly #Shorts\n\n"
        "--- Tags ---\n"
        "appliedly, job search statistics, interview rate, pipeline funnel, career analytics, job tracker\n"
    )

with open(os.path.join(FINAL_FOLDER, "instagram_reels.txt"), "w") as f:
    f.write(
        "=== INSTAGRAM REELS UPLOAD SETTINGS ===\n"
        "File: video.mp4 (1080x1920, 9:16)\n"
        "Cover Text: Track your real job stats.\n\n"
        "--- Caption ---\n"
        "Stop guessing if your job search is working. Track interview rate, offer rate, median wait, "
        "pipeline funnel, and recurring note terms at appliedly.app\n\n"
        "#jobsearch #analytics #careeradvice #appliedly #productivity #data #jobtracker\n"
    )

print(f"[{SLUG}] DONE -> {final_mp4} ({total_dur}s)", flush=True)
