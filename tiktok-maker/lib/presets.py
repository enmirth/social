"""Built-in presets for Enmirth Microsoft Store apps."""

from __future__ import annotations

from dataclasses import dataclass

from lib.script import ScriptBeat, TikTokScript
from lib.store import AppInfo


@dataclass(frozen=True)
class AppPreset:
    key: str
    store_url: str
    app_name: str
    category: str
    problem: str
    tagline: str
    hook: str
    demo: str


PRESETS: dict[str, AppPreset] = {
    "work-time-tracker-pro": AppPreset(
        key="work-time-tracker-pro",
        store_url="https://apps.microsoft.com/detail/9nf1pz1mf2fk",
        app_name="Work Time Tracker Pro",
        category="Productivity",
        hook="Still guessing how long you worked?",
        problem="Most time trackers feel like extra work: accounts, ads, and messy spreadsheets.",
        tagline="One click to start/stop, add a note, and see week/month/year totals on your PC.",
        demo="Track a session, open reports, export CSV. Local, encrypted, no account.",
    ),
    "draft-pal": AppPreset(
        key="draft-pal",
        store_url="https://apps.microsoft.com/detail/9MSSMR2XSLTW",
        app_name="Draft Pal",
        category="Productivity",
        hook="Blank screen when you need to send a message?",
        problem="Even simple notes take forever when you start from zero every time.",
        tagline="Pick a ready-made draft, fill the blanks, and copy in about 20 seconds.",
        demo="Sick day, follow-up, thank-you, or work email. Preview, copy, share anywhere.",
    ),
}


def get_preset(name: str) -> AppPreset:
    preset = PRESETS.get(name)
    if not preset:
        available = ", ".join(sorted(PRESETS))
        raise ValueError(f"Unknown preset '{name}'. Available: {available}")
    return preset


def app_info_from_preset(preset: AppPreset) -> AppInfo:
    from lib.store import fetch_app_info

    app = fetch_app_info(preset.store_url)
    app.name = preset.app_name
    app.category = preset.category
    return app


def script_from_preset(preset: AppPreset, app: AppInfo) -> TikTokScript:
    return TikTokScript(
        hook=ScriptBeat(
            kind="hook",
            on_screen="Still guessing your work hours?",
            voiceover=preset.hook,
            runway_prompt=(
                "Cinematic vertical Windows desk scene, person frustrated at laptop, "
                "soft morning light, subtle camera push-in, no readable text"
            ),
        ),
        problem=ScriptBeat(
            kind="problem",
            on_screen="No accounts. No ads. Just track.",
            voiceover=preset.problem,
            runway_prompt=(
                "Slow zoom on a Windows laptop screen with blurred productivity UI, "
                "premium software ad style, gentle motion"
            ),
        ),
        solution=ScriptBeat(
            kind="solution",
            on_screen="One click. Notes. Reports.",
            voiceover=preset.tagline,
            runway_prompt=(
                "Smooth parallax over a clean Windows app screenshot, gentle camera drift, "
                "bright optimistic mood, no added text"
            ),
        ),
        demo=ScriptBeat(
            kind="demo",
            on_screen="Fast. Local. Done.",
            voiceover=preset.demo,
            runway_prompt=(
                "Mouse click on Windows app UI, smooth highlight motion, crisp product demo, "
                "vertical 9:16 framing"
            ),
        ),
        cta=ScriptBeat(
            kind="cta",
            on_screen="Work Time Tracker Pro",
            voiceover=f"Search {app.name} on the Microsoft Store for Windows.",
            runway_prompt=(
                "Celebratory end card, Windows laptop with app icon glow, "
                "clean minimalist background, vertical ad finish"
            ),
        ),
    )
