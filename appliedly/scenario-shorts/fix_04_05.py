#!/usr/bin/env python3
"""Fix 04 and 05: regenerate silent no-talking Beat 2s, add focused commercial feature cards, and lock outro to 4.8s."""
import json
import os
import subprocess
from datetime import date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
APPLIEDLY_DIR = os.path.dirname(SCRIPT_DIR)
OUT_BASE = os.path.join(SCRIPT_DIR, "out")
FINAL_DIR = os.path.join(APPLIEDLY_DIR, "videos", "shorts")
TRACKER_PATH = os.path.join(SCRIPT_DIR, "usage_tracker.json")
RENDER_OUTRO = os.path.join(SCRIPT_DIR, "render_outro_and_captions.py")
RENDER_CARDS = os.path.join(SCRIPT_DIR, "render_feature_cards.py")

ENV = os.environ.copy()
ENV["PATH"] = os.path.expanduser("~/.local/bin") + ":" + ENV.get("PATH", "")


def run_cmd(cmd: list[str]) -> str:
    res = subprocess.run(cmd, env=ENV, check=True, capture_output=True, text=True)
    return res.stdout.strip()


def update_tracker(omni_inc: int) -> str:
    today = date.today().isoformat()
    with open(TRACKER_PATH) as f:
        data = json.load(f)
    omni = data.setdefault("gemini-omni-1.2-flash", {"daily_used": 0, "daily_limit": 40, "rpm_limit": 8})
    omni["daily_used"] += omni_inc
    with open(TRACKER_PATH, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    return f"Quota ({today}): Gemini Omni 1.2 Flash {omni['daily_used']} / {omni['daily_limit']} RPD"


JOBS = [
    {
        "slug": "04_criteria_recommendations",
        "card_kind": "criteria",
        "kicker": "CRITERIA YOU STEER",
        "new_b2_prompt": (
            "Vertical 9:16 realistic handheld smartphone video, side-profile angle of an East Asian woman "
            "in her mid-20s in a sunlit room, mouth closed and not speaking, smiling warmly with relief and "
            "giving a gentle nod while looking at her open laptop facing her (solid aluminum lid back, no screen "
            "facing camera). Authentic UGC style, shallow depth of field, no text or UI overlays."
        ),
        "cap1": "'Entry-level' job.\n10 years required?!",
        "cap2": "Job boards ignore\nyour real criteria.",
        "cap3": "Curated matches.\nZero repeat noise.",
        "cap4": "STEER YOUR INBOX\nappliedly.app",
    },
    {
        "slug": "05_briefings_company_dossier",
        "card_kind": "dossier",
        "kicker": "COMPANY DOSSIERS",
        "new_b2_prompt": (
            "Vertical 9:16 realistic handheld smartphone video, medium close-up of a Hispanic man in his late 20s "
            "wearing a button-down shirt in a bright sunlit room, mouth closed and not speaking, smiling with calm "
            "confidence and leaning back in his chair before his interview, framed chest-up with no laptop screen "
            "visible. Authentic UGC style, shallow depth of field, no text or UI overlays."
        ),
        "cap1": "Interview in 10 mins.\n15 tabs of notes.",
        "cap2": "Scrambling to research\nthe company?",
        "cap3": "Walk in prepared.\nEvery detail ready.",
        "cap4": "WALK IN PREPARED\nappliedly.app",
    },
]

for job in JOBS:
    slug = job["slug"]
    out_dir = os.path.join(OUT_BASE, slug)
    b1 = os.path.join(out_dir, "beat1_problem.mp4")
    b2 = os.path.join(out_dir, "beat2_solution.mp4")
    b2_5 = os.path.join(out_dir, "beat2_5_feature.mp4")
    b3 = os.path.join(out_dir, "beat3_outro.mp4")
    vo = os.path.join(out_dir, "voiceover.wav")
    final_mp4 = os.path.join(FINAL_DIR, slug, "video.mp4")

    print(f"[{slug}] Regenerating Beat 2 (clean silent reaction)...", flush=True)
    run_cmd([
        "gemini-api", "video", job["new_b2_prompt"],
        "-m", "gemini-omni-1.2-flash",
        "--aspect-ratio", "9:16",
        "--resolution", "1080p",
        "--out", b2,
    ])
    print(update_tracker(1), flush=True)

    vo_dur = float(run_cmd([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", vo
    ]))

    b1_dur = 5.5
    b2_dur = 4.5
    outro_dur = 4.8
    total_dur = round(vo_dur + 0.4, 2)
    card_dur = round(total_dur - b1_dur - b2_dur - outro_dur, 2)

    print(f"[{slug}] Rendering feature card ({card_dur}s) & outro ({outro_dur}s) for VO={vo_dur:.2f}s...", flush=True)
    run_cmd(["python3", RENDER_CARDS, job["card_kind"], b2_5, "--duration", str(card_dur)])
    run_cmd([
        "python3", RENDER_OUTRO, out_dir,
        "--kicker", job["kicker"],
        "--duration", str(outro_dur),
        "--cap1", job["cap1"],
        "--cap2", job["cap2"],
        "--cap3", job["cap3"],
        "--cap4", job["cap4"],
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
    print(f"[{slug}] FIXED -> {final_mp4} ({total_dur}s)", flush=True)
