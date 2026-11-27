import os
import base64
import tempfile
import subprocess
import fitz  # PyMuPDF

BASE_DIR = r"A:\Project Data\projects\enmirth\organization\publishing\software\appliedly"
BRAND_LOGO_DIR = os.path.join(BASE_DIR, "brand", "logo")
MARKETING_DIR = os.path.join(BASE_DIR, "marketing")
STICKERS_DIR = os.path.join(MARKETING_DIR, "stickers")
SOCIAL_DIR = os.path.join(MARKETING_DIR, "social-graphics")
EDGE_EXE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

for sub in [
    STICKERS_DIR,
    os.path.join(SOCIAL_DIR, "linkedin"),
    os.path.join(SOCIAL_DIR, "facebook"),
    os.path.join(SOCIAL_DIR, "tiktok-reels-shorts"),
    os.path.join(SOCIAL_DIR, "twitter-x"),
    os.path.join(SOCIAL_DIR, "product-hunt"),
]:
    os.makedirs(sub, exist_ok=True)

def load_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

logo_dark_b64 = load_b64(os.path.join(BRAND_LOGO_DIR, "png", "wordmark-on-dark-720.png"))
logo_trans_b64 = load_b64(os.path.join(BRAND_LOGO_DIR, "png", "wordmark-transparent-720.png"))

# ----------------------------------------------------------------------
# 1. DIE-CUT TRANSPARENT STICKERS (SVG -> Transparent 1200x1200 PNG via PyMuPDF)
# ----------------------------------------------------------------------
stickers = {
    "sticker_01_open_aperture_badge": """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1200" viewBox="0 0 1200 1200">
  <defs>
    <linearGradient id="bg1" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0A1220"/>
      <stop offset="100%" stop-color="#172A46"/>
    </linearGradient>
  </defs>
  <!-- White die-cut outer border -->
  <circle cx="600" cy="600" r="540" fill="#FFFFFF"/>
  <circle cx="600" cy="600" r="500" fill="url(#bg1)"/>
  <circle cx="600" cy="600" r="458" fill="none" stroke="#60A5FA" stroke-width="10" stroke-dasharray="18 12"/>
  <text x="600" y="340" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="42" font-weight="700" fill="#60A5FA" letter-spacing="10">OPEN APERTURE</text>
  <text x="600" y="615" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="148" font-weight="800" fill="#FFFFFF" letter-spacing="-4">appliedly</text>
  <rect x="330" y="690" width="540" height="72" rx="36" fill="#2563EB"/>
  <text x="600" y="740" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="36" font-weight="700" fill="#FFFFFF" letter-spacing="3">LAND THE RIGHT ROLE</text>
  <text x="600" y="880" text-anchor="middle" font-family="Consolas, monospace" font-size="34" fill="#9AADC4">appliedly.com</text>
</svg>""",

    "sticker_02_calm_pipeline_pill": """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="600" viewBox="0 0 1200 600">
  <rect x="20" y="40" width="1160" height="520" rx="260" fill="#FFFFFF"/>
  <rect x="52" y="72" width="1096" height="456" rx="228" fill="#0A1220"/>
  <rect x="76" y="96" width="1048" height="408" rx="204" fill="none" stroke="#60A5FA" stroke-width="8"/>
  <text x="600" y="215" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="44" font-weight="700" fill="#60A5FA" letter-spacing="8">CALM PIPELINE</text>
  <text x="600" y="345" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="76" font-weight="800" fill="#FFFFFF">SAVED &#8594; APPLIED &#8594; OFFER</text>
  <text x="600" y="435" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="38" font-weight="600" fill="#9AADC4">powered by appliedly</text>
</svg>""",

    "sticker_03_exclusion_contract_seal": """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1200" viewBox="0 0 1200 1200">
  <!-- Die-cut hexagon shield -->
  <polygon points="600,45 1095,315 1095,885 600,1155 105,885 105,315" fill="#FFFFFF"/>
  <polygon points="600,90 1055,340 1055,860 600,1110 145,860 145,340" fill="#0E1828"/>
  <polygon points="600,130 1018,362 1018,838 600,1070 182,838 182,362" fill="none" stroke="#60A5FA" stroke-width="10"/>
  <text x="600" y="370" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="46" font-weight="700" fill="#60A5FA" letter-spacing="6">THE EXCLUSION</text>
  <text x="600" y="455" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="88" font-weight="800" fill="#FFFFFF">CONTRACT</text>
  <rect x="290" y="520" width="620" height="90" rx="45" fill="#10B981"/>
  <text x="600" y="582" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="44" font-weight="800" fill="#06281E">ZERO DUPLICATES</text>
  <text x="600" y="720" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="38" fill="#E8EEF8">Never recommended twice.</text>
  <text x="600" y="885" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="68" font-weight="800" fill="#FFFFFF" letter-spacing="-2">appliedly</text>
</svg>""",

    "sticker_04_track_every_app_laptop": """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="720" viewBox="0 0 1200 720">
  <rect x="20" y="20" width="1160" height="680" rx="90" fill="#FFFFFF"/>
  <rect x="52" y="52" width="1096" height="616" rx="68" fill="#0A1220"/>
  <rect x="52" y="52" width="1096" height="110" rx="68" fill="#2563EB"/>
  <rect x="52" y="110" width="1096" height="52" fill="#2563EB"/>
  <text x="600" y="128" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="48" font-weight="800" fill="#FFFFFF" letter-spacing="6">APPLIEDLY</text>
  <text x="600" y="330" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="76" font-weight="800" fill="#FFFFFF">Track every application.</text>
  <text x="600" y="435" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="76" font-weight="800" fill="#60A5FA">Land the right role.</text>
  <text x="600" y="575" text-anchor="middle" font-family="Consolas, monospace" font-size="44" font-weight="700" fill="#9AADC4">appliedly.com  •  Web • iOS • Android</text>
</svg>""",
}

