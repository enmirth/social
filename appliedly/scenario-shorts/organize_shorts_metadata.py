#!/usr/bin/env python3
"""Organize Appliedly Shorts into per-video folders with ready-to-paste TikTok, YouTube Shorts, and Instagram Reels metadata."""
import os
import shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
APPLIEDLY_DIR = os.path.dirname(SCRIPT_DIR)
SHORTS_DIR = os.path.join(APPLIEDLY_DIR, "videos", "shorts")

METADATA = [
    {
        "slug": "01_generic_spreadsheet_chaos",
        "yt_title": "Stop tracking job applications in messy spreadsheets #Shorts",
        "yt_desc": (
            "47 browser tabs open and zero idea which company ghosted you?\n\n"
            "Appliedly replaces messy job-search spreadsheets with one calm pipeline. "
            "Track every application, block repeat noise, and stay on top of every follow-up.\n\n"
            "Start tracking free: https://appliedly.app\n\n"
            "#jobsearch #careeradvice #jobtracker #appliedly #productivity #Shorts"
        ),
        "yt_tags": "appliedly, job application tracker, job search tips, career advice, spreadsheet alternative, job hunt, productivity",
        "tt_caption": (
            "47 tabs open and zero callbacks? Stop tracking jobs in messy spreadsheets. "
            "Keep your whole search calm at appliedly.app"
        ),
        "tt_tags": "#jobsearch #jobhunt #careeradvice #appliedly #productivity #corporate #jobtracker",
        "cover_text": "47 tabs open. Zero callbacks.",
    },
    {
        "slug": "02_generic_spray_and_pray",
        "yt_title": "Tired of job boards sending you random roles? #Shorts",
        "yt_desc": (
            "Stop scrolling endless job feeds that ignore what you're actually looking for.\n\n"
            "At Appliedly, you set your criteria, block the spray-and-pray noise, and focus on roles that genuinely fit.\n\n"
            "Start calm at: https://appliedly.app\n\n"
            "#jobsearch #jobhunt #career #appliedly #worklife #Shorts"
        ),
        "yt_tags": "appliedly, job recommendations, job search, career tips, job boards, stop spray and pray, job hunt",
        "tt_caption": (
            "Why do job sites keep recommending roles you'd never apply to? "
            "Set your own criteria and block the noise at appliedly.app"
        ),
        "tt_tags": "#jobsearch #jobboards #career #appliedly #jobhunting #careertok #productivity",
        "cover_text": "Tired of the spray-and-pray?",
    },
    {
        "slug": "03_applications_rounds_cover_letter",
        "yt_title": "Track interview rounds & generate tailored cover letters #Shorts",
        "yt_desc": (
            "Three interview rounds, calendar invites, and another cover letter due tonight?\n\n"
            "Keep every round, prep note, .ics calendar invite, and tailored cover letter PDF in one living board.\n\n"
            "Organize your hunt: https://appliedly.app\n\n"
            "#interviewprep #coverletter #jobsearch #appliedly #Shorts"
        ),
        "yt_tags": "appliedly, interview prep, cover letter generator, job tracker, calendar invites, job interview tips",
        "tt_caption": (
            "3 interview rounds and another cover letter due tonight? Put rounds, .ics invites, "
            "and tailored cover letter PDFs in one place at appliedly.app"
        ),
        "tt_tags": "#interviewprep #coverletter #jobinterview #appliedly #jobsearch #careeradvice",
        "cover_text": "3 rounds. 1 living board.",
    },
    {
        "slug": "04_criteria_recommendations",
        "yt_title": "Entry-level job asking for 10 years experience?! #Shorts",
        "yt_desc": (
            "Done with job alerts that ignore your actual criteria?\n\n"
            "Set your exact roles, keywords, and locations on Appliedly, pin your resume, "
            "and keep companies you already applied to or unfollowed out of your inbox.\n\n"
            "Steer your inbox: https://appliedly.app\n\n"
            "#jobsearch #resume #careeradvice #appliedly #Shorts"
        ),
        "yt_tags": "appliedly, job search criteria, resume pinning, job inbox, job alerts, career advice",
        "tt_caption": (
            "'Entry-level' asking for 10 years?! Set your real criteria, pin your resume, "
            "and block repeat companies at appliedly.app"
        ),
        "tt_tags": "#jobsearch #entrylevel #resume #appliedly #careertok #jobhunt",
        "cover_text": "'Entry-level' = 10 yrs?!",
    },
    {
        "slug": "05_briefings_company_dossier",
        "yt_title": "Walk into every interview with a full company dossier #Shorts",
        "yt_desc": (
            "Interview in 10 minutes and your company research is buried in 15 open tabs?\n\n"
            "Appliedly generates printable job briefings and public company dossiers so you walk into the room prepared.\n\n"
            "Walk in prepared: https://appliedly.app\n\n"
            "#interviewtips #companyresearch #careeradvice #appliedly #Shorts"
        ),
        "yt_tags": "appliedly, company dossier, interview prep, job briefing, company research, interview tips",
        "tt_caption": (
            "Interview in 10 mins and 15 tabs of notes? Get printable job briefings and public "
            "company dossiers at appliedly.app"
        ),
        "tt_tags": "#interviewtips #interviewprep #jobsearch #appliedly #careertok #career",
        "cover_text": "Interview in 10 mins.",
    },
    {
        "slug": "06_pro_max_tiers",
        "yt_title": "Juggling two career tracks? Use isolated Desk Profiles #Shorts",
        "yt_desc": (
            "Applying to two different career tracks shouldn't mix into one messy list.\n\n"
            "Appliedly Pro & Max give you isolated Desk Profiles, match notes on every lead, "
            "personal goals, and peer percentiles.\n\n"
            "Unlock Pro & Max: https://appliedly.app\n\n"
            "#jobsearch #productivity #careerpivot #appliedly #Shorts"
        ),
        "yt_tags": "appliedly pro, appliedly max, career pivot, job tracker, desk profiles, peer percentiles",
        "tt_caption": (
            "Juggling two career tracks in one messy list? Unlock isolated Desk Profiles, "
            "match notes, goals, and peer percentiles at appliedly.app"
        ),
        "tt_tags": "#careerpivot #jobsearch #productivity #appliedly #careertok #jobhunt",
        "cover_text": "2 career tracks. 1 calm app.",
    },
    {
        "slug": "07_briefing_insights",
        "yt_title": "Stop guessing your salary target on job applications #Shorts",
        "yt_desc": (
            "Not sure if a role is paying fair or which skills are trending?\n\n"
            "Appliedly Briefing Insights show hiring velocity, 25th-to-90th pay quartiles, "
            "and skill momentum across your sector.\n\n"
            "Negotiate smarter: https://appliedly.app\n\n"
            "#salarynegotiation #careeradvice #jobmarket #appliedly #Shorts"
        ),
        "yt_tags": "appliedly, salary negotiation, pay quartiles, hiring trends, briefing insights, career advice",
        "tt_caption": (
            "Guessing your salary target blind? See 25th-to-90th pay quartiles, hiring velocity, "
            "and skill momentum at appliedly.app"
        ),
        "tt_tags": "#salarynegotiation #salary #jobmarket #appliedly #careertok #careeradvice",
        "cover_text": "Stop guessing salary.",
    },
    {
        "slug": "08_the_desk",
        "yt_title": "Every application, resume & alert on one calm Desk #Shorts",
        "yt_desc": (
            "Applications in one tab, resumes in three folders, follow-ups forgotten in your inbox.\n\n"
            "Put everything on one calm desk: applications, recommendations, criteria, alerts, and honest exclusions.\n\n"
            "Build your Desk: https://appliedly.app\n\n"
            "#jobsearch #organization #career #appliedly #Shorts"
        ),
        "yt_tags": "appliedly, career desk, job search organization, resume manager, job tracker",
        "tt_caption": (
            "Resumes in 3 folders and follow-ups forgotten? Put every app, alert, and file "
            "on one calm Desk at appliedly.app"
        ),
        "tt_tags": "#jobsearch #organization #career #appliedly #productivity #careertok",
        "cover_text": "One calm career Desk.",
    },
]

