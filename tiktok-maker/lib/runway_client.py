"""Thin Runway API client for image-to-video clip generation."""

from __future__ import annotations

import json
import mimetypes
import os
import sys
import time
from pathlib import Path

import requests

API_BASE = "https://api.dev.runwayml.com"
API_VERSION = "2024-11-06"


class RunwayError(RuntimeError):
    pass


def _headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "X-Runway-Version": API_VERSION,
        "Content-Type": "application/json",
    }


def get_api_key() -> str:
    key = os.environ.get("RUNWAYML_API_SECRET", "").strip()
    if not key:
        raise RunwayError(
            "RUNWAYML_API_SECRET is not set. Export it or copy tiktok-maker/.env.example."
        )
    return key


def upload_file(api_key: str, local_path: Path) -> str:
    response = requests.post(
        f"{API_BASE}/v1/uploads",
        headers=_headers(api_key),
        json={"filename": local_path.name, "type": "ephemeral"},
        timeout=30,
    )
    if not response.ok:
        raise RunwayError(f"Upload init failed: {response.status_code} {response.text[:300]}")

    data = response.json()
    upload_url = data.get("uploadUrl")
    fields = data.get("fields", {})
    runway_uri = data.get("runwayUri")
    if not upload_url or not runway_uri:
        raise RunwayError(f"Upload response missing fields: {json.dumps(data)}")

    mime_type = mimetypes.guess_type(str(local_path))[0] or "application/octet-stream"
    with local_path.open("rb") as handle:
        upload_response = requests.post(
            upload_url,
            data=fields,
            files={"file": (local_path.name, handle, mime_type)},
            timeout=120,
        )
    if not upload_response.ok:
        raise RunwayError(
            f"Upload failed: {upload_response.status_code} {upload_response.text[:300]}"
        )

    print(f"Uploaded {local_path.name} -> {runway_uri}", file=sys.stderr)
    return runway_uri


def _post(api_key: str, endpoint: str, body: dict) -> dict:
    response = requests.post(
        f"{API_BASE}{endpoint}",
        headers=_headers(api_key),
        json=body,
        timeout=30,
    )
    if not response.ok:
        raise RunwayError(f"API error {response.status_code}: {response.text[:500]}")
    return response.json()


def _get(api_key: str, path: str) -> dict:
    response = requests.get(f"{API_BASE}{path}", headers=_headers(api_key), timeout=30)
    if not response.ok:
        raise RunwayError(f"API error {response.status_code}: {response.text[:500]}")
    return response.json()


def poll_task(api_key: str, task_id: str, timeout: int = 900) -> dict:
    start = time.time()
    while time.time() - start < timeout:
        task = _get(api_key, f"/v1/tasks/{task_id}")
        status = task.get("status", "")
        if status == "SUCCEEDED":
            return task
        if status == "FAILED":
            raise RunwayError(f"Runway task failed: {task.get('failureCode')} {task.get('failure')}")
        if status == "CANCELLED":
            raise RunwayError("Runway task was cancelled.")
        print(f"[{task_id[:12]}] {status} ({int(time.time() - start)}s)", file=sys.stderr)
        time.sleep(5)
    raise RunwayError(f"Runway task timed out after {timeout}s")


def download_url(url: str, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(url, stream=True, timeout=120)
    response.raise_for_status()
    with output_path.open("wb") as handle:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                handle.write(chunk)
    return output_path


def generate_image_to_video(
    api_key: str,
    image_path: Path,
    prompt: str,
    output_path: Path,
    *,
    model: str = "gen4_turbo",
    ratio: str = "720:1280",
    duration: int = 5,
) -> Path:
    image_uri = upload_file(api_key, image_path)
    task = _post(
        api_key,
        "/v1/image_to_video",
        {
            "model": model,
            "promptImage": image_uri,
            "promptText": prompt,
            "ratio": ratio,
            "duration": duration,
        },
    )
    task_id = task["id"]
    print(f"Runway task created: {task_id}", file=sys.stderr)
    result = poll_task(api_key, task_id)
    urls = result.get("output") or []
    if not urls:
        raise RunwayError("Runway returned no output URLs.")
    return download_url(urls[0], output_path)


def generate_text_to_video(
    api_key: str,
    prompt: str,
    output_path: Path,
    *,
    model: str = "gen4.5",
    ratio: str = "720:1280",
    duration: int = 5,
) -> Path:
    task = _post(
        api_key,
        "/v1/text_to_video",
        {
            "model": model,
            "promptText": prompt,
            "ratio": ratio,
            "duration": duration,
        },
    )
    task_id = task["id"]
    print(f"Runway task created: {task_id}", file=sys.stderr)
    result = poll_task(api_key, task_id)
    urls = result.get("output") or []
    if not urls:
        raise RunwayError("Runway returned no output URLs.")
    return download_url(urls[0], output_path)
