#!/usr/bin/env python3
"""Render focused, Apple/Linear-style animated commercial UI feature cards & right-to-left swish carousels at 1080x1920 @ 30fps."""
import argparse
import os
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
FPS = 30


def load_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def ease_out_cubic(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 1.0 - (1.0 - t) ** 3


def ease_in_out_cubic(t: float) -> float:
    t = max(0.0, min(1.0, t))
    if t < 0.5:
        return 4.0 * t * t * t
    return 1.0 - ((-2.0 * t + 2.0) ** 3) / 2.0


def ease_out_back(t: float) -> float:
    t = max(0.0, min(1.0, t))
    c1 = 1.70158
    c3 = c1 + 1.0
    return 1.0 + c3 * ((t - 1.0) ** 3) + c1 * ((t - 1.0) ** 2)


def make_bg() -> Image.Image:
    bg = Image.new("RGBA", (W, H), (10, 18, 32, 255))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    cx, cy = W // 2, int(H * 0.45)
    for r in range(620, 60, -35):
        frac = 1.0 - (r / 620.0)
        a = int(255 * 0.25 * (frac ** 1.8) * 0.22)
        gd.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(96, 165, 250, a))
    glow = glow.filter(ImageFilter.GaussianBlur(40))
    return Image.alpha_composite(bg, glow)


