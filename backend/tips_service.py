"""Personalized carbon-reduction recommendation service."""
import json
import time
import logging
import os
from collections import OrderedDict
from typing import Any

import google.genai as genai


logger = logging.getLogger(__name__)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.0-flash",
)

CATEGORY_TIPS = {
    "transport": (
        "Use public transport, carpooling, cycling, or walking "
        "for short journeys to reduce transport emissions."
    ),
    "food": (
        "Reduce high-emission food consumption and include more "
        "plant-based meals in your weekly diet."
    ),
    "electricity": (
        "Switch off unused appliances, use LED bulbs, and prefer "
        "energy-efficient devices."
    ),
    "shopping": (
        "Buy durable products, reuse existing items, and prefer "
        "local or second-hand alternatives."
    ),
}

GENERAL_TIPS = [
    (
        "Track your activities regularly and set a small weekly "
        "carbon-reduction target."
    ),
    (
        "Choose reusable products and avoid unnecessary "
        "single-use packaging."
    ),
]

_client = None

CACHE_TTL_SECONDS = 600
MAX_CACHE_ENTRIES = 50

_tips_cache = OrderedDict()

def build_cache_key(
    footprint_data: dict[str, Any],
) -> str:
    """Create a stable key for equivalent footprint data."""

    return json.dumps(
        footprint_data,
        sort_keys=True,
        separators=(",", ":"),
    )


def get_cached_tips(
    cache_key: str,
) -> dict[str, str] | None:
    """Return a non-expired cached Gemini response."""

    cached_entry = _tips_cache.get(cache_key)

    if cached_entry is None:
        return None

    created_at, result = cached_entry

    if time.monotonic() - created_at > CACHE_TTL_SECONDS:
        del _tips_cache[cache_key]
        return None

    _tips_cache.move_to_end(cache_key)

    return result.copy()


def cache_tips(
    cache_key: str,
    result: dict[str, str],
) -> None:
    """Store a bounded Gemini response in memory."""

    _tips_cache[cache_key] = (
        time.monotonic(),
        result.copy(),
    )

    _tips_cache.move_to_end(cache_key)

    while len(_tips_cache) > MAX_CACHE_ENTRIES:
        _tips_cache.popitem(last=False)
        
        
def get_gemini_client():
    """Create and reuse a Gemini client only when recommendations are requested."""

    global _client

    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured")

        _client = genai.Client(api_key=api_key)

    return _client


def build_fallback_tips(
    footprint_data: dict[str, Any],
) -> list[str]:
    """Build deterministic recommendations from the emissions breakdown."""

    breakdown = footprint_data.get("breakdown", {})
    fallback_tips = []

    if breakdown:
        highest_category = max(
            breakdown,
            key=breakdown.get,
        )

        category_tip = CATEGORY_TIPS.get(
            highest_category,
            "",
        )

        fallback_tips.append(
            f"Your largest footprint source is {highest_category}. "
            f"{category_tip}"
        )

    fallback_tips.extend(GENERAL_TIPS)

    return fallback_tips[:3]


def build_gemini_prompt(
    footprint_data: dict[str, Any],
) -> str:
    """Create a concise prompt for personalized reduction advice."""

    return (
        "Based on this carbon footprint information:\n"
        f"{footprint_data}\n\n"
        "Give exactly 3 practical and personalized carbon reduction tips.\n"
        "Keep each tip short, specific, and easy to follow."
    )

def generate_reduction_tips(
    footprint_data: dict[str, Any],
) -> dict[str, str]:
    """Generate Gemini recommendations with deterministic fallback support."""

    cache_key = build_cache_key(footprint_data)
    cached_result = get_cached_tips(cache_key)

    if cached_result is not None:
        return cached_result

    fallback_tips = build_fallback_tips(footprint_data)

    try:
        client = get_gemini_client()

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=build_gemini_prompt(footprint_data),
        )

        response_text = getattr(response, "text", None)

        if not response_text:
            raise ValueError("Gemini returned an empty response")

        result = {
            "tips": response_text,
            "source": "gemini",
        }

        cache_tips(cache_key, result)

        return result

    except Exception as error:
        logger.warning(
            "Gemini tips unavailable; using fallback: %s",
            error,
        )

        return {
            "tips": "\n\n".join(
                f"{index + 1}. {tip}"
                for index, tip in enumerate(fallback_tips)
            ),
            "source": "fallback",
        }