#!/usr/bin/env python3
"""Batch generator for Appliedly's 7 themed TikTok/Shorts scenarios."""
import json
import os
import subprocess
import sys
from datetime import date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
APPLIEDLY_DIR = os.path.dirname(SCRIPT_DIR)
OUT_BASE = os.path.join(SCRIPT_DIR, "out")
FINAL_DIR = os.path.join(APPLIEDLY_DIR, "videos", "shorts")
TRACKER_PATH = os.path.join(SCRIPT_DIR, "usage_tracker.json")
RENDER_PY = os.path.join(SCRIPT_DIR, "render_outro_and_captions.py")

ENV = os.environ.copy()
ENV["PATH"] = os.path.expanduser("~/.local/bin") + ":" + ENV.get("PATH", "")

SCENARIOS = [
    {
        "slug": "02_generic_spray_and_pray",
        "kicker": "CALM JOB SEARCH",
        "voice": "aoede",
        "style": "Warm, relatable young creator talking to a friend—mildly fed up at first, then relieved and upbeat.",
        "vo": "Why do job sites keep sending you random roles you'd never apply to? Stop scrolling noise. Go to appliedly dot app—set your criteria, block the spray, and focus on roles that actually fit. Appliedly. Track every application. Land the right role.",
        "problem_prompt": "Vertical 9:16 realistic handheld smartphone video of a Black woman in her late 20s sitting on a couch in the evening, sighing and looking annoyed as she scrolls past irrelevant job listings on her phone. Warm indoor lamp lighting, authentic UGC style, shallow depth of field, no text or UI overlays.",
        "solution_prompt": "Vertical 9:16 realistic handheld smartphone video of a Black woman in her late 20s in the morning at a bright sunny cafe table, smiling calmly as she taps her phone and sips a latte. Natural morning light, authentic UGC style, shallow depth of field, no text or UI overlays.",
        "cap1": "Endless job feeds.\nZero real matches.",
        "cap2": "Tired of the\nspray-and-pray?",
        "cap3": "Roles you steer.\nNoise filtered out.",
        "cap4": "START CALM AT\nappliedly.app",
    },
    {
        "slug": "03_applications_rounds_cover_letter",
        "kicker": "INTERVIEWS & COVER LETTERS",
        "voice": "algieba",
        "style": "Smooth, confident, conversational creator—starts slightly rushed, then calm and assured.",
        "vo": "Three interview rounds, two calendar invites, and another cover letter due tonight? Put it all in one living board at appliedly dot app. Track every round, export calendar invites, and generate tailored cover letters straight from the role. Appliedly. Track every application. Land the right role.",
        "problem_prompt": "Vertical 9:16 realistic handheld smartphone video, medium close-up of a South Asian man in his early 30s at a home desk covered in sticky notes, looking stressed as he checks his watch and flips through papers before a video call. Only the solid silver aluminum back of his closed or angled laptop lid is visible in the foreground, no screen facing the camera. Natural indoor lighting, authentic UGC style, no text or UI overlays.",
        "solution_prompt": "Vertical 9:16 realistic handheld smartphone video, medium close-up of a South Asian man in his early 30s looking calm, smiling, and prepared at a clean desk with a notebook and pen before his video call. Bright natural daylight, authentic UGC style, no text or UI overlays.",
        "cap1": "3 interview rounds.\nMissing prep notes?",
        "cap2": "Writing cover letters\nfrom scratch again?",
        "cap3": "Rounds, .ics invites\n& tailored PDFs.",
        "cap4": "ORGANIZE YOUR HUNT\nappliedly.app",
    },
    {
        "slug": "04_criteria_recommendations",
        "kicker": "CRITERIA YOU STEER",
        "voice": "autonoe",
        "style": "Bright, energetic, relatable TikTok creator—playfully frustrated at first, then excited and clear.",
        "vo": "Ever get recommended a 'junior' role asking for ten years of experience? At appliedly dot app, you set the exact criteria, pin your resume, and companies you already applied to or unfollowed stay out for good. Appliedly. Track every application. Land the right role.",
        "problem_prompt": "Vertical 9:16 realistic handheld smartphone video, side-profile angle of an East Asian woman in her mid-20s at a cozy desk, squinting and shaking her head in disbelief at an open laptop facing her (solid matte aluminum lid back angled toward camera, screen facing only her). Natural indoor lighting, authentic UGC style, no text or UI overlays.",
        "solution_prompt": "Vertical 9:16 realistic handheld smartphone video, side-profile angle of an East Asian woman in her mid-20s smiling brightly and nodding at her open laptop facing her in a sunlit room (solid aluminum lid back, no screen facing camera). Authentic UGC style, no text or UI overlays.",
        "cap1": "'Entry-level' job.\n10 years required?!",
        "cap2": "Job boards ignore\nyour real criteria.",
        "cap3": "Pin your resume.\nBlock repeat noise.",
        "cap4": "STEER YOUR INBOX\nappliedly.app",
    },
    {
        "slug": "05_briefings_company_dossier",
        "kicker": "COMPANY DOSSIERS",
        "voice": "en-au-podcaster-2",
        "style": "Clear, engaging storyteller—starts tense like pre-interview panic, then composed and confident.",
        "vo": "Ten minutes until your interview and your company research is buried in fifteen open tabs? Appliedly builds printable job briefings and public company dossiers so you walk into the room prepared. Check it out at appliedly dot app. Appliedly. Track every application. Land the right role.",
        "problem_prompt": "Vertical 9:16 realistic handheld smartphone video, medium close-up of a Hispanic man in his late 20s wearing a button-down shirt, frantically typing on a keyboard and glancing at his watch 10 minutes before an interview, camera framed from chest up so no laptop screen is visible. Authentic UGC style, natural room lighting, no text or UI overlays.",
        "solution_prompt": "Vertical 9:16 realistic handheld smartphone video, medium close-up of a Hispanic man in his late 20s wearing a button-down shirt, smiling calmly and leaning back with confidence at a tidy desk before starting his video interview, framed chest-up with no laptop screen visible. Bright natural daylight, authentic UGC style, no text or UI overlays.",
        "cap1": "Interview in 10 mins.\n15 tabs of notes.",
        "cap2": "Scrambling to research\nthe company?",
        "cap3": "Printable briefings &\ncompany dossiers.",
        "cap4": "WALK IN PREPARED\nappliedly.app",
    },
    {
        "slug": "06_pro_max_tiers",
        "kicker": "PRO & MAX TIERS",
        "voice": "despina",
        "style": "Polished, modern commercial creator—conversational, sharp, and inspiring.",
        "vo": "Applying to two totally different career tracks shouldn't mix into one messy list. Upgrade to Pro or Max at appliedly dot app for isolated Desk Profiles, match notes on every lead, personal goals, and peer percentiles. Appliedly. Track every application. Land the right role.",
        "problem_prompt": "Vertical 9:16 realistic handheld smartphone video, medium shot of a woman in her 30s with curly dark hair looking overwhelmed at a cluttered desk stacked with folders and sticky notes, no laptop screen in frame. Natural indoor lighting, authentic UGC style, no text or UI overlays.",
        "solution_prompt": "Vertical 9:16 realistic handheld smartphone video, medium shot of a woman in her 30s with curly dark hair smiling calmly in a clean, stylish modern workspace with a neat desk and coffee cup, no laptop screen in frame. Warm sunlit room, authentic UGC style, no text or UI overlays.",
        "cap1": "Juggling two career\ntracks in one list?",
        "cap2": "No match notes.\nNo real benchmarks.",
        "cap3": "Isolated Desks, Goals\n& Peer Percentiles.",
        "cap4": "UNLOCK PRO & MAX\nappliedly.app",
    },
    {
        "slug": "07_briefing_insights",
        "kicker": "MARKET & PAY INSIGHTS",
        "voice": "en-au-storyteller-2",
        "style": "Bright, youthful, conversational creator—starts uncertain, then confident and empowered.",
        "vo": "Guessing your salary target on an application form? Don't fly blind. Appliedly Briefing Insights show hiring velocity, twenty-fifth to ninetieth pay quartiles, and skill momentum across your sector. See where you stand at appliedly dot app. Appliedly. Track every application. Land the right role.",
        "problem_prompt": "Vertical 9:16 realistic handheld smartphone video, side-profile shot of a Black man in his early 30s at his kitchen table, pausing thoughtfully and looking uncertain while staring at a laptop facing him (only the solid silver aluminum back of the lid visible). Natural daylight, authentic UGC style, no text or UI overlays.",
        "solution_prompt": "Vertical 9:16 realistic handheld smartphone video, medium close-up of a Black man in his early 30s smiling with quiet confidence and nodding during a conversation, framed chest-up with no laptop in frame. Bright natural light, authentic UGC style, no text or UI overlays.",
        "cap1": "Guessing your salary\ntarget blind?",
        "cap2": "No idea if a role\nis paying fair?",
        "cap3": "Pay quartiles, velocity\n& skill momentum.",
        "cap4": "NEGOTIATE SMARTER\nappliedly.app",
    },
    {
        "slug": "08_the_desk",
        "kicker": "YOUR CAREER DESK",
        "voice": "callirrhoe",
        "style": "Relaxed, friendly, encouraging guide—warm and grounded, like showing a friend a cleaner setup.",
        "vo": "Applications in one tab, resumes in three folders, follow-ups forgotten in your inbox. Put everything on one calm desk at appliedly dot app—applications, recommendations, criteria, alerts, and honest exclusions. Appliedly. Track every application. Land the right role.",
        "problem_prompt": "Vertical 9:16 realistic handheld smartphone video, front-three-quarter angle of a man in his late 40s with glasses rubbing his temples while looking at scattered paper folders and an overflowing desk. Natural indoor light, authentic UGC style, no text or UI overlays.",
        "solution_prompt": "Vertical 9:16 realistic handheld smartphone video, front-three-quarter angle of a man in his late 40s with glasses smiling warmly in a clean, sunlit home office with a tidy desk and coffee mug. Authentic UGC style, no text or UI overlays.",
        "cap1": "Resumes in 3 folders.\nFollow-ups forgotten.",
        "cap2": "Too many tools\nfor one job search?",
        "cap3": "Every app, alert &\nfile on one Desk.",
        "cap4": "BUILD YOUR DESK\nappliedly.app",
    },
]


