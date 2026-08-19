"""Fetch basic app metadata from App Store or Google Play URLs."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from urllib.parse import parse_qs, urlparse

import requests


@dataclass
class AppInfo:
    name: str
    description: str
    category: str
    store: str
    store_url: str


def _clean_text(text: str, limit: int = 600) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rsplit(" ", 1)[0] + "..."


def _slug_from_app_store_url(store_url: str) -> str:
    parts = [part for part in urlparse(store_url).path.split("/") if part]
    for part in parts:
        if part in {"app", "us", "gb", "ca", "au"}:
            continue
        if re.fullmatch(r"id\d+", part):
            continue
        if re.search(r"[a-zA-Z]", part):
            return part.replace("-", " ").strip()
    return ""


def _search_app_store(term: str) -> dict | None:
    response = requests.get(
        "https://itunes.apple.com/search",
        params={"term": term, "entity": "software", "limit": 5},
        timeout=20,
    )
    response.raise_for_status()
    for result in response.json().get("results") or []:
        if result.get("wrapperType") == "software" and result.get("trackName"):
            return result
    return None


def _fetch_app_store(store_url: str, app_id: str) -> AppInfo:
    response = requests.get(
        "https://itunes.apple.com/lookup",
        params={"id": app_id},
        timeout=20,
    )
    response.raise_for_status()
    payload = response.json()
    results = payload.get("results") or []
    app = results[0] if results else None

    if not app or app.get("wrapperType") != "software":
        search_term = _slug_from_app_store_url(store_url) or app_id
        app = _search_app_store(search_term)
        if not app:
            raise ValueError(
                "App Store app not found. Use a direct app link like "
                "https://apps.apple.com/app/id1234567890"
            )

    return AppInfo(
        name=app.get("trackName") or "Your app",
        description=_clean_text(app.get("description") or ""),
        category=app.get("primaryGenreName") or "Productivity",
        store="App Store",
        store_url=store_url,
    )


def _fetch_microsoft_store(store_url: str, product_id: str) -> AppInfo:
    response = requests.get(
        f"https://displaycatalog.mp.microsoft.com/v7.0/products/{product_id}",
        params={"market": "US", "languages": "en-US", "moId": "Public"},
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=20,
    )
    response.raise_for_status()
    payload = response.json()
    product = payload.get("Product") or {}
    localized = (product.get("LocalizedProperties") or [{}])[0]

    description = _clean_text(
        localized.get("ProductDescription")
        or localized.get("ShortDescription")
        or ""
    )
    category = localized.get("ProductCategoryId") or "Productivity"

    return AppInfo(
        name=localized.get("ProductTitle") or "Your app",
        description=description,
        category=str(category).replace("_", " ").title(),
        store="Microsoft Store",
        store_url=store_url,
    )


def _fetch_play_store(store_url: str, package_id: str) -> AppInfo:
    response = requests.get(
        store_url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=20,
    )
    response.raise_for_status()
    html = response.text

    name_match = re.search(r'<meta property="og:title" content="([^"]+)"', html)
    desc_match = re.search(r'<meta property="og:description" content="([^"]+)"', html)
    category_match = re.search(r'"genre":"([^"]+)"', html)

    name = name_match.group(1) if name_match else package_id.split(".")[-1].replace("_", " ").title()
    if " - Apps on Google Play" in name:
        name = name.split(" - Apps on Google Play")[0].strip()

    return AppInfo(
        name=name or "Your app",
        description=_clean_text(desc_match.group(1) if desc_match else ""),
        category=category_match.group(1) if category_match else "Productivity",
        store="Google Play",
        store_url=store_url,
    )


def fetch_app_info(store_url: str) -> AppInfo:
    parsed = urlparse(store_url)
    host = parsed.netloc.lower()

    if "apps.apple.com" in host:
        match = re.search(r"/id(\d+)", parsed.path)
        if not match:
            raise ValueError("Could not parse App Store id from URL.")
        return _fetch_app_store(store_url, match.group(1))

    if "play.google.com" in host:
        query = parse_qs(parsed.query)
        package_id = (query.get("id") or [None])[0]
        if not package_id:
            raise ValueError("Could not parse Play Store package id from URL.")
        return _fetch_play_store(store_url, package_id)

    if "apps.microsoft.com" in host:
        match = re.search(r"/detail/([A-Za-z0-9]+)", parsed.path, re.IGNORECASE)
        if not match:
            raise ValueError("Could not parse Microsoft Store product id from URL.")
        return _fetch_microsoft_store(store_url, match.group(1))

    raise ValueError(
        "Unsupported store URL. Use App Store, Google Play, or Microsoft Store link."
    )


def save_app_info(app: AppInfo, path: str) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(app.__dict__, handle, indent=2)
