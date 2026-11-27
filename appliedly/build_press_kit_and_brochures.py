import os
import base64
import shutil
import subprocess

BASE_DIR = r"A:\Project Data\projects\enmirth\organization\publishing\software\appliedly"
BRAND_LOGO_DIR = os.path.join(BASE_DIR, "brand", "logo")
MARKETING_DIR = os.path.join(BASE_DIR, "marketing")
PRESS_KIT_DIR = os.path.join(MARKETING_DIR, "press-kit")
PRESS_LOGOS_DIR = os.path.join(PRESS_KIT_DIR, "logos")
BROCHURES_DIR = os.path.join(MARKETING_DIR, "brochures")
EDGE_EXE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

os.makedirs(PRESS_LOGOS_DIR, exist_ok=True)
os.makedirs(BROCHURES_DIR, exist_ok=True)

def load_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

logo_dark_b64 = load_b64(os.path.join(BRAND_LOGO_DIR, "png", "wordmark-on-dark-720.png"))
logo_light_b64 = load_b64(os.path.join(BRAND_LOGO_DIR, "png", "wordmark-on-light-720.png"))
icon_512_b64 = load_b64(os.path.join(BRAND_LOGO_DIR, "publishing", "store-icon-512.png"))

# 1. Copy curated press logos into press-kit/logos/
curated_logos = [
    os.path.join(BRAND_LOGO_DIR, "wordmark-on-dark.svg"),
    os.path.join(BRAND_LOGO_DIR, "wordmark-on-light.svg"),
    os.path.join(BRAND_LOGO_DIR, "wordmark-transparent.svg"),
    os.path.join(BRAND_LOGO_DIR, "mark.svg"),
    os.path.join(BRAND_LOGO_DIR, "mark-on-dark.svg"),
    os.path.join(BRAND_LOGO_DIR, "png", "wordmark-on-dark-1440.png"),
    os.path.join(BRAND_LOGO_DIR, "png", "wordmark-on-light-1440.png"),
    os.path.join(BRAND_LOGO_DIR, "png", "wordmark-transparent-1440.png"),
    os.path.join(BRAND_LOGO_DIR, "png", "share-preview-1200x630.png"),
    os.path.join(BRAND_LOGO_DIR, "publishing", "store-icon-1024.png"),
]
copied_count = 0
for src in curated_logos:
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(PRESS_LOGOS_DIR, os.path.basename(src)))
        copied_count += 1
print(f"Copied {copied_count} curated logos to {PRESS_LOGOS_DIR}")

def html_to_pdf(html_str, html_path, pdf_path):
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_str)
    uri = "file:///" + html_path.replace("\\", "/")
    cmd = [
        EDGE_EXE,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        uri,
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"Generated PDF: {pdf_path} ({os.path.getsize(pdf_path)//1024} KB)")

