#!/usr/bin/env python3
"""Fix 03_applications_rounds_cover_letter (silent Beat 2 + 2-slide UI card + 4.8s outro) and create 10_documents."""
import os
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
APPLIEDLY_DIR = os.path.dirname(SCRIPT_DIR)
OUT_BASE = os.path.join(SCRIPT_DIR, "out")
FINAL_DIR = os.path.join(APPLIEDLY_DIR, "videos", "shorts")
RENDER_OUTRO = os.path.join(SCRIPT_DIR, "render_outro_and_captions.py")
RENDER_CARDS = os.path.join(SCRIPT_DIR, "render_feature_cards.py")

ENV = os.environ.copy()
ENV["PATH"] = os.path.expanduser("~/.local/bin") + ":" + ENV.get("PATH", "")


def run_cmd(cmd: list[str]) -> str:
    res = subprocess.run(cmd, env=ENV, check=True, capture_output=True, text=True)
    return res.stdout.strip()


def stitch_4beat(slug: str, card_kind: str, kicker: str, caps: tuple[str, str, str, str]) -> float:
    out_dir = os.path.join(OUT_BASE, slug)
    final_folder = os.path.join(FINAL_DIR, slug)
    os.makedirs(final_folder, exist_ok=True)

    b1 = os.path.join(out_dir, "beat1_problem.mp4")
    b2 = os.path.join(out_dir, "beat2_solution.mp4")
    b2_5 = os.path.join(out_dir, "beat2_5_feature.mp4")
    b3 = os.path.join(out_dir, "beat3_outro.mp4")
    vo = os.path.join(out_dir, "voiceover.wav")
    final_mp4 = os.path.join(final_folder, "video.mp4")

    vo_dur = float(run_cmd([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", vo,
    ]))

    b1_dur = 5.0
    b2_dur = 4.0
    outro_dur = 4.8
    total_dur = round(vo_dur + 0.4, 2)
    card_dur = round(total_dur - b1_dur - b2_dur - outro_dur, 2)

    print(f"[{slug}] Rendering {card_kind} ({card_dur}s) & outro ({outro_dur}s) for VO={vo_dur:.2f}s...", flush=True)
    run_cmd(["python3", RENDER_CARDS, card_kind, b2_5, "--duration", str(card_dur)])
    run_cmd([
        "python3", RENDER_OUTRO, out_dir,
        "--kicker", kicker,
        "--duration", str(outro_dur),
        "--cap1", caps[0],
        "--cap2", caps[1],
        "--cap3", caps[2],
        "--cap4", caps[3],
    ])

    c1 = os.path.join(out_dir, "cap1.png")
    c2 = os.path.join(out_dir, "cap2.png")
    c3 = os.path.join(out_dir, "cap3.png")
    c4 = os.path.join(out_dir, "cap4.png")

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
    print(f"[{slug}] DONE -> {final_mp4} ({total_dur}s)", flush=True)
    return total_dur


# 1) Fix 03_applications_rounds_cover_letter
s3 = "03_applications_rounds_cover_letter"
print(f"[{s3}] Regenerating Beat 2 (silent, no talking in air)...", flush=True)
run_cmd([
    "gemini-api", "video",
    "Vertical 9:16 realistic handheld smartphone video, medium close-up of a South Asian man in his early 30s "
    "in a bright sunlit workspace, mouth closed and not speaking, smiling with calm readiness and giving a subtle nod "
    "as he leans back comfortably in his chair. Tidy desk, no laptop screen visible. Authentic UGC style, shallow depth of field, no text or UI overlays.",
    "-m", "gemini-omni-1.2-flash", "--aspect-ratio", "9:16", "--resolution", "1080p",
    "--out", os.path.join(OUT_BASE, s3, "beat2_solution.mp4"),
])
stitch_4beat(
    s3,
    "applications",
    "INTERVIEWS & COVER LETTERS",
    (
        "3 interview rounds.\nMissing prep notes?",
        "Writing cover letters\nfrom scratch again?",
        "Rounds, .ics invites\n& tailored PDFs.",
        "ORGANIZE YOUR HUNT\nappliedly.app",
    ),
)

# 2) Create 10_documents
s10 = "10_documents"
out10 = os.path.join(OUT_BASE, s10)
final10 = os.path.join(FINAL_DIR, s10)
os.makedirs(out10, exist_ok=True)
os.makedirs(final10, exist_ok=True)

