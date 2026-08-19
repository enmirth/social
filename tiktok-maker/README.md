# TikTok Maker (Runway)

Turn an app store link plus a folder of screenshots into a simple TikTok-ready vertical video.

You only provide:

- App Store or Google Play URL
- Screenshots (PNG/JPG/WEBP)

The tool handles:

1. Pulling app name/description from the store
2. Writing a problem → solution script
3. Generating short Runway clips
4. Stitching them into a 9:16 video with on-screen captions
5. Writing a suggested TikTok caption

## Setup

```bash
cd tiktok-maker
python3 -m pip install -r requirements.txt
export RUNWAYML_API_SECRET="your_key_from_dev.runwayml.com"
```

You also need `ffmpeg` installed locally.

## Enmirth apps (Microsoft Store)

Built-in presets for your two shipping apps:

| Preset | App | Store link |
| --- | --- | --- |
| `work-time-tracker-pro` | Work Time Tracker Pro | https://apps.microsoft.com/detail/9nf1pz1mf2fk |
| `draft-pal` | Draft Pal | https://apps.microsoft.com/detail/9MSSMR2XSLTW |

```bash
# Work Time Tracker Pro
python3 make_tiktok.py \
  --preset work-time-tracker-pro \
  --screenshots ./screenshots/work-time-tracker-pro \
  --output-dir ./out/work-time-tracker-pro \
  --dry-run

# Draft Pal
python3 make_tiktok.py \
  --preset draft-pal \
  --screenshots ./screenshots/draft-pal \
  --output-dir ./out/draft-pal \
  --dry-run
```

Copy screenshots from your Microsoft Store listing or from https://enmirth.com/software into each folder, then remove `--dry-run` to generate the Runway video.

## Quick start

```bash
mkdir screenshots
# copy 1-3 app screenshots into ./screenshots

python3 make_tiktok.py \
  --store-url "https://apps.apple.com/app/idYOUR_APP_ID" \
  --screenshots ./screenshots \
  --output-dir ./out
```

Preview the plan first (no Runway credits used):

```bash
python3 make_tiktok.py \
  --store-url "https://apps.apple.com/app/idYOUR_APP_ID" \
  --screenshots ./screenshots \
  --dry-run
```

## What gets generated

```
out/
  app.json              # fetched store metadata
  script.json           # hook/problem/solution/demo/cta beats
  raw_clips/            # individual Runway clips
  tiktok_final.mp4      # stitched 9:16 video
  tiktok_caption.txt    # paste into TikTok
  summary.json
```

## Cost estimate

Default settings generate 5 clips at 5 seconds each:

- Hook + CTA use text-to-video (`gen4.5`)
- Middle beats use image-to-video from your screenshots (`gen4_turbo`)

Roughly 50–75 Runway credits per full video depending on model pricing. Start with `--dry-run`, then generate one video and iterate on the script before scaling.

## Recommended workflow

1. Run with `--dry-run` and edit `out/script.json` if needed
2. Generate one video
3. Post manually on TikTok (or schedule with Metricool/Later)
4. Keep the hook/screenshot combo that gets the most profile clicks
5. Re-run with small script changes to A/B test

## Notes

- Runway output URLs expire quickly; the tool downloads clips locally.
- TikTok posting is not fully automatable via official API for most creators. This tool automates creation, not publishing.
- For best results, use clean screenshots with no personal data and a strong first screenshot for the "solution" beat.

## Example

```bash
python3 make_tiktok.py \
  --store-url "https://play.google.com/store/apps/details?id=com.notion.id" \
  --screenshots ./screenshots \
  --max-screenshots 3 \
  --clip-seconds 5 \
  --output-dir ./out/notion-demo
```

Then upload `out/notion-demo/tiktok_final.mp`4 to TikTok and paste text from `tiktok_caption.txt`.