os.makedirs(SHORTS_DIR, exist_ok=True)

for item in METADATA:
    slug = item["slug"]
    folder = os.path.join(SHORTS_DIR, slug)
    os.makedirs(folder, exist_ok=True)

    # Move flat <slug>.mp4 into <slug>/video.mp4 if present
    flat_mp4 = os.path.join(SHORTS_DIR, f"{slug}.mp4")
    dest_mp4 = os.path.join(folder, "video.mp4")
    if os.path.exists(flat_mp4) and not os.path.exists(dest_mp4):
        shutil.move(flat_mp4, dest_mp4)

    with open(os.path.join(folder, "tiktok.txt"), "w") as f:
        f.write(
            f"=== TIKTOK UPLOAD SETTINGS ===\n"
            f"File: video.mp4 (1080x1920, 9:16)\n"
            f"Cover Text: {item['cover_text']}\n"
            f"Link / CTA: appliedly.app\n\n"
            f"--- Caption ---\n"
            f"{item['tt_caption']}\n\n"
            f"{item['tt_tags']}\n\n"
            f"--- Recommended Settings ---\n"
            f"- Who can watch: Everyone\n"
            f"- Allow comments / duet / stitch: On\n"
            f"- Auto-captions: Optional (video already has burned-in captions)\n"
        )

    with open(os.path.join(folder, "youtube_shorts.txt"), "w") as f:
        f.write(
            f"=== YOUTUBE SHORTS UPLOAD SETTINGS ===\n"
            f"File: video.mp4 (1080x1920, 9:16)\n\n"
            f"--- Title (<= 100 chars) ---\n"
            f"{item['yt_title']}\n\n"
            f"--- Description ---\n"
            f"{item['yt_desc']}\n\n"
            f"--- Tags ---\n"
            f"{item['yt_tags']}\n\n"
            f"--- Recommended Settings ---\n"
            f"- Visibility: Public\n"
            f"- Audience: No, it's not made for kids\n"
            f"- Category: Science & Technology (or Howto & Style)\n"
        )

    with open(os.path.join(folder, "instagram_reels.txt"), "w") as f:
        f.write(
            f"=== INSTAGRAM REELS UPLOAD SETTINGS ===\n"
            f"File: video.mp4 (1080x1920, 9:16)\n"
            f"Cover Text: {item['cover_text']}\n\n"
            f"--- Caption ---\n"
            f"{item['tt_caption']}\n\n"
            f"{item['tt_tags']}\n"
        )

print(f"Organized {len(METADATA)} folders in {SHORTS_DIR}")
