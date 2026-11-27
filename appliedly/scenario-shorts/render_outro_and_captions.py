#!/usr/bin/env python3
"""Render parameterized TV-commercial animated Appliedly wordmark outro (with themed kicker, logo-only shimmer, cursor click) and TikTok caption overlays."""
import argparse
import math
import os
import subprocess
import tempfile
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
FPS = 30

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
APPLIEDLY_DIR = os.path.dirname(SCRIPT_DIR)
LOGOS_DIR = os.path.join(APPLIEDLY_DIR, "press-kit", "logos")
WORDMARK_PATH = os.path.join(LOGOS_DIR, "wordmark-transparent-1440.png")


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


def make_gradient_bg(glow_alpha: float = 0.30) -> Image.Image:
    bg = Image.new("RGBA", (W, H), (10, 18, 32, 255))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    cx, cy = W // 2, int(H * 0.43)
    for r in range(600, 40, -30):
        frac = 1.0 - (r / 600.0)
        a = int(255 * glow_alpha * (frac ** 1.8) * 0.20)
        gd.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(96, 165, 250, a))
    glow = glow.filter(ImageFilter.GaussianBlur(40))
    return Image.alpha_composite(bg, glow)


def draw_cursor(draw: ImageDraw.ImageDraw, x: int, y: int, scale: float = 1.0, alpha: int = 255) -> None:
    pts = [(0, 0), (0, 56), (14, 43), (24, 64), (33, 60), (23, 39), (41, 39)]
    scaled = [(int(x + px * scale), int(y + py * scale)) for px, py in pts]
    draw.polygon(scaled, fill=(255, 255, 255, alpha), outline=(10, 18, 32, alpha), width=3)


