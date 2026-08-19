"""Generate a simple problem/solution TikTok script from app metadata."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass

from lib.store import AppInfo


@dataclass
class ScriptBeat:
    kind: str
    on_screen: str
    voiceover: str
    runway_prompt: str


@dataclass
class TikTokScript:
    hook: ScriptBeat
    problem: ScriptBeat
    solution: ScriptBeat
    demo: ScriptBeat
    cta: ScriptBeat

    def beats(self) -> list[ScriptBeat]:
        return [self.hook, self.problem, self.solution, self.demo, self.cta]


def _first_sentence(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    if not text:
        return ""
    parts = re.split(r"(?<=[.!?])\s+", text)
    return parts[0] if parts else text


def _problem_from_description(description: str, category: str) -> str:
    sentence = _first_sentence(description)
    if sentence:
        return sentence
    return f"Most {category.lower()} apps make simple tasks harder than they need to be."


def _benefit_from_description(description: str, app_name: str) -> str:
    sentence = _first_sentence(description)
    if sentence:
        return sentence
    return f"{app_name} keeps the workflow fast, clear, and easy to repeat."


def build_script(app: AppInfo) -> TikTokScript:
    problem = _problem_from_description(app.description, app.category)
    benefit = _benefit_from_description(app.description, app.name)

    return TikTokScript(
        hook=ScriptBeat(
            kind="hook",
            on_screen=f"Stop struggling with {app.category.lower()}",
            voiceover=f"If you keep hitting the same problem, this app might save you time.",
            runway_prompt=(
                f"Cinematic vertical phone UI ad, frustrated person scrolling on phone, "
                f"modern clean lighting, subtle camera push-in, no readable text"
            ),
        ),
        problem=ScriptBeat(
            kind="problem",
            on_screen=problem[:90],
            voiceover=problem,
            runway_prompt=(
                "Subtle slow zoom on a smartphone screen, soft natural motion, "
                "minimal UI blur, premium product demo style"
            ),
        ),
        solution=ScriptBeat(
            kind="solution",
            on_screen=f"{app.name} makes it simple",
            voiceover=benefit,
            runway_prompt=(
                "Smooth parallax motion over a clean mobile app screenshot, "
                "gentle camera drift, bright optimistic mood, no added text"
            ),
        ),
        demo=ScriptBeat(
            kind="demo",
            on_screen="Tap. Done. Repeat.",
            voiceover=f"Open {app.name}, do the task in seconds, and move on.",
            runway_prompt=(
                "Finger tap gesture on phone screen, smooth UI highlight motion, "
                "crisp product demo animation, vertical 9:16 framing"
            ),
        ),
        cta=ScriptBeat(
            kind="cta",
            on_screen=f"Get {app.name} on the {app.store}",
            voiceover=f"Search {app.name} on the {app.store} and try it today.",
            runway_prompt=(
                "Celebratory end card motion, phone in hand, app icon glow, "
                "clean minimalist background, vertical ad finish"
            ),
        ),
    )


def save_script(script: TikTokScript, path: str) -> None:
    payload = {beat.kind: asdict(beat) for beat in script.beats()}
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