print(f"[{s10}] Generating Beat 1 (Problem - messy files)...", flush=True)
run_cmd([
    "gemini-api", "video",
    "Vertical 9:16 realistic handheld smartphone video of a Latina woman in her late 20s at a home desk, "
    "mouth closed and not speaking, looking frustrated as she sorts through messy paper folders and loose resumes. "
    "No laptop screen visible. Natural indoor lighting, authentic UGC style, shallow depth of field, no text or UI overlays.",
    "-m", "gemini-omni-1.2-flash", "--aspect-ratio", "9:16", "--resolution", "1080p",
    "--out", os.path.join(out10, "beat1_problem.mp4"),
])

print(f"[{s10}] Generating Beat 2 (Silent Relief)...", flush=True)
run_cmd([
    "gemini-api", "video",
    "Vertical 9:16 realistic handheld smartphone video of a Latina woman in her late 20s in a bright sunlit workspace, "
    "mouth closed and not speaking, smiling warmly with relief and relaxing back in her chair. Clean desk, no laptop screen visible, "
    "no mugs. Authentic UGC style, shallow depth of field, no text or UI overlays.",
    "-m", "gemini-omni-1.2-flash", "--aspect-ratio", "9:16", "--resolution", "1080p",
    "--out", os.path.join(out10, "beat2_solution.mp4"),
])

print(f"[{s10}] Generating Voiceover (en-au-concierge-6)...", flush=True)
run_cmd([
    "gemini-api", "tts",
    "Still digging through five folders to remember which resume you sent? Save, view, and organize your resumes, "
    "portfolios, polished cover letters, and extras on one desk at appliedly dot app—and let your pinned docs power "
    "your criteria recommendations, briefings, and insights. Appliedly. Track every application. Land the right role.",
    "-m", "gemini-3.8-flash-tts",
    "-v", "en-au-concierge-6",
    "--style", "Natural, clear, warm young creator sharing a helpful tip with a friend—not a news reporter.",
    "--out", os.path.join(out10, "voiceover.wav"),
])

stitch_4beat(
    s10,
    "documents",
    "DOCUMENTS & COVER LETTERS",
    (
        "Which resume version\ndid I even send?!",
        "Files scattered across\nfolders and tabs?",
        "One library that powers\nyour whole search.",
        "ORGANIZE YOUR DOCS\nappliedly.app",
    ),
)

with open(os.path.join(final10, "tiktok.txt"), "w") as f:
    f.write(
        "=== TIKTOK UPLOAD SETTINGS ===\n"
        "File: video.mp4 (1080x1920, 9:16)\n"
        "Cover Text: Stop losing resume versions.\n"
        "Link / CTA: appliedly.app\n\n"
        "--- Caption ---\n"
        "Save, view, and pin your resumes, portfolios, polished cover letters, and extras in one place—"
        "and let them power your recommendations, briefings, and insights at appliedly.app\n\n"
        "#resume #coverletter #jobsearch #appliedly #portfolio #careeradvice #productivity\n"
    )

with open(os.path.join(final10, "youtube_shorts.txt"), "w") as f:
    f.write(
        "=== YOUTUBE SHORTS UPLOAD SETTINGS ===\n"
        "File: video.mp4 (1080x1920, 9:16)\n\n"
        "--- Title (<= 100 chars) ---\n"
        "One Document Library that powers your entire job search #Shorts\n\n"
        "--- Description ---\n"
        "Save, view, and attach your resumes, portfolios, polished cover letters, and extras on one desk.\n\n"
        "Pin your materials to drive criteria recommendations, job briefings, and sector insights.\n\n"
        "Organize your docs: https://appliedly.app\n\n"
        "#resume #coverletter #jobsearch #appliedly #Shorts\n\n"
        "--- Tags ---\n"
        "appliedly, resume organizer, portfolio, cover letter pdf, job search documents, career tools\n"
    )

with open(os.path.join(final10, "instagram_reels.txt"), "w") as f:
    f.write(
        "=== INSTAGRAM REELS UPLOAD SETTINGS ===\n"
        "File: video.mp4 (1080x1920, 9:16)\n"
        "Cover Text: Stop losing resume versions.\n\n"
        "--- Caption ---\n"
        "Save, view, and pin your resumes, portfolios, polished cover letters, and extras in one place—"
        "and let them power your recommendations, briefings, and insights at appliedly.app\n\n"
        "#resume #coverletter #jobsearch #appliedly #portfolio #careeradvice #productivity\n"
    )