def render_outro(out_mp4: str, kicker: str = "", duration: float = 6.5) -> None:
    raw_wm = Image.open(WORDMARK_PATH).convert("RGBA")
    bbox = raw_wm.getbbox()
    if bbox:
        raw_wm = raw_wm.crop(bbox)

    wm_w = 820
    wm_h = int(raw_wm.height * (wm_w / raw_wm.width))
    wordmark_base = raw_wm.resize((wm_w, wm_h), Image.Resampling.LANCZOS)

    font_kicker = load_font(30, bold=True)
    font_slogan = load_font(44, bold=False)
    font_url = load_font(52, bold=True)

    total_frames = int(duration * FPS)
    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(total_frames):
            t = i / FPS
            pulse = 0.25 + 0.08 * math.sin(t * 2.2)
            frame = make_gradient_bg(glow_alpha=pulse)

            # 0. Optional themed kicker pill above wordmark (0.2s -> 0.8s)
            if kicker and t >= 0.15:
                p_k = ease_out_cubic((t - 0.15) / 0.55)
                kl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                kd = ImageDraw.Draw(kl)
                kb = kd.textbbox((0, 0), kicker, font=font_kicker)
                kw, kh = kb[2] - kb[0], kb[3] - kb[1]
                pw, ph = kw + 56, kh + 28
                px, py = (W - pw) // 2, int(H * 0.23 + (1.0 - p_k) * 16)
                ka = int(235 * p_k)
                kd.rounded_rectangle(
                    (px, py, px + pw, py + ph),
                    radius=ph // 2,
                    fill=(37, 99, 235, int(45 * p_k)),
                    outline=(96, 165, 250, int(180 * p_k)),
                    width=2,
                )
                kd.text((px + 28, py + 12), kicker, font=font_kicker, fill=(147, 197, 253, ka))
                frame = Image.alpha_composite(frame, kl)

            # 1. Wordmark scales & fades in cleanly (0.0s -> 0.8s)
            p_wm = ease_out_cubic(t / 0.8)
            cur_scale = 0.90 + 0.10 * p_wm
            cw = max(10, int(wm_w * cur_scale))
            ch = max(10, int(wm_h * cur_scale))
            wm_layer = wordmark_base.resize((cw, ch), Image.Resampling.LANCZOS)

            # Logo-only shimmer strictly masked by wordmark alpha
            if 0.85 <= t <= 2.05:
                sweep_p = (t - 0.85) / 1.2
                sweep_x = int(-160 + sweep_p * (cw + 320))
                sweep = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
                sd = ImageDraw.Draw(sweep)
                sd.polygon(
                    [(sweep_x, 0), (sweep_x + 110, 0), (sweep_x + 40, ch), (sweep_x - 70, ch)],
                    fill=(255, 255, 255, 165),
                )
                sweep = sweep.filter(ImageFilter.GaussianBlur(10))
                logo_alpha = wm_layer.getchannel("A")
                sweep_alpha = sweep.getchannel("A")
                sweep.putalpha(ImageChops.multiply(sweep_alpha, logo_alpha))
                wm_layer = Image.alpha_composite(wm_layer, sweep)

            r, g, b, a = wm_layer.split()
            a = a.point(lambda px: int(px * p_wm))
            wm_layer = Image.merge("RGBA", (r, g, b, a))
            wm_x = (W - cw) // 2
            wm_y = int(H * 0.37 - ch // 2 + (1.0 - p_wm) * 28)
            frame.alpha_composite(wm_layer, (wm_x, wm_y))

            # 2. Official Slogan fades up
            if t >= 0.65:
                p_sl = ease_out_cubic((t - 0.65) / 0.7)
                txt_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                td = ImageDraw.Draw(txt_layer)
                slogan = "Track every application. Land the right role."
                sb = td.textbbox((0, 0), slogan, font=font_slogan)
                tw = sb[2] - sb[0]
                sl_y = int(H * 0.49 + (1.0 - p_sl) * 22)
                td.text(((W - tw) // 2, sl_y), slogan, font=font_slogan, fill=(216, 228, 242, int(235 * p_sl)))
                frame = Image.alpha_composite(frame, txt_layer)

            # 3. CTA Button (appliedly.app) + Click Animation
            btn_cx, btn_cy = W // 2, int(H * 0.61)
            if t >= 1.15:
                p_cta = ease_out_back((t - 1.15) / 0.6)
                btn_scale = min(1.0, 0.72 + 0.28 * p_cta)
                if 2.85 <= t <= 3.10:
                    click_p = math.sin(((t - 2.85) / 0.25) * math.pi)
                    btn_scale *= (1.0 - 0.065 * click_p)

                pw = int(500 * btn_scale)
                ph = int(112 * btn_scale)
                px = btn_cx - pw // 2
                py = btn_cy - ph // 2
                alpha_cta = int(255 * min(1.0, (t - 1.15) / 0.35))

                cta_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                cd = ImageDraw.Draw(cta_layer)

                if 2.92 <= t <= 3.65:
                    rp = (t - 2.92) / 0.73
                    expand = int(70 * ease_out_cubic(rp))
                    ra = int(200 * (1.0 - rp))
                    cd.rounded_rectangle(
                        (px - expand, py - expand // 2, px + pw + expand, py + ph + expand // 2),
                        radius=(ph + expand) // 2,
                        outline=(96, 165, 250, ra),
                        width=4,
                    )

                fill_col = (59, 130, 246, alpha_cta) if t >= 2.90 else (37, 99, 235, alpha_cta)
                cd.rounded_rectangle(
                    (px, py, px + pw, py + ph),
                    radius=ph // 2,
                    fill=fill_col,
                    outline=(147, 197, 253, alpha_cta),
                    width=3,
                )
                url_text = "appliedly.app"
                ub = cd.textbbox((0, 0), url_text, font=font_url)
                uw, uh = ub[2] - ub[0], ub[3] - ub[1]
                cd.text(
                    (btn_cx - uw // 2, btn_cy - uh // 2 - 6),
                    url_text,
                    font=font_url,
                    fill=(255, 255, 255, alpha_cta),
                )
                frame = Image.alpha_composite(frame, cta_layer)

            # 4. Animated Mouse Cursor gliding to button & clicking
            if 1.95 <= t <= 4.35:
                cur_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                crd = ImageDraw.Draw(cur_layer)
                start_x, start_y = int(W * 0.78), int(H * 0.78)
                target_x, target_y = btn_cx + 95, btn_cy + 14

                move_p = ease_in_out_cubic((t - 1.95) / 0.85)
                cx = int(start_x + (target_x - start_x) * move_p)
                cy = int(start_y + (target_y - start_y) * move_p)

                c_scale = 1.0
                if 2.85 <= t <= 3.10:
                    c_scale = 1.0 - 0.14 * math.sin(((t - 2.85) / 0.25) * math.pi)

                c_alpha = 255
                if t < 2.15:
                    c_alpha = int(255 * ((t - 1.95) / 0.20))
                elif t > 3.95:
                    c_alpha = int(255 * (1.0 - (t - 3.95) / 0.40))

                draw_cursor(crd, cx, cy, scale=c_scale, alpha=max(0, min(255, c_alpha)))
                frame = Image.alpha_composite(frame, cur_layer)

            frame.convert("RGB").save(os.path.join(tmpdir, f"frame_{i:04d}.png"))

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


def render_caption_png(text: str, out_png: str, accent_last_line: bool = False, style: str = "clean") -> None:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = load_font(52, bold=True)
    sub_font = load_font(32, bold=True)

    lines = text.replace("\\n", "\n").split("\n")
    line_heights, line_widths = [], []
    for idx, line in enumerate(lines):
        f = sub_font if (style == "cta" and idx == 0) else font
        bb = draw.textbbox((0, 0), line, font=f)
        line_widths.append(bb[2] - bb[0])
        line_heights.append(bb[3] - bb[1])

    pad_x, pad_y = 42, 24
    gap = 14
    box_w = max(line_widths) + pad_x * 2
    box_h = sum(line_heights) + gap * (len(lines) - 1) + pad_y * 2
    bx = (W - box_w) // 2
    by = int(H * 0.72)

    if style == "cta":
        draw.rounded_rectangle(
            (bx, by, bx + box_w, by + box_h),
            radius=28,
            fill=(15, 29, 54, 232),
            outline=(96, 165, 250, 220),
            width=3,
        )
    else:
        draw.rounded_rectangle(
            (bx, by, bx + box_w, by + box_h),
            radius=24,
            fill=(10, 18, 32, 190),
            outline=(255, 255, 255, 45),
            width=2,
        )

    cur_y = by + pad_y - 4
    for idx, line in enumerate(lines):
        f = sub_font if (style == "cta" and idx == 0) else font
        lx = (W - line_widths[idx]) // 2
        if style == "cta" and idx == 0:
            col = (147, 197, 253, 255)
        elif accent_last_line and idx == len(lines) - 1:
            col = (96, 165, 250, 255)
        else:
            col = (255, 255, 255, 255)
        draw.text((lx, cur_y), line, font=f, fill=col)
        cur_y += line_heights[idx] + gap

    img.save(out_png)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("out_dir")
    parser.add_argument("--kicker", default="")
    parser.add_argument("--duration", type=float, default=6.5)
    parser.add_argument("--cap1", default="47 tabs open.\nZero callbacks.")
    parser.add_argument("--cap2", default="Stop tracking jobs\nin messy spreadsheets.")
    parser.add_argument("--cap3", default="One calm pipeline.\nZero noise.")
    parser.add_argument("--cap4", default="START TRACKING FREE\nappliedly.app")
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    render_outro(os.path.join(args.out_dir, "beat3_outro.mp4"), kicker=args.kicker, duration=args.duration)
    render_caption_png(args.cap1, os.path.join(args.out_dir, "cap1.png"))
    render_caption_png(args.cap2, os.path.join(args.out_dir, "cap2.png"))
    render_caption_png(args.cap3, os.path.join(args.out_dir, "cap3.png"), accent_last_line=True)
    render_caption_png(args.cap4, os.path.join(args.out_dir, "cap4.png"), style="cta")
    print(f"Rendered outro (kicker={args.kicker!r}) and captions in {args.out_dir}.")