# ----------------------------------------------------------------------
# A. ELECTRONIC PRESS KIT (PDF)
# ----------------------------------------------------------------------
press_kit_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Appliedly — Official Press Kit</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Sora:wght@600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');
  @page {{ size: A4 portrait; margin: 16mm; }}
  * {{ box-sizing: border-box; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }}
  body {{ font-family: 'Manrope', 'Segoe UI', sans-serif; color: #132033; margin: 0; font-size: 9.5pt; line-height: 1.55; }}
  .hero {{ background: linear-gradient(135deg, #0A1220 0%, #0E1828 65%, #162947 100%); color: #E8EEF8; padding: 34px 32px; border-radius: 14px; margin-bottom: 22px; }}
  .hero-top {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }}
  .badge {{ background: rgba(96,165,250,0.18); color: #60A5FA; border: 1px solid rgba(96,165,250,0.4); padding: 4px 12px; border-radius: 999px; font-size: 8pt; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; }}
  h1 {{ font-family: 'Sora', sans-serif; font-size: 24pt; margin: 0 0 8px 0; color: #FFFFFF; letter-spacing: -0.02em; }}
  .lead {{ font-size: 11pt; color: #9AADC4; margin: 0; max-width: 90%; }}
  h2 {{ font-family: 'Sora', sans-serif; font-size: 13pt; color: #0A1220; border-bottom: 2px solid #2563EB; padding-bottom: 5px; margin: 22px 0 12px 0; page-break-after: avoid; }}
  .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
  .grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }}
  .card {{ background: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 10px; padding: 14px 16px; page-break-inside: avoid; }}
  .card-dark {{ background: #0E1828; color: #E8EEF8; border: 1px solid #1E2D42; border-radius: 10px; padding: 14px 16px; page-break-inside: avoid; }}
  .card h3 {{ font-family: 'Sora', sans-serif; font-size: 10pt; margin: 0 0 6px 0; color: #1E3A8A; }}
  .card-dark h3 {{ font-family: 'Sora', sans-serif; font-size: 10pt; margin: 0 0 6px 0; color: #60A5FA; }}
  table {{ width: 100%; border-collapse: collapse; margin: 8px 0 16px 0; font-size: 8.8pt; }}
  th, td {{ padding: 8px 10px; border-bottom: 1px solid #E2E8F0; text-align: left; vertical-align: top; }}
  th {{ width: 28%; background: #F1F5F9; font-weight: 700; color: #0A1220; }}
  .swatch-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 10px 0 16px 0; }}
  .swatch {{ border: 1px solid #CBD5E1; border-radius: 8px; overflow: hidden; page-break-inside: avoid; }}
  .swatch-color {{ height: 46px; }}
  .swatch-meta {{ padding: 7px 9px; font-size: 7.8pt; background: #FFF; }}
  .mono {{ font-family: 'IBM Plex Mono', Consolas, monospace; font-size: 8pt; color: #2563EB; }}
  .quote {{ background: #EFF6FF; border-left: 4px solid #2563EB; padding: 14px 18px; border-radius: 0 10px 10px 0; font-style: italic; margin: 12px 0; page-break-inside: avoid; }}
  .page-break {{ page-break-before: always; }}
</style>
</head>
<body>

<div class="hero">
  <div class="hero-top">
    <img src="data:image/png;base64,{logo_dark_b64}" style="height:38px;" alt="Appliedly" />
    <span class="badge">Official Media &amp; Press Kit</span>
  </div>
  <h1>Track every application.<br>Land the right role.</h1>
  <p class="lead">Appliedly is the personal job application tracker built around a calm pipeline, curated AI recommendation inbox, tailored cover letters, market briefings, and a strict Exclusion Contract.</p>
</div>

<h2>1. Fast Fact Sheet</h2>
<table>
  <tr><th>Product Name</th><td><strong>Appliedly</strong> (by Enmirth)</td></tr>
  <tr><th>Tagline</th><td>Track every application. Land the right role.</td></tr>
  <tr><th>Category</th><td>Career Productivity / Personal Job Application Tracker / AI Career Assistant</td></tr>
  <tr><th>Platforms</th><td>Web App (Primary), iOS (Apple), Android (Google Play), PWA</td></tr>
  <tr><th>Core Differentiator</th><td><strong>The Exclusion Contract</strong> — active applications automatically block duplicate company recommendations in the AI inbox.</td></tr>
  <tr><th>Brand Concept</th><td>Open Aperture #9 (wordmark-only identity, calm dark-first glass aesthetic)</td></tr>
  <tr><th>Press Assets Included</th><td>High-res SVG/PNG logos (dark, light, transparent), app icons, Open Graph cards, and product fact sheet in <code>press-kit/logos/</code>.</td></tr>
</table>

<h2>2. Approved Press Boilerplates</h2>
<div class="grid-2">
  <div class="card">
    <h3>Short Description (25 Words)</h3>
    <p style="margin:0;">Appliedly is a calm job application tracker with a curated recommendation inbox, tailored cover letters, market briefings, and automatic exclusions for companies already in your pipeline.</p>
  </div>
  <div class="card">
    <h3>Standard Description (65 Words)</h3>
    <p style="margin:0;">Modern job seekers are caught between fragile spreadsheets and noisy auto-apply spam. Appliedly restores calm and precision to the job hunt. Combining a structured visual pipeline with time-in-stage tracking, tailored cover letter drafts, market briefings, and a curated recommendation inbox governed by an Exclusion Contract, Appliedly ensures candidates never waste time on duplicate roles or broken tracking sheets.</p>
  </div>
</div>

<div class="page-break"></div>

<h2>3. Core Product Pillars</h2>
<div class="grid-3">
  <div class="card-dark">
    <h3>Calm Pipeline</h3>
    <p style="margin:0;font-size:8.5pt;">Track every role across clear deterministic stages (Saved, Applied, Interviewing, Offer, Archive) with duration metrics and private notes.</p>
  </div>
  <div class="card-dark">
    <h3>Exclusion Contract</h3>
    <p style="margin:0;font-size:8.5pt;">Your active Applications list acts as an automatic shield—Appliedly never recommends companies you have already applied to.</p>
  </div>
  <div class="card-dark">
    <h3>Market Briefings</h3>
    <p style="margin:0;font-size:8.5pt;">Receive high-signal role recommendations, market briefings, and tailored cover letter guidance aligned to your target positions.</p>
  </div>
</div>

<h2>4. Brand Identity &amp; Visual Guidelines (Open Aperture)</h2>
<p>Media outlets and partners are welcome to use the official Appliedly wordmark and palette below. Maintain clear breathing room around the wordmark and preserve original proportions.</p>

<div class="grid-2" style="margin-bottom:14px;">
  <div style="background:#0A1220;padding:20px;border-radius:10px;text-align:center;">
    <img src="data:image/png;base64,{logo_dark_b64}" style="height:34px;" alt="Wordmark on Dark" />
    <div style="color:#9AADC4;font-size:7.5pt;margin-top:8px;">Primary Wordmark on Deep Slate (#0A1220)</div>
  </div>
  <div style="background:#D8E4F2;padding:20px;border-radius:10px;text-align:center;border:1px solid #CBD5E1;">
    <img src="data:image/png;base64,{logo_light_b64}" style="height:34px;" alt="Wordmark on Light" />
    <div style="color:#5A6D84;font-size:7.5pt;margin-top:8px;">Wordmark on Paper Light (#D8E4F2)</div>
  </div>
</div>

<div class="swatch-grid">
  <div class="swatch"><div class="swatch-color" style="background:#0A1220;"></div><div class="swatch-meta"><strong>Deep Slate</strong><br><span class="mono">#0A1220</span></div></div>
  <div class="swatch"><div class="swatch-color" style="background:#0E1828;"></div><div class="swatch-meta"><strong>Glass Panel</strong><br><span class="mono">#0E1828</span></div></div>
  <div class="swatch"><div class="swatch-color" style="background:#60A5FA;"></div><div class="swatch-meta"><strong>Aperture Blue</strong><br><span class="mono">#60A5FA</span></div></div>
  <div class="swatch"><div class="swatch-color" style="background:#2563EB;"></div><div class="swatch-meta"><strong>Action Accent</strong><br><span class="mono">#2563EB</span></div></div>
</div>

<div class="card">
  <h3>Typography Specification</h3>
  <p style="margin:0;"><strong>Display / Headings:</strong> Sora (Semibold 600, Bold 700, tracking -0.02em) &nbsp;|&nbsp; <strong>Body / UI:</strong> Manrope (Regular 400, Medium 500, Semibold 600) &nbsp;|&nbsp; <strong>Data / Monospace:</strong> IBM Plex Mono</p>
</div>

<h2>5. Official Press Quote &amp; Media Inquiries</h2>
<div class="quote">
  "Job hunting shouldn't feel like managing a chaotic spreadsheet while dodging duplicate job alerts. We built Appliedly so candidates can focus their energy on high-signal applications, clear follow-ups, and landing the right role."
  <div style="font-style:normal;font-weight:700;margin-top:6px;color:#1E3A8A;">— Appliedly Product &amp; Marketing Team, Enmirth</div>
</div>

<div class="card">
  <h3>Press &amp; Partnership Inquiries</h3>
  <p style="margin:0;">For interviews, review accounts, high-resolution product walkthroughs, or cohort partnerships for bootcamps and universities, contact the Appliedly Marketing Development team and reference the <strong>Appliedly Official Press Kit v1.0</strong>.</p>
</div>

</body>
</html>
"""
html_to_pdf(
    press_kit_html,
    os.path.join(PRESS_KIT_DIR, "Appliedly_Press_Kit.html"),
    os.path.join(PRESS_KIT_DIR, "Appliedly_Press_Kit.pdf"),
)

# Press Kit README
press_readme = """# Appliedly Official Press Kit (v1.0)

## Quick Copy Boilerplates
- **Tagline**: Track every application. Land the right role.
- **One-Liner**: Appliedly is a personal job application tracker with a calm pipeline, curated AI recommendation inbox, tailored cover letters, market briefings, and automatic exclusions for companies already in your Applications.
- **Brand Concept**: Open Aperture #9

## Included Files
- `Appliedly_Press_Kit.pdf` — Complete multi-page Electronic Press Kit (Fact Sheet, Pillars, Palette, Typography, Quotes).
- `logos/` — Ready-to-use high-resolution SVG and PNG wordmarks (dark, light, transparent), app icon (`1024x1024`), and Open Graph share card (`1200x630`).

## Brand Colors
- Deep Slate Background: `#0A1220`
- Glass Surface: `#0E1828`
- Aperture Blue Accent: `#60A5FA`
- Action Blue (Light Mode): `#2563EB`
- Paper Surface: `#D8E4F2`
- Primary Ink: `#132033`
"""
with open(os.path.join(PRESS_KIT_DIR, "PRESS_KIT_README.md"), "w", encoding="utf-8") as f:
    f.write(press_readme)

# ----------------------------------------------------------------------
# B. ONE-PAGER EXECUTIVE FLYER (PDF - 1 Page A4)
# ----------------------------------------------------------------------
onepager_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Appliedly — One-Page Product Flyer</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Sora:wght@600;700&display=swap');
  @page {{ size: A4 portrait; margin: 0; }}
  * {{ box-sizing: border-box; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }}
  body {{ margin: 0; font-family: 'Manrope', 'Segoe UI', sans-serif; background: #0A1220; color: #E8EEF8; width: 210mm; height: 297mm; overflow: hidden; display: flex; flex-direction: column; justify-content: space-between; padding: 18mm 16mm; }}
  .top-bar {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(148,180,220,0.22); padding-bottom: 14px; }}
  .pill {{ background: rgba(96,165,250,0.16); color: #60A5FA; border: 1px solid rgba(96,165,250,0.4); padding: 5px 12px; border-radius: 999px; font-size: 8.5pt; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase; }}
  .hero-block {{ margin: 18px 0; }}
  h1 {{ font-family: 'Sora', sans-serif; font-size: 30pt; line-height: 1.12; margin: 0 0 12px 0; letter-spacing: -0.03em; color: #FFFFFF; }}
  .accent {{ color: #60A5FA; }}
  .sub {{ font-size: 11.5pt; color: #9AADC4; line-height: 1.5; margin: 0; max-width: 92%; }}
  .cards {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin: 16px 0; }}
  .card {{ background: #0E1828; border: 1px solid rgba(148,180,220,0.25); border-radius: 12px; padding: 16px 18px; }}
  .card-num {{ font-family: 'Sora', sans-serif; color: #60A5FA; font-size: 9pt; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 5px; }}
  .card h3 {{ font-family: 'Sora', sans-serif; font-size: 12pt; margin: 0 0 6px 0; color: #FFFFFF; }}
  .card p {{ font-size: 9pt; color: #9AADC4; margin: 0; line-height: 1.5; }}
  .compare {{ background: rgba(96,165,250,0.08); border: 1px solid rgba(96,165,250,0.3); border-radius: 12px; padding: 16px 20px; margin: 10px 0; }}
  .compare h3 {{ font-family: 'Sora', sans-serif; font-size: 11pt; margin: 0 0 10px 0; color: #FFFFFF; }}
  .compare-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; font-size: 9pt; }}
  .footer {{ background: linear-gradient(90deg, #2563EB 0%, #1D4ED8 100%); border-radius: 12px; padding: 18px 22px; display: flex; justify-content: space-between; align-items: center; }}
  .footer h2 {{ font-family: 'Sora', sans-serif; font-size: 14pt; margin: 0 0 4px 0; color: #FFFFFF; }}
  .footer p {{ margin: 0; font-size: 9.5pt; color: #DBEAFE; }}
  .cta-box {{ background: #FFFFFF; color: #0A1220; font-family: 'Sora', sans-serif; font-weight: 700; font-size: 10.5pt; padding: 10px 18px; border-radius: 8px; }}
</style>
</head>
<body>
  <div class="top-bar">
    <img src="data:image/png;base64,{logo_dark_b64}" style="height:36px;" alt="Appliedly" />
    <span class="pill">Web • iOS • Android</span>
  </div>

  <div class="hero-block">
    <h1>Track every application.<br><span class="accent">Land the right role.</span></h1>
    <p class="sub">Replace chaotic spreadsheets and noisy job boards with a calm visual pipeline, curated AI recommendations, tailored cover letters, and automatic duplicate company exclusions.</p>
  </div>

  <div class="cards">
    <div class="card">
      <div class="card-num">01 / Calm Pipeline</div>
      <h3>Visual Stage &amp; Duration Tracking</h3>
      <p>Move opportunities cleanly from Saved → Applied → Interviewing → Offer. Time-in-stage indicators show exactly when to follow up before a lead goes cold.</p>
    </div>
    <div class="card">
      <div class="card-num">02 / Exclusion Contract</div>
      <h3>Zero Duplicate Recommendations</h3>
      <p>Appliedly cross-references your active Applications list in real time. Companies you have already applied to are automatically excluded from your recommendation inbox.</p>
    </div>
    <div class="card">
      <div class="card-num">03 / Tailored Craft</div>
      <h3>Bespoke Cover Letters</h3>
      <p>Generate structured, role-aligned cover letter drafts anchored to the real job description—eliminating robotic spam while saving hours per week.</p>
    </div>
    <div class="card">
      <div class="card-num">04 / Market Intelligence</div>
      <h3>Curated Market Briefings</h3>
      <p>Stay sharp with clear market briefings and high-signal role recommendations tailored to your skills, seniority, and career goals.</p>
    </div>
  </div>

  <div class="compare">
    <h3>Why Job Seekers Switch to Appliedly</h3>
    <div class="compare-grid">
      <div>
        <strong style="color:#F87171;">Traditional Spreadsheets &amp; Boards</strong>
        <ul style="margin:6px 0 0 16px;padding:0;color:#9AADC4;line-height:1.6;">
          <li>40-column sheets that break after week two</li>
          <li>Repeated alerts for companies already applied to</li>
          <li>Forgotten follow-ups and scattered interview notes</li>
        </ul>
      </div>
      <div>
        <strong style="color:#34D399;">The Appliedly Workflow</strong>
        <ul style="margin:6px 0 0 16px;padding:0;color:#E8EEF8;line-height:1.6;">
          <li>Serene, synced web &amp; mobile pipeline</li>
          <li>Guaranteed Exclusion Contract on recommendations</li>
          <li>Structured notes, durations, and tailored briefs</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="footer">
    <div>
      <h2>Ready for a calmer job search?</h2>
      <p>Start organizing your pipeline across Web, iOS, and Android today.</p>
    </div>
    <div class="cta-box">appliedly.com</div>
  </div>
</body>
</html>
"""
html_to_pdf(
    onepager_html,
    os.path.join(BROCHURES_DIR, "Appliedly_OnePager_Flyer.html"),
    os.path.join(BROCHURES_DIR, "Appliedly_OnePager_Flyer.pdf"),
)

# ----------------------------------------------------------------------
# C. TRI-FOLD BROCHURE (PDF - 2-Sided Landscape A4, 3 Panels per side)
# ----------------------------------------------------------------------
trifold_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Appliedly — Tri-Fold Brochure</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Sora:wght@600;700&display=swap');
  @page {{ size: A4 landscape; margin: 0; }}
  * {{ box-sizing: border-box; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }}
  body {{ margin: 0; font-family: 'Manrope', 'Segoe UI', sans-serif; color: #132033; }}
  .sheet {{ width: 297mm; height: 210mm; display: grid; grid-template-columns: repeat(3, 99mm); page-break-after: always; overflow: hidden; }}
  .sheet:last-child {{ page-break-after: auto; }}
  .panel {{ padding: 14mm 10mm; height: 210mm; position: relative; display: flex; flex-direction: column; justify-content: space-between; border-right: 1px dashed rgba(148,180,220,0.35); }}
  .panel:last-child {{ border-right: none; }}
  .dark {{ background: #0A1220; color: #E8EEF8; }}
  .slate {{ background: #0E1828; color: #E8EEF8; }}
  .light {{ background: #F8FAFC; color: #132033; }}
  .paper {{ background: #D8E4F2; color: #132033; }}
  h2 {{ font-family: 'Sora', sans-serif; font-size: 16pt; line-height: 1.2; margin: 0 0 10px 0; }}
  h3 {{ font-family: 'Sora', sans-serif; font-size: 11pt; margin: 14px 0 6px 0; }}
  p {{ font-size: 9pt; line-height: 1.55; margin: 0 0 10px 0; }}
  .tag {{ display: inline-block; background: rgba(96,165,250,0.18); color: #60A5FA; border: 1px solid rgba(96,165,250,0.4); padding: 3px 10px; border-radius: 999px; font-size: 7.5pt; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 10px; }}
  .tag-light {{ display: inline-block; background: #DBEAFE; color: #1E40AF; padding: 3px 10px; border-radius: 999px; font-size: 7.5pt; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 10px; }}
  .box {{ background: rgba(255,255,255,0.05); border: 1px solid rgba(148,180,220,0.22); border-radius: 10px; padding: 12px; margin-bottom: 10px; }}
  .box-light {{ background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 10px; padding: 12px; margin-bottom: 10px; }}
  .small-foot {{ font-size: 7.5pt; opacity: 0.7; }}
</style>
</head>
<body>

<!-- SIDE 1: OUTSIDE (Left: Inside Flap | Center: Back Cover | Right: Front Cover) -->
<div class="sheet">
  <!-- Panel 1: Inside Flap -->
  <div class="panel slate">
    <div>
      <span class="tag">Built For Focus</span>
      <h2 style="color:#FFFFFF;">For Bootcamps, Coaches &amp; Teams</h2>
      <p style="color:#9AADC4;">Career coaches and university career centers recommend Appliedly so cohorts maintain disciplined, transparent pipelines without fighting broken spreadsheets.</p>
      <div class="box">
        <strong style="color:#60A5FA;">Cohort Benefits</strong>
        <ul style="margin:6px 0 0 16px;padding:0;font-size:8.5pt;color:#E8EEF8;line-height:1.6;">
          <li>Consistent stage definitions across every candidate</li>
          <li>Zero duplicate company applications</li>
          <li>Time-in-stage visibility for weekly coaching check-ins</li>
        </ul>
      </div>
    </div>
    <div class="small-foot">Appliedly Cohort &amp; Partner Program</div>
  </div>

  <!-- Panel 2: Back Cover -->
  <div class="panel light" style="text-align:center;justify-content:center;align-items:center;">
    <img src="data:image/png;base64,{logo_light_b64}" style="height:30px;margin-bottom:14px;" alt="Appliedly" />
    <p style="max-width:74mm;color:#5A6D84;">Personal job application tracker with a calm pipeline, curated recommendation inbox, tailored cover letters, market briefings, and automatic company exclusions.</p>
    <div class="box-light" style="width:74mm;margin-top:12px;">
      <strong style="color:#1E3A8A;">Get Started Today</strong><br>
      <span style="font-size:10pt;font-weight:700;color:#2563EB;">https://appliedly.com</span><br>
      <span style="font-size:8pt;color:#5A6D84;">Available on Web, iOS, and Android</span>
    </div>
    <p class="small-foot" style="margin-top:24px;">© Enmirth • Appliedly Marketing Kit</p>
  </div>

  <!-- Panel 3: Front Cover -->
  <div class="panel dark">
    <div>
      <img src="data:image/png;base64,{logo_dark_b64}" style="height:34px;" alt="Appliedly" />
    </div>
    <div>
      <span class="tag">Open Aperture Edition</span>
      <h2 style="font-size:24pt;color:#FFFFFF;letter-spacing:-0.02em;">Track every application.<br><span style="color:#60A5FA;">Land the right role.</span></h2>
      <p style="color:#9AADC4;font-size:10pt;">The calm, intelligent job search workspace engineered for modern professionals.</p>
    </div>
    <div style="border-top:1px solid rgba(148,180,220,0.25);padding-top:10px;display:flex;justify-content:space-between;font-size:8pt;color:#9AADC4;">
      <span>Web • iOS • Android</span>
      <span style="color:#60A5FA;font-weight:700;">appliedly.com</span>
    </div>
  </div>
</div>

<!-- SIDE 2: INSIDE SPREAD (3 Panels Left -> Right) -->
<div class="sheet">
  <!-- Inside Left -->
  <div class="panel light">
    <div>
      <span class="tag-light">01 / The Problem</span>
      <h2>Why Modern Job Hunts Burn People Out</h2>
      <p>Applying to great roles requires focus—yet most candidates lose hours every week to fragmented tools:</p>
      <div class="box-light">
        <strong>Spreadsheet Chaos</strong>
        <p style="margin:4px 0 0 0;color:#5A6D84;">Dozens of browser tabs, stale status cells, and forgotten follow-up dates.</p>
      </div>
      <div class="box-light">
        <strong>Duplicate Noise</strong>
        <p style="margin:4px 0 0 0;color:#5A6D84;">Job boards repeatedly recommend roles at companies you already applied to or interviewed with.</p>
      </div>
      <div class="box-light">
        <strong>Generic Auto-Apply Spam</strong>
        <p style="margin:4px 0 0 0;color:#5A6D84;">Spray-and-pray bots flood recruiters and hurt candidate credibility.</p>
      </div>
    </div>
    <div class="small-foot">01 • Calm over chaos</div>
  </div>

  <!-- Inside Center -->
  <div class="panel paper">
    <div>
      <span class="tag-light">02 / The Solution</span>
      <h2>Your Calm Application Pipeline</h2>
      <p>Appliedly replaces clutter with a structured, serene workspace built specifically for intentional candidates:</p>
      <div class="box-light">
        <strong style="color:#1E3A8A;">Deterministic Pipeline Stages</strong>
        <p style="margin:4px 0 0 0;color:#5A6D84;">Track Saved, Applied, Interviewing, Offer, and Archived roles with instant time-in-stage visibility.</p>
      </div>
      <div class="box-light">
        <strong style="color:#1E3A8A;">Tailored Cover Letters</strong>
        <p style="margin:4px 0 0 0;color:#5A6D84;">Draft sharp, relevant cover notes aligned to each role’s exact requirements.</p>
      </div>
      <div class="box-light">
        <strong style="color:#1E3A8A;">Market Briefings</strong>
        <p style="margin:4px 0 0 0;color:#5A6D84;">Receive concise intelligence on hiring trends and target roles.</p>
      </div>
    </div>
    <div class="small-foot">02 • Built for clarity</div>
  </div>

  <!-- Inside Right -->
  <div class="panel dark">
    <div>
      <span class="tag">03 / The Exclusion Contract</span>
      <h2 style="color:#FFFFFF;">Smarter Recommendations. Zero Duplicates.</h2>
      <p style="color:#9AADC4;">Our recommendation inbox obeys one strict rule: <strong style="color:#FFFFFF;">The Exclusion Contract</strong>.</p>
      <div class="box">
        <strong style="color:#60A5FA;">How It Protects Your Time</strong>
        <p style="margin:6px 0 0 0;color:#E8EEF8;">Any company already in your active Applications pipeline is automatically excluded from future AI recommendations—ensuring every match is genuinely new.</p>
      </div>
      <div class="box" style="background:#2563EB;border-color:#60A5FA;">
        <strong style="color:#FFFFFF;font-size:10pt;">Start Tracking Free</strong>
        <p style="margin:4px 0 0 0;color:#DBEAFE;">Sync seamlessly across Web, iOS, and Android at <strong>appliedly.com</strong>.</p>
      </div>
    </div>
    <div class="small-foot">03 • Intentional job discovery</div>
  </div>
</div>

</body>
</html>
"""
html_to_pdf(
    trifold_html,
    os.path.join(BROCHURES_DIR, "Appliedly_Trifold_Brochure.html"),
    os.path.join(BROCHURES_DIR, "Appliedly_Trifold_Brochure.pdf"),
)
print("Press kit and brochures complete!")