sticker_png_b64s = {}
for name, svg_code in stickers.items():
    svg_path = os.path.join(STICKERS_DIR, f"{name}.svg")
    png_path = os.path.join(STICKERS_DIR, f"{name}.png")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_code)
    doc = fitz.open(svg_path)
    pix = doc[0].get_pixmap(alpha=True)
    pix.save(png_path)
    doc.close()
    sticker_png_b64s[name] = load_b64(png_path)
    print(f"Sticker generated: {png_path} ({pix.width}x{pix.height})")

# Print-ready A4 Sticker Sheet PDF
sticker_sheet_html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
@page {{ size: A4 portrait; margin: 12mm; }}
body {{ margin: 0; font-family: 'Segoe UI', sans-serif; background: #F1F5F9; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }}
.header {{ text-align: center; margin-bottom: 12px; color: #132033; }}
.grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; align-items: center; justify-items: center; }}
.cell {{ background: #E2E8F0; border: 1px dashed #94A3B8; border-radius: 12px; padding: 14px; text-align: center; width: 100%; }}
.cell img {{ max-width: 100%; max-height: 92mm; object-fit: contain; }}
.cap {{ font-size: 8pt; color: #475569; margin-top: 6px; font-weight: 600; }}
</style></head><body>
<div class="header">
  <h2 style="margin:0;font-size:15pt;">Appliedly Official Die-Cut Sticker Sheet (Print Ready A4)</h2>
  <p style="margin:4px 0 0 0;font-size:9pt;color:#475569;">Transparent 300 DPI PNGs &amp; Vector SVGs included in <code>marketing/stickers/</code></p>
</div>
<div class="grid">
  <div class="cell"><img src="data:image/png;base64,{sticker_png_b64s['sticker_01_open_aperture_badge']}" /><div class="cap">01 • Open Aperture Circular Badge</div></div>
  <div class="cell"><img src="data:image/png;base64,{sticker_png_b64s['sticker_03_exclusion_contract_seal']}" /><div class="cap">03 • Exclusion Contract Shield</div></div>
  <div class="cell"><img src="data:image/png;base64,{sticker_png_b64s['sticker_02_calm_pipeline_pill']}" /><div class="cap">02 • Calm Pipeline Pill</div></div>
  <div class="cell"><img src="data:image/png;base64,{sticker_png_b64s['sticker_04_track_every_app_laptop']}" /><div class="cap">04 • Track Every Application Laptop Sticker</div></div>
</div>
</body></html>"""

sheet_html_path = os.path.join(STICKERS_DIR, "Appliedly_Sticker_Sheet_Print.html")
sheet_pdf_path = os.path.join(STICKERS_DIR, "Appliedly_Sticker_Sheet_Print.pdf")
with open(sheet_html_path, "w", encoding="utf-8") as f:
    f.write(sticker_sheet_html)
subprocess.run([
    EDGE_EXE, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
    f"--print-to-pdf={sheet_pdf_path}", "file:///" + sheet_html_path.replace("\\", "/")
], check=True, capture_output=True)
print(f"Sticker Sheet PDF generated: {sheet_pdf_path}")

# ----------------------------------------------------------------------
# 2. PLATFORM-SIZED SOCIAL GRAPHICS & ADS (Edge Headless Screenshot)
# ----------------------------------------------------------------------
def render_card(out_png, width, height, body_html, extra_css=""):
    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Sora:wght@600;700;800&family=IBM+Plex+Mono:wght@500;700&display=swap');
* {{ box-sizing: border-box; }}
html, body {{
  margin: 0; padding: 0;
  width: {width}px; height: {height}px;
  overflow: hidden;
  font-family: 'Manrope', 'Segoe UI', sans-serif;
  background: radial-gradient(circle at 85% 15%, #163059 0%, #0A1220 60%, #070C16 100%);
  color: #E8EEF8;
}}
.wrap {{
  width: 100%; height: 100%;
  padding: {int(min(width, height)*0.075)}px;
  display: flex; flex-direction: column; justify-content: space-between;
  position: relative;
}}
.glow {{
  position: absolute; width: {int(width*0.55)}px; height: {int(width*0.55)}px;
  border-radius: 50%; background: radial-gradient(circle, rgba(96,165,250,0.22) 0%, rgba(96,165,250,0) 70%);
  top: -{int(height*0.18)}px; right: -{int(width*0.12)}px; pointer-events: none;
}}
.top {{ display: flex; justify-content: space-between; align-items: center; z-index: 2; }}
.pill {{ background: rgba(96,165,250,0.16); color: #60A5FA; border: 1px solid rgba(96,165,250,0.45); padding: 8px 20px; border-radius: 999px; font-weight: 700; font-size: {max(16, int(min(width,height)*0.022))}px; letter-spacing: 0.06em; text-transform: uppercase; }}
.title {{ font-family: 'Sora', sans-serif; font-weight: 800; line-height: 1.1; letter-spacing: -0.03em; color: #FFFFFF; margin: 0; z-index: 2; }}
.accent {{ color: #60A5FA; }}
.green {{ color: #34D399; }}
.red {{ color: #F87171; }}
.sub {{ color: #9AADC4; line-height: 1.45; margin: 0; z-index: 2; }}
.glass {{ background: rgba(14,24,40,0.85); border: 1px solid rgba(148,180,220,0.28); border-radius: 20px; padding: 24px 28px; z-index: 2; }}
.cta {{ display: inline-block; background: #2563EB; color: #FFFFFF; font-family: 'Sora', sans-serif; font-weight: 700; padding: 14px 30px; border-radius: 12px; }}
.foot {{ display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(148,180,220,0.2); padding-top: 18px; color: #9AADC4; font-size: {max(16, int(min(width,height)*0.022))}px; z-index: 2; }}
.mono {{ font-family: 'IBM Plex Mono', Consolas, monospace; color: #60A5FA; font-weight: 700; }}
{extra_css}
</style></head><body><div class="wrap"><div class="glow"></div>{body_html}</div></body></html>"""
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tf:
        tf.write(html)
        tmp_html = tf.name
    try:
        subprocess.run([
            EDGE_EXE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            f"--window-size={width},{height}",
            f"--screenshot={out_png}",
            "file:///" + tmp_html.replace("\\", "/")
        ], check=True, capture_output=True)
        print(f"Rendered {width}x{height} -> {os.path.basename(out_png)}")
    finally:
        if os.path.exists(tmp_html):
            os.remove(tmp_html)

logo_img = f'<img src="data:image/png;base64,{logo_dark_b64}" style="height:44px;" />'
logo_img_lg = f'<img src="data:image/png;base64,{logo_dark_b64}" style="height:56px;" />'

# --- LINKEDIN ---
render_card(
    os.path.join(SOCIAL_DIR, "linkedin", "linkedin_feed_1200x627_hero.png"), 1200, 627,
    f"""
    <div class="top">{logo_img}<span class="pill">Calm Job Application Tracker</span></div>
    <div>
      <h1 class="title" style="font-size:60px;">Track every application.<br><span class="accent">Land the right role.</span></h1>
      <p class="sub" style="font-size:24px;margin-top:16px;max-width:860px;">Replace fragile spreadsheets with a calm visual pipeline, curated AI recommendations, tailored cover letters, and our Exclusion Contract.</p>
    </div>
    <div class="foot"><span>Web • iOS • Android</span><span class="mono">appliedly.com</span></div>
    """
)

render_card(
    os.path.join(SOCIAL_DIR, "linkedin", "linkedin_square_1080x1080_exclusion_contract.png"), 1080, 1080,
    f"""
    <div class="top">{logo_img_lg}<span class="pill">The Exclusion Contract</span></div>
    <div>
      <h1 class="title" style="font-size:74px;">Zero duplicate<br><span class="accent">job recommendations.</span></h1>
      <p class="sub" style="font-size:30px;margin-top:24px;">If a company is already in your active pipeline, Appliedly automatically excludes it from your AI recommendation inbox.</p>
      <div class="glass" style="margin-top:34px;font-size:26px;line-height:1.6;">
        <span class="green">✓</span> Fresh, high-signal roles only<br>
        <span class="green">✓</span> Tailored market briefings &amp; cover notes<br>
        <span class="green">✓</span> Calm stage &amp; duration tracking
      </div>
    </div>
    <div class="foot"><span style="font-size:24px;">Intentional job tracking</span><span class="mono" style="font-size:26px;">appliedly.com</span></div>
    """
)

carousel_slides = [
    ("linkedin_carousel_01_hook.png", "01 / 05 • SWIPE →",
     'Stop tracking your job search in a <span class="accent">broken spreadsheet.</span>',
     "50 open tabs, missed follow-ups, and duplicate job alerts drain your energy before the interview even starts.",
     "Swipe to see the calmer system →"),
    ("linkedin_carousel_02_problem.png", "02 / 05 • THE PROBLEM",
     'Why modern job hunts <span class="red">burn people out.</span>',
     "• Fragile 40-column sheets abandoned by week 3\n• Boards recommending companies you already applied to\n• Zero visibility into how long an application has sat silent",
     "There is a structured way forward →"),
    ("linkedin_carousel_03_pipeline.png", "03 / 05 • CALM PIPELINE",
     'One serene board for <span class="accent">every stage.</span>',
     "Move opportunities cleanly from Saved → Applied → Interviewing → Offer with time-in-stage indicators and private interview notes synced across Web, iOS, and Android.",
     "And smarter job discovery →"),
    ("linkedin_carousel_04_exclusion.png", "04 / 05 • EXCLUSION CONTRACT",
     'Never get recommended <span class="green">the same company twice.</span>',
     "Appliedly’s Exclusion Contract cross-references your active Applications in real time so your curated recommendation inbox only delivers genuinely new roles.",
     "Ready to upgrade your search? →"),
    ("linkedin_carousel_05_cta.png", "05 / 05 • GET STARTED",
     'Track every application.<br><span class="accent">Land the right role.</span>',
     "Calm pipeline. Curated recommendations. Tailored cover letters. Market briefings.",
     "Start free today at appliedly.com"),
]
for fname, badge, heading, body_txt, foot_l in carousel_slides:
    body_html_p = body_txt.replace("\n", "<br>")
    render_card(
        os.path.join(SOCIAL_DIR, "linkedin", fname), 1080, 1350,
        f"""
        <div class="top">{logo_img_lg}<span class="pill">{badge}</span></div>
        <div>
          <h1 class="title" style="font-size:78px;">{heading}</h1>
          <div class="glass" style="margin-top:42px;font-size:32px;line-height:1.55;color:#E8EEF8;">{body_html_p}</div>
        </div>
        <div class="foot"><span style="font-size:26px;color:#E8EEF8;font-weight:700;">{foot_l}</span><span class="mono" style="font-size:26px;">appliedly.com</span></div>
        """
    )

# --- FACEBOOK ---
render_card(
    os.path.join(SOCIAL_DIR, "facebook", "facebook_feed_1200x630_launch.png"), 1200, 630,
    f"""
    <div class="top">{logo_img}<span class="pill">Now Available • Web &amp; Mobile</span></div>
    <div>
      <h1 class="title" style="font-size:58px;">Organize your job hunt<br><span class="accent">without the chaos.</span></h1>
      <p class="sub" style="font-size:24px;margin-top:14px;max-width:880px;">Calm application tracking, tailored cover letters, and smart job matches that never repeat companies you already applied to.</p>
    </div>
    <div class="foot"><span>Try Appliedly Free Today</span><span class="mono">appliedly.com</span></div>
    """
)

render_card(
    os.path.join(SOCIAL_DIR, "facebook", "facebook_square_1080x1080_calm_pipeline.png"), 1080, 1080,
    f"""
    <div class="top">{logo_img_lg}<span class="pill">Job Search Upgrade</span></div>
    <div>
      <h1 class="title" style="font-size:72px;">Ditch the messy<br><span class="accent">job spreadsheet.</span></h1>
      <div class="glass" style="margin-top:34px;font-size:28px;line-height:1.65;">
        <strong style="color:#60A5FA;">SAVED &#8594; APPLIED &#8594; INTERVIEWING &#8594; OFFER</strong><br><br>
        Track durations, write tailored cover letters, and receive curated recommendations—all in one calm workspace.
      </div>
    </div>
    <div class="foot"><span style="font-size:24px;">Web • iOS • Android</span><span class="mono" style="font-size:26px;">appliedly.com</span></div>
    """
)

render_card(
    os.path.join(SOCIAL_DIR, "facebook", "facebook_story_1080x1920_vertical.png"), 1080, 1920,
    f"""
    <div class="top" style="margin-top:80px;">{logo_img_lg}<span class="pill">Appliedly</span></div>
    <div>
      <h1 class="title" style="font-size:88px;line-height:1.08;">Job hunting<br>should feel<br><span class="accent">calm.</span></h1>
      <p class="sub" style="font-size:36px;margin-top:34px;">Track every stage, get tailored cover letters, and block duplicate recommendations automatically.</p>
      <div class="glass" style="margin-top:50px;font-size:32px;line-height:1.7;">
        <span class="green">✓</span> Visual Pipeline &amp; Follow-Up Timers<br>
        <span class="green">✓</span> Curated Recommendation Inbox<br>
        <span class="green">✓</span> Guaranteed Exclusion Contract
      </div>
      <div style="margin-top:54px;"><span class="cta" style="font-size:34px;padding:22px 44px;">Start Free at appliedly.com</span></div>
    </div>
    <div class="foot" style="margin-bottom:60px;"><span style="font-size:26px;">Web • iOS • Android</span><span class="mono" style="font-size:26px;">@appliedly</span></div>
    """
)

# --- TIKTOK / REELS / SHORTS (9:16 1080x1920) ---
render_card(
    os.path.join(SOCIAL_DIR, "tiktok-reels-shorts", "vertical_ad_01_spreadsheet_chaos_1080x1920.png"), 1080, 1920,
    f"""
    <div class="top" style="margin-top:90px;">{logo_img_lg}<span class="pill">Job Search Reality</span></div>
    <div>
      <h1 class="title" style="font-size:86px;">50 open tabs.<br><span class="red">1 broken sheet.</span><br><span class="accent">Zero calm.</span></h1>
      <div class="glass" style="margin-top:48px;font-size:34px;line-height:1.6;">
        Upgrade to <strong style="color:#FFFFFF;">Appliedly</strong>:<br>
        • Clean pipeline stages<br>
        • Time-in-stage follow-up alerts<br>
        • Zero duplicate company alerts
      </div>
      <div style="margin-top:52px;"><span class="cta" style="font-size:34px;padding:22px 42px;">Link in Bio • appliedly.com</span></div>
    </div>
    <div class="foot" style="margin-bottom:80px;"><span style="font-size:26px;">Track every application.</span><span class="mono" style="font-size:26px;">Land the right role.</span></div>
    """
)

render_card(
    os.path.join(SOCIAL_DIR, "tiktok-reels-shorts", "vertical_ad_02_exclusion_contract_1080x1920.png"), 1080, 1920,
    f"""
    <div class="top" style="margin-top:90px;">{logo_img_lg}<span class="pill">The Exclusion Contract</span></div>
    <div>
      <h1 class="title" style="font-size:84px;">Stop getting<br>recommended<br><span class="accent">jobs you already<br>applied to.</span></h1>
      <p class="sub" style="font-size:36px;margin-top:34px;">Appliedly automatically filters out every company already in your active pipeline.</p>
      <div class="glass" style="margin-top:46px;font-size:34px;color:#34D399;font-weight:700;text-align:center;">100% FRESH RECOMMENDATIONS ONLY</div>
    </div>
    <div class="foot" style="margin-bottom:80px;"><span style="font-size:26px;">Web • iOS • Android</span><span class="mono" style="font-size:28px;">appliedly.com</span></div>
    """
)

render_card(
    os.path.join(SOCIAL_DIR, "tiktok-reels-shorts", "vertical_cover_03_3_green_flags_1080x1920.png"), 1080, 1920,
    f"""
    <div class="top" style="margin-top:90px;">{logo_img_lg}<span class="pill">Career Tips</span></div>
    <div style="text-align:center;">
      <div style="font-size:150px;font-family:'Sora',sans-serif;font-weight:800;color:#60A5FA;line-height:1;">3</div>
      <h1 class="title" style="font-size:86px;margin-top:10px;">Job Tracker<br><span class="green">Green Flags</span></h1>
      <p class="sub" style="font-size:36px;margin-top:28px;">What every serious job seeker needs in 2026.</p>
    </div>
    <div class="foot" style="margin-bottom:80px;"><span style="font-size:26px;">Watch to the end</span><span class="mono" style="font-size:26px;">appliedly.com</span></div>
    """
)

# --- TWITTER / X ---
render_card(
    os.path.join(SOCIAL_DIR, "twitter-x", "x_card_1600x900_launch.png"), 1600, 900,
    f"""
    <div class="top">{logo_img_lg}<span class="pill">Launch Announcement</span></div>
    <div>
      <h1 class="title" style="font-size:82px;">Track every application.<br><span class="accent">Land the right role.</span></h1>
      <p class="sub" style="font-size:32px;margin-top:24px;max-width:1180px;">Calm pipeline tracking • Curated recommendation inbox • Tailored cover letters • Guaranteed Exclusion Contract.</p>
    </div>
    <div class="foot"><span style="font-size:26px;">Built for intentional job seekers • Web, iOS &amp; Android</span><span class="mono" style="font-size:28px;">appliedly.com</span></div>
    """
)

render_card(
    os.path.join(SOCIAL_DIR, "twitter-x", "x_header_1500x500_banner.png"), 1500, 500,
    f"""
    <div style="display:flex;justify-content:space-between;align-items:center;height:100%;z-index:2;">
      <div>
        {logo_img_lg}
        <h1 class="title" style="font-size:58px;margin-top:18px;">Track every application. <span class="accent">Land the right role.</span></h1>
        <p class="sub" style="font-size:24px;margin-top:10px;">Calm pipeline • Curated AI inbox • The Exclusion Contract</p>
      </div>
      <div class="glass" style="text-align:right;padding:22px 30px;">
        <div class="mono" style="font-size:28px;">appliedly.com</div>
        <div style="color:#9AADC4;font-size:20px;margin-top:6px;">Web • iOS • Android</div>
      </div>
    </div>
    """
)

# --- PRODUCT HUNT GALLERY (1270x760) ---
ph_cards = [
    ("ph_gallery_01_hero_1270x760.png", "01 • OVERVIEW",
     'The calm job application<br><span class="accent">tracker built for focus.</span>',
     "Replace fragile spreadsheets and noisy auto-apply spam with a structured pipeline across Web, iOS, and Android."),
    ("ph_gallery_02_pipeline_1270x760.png", "02 • CALM PIPELINE",
     'Every stage &amp; duration<br><span class="accent">in crystal clarity.</span>',
     "Saved → Applied → Interviewing → Offer. Know exactly how long each application has been waiting so you follow up at the right moment."),
    ("ph_gallery_03_exclusion_1270x760.png", "03 • THE EXCLUSION CONTRACT",
     'Curated recommendations.<br><span class="green">Zero duplicates.</span>',
     "Any company already in your Applications list is automatically excluded from your AI recommendation inbox—paired with tailored cover letters and market briefings."),
]
for fname, badge, heading, desc in ph_cards:
    render_card(
        os.path.join(SOCIAL_DIR, "product-hunt", fname), 1270, 760,
        f"""
        <div class="top">{logo_img}<span class="pill">{badge}</span></div>
        <div>
          <h1 class="title" style="font-size:66px;">{heading}</h1>
          <p class="sub" style="font-size:28px;margin-top:22px;max-width:980px;">{desc}</p>
        </div>
        <div class="foot"><span>Appliedly — Open Aperture Edition</span><span class="mono">appliedly.com</span></div>
        """
    )

print("All stickers and social graphics generated successfully!")
