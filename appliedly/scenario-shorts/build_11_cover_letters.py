#!/usr/bin/env python3
"""Generate 11_cover_letters Short: cover letter burnout -> tailored PDF from logged application + Documents summary."""
import os
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
APPLIEDLY_DIR = os.path.dirname(SCRIPT_DIR)
SLUG = "11_cover_letters"
OUT_DIR = os.path.join(SCRIPT_DIR, "out", SLUG)
FINAL_FOLDER = os.path.join(APPLIEDLY_DIR, "videos", "shorts", SLUG)
RENDER_OUTRO = os.path.join(SCRIPT_DIR, "render_outro_and_captions.py")
RENDER_CARDS = os.path.join(SCRIPT_DIR, "render_feature_cards.py")

ENV = os.environ.copy()
ENV["PATH"] = os.path.expanduser("~/.local/bin") + ":" + ENV.get("PATH", "")

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(FINAL_FOLDER, exist_ok=True)


def run_cmd(cmd: list[str], retries: int = 2) -> str:
    import sys, time
    for attempt in range(retries + 1):
        try:
            res = subprocess.run(cmd, env=ENV, check=True, capture_output=True, text=True)
            return res.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Command failed (attempt {attempt + 1}/{retries + 1}): {e.stderr}", file=sys.stderr, flush=True)
            if attempt == retries:
                raise
            time.sleep(5)
    return ""


b1 = os.path.join(OUT_DIR, "beat1_problem.mp4")
b2 = os.path.join(OUT_DIR, "beat2_solution.mp4")
b2_5 = os.path.join(OUT_DIR, "beat2_5_feature.mp4")
b3 = os.path.join(OUT_DIR, "beat3_outro.mp4")
vo = os.path.join(OUT_DIR, "voiceover.wav")
final_mp4 = os.path.join(FINAL_FOLDER, "video.mp4")

print(f"[{SLUG}] Generating Beat 1 (Problem - cover letter burnout)...", flush=True)
run_cmd([
    "gemini-api", "video",
    "Vertical 9:16 realistic handheld smartphone video of a young man in his late 20s sitting at a home "
    "desk in the evening, mouth closed and not speaking, frowning thoughtfully while flipping through a stack of "
    "blank papers with a pen in hand. Warm indoor lamp light, authentic UGC style, shallow depth of field, no text or UI overlays.",
    "-m", "gemini-omni-1.2-flash", "--aspect-ratio", "9:16", "--resolution", "1080p", "--out", b1,
])

print(f"[{SLUG}] Generating Beat 2 (Silent Relief)...", flush=True)
run_cmd([
    "gemini-api", "video",
    "Vertical 9:16 realistic handheld smartphone video of a young man in his late 20s in a bright "
    "sunlit workspace, mouth closed and not speaking, smiling warmly with genuine relief and leaning back comfortably "
    "in his chair. Clean desk, authentic UGC style, shallow depth of field, no text or UI overlays.",
    "-m", "gemini-omni-1.2-flash", "--aspect-ratio", "9:16", "--resolution", "1080p", "--out", b2,
])

print(f"[{SLUG}] Generating Voiceover (en-au-concierge-7)...", flush=True)
run_cmd([
    "gemini-api", "tts",
    "Burning an hour on a cover letter for every single application? Stop rewriting from scratch. "
    "At appliedly dot app, generate a tailored cover letter PDF straight from the role you logged and your saved "
    "documents summary—ready to download in seconds. Appliedly. Track every application. Land the right role.",
    "-m", "gemini-3.8-flash-tts",
    "-v", "en-au-concierge-7",
    "--style", "Warm, engaging young creator sharing a real shortcut with a friend—not a news reporter.",
    "--out", vo,
])

vo_dur = float(run_cmd([
    "ffprobe", "-v", "error", "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1", vo,
]))

b1_dur = 5.0
b2_dur = 4.0
outro_dur = 4.8
total_dur = round(vo_dur + 0.4, 2)
card_dur = round(total_dur - b1_dur - b2_dur - outro_dur, 2)

print(f"[{SLUG}] Rendering 2-slide Cover Letter swish ({card_dur}s) & outro ({outro_dur}s) for VO={vo_dur:.2f}s...", flush=True)
run_cmd(["python3", RENDER_CARDS, "cover_letter", b2_5, "--duration", str(card_dur)])
run_cmd([
    "python3", RENDER_OUTRO, OUT_DIR,
    "--kicker", "TAILORED COVER LETTERS",
    "--duration", str(outro_dur),
    "--cap1", "45 mins writing\nanother cover letter?",
    "--cap2", "All that effort\njust to get ghosted?",
    "--cap3", "Tailored PDF straight\nfrom the role.",
    "--cap4", "SKIP THE BLANK PAGE\nappliedly.app",
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
    f"[vbase][4:v]overlay=0:0:enable='between(t,0.1,2.5)'[vc1]; "
    f"[vc1][5:v]overlay=0:0:enable='between(t,2.5,4.9)'[vc2]; "
    f"[vc2][6:v]overlay=0:0:enable='between(t,5.1,7.3)'[vc3]; "
    f"[vc3][7:v]overlay=0:0:enable='between(t,7.3,8.9)'[vout]; "
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

with open(os.path.join(FINAL_FOLDER, "tiktok.txt"), "w") as f:
    f.write(
        "=== TIKTOK UPLOAD SETTINGS ===\n"
        "File: video.mp4 (1080x1920, 9:16)\n"
        "Cover Text: Stop rewriting cover letters.\n"
        "Link / CTA: appliedly.app\n\n"
        "--- Caption ---\n"
        "Burning an hour on a cover letter for every application? Generate a tailored PDF straight from the role "
        "you logged and your saved documents summary at appliedly.app\n\n"
        "#coverletter #jobsearch #resume #appliedly #careeradvice #productivity #jobhunt\n"
    )

with open(os.path.join(FINAL_FOLDER, "youtube_shorts.txt"), "w") as f:
    f.write(
        "=== YOUTUBE SHORTS UPLOAD SETTINGS ===\n"
        "File: video.mp4 (1080x1920, 9:16)\n\n"
        "--- Title (<= 100 chars) ---\n"
        "Stop burning hours writing cover letters from scratch #Shorts\n\n"
        "--- Description ---\n"
        "Spending 45 minutes on every cover letter with no clear payoff?\n\n"
        "Appliedly generates a tailored cover letter PDF straight from the application you logged "
        "and your saved Documents summary.\n\n"
        "Skip the blank page: https://appliedly.app\n\n"
        "#coverletter #jobsearch #careeradvice #appliedly #Shorts\n\n"
        "--- Tags ---\n"
        "appliedly, cover letter generator, tailored cover letter pdf, job application tracker, job search tips\n"
    )

with open(os.path.join(FINAL_FOLDER, "instagram_reels.txt"), "w") as f:
    f.write(
        "=== INSTAGRAM REELS UPLOAD SETTINGS ===\n"
        "File: video.mp4 (1080x1920, 9:16)\n"
        "Cover Text: Stop rewriting cover letters.\n\n"
        "--- Caption ---\n"
        "Burning an hour on a cover letter for every application? Generate a tailored PDF straight from the role "
        "you logged and your saved documents summary at appliedly.app\n\n"
        "#coverletter #jobsearch #resume #appliedly #careeradvice #productivity #jobhunt\n"
    )

print(f"[{SLUG}] DONE -> {final_mp4} ({total_dur}s)", flush=True)