def update_tracker(omni_inc: int, tts_inc: int) -> str:
    today = date.today().isoformat()
    try:
        with open(TRACKER_PATH) as f:
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

    with open(TRACKER_PATH, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")

    return f"Quota ({today}): Gemini Omni 1.2 Flash {omni['daily_used']} / {omni['daily_limit']} RPD | TTS {tts['daily_used']} calls"


def run_cmd(cmd: list[str], retries: int = 2) -> str:
    import time
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


def build_one(sc: dict) -> None:
    slug = sc["slug"]
    out_dir = os.path.join(OUT_BASE, slug)
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(FINAL_DIR, exist_ok=True)

    b1 = os.path.join(out_dir, "beat1_problem.mp4")
    b2 = os.path.join(out_dir, "beat2_solution.mp4")
    vo = os.path.join(out_dir, "voiceover.wav")
    final_folder = os.path.join(FINAL_DIR, slug)
    os.makedirs(final_folder, exist_ok=True)
    final_mp4 = os.path.join(final_folder, "video.mp4")

    omni_inc = 0
    tts_inc = 0

    if not os.path.exists(b1):
        print(f"[{slug}] Generating Beat 1 (Problem)...", flush=True)
        run_cmd([
            "gemini-api", "video", sc["problem_prompt"],
            "-m", "gemini-omni-1.2-flash",
            "--aspect-ratio", "9:16",
            "--resolution", "1080p",
            "--out", b1,
        ])
        omni_inc += 1

    if not os.path.exists(b2):
        print(f"[{slug}] Generating Beat 2 (Solution)...", flush=True)
        run_cmd([
            "gemini-api", "video", sc["solution_prompt"],
            "-m", "gemini-omni-1.2-flash",
            "--aspect-ratio", "9:16",
            "--resolution", "1080p",
            "--out", b2,
        ])
        omni_inc += 1

    if not os.path.exists(vo):
        print(f"[{slug}] Generating Voiceover ({sc['voice']})...", flush=True)
        run_cmd([
            "gemini-api", "tts", sc["vo"],
            "-m", "gemini-3.8-flash-tts",
            "-v", sc["voice"],
            "--style", sc["style"],
            "--out", vo,
        ])
        tts_inc += 1

    vo_dur = float(run_cmd([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", vo
    ]))
    # Beat 1 (5.0s) + Beat 2 (6.0s) = 11.0s; make Beat 3 long enough for voiceover + 0.7s tail (min 5.5s)
    outro_dur = max(5.5, round(vo_dur - 11.0 + 0.7, 2))
    total_dur = round(11.0 + outro_dur, 2)

    print(f"[{slug}] Rendering outro ({outro_dur}s) & captions (VO={vo_dur:.2f}s)...", flush=True)
    run_cmd([
        "python3", RENDER_PY, out_dir,
        "--kicker", sc["kicker"],
        "--duration", str(outro_dur),
        "--cap1", sc["cap1"],
        "--cap2", sc["cap2"],
        "--cap3", sc["cap3"],
        "--cap4", sc["cap4"],
    ])

    print(f"[{slug}] Stitching final MP4 ({total_dur}s)...", flush=True)
    b3 = os.path.join(out_dir, "beat3_outro.mp4")
    c1 = os.path.join(out_dir, "cap1.png")
    c2 = os.path.join(out_dir, "cap2.png")
    c3 = os.path.join(out_dir, "cap3.png")
    c4 = os.path.join(out_dir, "cap4.png")

    filter_complex = (
        f"[0:v]trim=duration=5,setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[v0]; "
        f"[1:v]trim=duration=6,setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[v1]; "
        f"[2:v]trim=duration={outro_dur},setpts=PTS-STARTPTS,fps=30,setsar=1[v2]; "
        f"[v0][v1][v2]concat=n=3:v=1:a=0[vbase]; "
        f"[vbase][3:v]overlay=0:0:enable='between(t,0.1,2.5)'[vc1]; "
        f"[vc1][4:v]overlay=0:0:enable='between(t,2.5,5.0)'[vc2]; "
        f"[vc2][5:v]overlay=0:0:enable='between(t,5.1,8.2)'[vc3]; "
        f"[vc3][6:v]overlay=0:0:enable='between(t,8.2,10.9)'[vout]; "
        f"[7:a]aresample=48000,apad=whole_dur={total_dur}[aout]"
    )

    run_cmd([
        "ffmpeg", "-y",
        "-i", b1, "-i", b2, "-i", b3,
        "-i", c1, "-i", c2, "-i", c3, "-i", c4,
        "-i", vo,
        "-filter_complex", filter_complex,
        "-map", "[vout]", "-map", "[aout]",
        "-t", str(total_dur),
        "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
        final_mp4,
    ])

    status = update_tracker(omni_inc, tts_inc)
    print(f"[{slug}] DONE -> {final_mp4} | {status}", flush=True)


if __name__ == "__main__":
    targets = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    for sc in SCENARIOS:
        if targets and sc["slug"] not in targets:
            continue
        build_one(sc)