def draw_pill(d: ImageDraw.ImageDraw, x: int, y: int, text: str, font, fill_col, text_col, outline_col=None, pad_x=28, h=52) -> int:
    """Draw a pill auto-sized to its exact text width and return its right x coordinate."""
    bb = d.textbbox((0, 0), text, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pw = tw + pad_x * 2
    d.rounded_rectangle((x, y, x + pw, y + h), radius=h // 2, fill=fill_col, outline=outline_col, width=2 if outline_col else 0)
    d.text((x + pad_x, y + (h - th) // 2 - 3), text, font=font, fill=text_col)
    return x + pw


def encode_frames(tmpdir: str, out_mp4: str) -> None:
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-framerate", str(FPS),
            "-i", os.path.join(tmpdir, "frame_%04d.png"),
            "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
            out_mp4,
        ],
        check=True,
        capture_output=True,
    )


def build_swish_slides(slides: list[Image.Image], duration: float, out_mp4: str) -> None:
    """Composite a list of 1080x1920 RGBA slide layers over base_bg with smooth right-to-left swish transitions."""
    base_bg = make_bg()
    n = len(slides)
    seg_dur = duration / n
    trans_dur = min(0.55, seg_dur * 0.30)

    total_frames = int(round(duration * FPS))
    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(total_frames):
            t = i / FPS
            frame = base_bg.copy()

            # Determine active slide and whether we are swishing to next
            idx = min(n - 1, int(t / seg_dur))
            local_t = t - idx * seg_dur

            # Initial entrance on slide 0
            if idx == 0 and local_t < 0.40:
                p = ease_out_cubic(local_t / 0.40)
                dx = int((1.0 - p) * 140)
                s_cur = slides[0]
                r, g, b, a = s_cur.split()
                a = a.point(lambda px: int(px * p))
                frame.alpha_composite(Image.merge("RGBA", (r, g, b, a)), (dx, 0))
            elif idx < n - 1 and local_t >= seg_dur - trans_dur:
                # Swish current slide out left, next slide in from right
                tp = ease_in_out_cubic((local_t - (seg_dur - trans_dur)) / trans_dur)
                out_x = int(-W * tp)
                in_x = int(W * (1.0 - tp))
                frame.alpha_composite(slides[idx], (out_x, 0))
                frame.alpha_composite(slides[idx + 1], (in_x, 0))
            else:
                frame.alpha_composite(slides[idx], (0, 0))

            frame.convert("RGB").save(os.path.join(tmpdir, f"frame_{i:04d}.png"))
        encode_frames(tmpdir, out_mp4)


def render_pro_max(out_mp4: str, duration: float) -> None:
    """3-slide right-to-left swish showcase for Pro & Max (Desk Profiles, Match Notes & Criteria, Goals & Percentiles)."""
    f_eyebrow = load_font(30, bold=True)
    f_title = load_font(54, bold=True)
    f_card_title = load_font(38, bold=True)
    f_body = load_font(32, bold=False)
    f_badge = load_font(28, bold=True)

    # Slide 1: Isolated Desk Profiles
    s1 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d1 = ImageDraw.Draw(s1)
    d1.text((90, 290), "PRO & MAX · 1 OF 3", font=f_eyebrow, fill=(96, 165, 250, 255))
    d1.text((90, 340), "Isolated Desk Profiles", font=f_title, fill=(255, 255, 255, 255))
    d1.rounded_rectangle((90, 460, 990, 820), radius=32, fill=(14, 24, 40, 240), outline=(96, 165, 250, 140), width=2)
    d1.text((135, 505), "Separate tracks. Zero overlap.", font=f_card_title, fill=(255, 255, 255, 255))
    d1.text((135, 565), "Each Desk isolates its own applications,", font=f_body, fill=(180, 198, 224, 255))
    d1.text((135, 610), "criteria, recommendations & custom theme.", font=f_body, fill=(180, 198, 224, 255))
    x_next = draw_pill(d1, 135, 700, "Desk 1: Product Lead", f_badge, (37, 99, 235, 255), (255, 255, 255, 255))
    draw_pill(d1, x_next + 20, 700, "Desk 2: Advisory", f_badge, (24, 38, 62, 255), (147, 197, 253, 255), outline_col=(96, 165, 250, 200))

    # Slide 2: Match Notes & Multiple Criteria
    s2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(s2)
    d2.text((90, 290), "PRO & MAX · 2 OF 3", font=f_eyebrow, fill=(52, 211, 153, 255))
    d2.text((90, 340), "Match Notes & Criteria", font=f_title, fill=(255, 255, 255, 255))
    d2.rounded_rectangle((90, 460, 990, 860), radius=32, fill=(14, 24, 40, 240), outline=(52, 211, 153, 150), width=2)
    draw_pill(d2, 135, 505, "WHY IT FITS YOUR CRITERIA", f_badge, (16, 185, 129, 55), (52, 211, 153, 255), outline_col=(52, 211, 153, 255))
    d2.text((135, 585), "Staff API Product Manager", font=f_card_title, fill=(255, 255, 255, 255))
    d2.text((135, 648), "• Matches 6+ yrs B2B SaaS platform scope", font=f_body, fill=(216, 228, 242, 255))
    d2.text((135, 698), "• Remote EU/US · Base above target", font=f_body, fill=(216, 228, 242, 255))
    d2.text((135, 748), "• Save & copy multiple criteria sets across Desks", font=f_body, fill=(147, 197, 253, 255))

    # Slide 3: Max Goals & Peer Percentiles
    s3 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d3 = ImageDraw.Draw(s3)
    d3.text((90, 290), "MAX TIER · 3 OF 3", font=f_eyebrow, fill=(96, 165, 250, 255))
    d3.text((90, 340), "Goals & Peer Percentiles", font=f_title, fill=(255, 255, 255, 255))
    d3.rounded_rectangle((90, 460, 990, 870), radius=32, fill=(14, 24, 40, 240), outline=(96, 165, 250, 140), width=2)
    d3.text((135, 505), "Interview Rate vs. Peers", font=f_card_title, fill=(255, 255, 255, 255))
    d3.rounded_rectangle((135, 585, 945, 627), radius=21, fill=(24, 38, 62, 255))
    d3.rounded_rectangle((135, 585, 845, 627), radius=21, fill=(96, 165, 250, 255))
    draw_pill(d3, 135, 665, "TOP 12% INTERVIEW RATE", f_badge, (37, 99, 235, 255), (255, 255, 255, 255))
    d3.text((135, 745), "Track apply streaks, offer rates & custom themes.", font=f_body, fill=(180, 198, 224, 255))

    build_swish_slides([s1, s2, s3], duration, out_mp4)


def render_dossier(out_mp4: str, duration: float) -> None:
    """2-slide right-to-left swish for Briefings & Company Dossier: Overview -> Live Recommendation Briefing Sample."""
    f_eyebrow = load_font(30, bold=True)
    f_title = load_font(54, bold=True)
    f_card_title = load_font(36, bold=True)
    f_body = load_font(30, bold=False)
    f_badge = load_font(26, bold=True)

    # Slide 1: Overview
    s1 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d1 = ImageDraw.Draw(s1)
    d1.text((90, 240), "BRIEFINGS & DOSSIERS", font=f_eyebrow, fill=(96, 165, 250, 255))
    d1.text((90, 290), "Walk into the room ready.", font=f_title, fill=(255, 255, 255, 255))
    rows = [
        ("Fit & Interview Gates", "Role alignment, key risks & prep focus", "READY", (52, 211, 153)),
        ("Company Dossier", "Business model, leadership & public profile", "PRO & MAX", (96, 165, 250)),
        ("Printable PDF Briefing", "Clean summary you take into the room", "EXPORT PDF", (147, 197, 253)),
    ]
    for idx, (title, sub, tag, col) in enumerate(rows):
        ry = 430 + idx * 245
        d1.rounded_rectangle((90, ry, 990, ry + 210), radius=32, fill=(14, 24, 40, 240), outline=(*col, 150), width=2)
        d1.text((130, ry + 36), title, font=f_card_title, fill=(255, 255, 255, 255))
        d1.text((130, ry + 98), sub, font=f_body, fill=(180, 198, 224, 255))
        tb = d1.textbbox((0, 0), tag, font=f_badge)
        pw = (tb[2] - tb[0]) + 44
        draw_pill(d1, 950 - pw, ry + 32, tag, f_badge, (*col, 45), (*col, 255), outline_col=(*col, 255), pad_x=22, h=48)

    # Slide 2: Live Recommendation Briefing Demo
    s2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(s2)
    d2.text((90, 240), "GENERATED BRIEFING SAMPLE", font=f_eyebrow, fill=(52, 211, 153, 255))
    d2.text((90, 290), "From Recommendation → Prep", font=f_title, fill=(255, 255, 255, 255))
    d2.rounded_rectangle((90, 420, 990, 1180), radius=32, fill=(14, 24, 40, 245), outline=(96, 165, 250, 180), width=2)
    x1 = draw_pill(d2, 130, 465, "FIT SCORE: 92%", f_badge, (16, 185, 129, 50), (52, 211, 153, 255), outline_col=(52, 211, 153, 255), pad_x=22, h=48)
    draw_pill(d2, x1 + 18, 465, "DOSSIER ATTACHED", f_badge, (37, 99, 235, 50), (147, 197, 253, 255), outline_col=(96, 165, 250, 255), pad_x=22, h=48)
    d2.text((130, 545), "Senior Platform Engineer · FinTech", font=f_card_title, fill=(255, 255, 255, 255))
    d2.text((130, 615), "Interview Gates:", font=f_badge, fill=(96, 165, 250, 255))
    d2.text((130, 660), "• Distributed systems & idempotent billing", font=f_body, fill=(216, 228, 242, 255))
    d2.text((130, 705), "• High-throughput API reliability", font=f_body, fill=(216, 228, 242, 255))
    d2.text((130, 775), "Company Dossier:", font=f_badge, fill=(52, 211, 153, 255))
    d2.text((130, 820), "• Public FinTech · Global payments infra", font=f_body, fill=(216, 228, 242, 255))
    d2.text((130, 865), "• Recent focus: real-time ledger & AI fraud", font=f_body, fill=(216, 228, 242, 255))
    d2.text((130, 935), "Next Step:", font=f_badge, fill=(147, 197, 253, 255))
    d2.text((130, 980), "Review payment-retry architecture + export PDF", font=f_body, fill=(255, 255, 255, 255))
    draw_pill(d2, 130, 1065, "EXPORT BRIEFING PDF", f_badge, (37, 99, 235, 255), (255, 255, 255, 255), pad_x=28, h=54)

    build_swish_slides([s1, s2], duration, out_mp4)


def render_desk(out_mp4: str, duration: float) -> None:
    """2-slide right-to-left swish for The Desk (6 roomy entries per slide filling the vertical frame cleanly)."""
    f_eyebrow = load_font(30, bold=True)
    f_title = load_font(56, bold=True)
    f_card_title = load_font(36, bold=True)
    f_body = load_font(29, bold=False)
    f_badge = load_font(23, bold=True)

    # Slide 1: Core Desk & Companion (6 elongated entries)
    s1 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d1 = ImageDraw.Draw(s1)
    d1.text((90, 175), "YOUR CAREER DESK", font=f_eyebrow, fill=(96, 165, 250, 255))
    d1.text((90, 222), "Everything in one place.", font=f_title, fill=(255, 255, 255, 255))
    tiles1 = [
        ("Welcoming Assistant", "Personal companion guiding daily next steps", "COMPANION", (96, 165, 250)),
        ("Applications & Rounds", "Status, prep notes & .ics calendar invites", "LIVE BOARD", (147, 197, 253)),
        ("Recommendations & Criteria", "Roles you steer, tuned to your criteria", "CURATED", (52, 211, 153)),
        ("Documents & Cover Letters", "Resumes, portfolios & tailored PDFs", "ORGANIZED", (96, 165, 250)),
        ("Archive & Unfollow", "Clear noise & keep exclusions locked", "CLEAN INBOX", (52, 211, 153)),
        ("Smart Alerts", "Interview reminders & overdue follow-ups", "ON TIME", (147, 197, 253)),
    ]
    for idx, (title, sub, tag, col) in enumerate(tiles1):
        ty = 325 + idx * 205
        d1.rounded_rectangle((90, ty, 990, ty + 178), radius=28, fill=(14, 24, 40, 240), outline=(*col, 135), width=2)
        d1.text((130, ty + 32), title, font=f_card_title, fill=(255, 255, 255, 255))
        d1.text((130, ty + 96), sub, font=f_body, fill=(180, 198, 224, 255))
        tb = d1.textbbox((0, 0), tag, font=f_badge)
        pw = (tb[2] - tb[0]) + 40
        draw_pill(d1, 952 - pw, ty + 28, tag, f_badge, (*col, 45), (*col, 255), outline_col=(*col, 255), pad_x=20, h=44)

    # Slide 2: Intelligence, Statistics, Personalization & Security (6 elongated entries)
    s2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(s2)
    d2.text((90, 175), "BUILT FOR YOUR SEARCH", font=f_eyebrow, fill=(52, 211, 153, 255))
    d2.text((90, 222), "Intelligence & control.", font=f_title, fill=(255, 255, 255, 255))
    tiles2 = [
        ("Briefings & Dossiers", "Printable prep & company intelligence", "INTERVIEW", (52, 211, 153)),
        ("Briefing Insights", "Sector velocity, pay quartiles & skill trends", "MARKET", (96, 165, 250)),
        ("Statistics & Goals", "Volume, interview rate, offer rate & streaks", "ANALYTICS", (147, 197, 253)),
        ("Themes, Accents & Scenery", "Custom desk backgrounds & color accents", "SCENERY", (96, 165, 250)),
        ("Custom Navigation", "Reorder your side menu your way", "PERSONAL", (147, 197, 253)),
        ("Privacy & Security", "Passwordless sign-in, passkeys, 2FA & backup codes", "PROTECTED", (52, 211, 153)),
    ]
    for idx, (title, sub, tag, col) in enumerate(tiles2):
        ty = 325 + idx * 205
        d2.rounded_rectangle((90, ty, 990, ty + 178), radius=28, fill=(14, 24, 40, 240), outline=(*col, 135), width=2)
        d2.text((130, ty + 32), title, font=f_card_title, fill=(255, 255, 255, 255))
        d2.text((130, ty + 96), sub, font=f_body, fill=(180, 198, 224, 255))
        tb = d2.textbbox((0, 0), tag, font=f_badge)
        pw = (tb[2] - tb[0]) + 40
        draw_pill(d2, 952 - pw, ty + 28, tag, f_badge, (*col, 45), (*col, 255), outline_col=(*col, 255), pad_x=20, h=44)

    build_swish_slides([s1, s2], duration, out_mp4)


def render_criteria(out_mp4: str, duration: float) -> None:
    """Focused commercial UI card for Criteria & Recommendations with auto-sized pills (never clipped)."""
    base_bg = make_bg()
    f_eyebrow = load_font(30, bold=True)
    f_title = load_font(56, bold=True)
    f_card_title = load_font(36, bold=True)
    f_body = load_font(30, bold=False)
    f_badge = load_font(26, bold=True)

    total_frames = int(round(duration * FPS))
    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(total_frames):
            t = i / FPS
            frame = base_bg.copy()
            layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)

            p_h = ease_out_cubic(t / 0.45)
            hy = int(230 + (1 - p_h) * 30)
            ha = int(255 * p_h)
            d.text((90, hy), "CRITERIA & INBOX", font=f_eyebrow, fill=(96, 165, 250, ha))
            d.text((90, hy + 48), "Roles you actually steer.", font=f_title, fill=(255, 255, 255, ha))

            if t >= 0.25:
                p1 = ease_out_cubic((t - 0.25) / 0.50)
                a1 = int(255 * p1)
                y1 = int(420 + (1 - p1) * 35)
                d.rounded_rectangle((90, y1, 990, y1 + 260), radius=32, fill=(14, 24, 40, int(235 * p1)), outline=(96, 165, 250, int(120 * p1)), width=2)
                d.text((130, y1 + 32), "Your Exact Criteria", font=f_card_title, fill=(255, 255, 255, a1))
                x_end = draw_pill(d, 130, y1 + 102, "Senior Product", f_badge, (37, 99, 235, a1), (255, 255, 255, a1), pad_x=28, h=54)
                draw_pill(d, x_end + 18, y1 + 102, "Remote · US/EU", f_badge, (24, 38, 62, a1), (147, 197, 253, a1), outline_col=(96, 165, 250, a1), pad_x=28, h=54)
                d.text((130, y1 + 190), "Auto-refresh on your schedule or on demand", font=f_body, fill=(180, 198, 224, a1))

            if t >= 0.85:
                p2 = ease_out_cubic((t - 0.85) / 0.50)
                a2 = int(255 * p2)
                y2 = int(720 + (1 - p2) * 35)
                d.rounded_rectangle((90, y2, 990, y2 + 230), radius=32, fill=(14, 24, 40, int(235 * p2)), outline=(52, 211, 153, int(130 * p2)), width=2)
                d.text((130, y2 + 32), "Pinned Resume & Portfolio", font=f_card_title, fill=(255, 255, 255, a2))
                draw_pill(d, 130, y2 + 98, "PINNED: Resume_2026.pdf", f_badge, (16, 185, 129, int(45 * p2)), (52, 211, 153, a2), outline_col=(52, 211, 153, a2), pad_x=28, h=52)
                d.text((130, y2 + 172), "Matching uses your real background", font=f_body, fill=(216, 228, 242, a2))

            if t >= 1.50:
                p3 = ease_out_cubic((t - 1.50) / 0.50)
                a3 = int(255 * p3)
                y3 = int(990 + (1 - p3) * 35)
                d.rounded_rectangle((90, y3, 990, y3 + 230), radius=32, fill=(14, 24, 40, int(235 * p3)), outline=(96, 165, 250, int(120 * p3)), width=2)
                d.text((130, y3 + 32), "Honest Exclusions", font=f_card_title, fill=(255, 255, 255, a3))
                d.text((130, y3 + 90), "Companies in Applications stay out of your inbox.", font=f_body, fill=(180, 198, 224, a3))
                d.text((130, y3 + 140), "Unfollowed companies stay blocked for good.", font=f_body, fill=(96, 165, 250, a3))

            frame = Image.alpha_composite(frame, layer)
            frame.convert("RGB").save(os.path.join(tmpdir, f"frame_{i:04d}.png"))
        encode_frames(tmpdir, out_mp4)


def render_insights(out_mp4: str, duration: float) -> None:
    """3-slide right-to-left swish modeled directly on Appliedly's real Briefing Insights UI (Investment Banking)."""
    f_eyebrow = load_font(28, bold=True)
    f_title = load_font(54, bold=True)
    f_card_title = load_font(36, bold=True)
    f_body = load_font(28, bold=False)
    f_badge = load_font(22, bold=True)
    f_num = load_font(28, bold=True)

    # Slide 1: Compensation Quartiles (USD) + Negotiation Benchmark (matches real horizontal quartile bar)
    s1 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d1 = ImageDraw.Draw(s1)
    d1.text((90, 210), "INVESTMENT BANKING · VERIFIED MARKET DATA", font=f_eyebrow, fill=(96, 165, 250, 255))
    d1.text((90, 255), "Compensation Quartiles (USD)", font=f_title, fill=(255, 255, 255, 255))

    x_c = draw_pill(d1, 90, 345, "Main (USD)", f_badge, (59, 130, 246, 255), (255, 255, 255, 255), pad_x=22, h=42)
    x_c = draw_pill(d1, x_c + 12, 345, "USD", f_badge, (24, 38, 62, 255), (180, 198, 224, 255), outline_col=(96, 165, 250, 120), pad_x=22, h=42)
    draw_pill(d1, x_c + 12, 345, "LOC (USD)", f_badge, (24, 38, 62, 255), (180, 198, 224, 255), outline_col=(96, 165, 250, 120), pad_x=22, h=42)

    d1.rounded_rectangle((90, 425, 990, 1085), radius=32, fill=(14, 24, 40, 240), outline=(96, 165, 250, 140), width=2)
    d1.text((130, 465), "Annual base + bonus range", font=f_card_title, fill=(255, 255, 255, 255))
    d1.text((735, 472), "YoY Trend: +6%", font=f_badge, fill=(147, 197, 253, 255))
    d1.text((130, 515), "Verified across active sector openings", font=f_body, fill=(180, 198, 224, 255))

    # Median floating pill + pointer
    draw_pill(d1, 250, 585, "Median $285k", f_badge, (59, 130, 246, 255), (255, 255, 255, 255), pad_x=20, h=40)
    # Horizontal segmented gradient quartile bar
    bar_x, bar_y, bar_w, bar_h = 130, 645, 820, 32
    d1.rounded_rectangle((bar_x, bar_y, bar_x + bar_w, bar_y + bar_h), radius=16, fill=(24, 38, 62, 255))
    d1.rounded_rectangle((bar_x, bar_y, bar_x + int(bar_w * 0.85), bar_y + bar_h), radius=16, fill=(37, 99, 235, 255))
    d1.rounded_rectangle((bar_x + int(bar_w * 0.16), bar_y, bar_x + int(bar_w * 0.62), bar_y + bar_h), radius=0, fill=(96, 165, 250, 255))
    # Median white tick
    d1.rectangle((326, bar_y - 6, 333, bar_y + bar_h + 6), fill=(255, 255, 255, 255))

    d1.text((130, 698), "25th: $180k", font=f_badge, fill=(180, 198, 224, 255))
    d1.text((310, 698), "Median: $285k", font=f_badge, fill=(96, 165, 250, 255))
    d1.text((575, 698), "75th: $475k", font=f_badge, fill=(180, 198, 224, 255))
    d1.text((810, 698), "90th: $820k", font=f_badge, fill=(180, 198, 224, 255))

    # Negotiation Benchmark inner card
    d1.rounded_rectangle((130, 775, 950, 1035), radius=24, fill=(18, 30, 50, 240), outline=(96, 165, 250, 110), width=2)
    d1.text((165, 810), "Negotiation Benchmark", font=f_card_title, fill=(255, 255, 255, 255))
    d1.text((165, 868), "Sector market median sits at $285k USD/yr,", font=f_body, fill=(216, 228, 242, 255))
    d1.text((165, 912), "while top-quartile senior packages reach", font=f_body, fill=(216, 228, 242, 255))
    d1.text((165, 956), "$475k–$820k.", font=f_num, fill=(52, 211, 153, 255))

    # Slide 2: Hiring Velocity Telemetry (glowing line chart) + Market Summary & Sources
    s2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(s2)
    d2.text((90, 210), "HIRING VELOCITY TELEMETRY", font=f_eyebrow, fill=(96, 165, 250, 255))
    d2.text((90, 255), "30d Trend & Market Pulse", font=f_title, fill=(255, 255, 255, 255))

    d2.rounded_rectangle((90, 355, 990, 815), radius=32, fill=(14, 24, 40, 240), outline=(96, 165, 250, 140), width=2)
    d2.text((130, 392), "30d requisition trend: +5%", font=f_card_title, fill=(255, 255, 255, 255))
    draw_pill(d2, 665, 388, "Score: 74/100 · Selective", f_badge, (37, 99, 235, 70), (147, 197, 253, 255), outline_col=(96, 165, 250, 200), pad_x=18, h=40)
    d2.text((130, 444), "Median time-to-fill: 41 days", font=f_body, fill=(180, 198, 224, 255))

    # Glowing area-line chart matching the real UI
    pts = [(150, 695), (275, 675), (400, 660), (525, 645), (650, 628), (775, 590), (915, 568)]
    poly_pts = pts + [(915, 725), (150, 725)]
    area = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(area).polygon(poly_pts, fill=(59, 130, 246, 55))
    s2 = Image.alpha_composite(s2, area)
    d2 = ImageDraw.Draw(s2)
    d2.line(pts, fill=(96, 165, 250, 255), width=6)
    for idx, (px, py) in enumerate(pts):
        r = 10 if idx == len(pts) - 1 else 7
        d2.ellipse((px - r, py - r, px + r, py + r), fill=(14, 24, 40, 255), outline=(96, 165, 250, 255), width=4)
    d2.text((135, 745), "7 weeks ago", font=f_badge, fill=(148, 163, 184, 255))
    d2.text((465, 745), "4 weeks ago", font=f_badge, fill=(148, 163, 184, 255))
    d2.text((805, 745), "Current Pulse", font=f_badge, fill=(96, 165, 250, 255))

    # Market Summary & Verified Sources card below
    d2.rounded_rectangle((90, 855, 990, 1235), radius=32, fill=(14, 24, 40, 240), outline=(52, 211, 153, 130), width=2)
    d2.text((130, 895), "Market Summary & Verified Sources", font=f_card_title, fill=(255, 255, 255, 255))
    d2.text((130, 955), "New York, San Francisco & Chicago hiring analysts.", font=f_body, fill=(216, 228, 242, 255))
    d2.text((130, 1005), "• SIFMA capital markets survey", font=f_body, fill=(147, 197, 253, 255))
    d2.text((130, 1052), "• BLS wage data, securities brokers", font=f_body, fill=(147, 197, 253, 255))
    d2.text((130, 1099), "• Robert Half finance salary guide", font=f_body, fill=(147, 197, 253, 255))

    # Slide 3: Skill Momentum Matrix (exact Accelerating / Baseline / Cooling cards)
    s3 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d3 = ImageDraw.Draw(s3)
    d3.text((90, 210), "SKILL MOMENTUM MATRIX", font=f_eyebrow, fill=(96, 165, 250, 255))
    d3.text((90, 255), "What's accelerating now.", font=f_title, fill=(255, 255, 255, 255))

    cards = [
        ("ACCELERATING", "LBO models", "Posting Share: 58%", "+16%", (96, 165, 250), (37, 99, 235, 55), (96, 165, 250)),
        ("ACCELERATING", "Sponsor coverage", "Posting Share: 34%", "+11%", (96, 165, 250), (37, 99, 235, 55), (96, 165, 250)),
        ("BASELINE", "Merger models", "Posting Share: 74%", "+3%", (148, 163, 184), (30, 41, 59, 180), (148, 163, 184)),
        ("BASELINE", "Trading comps", "Posting Share: 69%", "+1%", (148, 163, 184), (30, 41, 59, 180), (148, 163, 184)),
        ("COOLING", "Pitch-book slides", "Posting Share: 22%", "-9%", (248, 113, 113), (127, 29, 29, 70), (248, 113, 113)),
    ]
    for idx, (badge, skill, share, delta, border_col, badge_bg, delta_col) in enumerate(cards):
        col_i = idx % 2
        row_i = idx // 2
        cx = 90 + col_i * 462
        cy = 365 + row_i * 235
        cw = 438
        ch = 205
        d3.rounded_rectangle((cx, cy, cx + cw, cy + ch), radius=26, fill=(14, 24, 40, 240), outline=(*border_col, 150), width=2)
        draw_pill(d3, cx + 26, cy + 24, badge, f_badge, badge_bg, (*border_col, 255), pad_x=16, h=34)
        d3.text((cx + 26, cy + 78), skill, font=f_card_title, fill=(255, 255, 255, 255))
        d3.text((cx + 26, cy + 138), share, font=f_badge, fill=(180, 198, 224, 255))
        d3.text((cx + cw - 92, cy + 136), delta, font=f_num, fill=(*delta_col, 255))

    # Bottom takeaway card
    d3.rounded_rectangle((90, 1085, 990, 1245), radius=28, fill=(14, 24, 40, 240), outline=(52, 211, 153, 140), width=2)
    d3.text((130, 1122), "LBO models & sponsor coverage are accelerating.", font=f_body, fill=(255, 255, 255, 255))
    d3.text((130, 1172), "Exportable PDF briefings for every sector.", font=f_body, fill=(52, 211, 153, 255))

    build_swish_slides([s1, s2, s3], duration, out_mp4)


def render_statistics(out_mp4: str, duration: float) -> None:
    """3-slide right-to-left swish modeled directly on Appliedly's real Statistics UI."""
    f_eyebrow = load_font(28, bold=True)
    f_title = load_font(54, bold=True)
    f_card_title = load_font(34, bold=True)
    f_body = load_font(26, bold=False)
    f_badge = load_font(21, bold=True)
    f_kpi = load_font(54, bold=True)

    # Slide 1: Overview KPIs + Section Tabs
    s1 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d1 = ImageDraw.Draw(s1)
    d1.text((90, 195), "STATISTICS · OVERVIEW", font=f_eyebrow, fill=(96, 165, 250, 255))
    d1.text((90, 240), "Every metric in one view.", font=f_title, fill=(255, 255, 255, 255))

    xt = draw_pill(d1, 90, 325, "Overview", f_badge, (59, 130, 246, 255), (255, 255, 255, 255), pad_x=20, h=40)
    xt = draw_pill(d1, xt + 10, 325, "Applications", f_badge, (24, 38, 62, 255), (180, 198, 224, 255), outline_col=(96, 165, 250, 120), pad_x=20, h=40)
    xt = draw_pill(d1, xt + 10, 325, "Recs & market", f_badge, (24, 38, 62, 255), (180, 198, 224, 255), outline_col=(96, 165, 250, 120), pad_x=20, h=40)
    draw_pill(d1, xt + 10, 325, "Pipeline & wait", f_badge, (24, 38, 62, 255), (180, 198, 224, 255), outline_col=(96, 165, 250, 120), pad_x=18, h=40)

    kpis = [
        ("Applications filed", "24", "Logged in this range", (96, 165, 250)),
        ("Interview rate", "25%", "Share in interview", (52, 211, 153)),
        ("Offer rate", "12%", "Offered or accepted", (52, 211, 153)),
        ("Avg fit score", "84", "AI match average", (147, 197, 253)),
        ("Median wait", "6d", "Days since update", (96, 165, 250)),
        ("Apply rate", "68%", "Inbox → Applications", (147, 197, 253)),
    ]
    for idx, (label, val, sub, col) in enumerate(kpis):
        ci = idx % 2
        ri = idx // 2
        kx = 90 + ci * 462
        ky = 405 + ri * 280
        kw, kh = 438, 250
        d1.rounded_rectangle((kx, ky, kx + kw, ky + kh), radius=28, fill=(14, 24, 40, 240), outline=(*col, 130), width=2)
        d1.text((kx + 30, ky + 28), label, font=f_body, fill=(180, 198, 224, 255))
        d1.text((kx + 30, ky + 88), val, font=f_kpi, fill=(*col, 255))
        d1.text((kx + 30, ky + 185), sub, font=f_badge, fill=(148, 163, 184, 255))

    # Slide 2: Pipeline Funnel + Applications by Week
    s2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(s2)
    d2.text((90, 195), "STATISTICS · PIPELINE & WAIT", font=f_eyebrow, fill=(52, 211, 153, 255))
    d2.text((90, 240), "Funnel & weekly pace.", font=f_title, fill=(255, 255, 255, 255))

    # Card 1: Pipeline funnel bar chart
    d2.rounded_rectangle((90, 345, 990, 815), radius=30, fill=(14, 24, 40, 240), outline=(96, 165, 250, 140), width=2)
    d2.text((130, 382), "Pipeline funnel", font=f_card_title, fill=(255, 255, 255, 255))
    d2.text((130, 430), "How volume thins from recommendations to offers", font=f_body, fill=(180, 198, 224, 255))

    stages = [("Recs", 0.72, (96, 165, 250)), ("Applied", 0.92, (59, 130, 246)), ("Screen", 0.48, (96, 165, 250)), ("Interview", 0.30, (52, 211, 153)), ("Offer", 0.22, (52, 211, 153))]
    base_y = 720
    for idx, (st, frac, col) in enumerate(stages):
        bx = 140 + idx * 165
        bh = int(205 * frac)
        d2.rounded_rectangle((bx, base_y - bh, bx + 115, base_y), radius=14, fill=(*col, 245))
        d2.text((bx + 18, base_y + 16), st, font=f_badge, fill=(180, 198, 224, 255))

    # Card 2: Applications by week line chart
    d2.rounded_rectangle((90, 855, 990, 1255), radius=30, fill=(14, 24, 40, 240), outline=(52, 211, 153, 130), width=2)
    d2.text((130, 892), "Applications by week", font=f_card_title, fill=(255, 255, 255, 255))
    d2.text((130, 940), "Consistent weekly momentum (UTC)", font=f_body, fill=(180, 198, 224, 255))
    wpts = [(150, 1145), (305, 1110), (460, 1085), (615, 1060), (770, 1030), (925, 1015)]
    d2.line(wpts, fill=(96, 165, 250, 255), width=6)
    for px, py in wpts:
        d2.ellipse((px - 8, py - 8, px + 8, py + 8), fill=(14, 24, 40, 255), outline=(96, 165, 250, 255), width=4)
    d2.text((140, 1185), "6w ago", font=f_badge, fill=(148, 163, 184, 255))
    d2.text((490, 1185), "3w ago", font=f_badge, fill=(148, 163, 184, 255))
    d2.text((835, 1185), "This week", font=f_badge, fill=(96, 165, 250, 255))

    # Slide 3: Recurring Note Terms + Recommendations & Market
    s3 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d3 = ImageDraw.Draw(s3)
    d3.text((90, 195), "STATISTICS · NOTE PATTERNS", font=f_eyebrow, fill=(96, 165, 250, 255))
    d3.text((90, 240), "Spot what drives offers.", font=f_title, fill=(255, 255, 255, 255))

    d3.rounded_rectangle((90, 345, 990, 995), radius=30, fill=(14, 24, 40, 240), outline=(52, 211, 153, 140), width=2)
    d3.text((130, 385), "Recurring note terms", font=f_card_title, fill=(255, 255, 255, 255))
    d3.text((130, 435), "Words surfacing in app notes, rejections & statuses", font=f_body, fill=(180, 198, 224, 255))

    xl = draw_pill(d3, 130, 500, "Mostly in app notes", f_badge, (16, 185, 129, 55), (52, 211, 153, 255), outline_col=(52, 211, 153, 200), pad_x=18, h=38)
    xl = draw_pill(d3, xl + 12, 500, "Rejection notes", f_badge, (239, 68, 68, 45), (252, 165, 165, 255), outline_col=(248, 113, 113, 180), pad_x=18, h=38)
    draw_pill(d3, xl + 12, 500, "Statuses", f_badge, (37, 99, 235, 55), (147, 197, 253, 255), outline_col=(96, 165, 250, 180), pad_x=18, h=38)

    # Word cloud pills matching real UI
    f_wc_lg = load_font(42, bold=True)
    f_wc_md = load_font(32, bold=True)
    draw_pill(d3, 165, 610, "recruiter", f_wc_lg, (16, 185, 129, 175), (255, 255, 255, 255), pad_x=34, h=76)
    draw_pill(d3, 495, 625, "system design", f_wc_md, (37, 99, 235, 175), (255, 255, 255, 255), pad_x=28, h=64)
    draw_pill(d3, 230, 725, "callback", f_wc_md, (16, 185, 129, 155), (255, 255, 255, 255), pad_x=28, h=64)
    draw_pill(d3, 520, 735, "compensation", f_wc_md, (239, 68, 68, 125), (255, 255, 255, 255), pad_x=26, h=60)
    draw_pill(d3, 310, 830, "take-home", f_wc_md, (37, 99, 235, 155), (255, 255, 255, 255), pad_x=28, h=60)

    d3.rounded_rectangle((90, 1035, 990, 1235), radius=28, fill=(14, 24, 40, 240), outline=(96, 165, 250, 140), width=2)
    d3.text((130, 1075), "Enlarge charts · Compare across time ranges", font=f_card_title, fill=(255, 255, 255, 255))
    d3.text((130, 1135), "Turn your raw hunt activity into clear, actionable data.", font=f_body, fill=(147, 197, 253, 255))

    build_swish_slides([s1, s2, s3], duration, out_mp4)


def render_applications(out_mp4: str, duration: float) -> None:
    """2-slide right-to-left swish for 03_applications_rounds_cover_letter: Rounds & .ics -> Tailored Cover Letter PDF."""
    f_eyebrow = load_font(28, bold=True)
    f_title = load_font(54, bold=True)
    f_card_title = load_font(36, bold=True)
    f_body = load_font(29, bold=False)
    f_badge = load_font(23, bold=True)

    # Slide 1: Interview Rounds & .ics Calendar Invites
    s1 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d1 = ImageDraw.Draw(s1)
    d1.text((90, 220), "APPLICATIONS & ROUNDS", font=f_eyebrow, fill=(96, 165, 250, 255))
    d1.text((90, 268), "One living pipeline.", font=f_title, fill=(255, 255, 255, 255))
    d1.rounded_rectangle((90, 385, 990, 1080), radius=32, fill=(14, 24, 40, 240), outline=(96, 165, 250, 150), width=2)
    draw_pill(d1, 130, 425, "IN INTERVIEW · ROUND 2 OF 3", f_badge, (16, 185, 129, 50), (52, 211, 153, 255), outline_col=(52, 211, 153, 255), pad_x=22, h=44)
    d1.text((130, 500), "Senior Product Designer · Linear", font=f_card_title, fill=(255, 255, 255, 255))

    rounds = [
        ("Round 1 · Recruiter Screen", "Completed · Notes saved", (52, 211, 153)),
        ("Round 2 · Portfolio Walkthrough", "Thu 2:00 PM · Prep notes ready", (96, 165, 250)),
        ("Round 3 · Final Panel", "Upcoming · Follow-up alert set", (147, 197, 253)),
    ]
    for idx, (rtitle, rsub, col) in enumerate(rounds):
        ry = 585 + idx * 125
        d1.rounded_rectangle((130, ry, 950, ry + 102), radius=20, fill=(18, 30, 50, 240), outline=(*col, 110), width=2)
        d1.text((160, ry + 18), rtitle, font=f_badge, fill=(255, 255, 255, 255))
        d1.text((160, ry + 54), rsub, font=f_body, fill=(*col, 255))

    draw_pill(d1, 130, 985, "EXPORT .ICS CALENDAR INVITE", f_badge, (37, 99, 235, 255), (255, 255, 255, 255), pad_x=26, h=50)

    # Slide 2: Tailored Cover Letter PDF
    s2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(s2)
    d2.text((90, 220), "TAILORED COVER LETTERS", font=f_eyebrow, fill=(52, 211, 153, 255))
    d2.text((90, 268), "Generated from the role.", font=f_title, fill=(255, 255, 255, 255))
    d2.rounded_rectangle((90, 385, 990, 1080), radius=32, fill=(14, 24, 40, 240), outline=(52, 211, 153, 150), width=2)
    x_p = draw_pill(d2, 130, 425, "FROM LOGGED APPLICATION", f_badge, (37, 99, 235, 60), (147, 197, 253, 255), outline_col=(96, 165, 250, 200), pad_x=20, h=44)
    draw_pill(d2, x_p + 14, 425, "+ DOCUMENTS SUMMARY", f_badge, (16, 185, 129, 50), (52, 211, 153, 255), outline_col=(52, 211, 153, 200), pad_x=20, h=44)
    d2.text((130, 505), "Cover_Letter_Linear.pdf", font=f_card_title, fill=(255, 255, 255, 255))
    d2.rounded_rectangle((130, 575, 950, 955), radius=22, fill=(18, 30, 50, 240), outline=(96, 165, 250, 90), width=2)
    d2.text((165, 610), "Tailored to the role description, your pinned", font=f_body, fill=(216, 228, 242, 255))
    d2.text((165, 655), "resume & portfolio highlights—ready in seconds.", font=f_body, fill=(216, 228, 242, 255))
    d2.text((165, 735), "• Highlights 6 yrs design systems impact", font=f_body, fill=(147, 197, 253, 255))
    d2.text((165, 785), "• Matches company product stage & craft", font=f_body, fill=(147, 197, 253, 255))
    d2.text((165, 835), "• Zero generic fluff", font=f_body, fill=(52, 211, 153, 255))
    draw_pill(d2, 130, 985, "DOWNLOAD POLISHED PDF", f_badge, (37, 99, 235, 255), (255, 255, 255, 255), pad_x=26, h=50)

    build_swish_slides([s1, s2], duration, out_mp4)


def render_documents(out_mp4: str, duration: float) -> None:
    """2-slide right-to-left swish for 10_documents: File Library (Save/View/Attach) -> Powers Recs, Briefings & Insights."""
    f_eyebrow = load_font(28, bold=True)
    f_title = load_font(54, bold=True)
    f_card_title = load_font(35, bold=True)
    f_body = load_font(28, bold=False)
    f_badge = load_font(22, bold=True)

    # Slide 1: Every File on One Desk
    s1 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d1 = ImageDraw.Draw(s1)
    d1.text((90, 200), "DOCUMENTS LIBRARY", font=f_eyebrow, fill=(96, 165, 250, 255))
    d1.text((90, 248), "Save, view & attach cleanly.", font=f_title, fill=(255, 255, 255, 255))

    docs = [
        ("Resumes", "Resume_2026_Product.pdf · Preview & pin", "PINNED", (52, 211, 153)),
        ("Portfolios", "Case_Studies_Deck.pdf · Ready for rounds", "PORTFOLIO", (96, 165, 250)),
        ("Cover Letters", "Polished PDFs tailored per application", "COVER LETTER", (147, 197, 253)),
        ("Extras & Certs", "References, transcripts & work samples", "EXTRAS", (52, 211, 153)),
    ]
    for idx, (title, sub, tag, col) in enumerate(docs):
        ty = 365 + idx * 205
        d1.rounded_rectangle((90, ty, 990, ty + 176), radius=28, fill=(14, 24, 40, 240), outline=(*col, 140), width=2)
        d1.text((130, ty + 30), title, font=f_card_title, fill=(255, 255, 255, 255))
        d1.text((130, ty + 92), sub, font=f_body, fill=(180, 198, 224, 255))
        tb = d1.textbbox((0, 0), tag, font=f_badge)
        pw = (tb[2] - tb[0]) + 38
        draw_pill(d1, 952 - pw, ty + 28, tag, f_badge, (*col, 45), (*col, 255), outline_col=(*col, 255), pad_x=19, h=42)

    # Slide 2: How Pinned Documents Power Everything
    s2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(s2)
    d2.text((90, 200), "ONE LIBRARY · FULL POWER", font=f_eyebrow, fill=(52, 211, 153, 255))
    d2.text((90, 248), "Your docs drive the hunt.", font=f_title, fill=(255, 255, 255, 255))

    powered = [
        ("Criteria Recommendations", "Matches roles to your pinned resume & skills", "INBOX", (96, 165, 250)),
        ("Job Briefings & Dossiers", "Scores role fit & interview prep against your profile", "BRIEFINGS", (52, 211, 153)),
        ("Briefing Insights", "Max Profile Fit compares your background to sector trends", "INSIGHTS", (147, 197, 253)),
        ("Tailored Cover Letters", "Generates polished PDFs straight from your saved summary", "APPLY FAST", (52, 211, 153)),
    ]
    for idx, (title, sub, tag, col) in enumerate(powered):
        ty = 365 + idx * 205
        d2.rounded_rectangle((90, ty, 990, ty + 176), radius=28, fill=(14, 24, 40, 240), outline=(*col, 140), width=2)
        d2.text((130, ty + 30), title, font=f_card_title, fill=(255, 255, 255, 255))
        d2.text((130, ty + 92), sub, font=f_body, fill=(180, 198, 224, 255))
        tb = d2.textbbox((0, 0), tag, font=f_badge)
        pw = (tb[2] - tb[0]) + 38
        draw_pill(d2, 952 - pw, ty + 28, tag, f_badge, (*col, 45), (*col, 255), outline_col=(*col, 255), pad_x=19, h=42)

    build_swish_slides([s1, s2], duration, out_mp4)


def render_cover_letter(out_mp4: str, duration: float) -> None:
    """2-slide right-to-left swish for 11_cover_letters: Logged Role + Docs -> Polished Tailored PDF."""
    f_eyebrow = load_font(28, bold=True)
    f_title = load_font(54, bold=True)
    f_card_title = load_font(35, bold=True)
    f_body = load_font(28, bold=False)
    f_badge = load_font(22, bold=True)

    # Slide 1: Clean Application Sample Card (pure app data inside card, feature context in header)
    s1 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d1 = ImageDraw.Draw(s1)
    d1.text((90, 200), "COVER LETTERS · 1-CLICK FROM YOUR APPLICATION", font=f_eyebrow, fill=(96, 165, 250, 255))
    d1.text((90, 248), "Skip the blank page.", font=f_title, fill=(255, 255, 255, 255))

    d1.rounded_rectangle((90, 365, 990, 1080), radius=32, fill=(14, 24, 40, 240), outline=(96, 165, 250, 150), width=2)
    draw_pill(d1, 130, 410, "LOGGED APPLICATION", f_badge, (37, 99, 235, 60), (147, 197, 253, 255), outline_col=(96, 165, 250, 200), pad_x=20, h=42)
    d1.text((130, 485), "Staff Product Engineer · Figma", font=f_card_title, fill=(255, 255, 255, 255))
    d1.text((130, 540), "San Francisco / Remote · Status: Saved", font=f_body, fill=(180, 198, 224, 255))

    d1.rounded_rectangle((130, 615, 950, 765), radius=22, fill=(18, 30, 50, 240), outline=(96, 165, 250, 110), width=2)
    d1.text((160, 643), "Role Context", font=f_card_title, fill=(147, 197, 253, 255))
    d1.text((160, 696), "Design systems tooling, multiplayer canvas & React", font=f_body, fill=(216, 228, 242, 255))

    d1.rounded_rectangle((130, 800, 950, 945), radius=22, fill=(18, 30, 50, 240), outline=(52, 211, 153, 130), width=2)
    d1.text((160, 828), "Pinned Documents", font=f_card_title, fill=(52, 211, 153, 255))
    d1.text((160, 882), "Resume_2026.pdf · Case_Studies_Deck.pdf", font=f_body, fill=(216, 228, 242, 255))

    draw_pill(d1, 130, 985, "GENERATE COVER LETTER PDF", f_badge, (37, 99, 235, 255), (255, 255, 255, 255), pad_x=26, h=52)

    # Slide 2: Clear Sample Cover Letter PDF Output
    s2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(s2)
    d2.text((90, 200), "SAMPLE PDF OUTPUT", font=f_eyebrow, fill=(52, 211, 153, 255))
    d2.text((90, 248), "Tailored in seconds.", font=f_title, fill=(255, 255, 255, 255))

    d2.rounded_rectangle((90, 365, 990, 1080), radius=32, fill=(14, 24, 40, 240), outline=(52, 211, 153, 150), width=2)
    x_p = draw_pill(d2, 130, 410, "COVER_LETTER_FIGMA.PDF", f_badge, (16, 185, 129, 50), (52, 211, 153, 255), outline_col=(52, 211, 153, 255), pad_x=20, h=42)
    draw_pill(d2, x_p + 14, 410, "READY TO ATTACH", f_badge, (37, 99, 235, 55), (147, 197, 253, 255), outline_col=(96, 165, 250, 200), pad_x=20, h=42)

    # Crisp white-paper PDF preview inside the dark frame
    d2.rounded_rectangle((130, 480, 950, 955), radius=20, fill=(241, 245, 249, 255))
    f_doc_h = load_font(28, bold=True)
    f_doc_b = load_font(25, bold=False)
    d2.text((170, 515), "Dear Figma Hiring Team,", font=f_doc_h, fill=(15, 23, 42, 255))
    d2.text((170, 568), "I'm excited to apply for Staff Product Engineer.", font=f_doc_b, fill=(30, 41, 59, 255))
    d2.text((170, 606), "Over the past 6 years leading design-system", font=f_doc_b, fill=(30, 41, 59, 255))
    d2.text((170, 644), "tooling and real-time canvas performance, I've", font=f_doc_b, fill=(30, 41, 59, 255))
    d2.text((170, 682), "shipped systems used by 40k+ engineers daily.", font=f_doc_b, fill=(30, 41, 59, 255))
    d2.text((170, 742), "My attached portfolio highlights how we cut", font=f_doc_b, fill=(30, 41, 59, 255))
    d2.text((170, 780), "render latency by 42%—directly aligned with", font=f_doc_b, fill=(30, 41, 59, 255))
    d2.text((170, 818), "your multiplayer editor roadmap.", font=f_doc_b, fill=(30, 41, 59, 255))
    d2.text((170, 882), "Best regards, Alex Chen", font=f_doc_h, fill=(37, 99, 235, 255))

    draw_pill(d2, 130, 985, "DOWNLOAD PDF", f_badge, (37, 99, 235, 255), (255, 255, 255, 255), pad_x=28, h=52)

    build_swish_slides([s1, s2], duration, out_mp4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", choices=["pro_max", "insights", "desk", "criteria", "dossier", "statistics", "applications", "documents", "cover_letter"])
    parser.add_argument("out_mp4")
    parser.add_argument("--duration", type=float, default=5.0)
    args = parser.parse_args()

    if args.kind == "pro_max":
        render_pro_max(args.out_mp4, args.duration)
    elif args.kind == "insights":
        render_insights(args.out_mp4, args.duration)
    elif args.kind == "desk":
        render_desk(args.out_mp4, args.duration)
    elif args.kind == "criteria":
        render_criteria(args.out_mp4, args.duration)
    elif args.kind == "dossier":
        render_dossier(args.out_mp4, args.duration)
    elif args.kind == "statistics":
        render_statistics(args.out_mp4, args.duration)
    elif args.kind == "applications":
        render_applications(args.out_mp4, args.duration)
    elif args.kind == "documents":
        render_documents(args.out_mp4, args.duration)
    elif args.kind == "cover_letter":
        render_cover_letter(args.out_mp4, args.duration)
    print(f"Rendered {args.kind} feature card ({args.duration}s) -> {args.out_mp4}")
