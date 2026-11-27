import os
import sys
import base64
import subprocess
import shutil

LOGO_PNG_PATH = r"A:\Project Data\projects\enmirth\organization\publishing\software\appliedly\brand\logo\png\wordmark-on-dark-720.png"
OUTPUT_DIR = r"A:\Project Data\projects\enmirth\organization\publishing\software\appliedly\marketing"
HTML_PATH = os.path.join(OUTPUT_DIR, "Appliedly_Marketing_Directory_and_Materials.html")
PDF_PATH = os.path.join(OUTPUT_DIR, "Appliedly_Marketing_Directory_and_Materials.pdf")
ARTIFACT_DIR = r"C:\Users\Enmirth\.gemini\antigravity\brain\00c9a073-2960-44eb-9c78-e811c9a2d6a9"
ARTIFACT_PDF_PATH = os.path.join(ARTIFACT_DIR, "Appliedly_Marketing_Directory_and_Materials.pdf")

logo_b64 = ""
if os.path.exists(LOGO_PNG_PATH):
    with open(LOGO_PNG_PATH, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode("utf-8")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Appliedly — GTM Marketing Channels Directory & Production Materials Report</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Sora:wght@600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

  @page {{
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
    @bottom-right {{
      content: "Page " counter(page);
      font-size: 8pt;
      color: #5A6D84;
      font-family: 'Manrope', sans-serif;
    }}
  }}

  * {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }}

  body {{
    font-family: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background-color: #FFFFFF;
    color: #132033;
    line-height: 1.55;
    font-size: 9.5pt;
    margin: 0;
    padding: 0;
  }}

  .header-card {{
    background: #0A1220;
    color: #E8EEF8;
    padding: 24px 28px;
    border-radius: 12px;
    margin-bottom: 24px;
    border: 1px solid #1E2D42;
  }}

  .header-flex {{
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}

  .logo-img {{
    max-height: 40px;
    width: auto;
  }}

  .header-badge {{
    background: rgba(96, 165, 250, 0.16);
    color: #60A5FA;
    font-size: 8pt;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 999px;
    border: 1px solid rgba(96, 165, 250, 0.35);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }}

  .doc-title {{
    font-family: 'Sora', sans-serif;
    font-size: 19pt;
    font-weight: 700;
    color: #FFFFFF;
    margin: 12px 0 6px 0;
    letter-spacing: -0.02em;
  }}

  .doc-subtitle {{
    color: #9AADC4;
    font-size: 10pt;
    margin: 0 0 14px 0;
  }}

  .meta-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    border-top: 1px solid #1E2D42;
    padding-top: 12px;
    font-size: 8pt;
  }}

  .meta-item strong {{
    display: block;
    color: #60A5FA;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    font-size: 7pt;
    margin-bottom: 2px;
  }}

  .meta-item span {{
    color: #E8EEF8;
  }}

  h2 {{
    font-family: 'Sora', sans-serif;
    font-size: 13pt;
    font-weight: 700;
    color: #0A1220;
    margin: 24px 0 12px 0;
    padding-bottom: 6px;
    border-bottom: 2px solid #2563EB;
    display: flex;
    align-items: center;
    justify-content: space-between;
    page-break-after: avoid;
  }}

  h3 {{
    font-family: 'Sora', sans-serif;
    font-size: 10.5pt;
    font-weight: 600;
    color: #132033;
    margin: 16px 0 8px 0;
    page-break-after: avoid;
  }}

  p {{
    margin: 0 0 10px 0;
  }}

  .pill {{
    display: inline-block;
    padding: 2px 7px;
    border-radius: 4px;
    font-size: 7.5pt;
    font-weight: 600;
    text-transform: uppercase;
  }}
  .pill-tier1 {{ background: #DBEAFE; color: #1E40AF; }}
  .pill-tier2 {{ background: #FEF3C7; color: #92400E; }}
  .pill-tier3 {{ background: #E0E7FF; color: #3730A3; }}
  .pill-tier4 {{ background: #D1FAE5; color: #065F46; }}

  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0 18px 0;
    font-size: 8.5pt;
    page-break-inside: auto;
  }}

  tr {{
    page-break-inside: avoid;
    page-break-after: auto;
  }}

  th {{
    background-color: #0A1220;
    color: #FFFFFF;
    text-align: left;
    padding: 8px 10px;
    font-weight: 600;
    font-size: 8pt;
    letter-spacing: 0.02em;
  }}

  td {{
    padding: 8px 10px;
    border-bottom: 1px solid #E2E8F0;
    vertical-align: top;
  }}

  tr:nth-child(even) td {{
    background-color: #F8FAFC;
  }}

  .site-name {{
    font-weight: 700;
    color: #1E3A8A;
    font-size: 9pt;
  }}

  .site-url {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 7.5pt;
    color: #2563EB;
    display: block;
    margin-top: 1px;
  }}

  .badge-tag {{
    display: inline-block;
    background: #EFF6FF;
    color: #1D4ED8;
    border: 1px solid #BFDBFE;
    padding: 1px 6px;
    border-radius: 3px;
    font-size: 7.5pt;
    font-weight: 500;
    margin-top: 3px;
  }}

  .callout {{
    background-color: #F0F7FF;
    border-left: 4px solid #2563EB;
    padding: 12px 14px;
    border-radius: 0 8px 8px 0;
    margin: 12px 0 16px 0;
    font-size: 8.5pt;
    page-break-inside: avoid;
  }}

  .callout strong {{
    color: #1E40AF;
  }}

  .asset-box {{
    background: #0E1828;
    color: #E8EEF8;
    border: 1px solid #1E2D42;
    border-radius: 8px;
    padding: 14px 16px;
    margin: 10px 0 16px 0;
    page-break-inside: avoid;
  }}

  .asset-box-title {{
    font-family: 'Sora', sans-serif;
    color: #60A5FA;
    font-size: 9.5pt;
    font-weight: 700;
    margin-bottom: 6px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}

  .asset-content {{
    font-family: 'IBM Plex Mono', Consolas, monospace;
    font-size: 8pt;
    line-height: 1.45;
    white-space: pre-wrap;
    background: #070D17;
    padding: 10px 12px;
    border-radius: 6px;
    border: 1px solid #162438;
    color: #D1D5DB;
  }}

  .copy-text {{
    font-size: 8.5pt;
    line-height: 1.5;
    background: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 12px 14px;
    margin: 8px 0 14px 0;
    page-break-inside: avoid;
  }}

  .page-break {{
    page-break-before: auto;
    margin-top: 18px;
  }}

  .checklist {{
    list-style: none;
    padding-left: 0;
    margin: 8px 0;
  }}

  .checklist li {{
    padding: 4px 0;
    font-size: 8.5pt;
    display: flex;
    align-items: flex-start;
  }}

  .checklist li::before {{
    content: "☐";
    margin-right: 8px;
    color: #2563EB;
    font-size: 10pt;
    line-height: 1;
  }}

  .grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
  }}
</style>
</head>
<body>

  <!-- HEADER / COVER BANNER -->
  <div class="header-card">
    <div class="header-flex">
      {"<img class='logo-img' src='data:image/png;base64," + logo_b64 + "' alt='Appliedly' />" if logo_b64 else "<h1 style='color:#fff;margin:0;'>Appliedly</h1>"}
      <span class="header-badge">GTM Strategy & Production Assets</span>
    </div>
    <div class="doc-title">Marketing Directory & Production Materials Report</div>
    <div class="doc-subtitle">A curated registry of high-impact marketing launch sites, directory distribution channels, and production-ready promotional copy engineered for Appliedly.</div>
    
    <div class="meta-grid">
      <div class="meta-item">
        <strong>Product</strong>
        <span>Appliedly Web & Mobile</span>
      </div>
      <div class="meta-item">
        <strong>Brand Concept</strong>
        <span>Open Aperture #9</span>
      </div>
      <div class="meta-item">
        <strong>Core UVP</strong>
        <span>Calm Tracker + Exclusion AI</span>
      </div>
      <div class="meta-item">
        <strong>Date & Version</strong>
        <span>November 2026 • v1.0.0</span>
      </div>
    </div>
  </div>

  <!-- SECTION 1: EXECUTIVE POSITIONING SUMMARY -->
  <h2>1. Strategic Positioning & Core Value Proposition</h2>
  <p>Appliedly solves <strong>application fatigue and search chaos</strong> for intentional modern job seekers. While legacy platforms overwhelm users with noisy notifications and spreadsheets quickly degrade into unmanageable clutter, Appliedly provides a serene, structured application pipeline paired with high-precision AI recommendations.</p>

  <div class="grid-2">
    <div class="callout" style="margin-top:0;">
      <strong>The 3 Unfair Advantages to Market:</strong>
      <ul style="margin: 6px 0 0 16px; padding: 0;">
        <li><strong>Calm Pipeline Tracker:</strong> Clear status stages (Saved, Applied, Interviewing, Offer, Archive) with duration tracking and notes.</li>
        <li><strong>The Exclusion Contract:</strong> AI recommendations automatically filter out companies already in your active pipeline. Zero duplicates. Zero spam.</li>
        <li><strong>Tailored Market Intelligence:</strong> Curated recommendation inbox, market briefings, and bespoke cover letter guidance.</li>
      </ul>
    </div>
    <div class="callout" style="margin-top:0; border-left-color: #059669; background-color: #ECFDF5;">
      <strong style="color: #065F46;">Primary Target Audiences:</strong>
      <ul style="margin: 6px 0 0 16px; padding: 0;">
        <li><strong>Tech & Knowledge Workers:</strong> Developers, designers, and PMs tracking 20–100+ intentional applications.</li>
        <li><strong>Career Pivoters:</strong> Candidates targeting new industries who require tailored positioning and market briefings.</li>
        <li><strong>Spreadsheet Exhausted Applicants:</strong> Users struggling with brittle Notion templates and Excel formulas.</li>
      </ul>
    </div>
  </div>

  <!-- SECTION 2: DIRECTORY OF MARKETING SITES -->
  <h2>2. Master Directory: Where to Sign Up & Market Appliedly</h2>
  <p>The following platforms are segmented by tier and channel type. Each entry includes registration requirements, audience fit, and concrete action steps for the Appliedly launch.</p>

  <h3>Tier 1: High-Impact Product Launch & Startup Discovery Sites</h3>
  <table>
    <thead>
      <tr>
        <th style="width: 22%;">Platform & URL</th>
        <th style="width: 20%;">Audience & Reach</th>
        <th style="width: 25%;">Signup / Submission Details</th>
        <th style="width: 33%;">Appliedly Tactical Playbook</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>
          <span class="site-name">Product Hunt</span>
          <span class="site-url">producthunt.com</span>
          <span class="pill pill-tier1">Launchpad</span>
        </td>
        <td>Tech enthusiasts, early adopters, venture builders, founders (~5M/mo visits).</td>
        <td>Free personal account. Needs maker profile, logo (240x240), gallery images (1270x760), tagline (&lt;60 chars).</td>
        <td>Schedule launch for Tuesday 12:01 AM PT. Post maker comment explaining the "Exclusion Contract" philosophy. Engage comments within 15 minutes.</td>
      </tr>
      <tr>
        <td>
          <span class="site-name">BetaList</span>
          <span class="site-url">betalist.com</span>
          <span class="pill pill-tier1">Early Beta</span>
        </td>
        <td>Early adopters eager to test unreleased or newly launched consumer apps.</td>
        <td>Submit free (takes ~2-4 weeks queue) or expedited ($129-$299). Requires landing page with email waitlist/signup.</td>
        <td>Submit Appliedly web app highlighting "curated recommendation inbox". Drives 200–800 qualified early trial signups.</td>
      </tr>
      <tr>
        <td>
          <span class="site-name">Uneed Best</span>
          <span class="site-url">uneed.best</span>
          <span class="pill pill-tier1">Daily Leaderboard</span>
        </td>
        <td>Curated daily tool leaderboard popular among indie builders and productivity tool lovers.</td>
        <td>Simple form: tool name, clean screenshot, description, category (Productivity / Career). Free & paid boost.</td>
        <td>Compete for "Tool of the Day". Clean dark-mode screenshots from the Open Aperture brand library perform exceptionally well here.</td>
      </tr>
      <tr>
        <td>
          <span class="site-name">AlternativeTo</span>
          <span class="site-url">alternativeto.net</span>
          <span class="pill pill-tier1">High Intent Search</span>
        </td>
        <td>Users specifically searching to replace bloated, expensive, or abandoned tools.</td>
        <td>Free user account. Submit new software listing, specify platforms (Web, iOS, Android, PWA), add tags.</td>
        <td>Position Appliedly as the lightweight, modern alternative to <strong>Huntr, Teal, and Notion Job Tracking Templates</strong>. Generates perpetual high-intent organic traffic.</td>
      </tr>
      <tr>
        <td>
          <span class="site-name">SaaSHub</span>
          <span class="site-url">saashub.com</span>
          <span class="pill pill-tier1">SEO Directory</span>
        </td>
        <td>B2C & B2B software shoppers comparing pricing and features.</td>
        <td>Free software submission. Verifies domain ownership and meta descriptions.</td>
        <td>List under Job Search & Career Management. Generates authoritative backlink equity and automated comparison pages.</td>
      </tr>
    </tbody>
  </table>

  <div class="page-break"></div>

  <h3>Tier 2: AI & Productivity Aggregators (High SEO & Discovery Velocity)</h3>
  <table>
    <thead>
      <tr>
        <th style="width: 22%;">Platform & URL</th>
        <th style="width: 20%;">Audience & Reach</th>
        <th style="width: 25%;">Signup / Submission Details</th>
        <th style="width: 33%;">Appliedly Tactical Playbook</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>
          <span class="site-name">There's An AI For That</span>
          <span class="site-url">theresanaiforthat.com</span>
          <span class="pill pill-tier2">Top AI Portal</span>
        </td>
        <td>Over 4M+ monthly visits searching for task-specific AI solutions.</td>
        <td>Sign up, submit tool listing under "Job Search" / "Resume". Free queue (~2 weeks) or instant review pass.</td>
        <td>Highlight: <em>"AI Recommendation Inbox with Active Application Exclusion Contract"</em>. Ranks for queries like "AI job application tracker".</td>
      </tr>
      <tr>
        <td>
          <span class="site-name">Futurepedia</span>
          <span class="site-url">futurepedia.io</span>
          <span class="pill pill-tier2">AI Directory</span>
        </td>
        <td>Curated directory of legitimate AI-assisted software and workflows.</td>
        <td>Submit app via standard form. Verifies working demo, pricing model (Freemium/Free), and feature accuracy.</td>
        <td>Tag under Productivity, Career, and Job Search. Emphasize personalized job matching without spam auto-apply bots.</td>
      </tr>
      <tr>
        <td>
          <span class="site-name">Toolify.ai</span>
          <span class="site-url">toolify.ai</span>
          <span class="pill pill-tier2">High Volume</span>
        </td>
        <td>Massive global index of AI tools; ranks heavily on Google international search.</td>
        <td>Instant account creation via Google/GitHub. Fast approval cycle.</td>
        <td>Input Appliedly's key keywords: "Job tracker", "AI career assistant", "Application pipeline".</td>
      </tr>
      <tr>
        <td>
          <span class="site-name">MicroLaunch</span>
          <span class="site-url">microlaunch.net</span>
          <span class="pill pill-tier2">Indie Showcase</span>
        </td>
        <td>Active micro-SaaS and indie hacker community tracking fresh releases.</td>
        <td>Free profile creation. Monthly launch competition format.</td>
        <td>Run a monthly showcase post detailing our engineering progress and mobile app releases.</td>
      </tr>
    </tbody>
  </table>

  <h3>Tier 3: Communities for Organic & Value-First Seeding</h3>
  <table>
    <thead>
      <tr>
        <th style="width: 22%;">Platform & Channel</th>
        <th style="width: 20%;">Audience Dynamic</th>
        <th style="width: 25%;">Format & Policy</th>
        <th style="width: 33%;">Appliedly Tactical Playbook</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>
          <span class="site-name">Hacker News: Show HN</span>
          <span class="site-url">news.ycombinator.com</span>
          <span class="pill pill-tier3">Developer Core</span>
        </td>
        <td>Engineers, technical founders, and product designers. Highly skeptical of generic marketing.</td>
        <td>Post format must start with <code>Show HN: Appliedly – ...</code>. Plain text submission with URL.</td>
        <td>Position with complete technical transparency. Focus on user sovereignty, avoiding dark patterns, and eliminating spam recommendations.</td>
      </tr>
      <tr>
        <td>
          <span class="site-name">Reddit (r/jobs, r/resumes, r/cscareerquestions)</span>
          <span class="site-url">reddit.com</span>
          <span class="pill pill-tier3">Viral Communities</span>
        </td>
        <td>Active job hunters facing ghosting, fatigue, and disorganized application spreadsheets.</td>
        <td>Strict anti-self-promotion rules. Direct promotional links get banned. Value-first posting only.</td>
        <td>Share data-driven insights: "What tracking 100 applications taught me about follow-up timing". Offer Appliedly organically in comment replies.</td>
      </tr>
      <tr>
        <td>
          <span class="site-name">Peerlist</span>
          <span class="site-url">peerlist.io</span>
          <span class="pill pill-tier3">Modern Tech Network</span>
        </td>
        <td>Designers, developers, and product creators looking for work and showcasing portfolio apps.</td>
        <td>Create personal verified profile; submit to "Peerlist Spotlight" (Project of the Week).</td>
        <td>Appliedly is a natural fit for Peerlist members actively applying for roles. Run a Spotlight campaign with product demo clips.</td>
      </tr>
      <tr>
        <td>
          <span class="site-name">Indie Hackers</span>
          <span class="site-url">indiehackers.com</span>
          <span class="pill pill-tier3">Builder Network</span>
        </td>
        <td>Founders and solopreneurs exchanging growth strategies and launch metrics.</td>
        <td>Create product page under Products. Publish milestone posts and post-mortem launch reviews.</td>
        <td>Post weekly milestones: "From MVP to 100 active job seekers: what channels worked". Builds organic inbound trust.</td>
      </tr>
    </tbody>
  </table>

  <div class="page-break"></div>

  <!-- SECTION 3: GENERATED PRODUCTION MARKETING MATERIALS -->
  <h2>3. Ready-to-Deploy Production Marketing Materials</h2>
  <p>All assets below are custom-drafted according to Appliedly’s <em>Open Aperture</em> brand guidelines, emphasizing intentionality, calm organization, and the AI Exclusion Contract.</p>

  <h3>Material Pack A: Product Hunt Launch Suite</h3>
  
  <div class="asset-box">
    <div class="asset-box-title">
      <span>1. Product Hunt Listing Fields</span>
      <span class="pill pill-tier1">Ready to Copy</span>
    </div>
    <div class="asset-content">Product Name: Appliedly
Tagline: Track every application. Land the right role.
Category: Productivity, Career, Artificial Intelligence

Short Description (60 words):
Appliedly is the calm job application tracker designed for modern seekers. Replace cluttered spreadsheets with an organized visual pipeline, tailored market briefings, and an intelligent recommendation inbox that guarantees an "Exclusion Contract"—never recommending companies you’ve already applied to. Web and mobile ready.</div>
  </div>

  <div class="asset-box">
    <div class="asset-box-title">
      <span>2. First Maker Comment (By Founder / Lead Agent)</span>
      <span class="pill pill-tier1">Engage at Launch</span>
    </div>
    <div class="asset-content">Hey Product Hunt community! 👋

Like many of you, we watched the modern job search become an overwhelming numbers game. Between endless LinkedIn tabs, automated recruiter spam, and chaotic Excel spreadsheets that break after week three, candidates are suffering from severe application fatigue.

We built Appliedly to bring calm and control back to the job hunter:

1. 📂 A Calm Visual Pipeline: Clear application stages with duration tracking, status updates, and private notes.
2. 🎯 Curated Recommendation Inbox: High-signal job matches tailored to your profile rather than algorithmic noise.
3. 🔒 The Exclusion Contract: Our foundational rule—if a company is already in your active pipeline, Appliedly will NEVER recommend it again. No duplicate applications, no wasted hours.
4. 📱 Multi-Platform Flow: Built web-first, with native companion experiences for iOS and Android.

We’re live today and would love to hear your feedback on how we can make your job search more focused and less stressful. What’s your biggest frustration with tracking applications today?

— The Appliedly Team</div>
  </div>

  <h3>Material Pack B: Show HN Submission (Hacker News)</h3>
  <div class="copy-text">
    <strong>Post Title:</strong> <code>Show HN: Appliedly – A calm job application tracker with an exclusion contract</code><br><br>
    <strong>Submission Body:</strong><br>
    Hi HN,<br><br>
    Over the past year, the tech job market shifted from a targeted conversation into high-volume noise. Most job seekers we talked with were either maintaining fragile 40-column Google Sheets or getting spammed by "auto-apply" bots that spray generic resumes across the web.<br><br>
    We built <strong>Appliedly</strong> (https://appliedly.com) to solve this with a clean, calm workflow:<br><br>
    • <strong>Deterministic Pipeline:</strong> Stages for Saved, Applied, Interviewing, and Offers with time-in-stage metrics so you know when a lead has gone cold.<br>
    • <strong>Recommendation Inbox with an Exclusion Contract:</strong> Most job boards push jobs you've already applied to or rejected. Appliedly enforces a strict exclusion rule: your active application state is a barrier against recommendation duplicates.<br>
    • <strong>Tailored Market Briefings:</strong> Contextual role alignment and customized cover letter pointers generated directly against the target description.<br>
    • <strong>No Data Brokering:</strong> Your application data belongs to you. We don't sell candidate lists to recruiters.<br><br>
    We'd love HN's candid feedback on the UX, our data architecture, and what features you look for when organizing a multi-stage career search.
  </div>

  <div class="page-break"></div>

  <h3>Material Pack C: High-Conversion LinkedIn Content Engine</h3>

  <div class="asset-box">
    <div class="asset-box-title">
      <span>Post 1: The Founder Story / Problem Awareness (High Reach)</span>
      <span class="pill pill-tier3">LinkedIn</span>
    </div>
    <div class="asset-content">The modern job hunt is broken. Not because there aren't opportunities, but because the workflow is chaos.

Most job seekers are juggling:
❌ 32 open browser tabs
❌ A Google Sheet last updated 12 days ago
❌ Recruiter DMs asking for roles they applied to 3 weeks ago
❌ AI tools spamming 500 low-effort applications that end in instant rejections

High-volume spam isn't the answer. Intentional tracking is.

When you treat your job search like an intentional pipeline:
→ You know exactly which companies have had your resume for &gt;14 days
→ You prepare for interviews with structured notes in one place
→ You never accidentally re-apply to the same company with conflicting resumes

That's why we created Appliedly. A calm, focused application tracker and recommendation engine that respects your time.

If you're currently in the market, how are you organizing your pipeline? Drop your current setup below.

#JobSearch #CareerGrowth #TechJobs #Appliedly #Productivity</div>
  </div>

  <div class="asset-box">
    <div class="asset-box-title">
      <span>Post 2: Feature Spotlight — The "Exclusion Contract"</span>
      <span class="pill pill-tier3">LinkedIn</span>
    </div>
    <div class="asset-content">Ever notice how standard job boards keep recommending jobs at companies you applied to two weeks ago?

It’s one of the most frustrating time-wasters in a job search.

When designing Appliedly, we established one non-negotiable rule:
The "Exclusion Contract".

Here’s how it works:
1. When you add an application to your Appliedly pipeline, that company is tagged instantly.
2. Our recommendation inbox cross-references your active pipeline in real time.
3. Every recommendation you receive is guaranteed to be a company you haven’t already contacted.

Zero duplicates. Zero wasted clicks. Only fresh, high-signal matches.

Track every application. Land the right role.
Try Appliedly today on web and mobile: [Link in comments]

#JobHunt #CareerTips #SoftwareEngineering #Appliedly</div>
  </div>

  <h3>Material Pack D: X / Twitter Launch Thread (6-Part Hook Series)</h3>
  <div class="copy-text">
    <strong>Tweet 1 (The Hook):</strong><br>
    Applying to 100 jobs shouldn't feel like running a disorganized warehouse.<br><br>
    Spreadsheets break. Tabs get lost. Ghosting hurts.<br><br>
    Today, we're launching Appliedly: the calm job application tracker with an intelligent recommendation inbox. 🧵👇<br><br>
    <strong>Tweet 2:</strong><br>
    The biggest myth in tech right now? "Just auto-apply to 500 companies with AI bots."<br><br>
    Recruiters filter generic blasts instantly. The candidates who win are the ones who stay organized, tailor their follow-ups, and track time-in-stage.<br><br>
    <strong>Tweet 3:</strong><br>
    Here is what Appliedly looks like:<br>
    • A serene, distraction-free board (Saved → Applied → Interviewing → Offer)<br>
    • Time-in-stage duration tracking so you know when to follow up<br>
    • Private notes, salary expectations, and interview contact logs<br><br>
    <strong>Tweet 4:</strong><br>
    Our favorite feature: The Exclusion Contract.<br><br>
    Traditional platforms keep showing you jobs you already applied to.<br>
    Appliedly’s AI recommendation engine automatically filters out any company already in your pipeline. Zero spam matches.<br><br>
    <strong>Tweet 5:</strong><br>
    Built web-first with seamless native mobile experiences for iOS and Android. Your search stays in sync whether you're at your desk or walking into an interview.<br><br>
    <strong>Tweet 6 (CTA):</strong><br>
    Stop fighting messy sheets. Start tracking with clarity.<br><br>
    Check out Appliedly today: https://appliedly.com<br>
    We'd love your thoughts and feedback! ❤️
  </div>

  <div class="page-break"></div>

  <h3>Material Pack E: Short-Form Video Scripts (TikTok / Reels / YouTube Shorts)</h3>

  <div class="grid-2">
    <div class="asset-box">
      <div class="asset-box-title">
        <span>Script 1: "The Spreadsheet Reality Check"</span>
        <span class="pill pill-tier4">25 Secs</span>
      </div>
      <div class="asset-content"><strong>[0:00 - 0:05] HOOK:</strong>
(On camera: Person staring in horror at an Excel sheet with 50 colored columns and broken formulas)
"Tell me why nobody told me that job hunting in 2026 is actually just spreadsheet management?"

<strong>[0:05 - 0:15] PROBLEM:</strong>
(Cut to screen recording of tabs crashing, emails scattered)
"You lose track of who you applied to, you forget follow-ups, and you keep getting recommended the same job 5 times."

<strong>[0:15 - 0:22] SOLUTION:</strong>
(Cut to clean Appliedly UI showing smooth pipeline movement)
"Switch to Appliedly. It tracks every stage cleanly and has an exclusion rule so you never get recommended jobs you already applied to."

<strong>[0:22 - 0:25] CTA:</strong>
"Link in bio. Your sanity will thank you."</div>
    </div>

    <div class="asset-box">
      <div class="asset-box-title">
        <span>Script 2: "3 Job Tracker Green Flags"</span>
        <span class="pill pill-tier4">30 Secs</span>
      </div>
      <div class="asset-content"><strong>[0:00 - 0:06] HOOK:</strong>
"3 subtle things your job tracker MUST have if you want to actually get hired:"

<strong>[0:06 - 0:13] POINT 1:</strong>
"1. Time-in-stage tracking. If a company hasn't responded in 14 days, your tool should flag it so you can send a follow-up or move on."

<strong>[0:13 - 0:20] POINT 2:</strong>
"2. An exclusion filter. Why are you seeing recommendations for companies you already interviewed with?"

<strong>[0:20 - 0:26] POINT 3:</strong>
"3. Tailored cover letter briefs based on real job descriptions, not generic robotic gibberish."

<strong>[0:26 - 0:30] CTA:</strong>
"Appliedly does all three out of the box. Check the link in our bio."</div>
    </div>
  </div>

  <h3>Material Pack F: Direct Outreach Pitch (Career Coaches & Bootcamps)</h3>
  <div class="copy-text">
    <strong>Subject:</strong> A cleaner job application tracker for your [Cohort / Clients] (Appliedly)<br><br>
    Hi [First Name],<br><br>
    I’ve been following your advice on [specific topic, e.g., tech interview preparation / career transitions]—the tactical insights you share for job seekers are top-notch.<br><br>
    One recurring problem we noticed among candidates is <strong>application tracking breakdown</strong>: spreadsheets get abandoned after 20 entries, follow-ups are missed, and candidates waste hours re-applying to roles they’ve already submitted for.<br><br>
    We built <strong>Appliedly</strong> (https://appliedly.com) to solve this. It gives candidates a calm visual pipeline, duration alerts, and an intelligent recommendation inbox that enforces an "Exclusion Contract" (never recommending companies already in their active pipeline).<br><br>
    We'd love to offer your current [cohort / coaching clients] complimentary extended access to Appliedly to help them keep their pipelines organized and focused. Would you be open to a quick 5-minute walkthrough or preview link?<br><br>
    Best regards,<br>
    [Your Name]<br>
    Marketing Development | Appliedly
  </div>

  <!-- SECTION 4: 14-DAY LAUNCH EXECUTION CHECKLIST -->
  <h2>4. 14-Day Launch & Quality Review Checklist</h2>
  <div class="grid-2">
    <div>
      <h3 style="margin-top:0;">Week 1: Staging & Foundation</h3>
      <ul class="checklist">
        <li>Finalize Open Graph preview images (<code>og-1200x630.png</code>) and wordmark badges.</li>
        <li>Submit profile listings to <strong>AlternativeTo</strong> and <strong>SaaSHub</strong>.</li>
        <li>Submit Appliedly to <strong>BetaList</strong>, <strong>There's An AI For That</strong>, and <strong>Toolify.ai</strong>.</li>
        <li>Schedule Product Hunt launch date (target: Tuesday 12:01 AM PT).</li>
        <li>Prepare 3 high-resolution UI screen capture videos for social reels.</li>
      </ul>
    </div>
    <div>
      <h3 style="margin-top:0;">Week 2: Launch & Review Cadence</h3>
      <ul class="checklist">
        <li><strong>Day 0 (00:01 PT):</strong> Publish Product Hunt listing & First Maker Comment.</li>
        <li><strong>Day 0 (07:30 ET):</strong> Post <code>Show HN: Appliedly</code> on Hacker News.</li>
        <li><strong>Day 0 (09:00 ET):</strong> Deploy LinkedIn Founder Story & X/Twitter 6-tweet thread.</li>
        <li><strong>Day +1 to +3:</strong> Monitor HN/PH comments; answer every technical query in &lt;30m.</li>
        <li><strong>Day +7:</strong> Review conversion rates (Visits $\rightarrow$ Signups $\rightarrow$ Active Pipelines).</li>
      </ul>
    </div>
  </div>

</body>
</html>
"""

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML generated at: {HTML_PATH}")

# Compile with Edge headless
edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
file_uri = f"file:///{HTML_PATH.replace(os.sep, '/')}"

cmd = [
    edge_exe,
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={PDF_PATH}",
    file_uri
]

print("Compiling PDF with Microsoft Edge...")
result = subprocess.run(cmd, capture_output=True, text=True)
print(result.stdout)
print(result.stderr)

if os.path.exists(PDF_PATH):
    file_size = os.path.getsize(PDF_PATH)
    print(f"PDF successfully compiled! Size: {file_size} bytes ({round(file_size/1024, 1)} KB)")
    
    # Also copy to Artifact directory
    os.makedirs(ARTIFACT_DIR, exist_ok=True)
    shutil.copy2(PDF_PATH, ARTIFACT_PDF_PATH)
    print(f"Copied to artifact directory: {ARTIFACT_PDF_PATH}")
else:
    print("PDF compilation failed.")
