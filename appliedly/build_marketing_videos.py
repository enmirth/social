import os
import base64
import tempfile
import subprocess

BASE_DIR = r"A:\Project Data\projects\enmirth\organization\publishing\software\appliedly"
BRAND_LOGO_DIR = os.path.join(BASE_DIR, "brand", "logo")
MARKETING_DIR = os.path.join(BASE_DIR, "marketing")
VIDEOS_DIR = os.path.join(MARKETING_DIR, "videos")
EDGE_EXE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
SRC_VIDEO = r"C:\Users\Enmirth\Videos\Screen Recordings\Screen Recording 2026-11-17 154215.mp4"

os.makedirs(VIDEOS_DIR, exist_ok=True)

def load_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

logo_dark_b64 = load_b64(os.path.join(BRAND_LOGO_DIR, "png", "wordmark-on-dark-720.png"))

def render_bg(out_png, width, height, inner_html):
    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@500;700;800&family=Sora:wght@700;800&family=IBM+Plex+Mono:wght@600&display=swap');
* {{ box-sizing: border-box; }}
html, body {{
  margin: 0; padding: 0; width: {width}px; height: {height}px; overflow: hidden;
  background: radial-gradient(circle at 85% 12%, #173058 0%, #0A1220 55%, #070C16 100%);
  color: #E8EEF8; font-family: 'Manrope', 'Segoe UI', sans-serif;
}}
.accent {{ color: #60A5FA; }}
.green {{ color: #34D399; }}
.pill {{ display:inline-block; background:rgba(96,165,250,0.16); color:#60A5FA; border:1px solid rgba(96,165,250,0.45); padding:8px 20px; border-radius:999px; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; }}
.cta {{ display:inline-block; background:#2563EB; color:#FFFFFF; font-family:'Sora',sans-serif; font-weight:700; border-radius:14px; }}
</style></head><body>{inner_html}</body></html>"""
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tf:
        tf.write(html)
        tmp_html = tf.name
    try:
        subprocess.run([
            EDGE_EXE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            f"--window-size={width},{height}", f"--screenshot={out_png}",
            "file:///" + tmp_html.replace("\\", "/")
        ], check=True, capture_output=True)
    finally:
        if os.path.exists(tmp_html):
            os.remove(tmp_html)

def build_video(name, width, height, vid_w, vid_h, vid_x, vid_y, bg_html, start_sec=5, duration_sec=30):
    bg_png = os.path.join(VIDEOS_DIR, f"_bg_{name}.png")
    out_mp4 = os.path.join(VIDEOS_DIR, f"{name}.mp4")
    render_bg(bg_png, width, height, bg_html)

    # Composite screen recording onto branded background frame
    filter_complex = (
        f"[1:v]scale={vid_w}:{vid_h}:force_original_aspect_ratio=decrease,"
        f"pad={vid_w}:{vid_h}:(ow-iw)/2:(oh-ih)/2:color=#0E1828[vid];"
        f"[0:v][vid]overlay={vid_x}:{vid_y}:shortest=1[out]"
    )
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", bg_png,
        "-ss", str(start_sec), "-t", str(duration_sec), "-i", SRC_VIDEO,
        "-filter_complex", filter_complex,
        "-map", "[out]", "-map", "1:a?",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
        "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        "-t", str(duration_sec),
        out_mp4
    ]
    print(f"Encoding {out_mp4} ({width}x{height})...")
    subprocess.run(cmd, check=True, capture_output=True)
    if os.path.exists(bg_png):
        os.remove(bg_png)
    print(f"Created {out_mp4} ({os.path.getsize(out_mp4)//1024} KB)")

# 1. TikTok / Instagram Reels / YouTube Shorts (9:16 - 1080x1920)
build_video(
    "appliedly_tiktok_reels_shorts_9x16_1080x1920",
    1080, 1920,
    vid_w=1016, vid_h=736, vid_x=32, vid_y=590,
    bg_html=f"""
    <div style="padding:120px 56px 0 56px;text-align:center;">
      <img src="data:image/png;base64,{logo_dark_b64}" style="height:56px;" />
      <h1 style="font-family:'Sora',sans-serif;font-size:62px;line-height:1.12;margin:28px 0 14px 0;color:#FFF;">
        Track every application.<br><span class="accent">Land the right role.</span>
      </h1>
      <p style="font-size:28px;color:#9AADC4;margin:0;">Calm pipeline + Zero duplicate recommendations</p>
    </div>
    <div style="position:absolute;left:28px;top:586px;width:1024px;height:744px;border:4px solid #60A5FA;border-radius:16px;"></div>
    <div style="position:absolute;bottom:170px;left:0;right:0;text-align:center;">
      <div class="cta" style="font-size:34px;padding:22px 46px;">Try Free at appliedly.com</div>
      <div style="font-size:24px;color:#9AADC4;margin-top:22px;">Web • iOS • Android</div>
    </div>
    """
)

# 2. LinkedIn / YouTube / X / Product Hunt (16:9 - 1920x1080)
build_video(
    "appliedly_linkedin_youtube_x_16x9_1920x1080",
    1920, 1080,
    vid_w=1220, vid_h=884, vid_x=650, vid_y=98,
    bg_html=f"""
    <div style="position:absolute;left:64px;top:98px;width:540px;height:884px;display:flex;flex-direction:column;justify-content:space-between;">
      <div>
        <img src="data:image/png;base64,{logo_dark_b64}" style="height:48px;" />
        <div class="pill" style="font-size:17px;margin-top:34px;">Live Product Demo</div>
        <h1 style="font-family:'Sora',sans-serif;font-size:58px;line-height:1.12;margin:22px 0 18px 0;color:#FFF;">
          Track every application.<br><span class="accent">Land the right role.</span>
        </h1>
        <p style="font-size:24px;color:#9AADC4;line-height:1.5;">
          Replace chaotic spreadsheets with a calm visual pipeline, curated AI recommendations, and our Exclusion Contract.
        </p>
      </div>
      <div>
        <div style="font-size:22px;line-height:1.8;margin-bottom:26px;">
          <span class="green">✓</span> Visual stage &amp; duration tracking<br>
          <span class="green">✓</span> Zero duplicate company alerts<br>
          <span class="green">✓</span> Tailored cover letters &amp; briefs
        </div>
        <div class="cta" style="font-size:26px;padding:18px 34px;">appliedly.com</div>
      </div>
    </div>
    <div style="position:absolute;left:646px;top:94px;width:1228px;height:892px;border:4px solid #60A5FA;border-radius:14px;"></div>
    """
)

# 3. Facebook / Instagram Square Feed (1:1 - 1080x1080)
build_video(
    "appliedly_facebook_instagram_1x1_1080x1080",
    1080, 1080,
    vid_w=960, vid_h=696, vid_x=60, vid_y=216,
    bg_html=f"""
    <div style="padding:40px 60px 0 60px;display:flex;justify-content:space-between;align-items:center;">
      <img src="data:image/png;base64,{logo_dark_b64}" style="height:42px;" />
      <span class="pill" style="font-size:18px;">Calm Job Tracker</span>
    </div>
    <div style="text-align:center;margin-top:20px;">
      <div style="font-family:'Sora',sans-serif;font-size:38px;font-weight:800;color:#FFFFFF;">
        Track every application. <span class="accent">Land the right role.</span>
      </div>
    </div>
    <div style="position:absolute;left:56px;top:212px;width:968px;height:704px;border:4px solid #60A5FA;border-radius:12px;"></div>
    <div style="position:absolute;bottom:34px;left:60px;right:60px;display:flex;justify-content:space-between;align-items:center;">
      <span style="font-size:24px;color:#9AADC4;">Web • iOS • Android • Exclusion Contract</span>
      <span class="cta" style="font-size:24px;padding:12px 26px;">appliedly.com</span>
    </div>
    """
)

print("All 3 platform-formatted marketing videos generated successfully!")
