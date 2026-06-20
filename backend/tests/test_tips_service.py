from fastapi.testclient import TestClient

import time
import tips_service
from main import app
from tips_service import (
    build_cache_key,
    build_fallback_tips,
    build_gemini_prompt,
    cache_tips,
    generate_reduction_tips,
    get_cached_tips,
)


client = TestClient(app)


SAMPLE_FOOTPRINT = {
    "total_footprint": 12.5,
    "breakdown": {
        "transport": 7.0,
        "food": 2.0,
        "electricity": 2.5,
        "shopping": 1.0,
    },
    "insight": {
        "impact_level": "moderate",
        "dominant_category": "transport",
        "dominant_percentage": 56.0,
        "target_reduction_percent": 10,
        "potential_savings": 1.25,
        "target_footprint": 11.25,
        "message": (
            "Transport contributes approximately 56.0% of your footprint. "
            "Prioritize public transport, carpooling, walking, or cycling."
        ),
    },
}


def test_fallback_tips_prioritize_highest_category():
    tips = build_fallback_tips(SAMPLE_FOOTPRINT)

    assert len(tips) == 3
    assert "largest footprint source is transport" in tips[0]
    assert "public transport" in tips[0]


def test_gemini_prompt_contains_user_context():
    prompt = build_gemini_prompt(SAMPLE_FOOTPRINT)

    assert "transport" in prompt
    assert "7.0" in prompt
    assert "exactly 3" in prompt


def test_missing_gemini_key_returns_fallback(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setattr(tips_service, "_client", None)

    result = generate_reduction_tips(SAMPLE_FOOTPRINT)

    assert result["source"] == "fallback"
    assert "transport" in result["tips"]
    assert result["tips"].count("\n\n") == 2


def test_tips_endpoint_returns_fallback_without_gemini_key(
    monkeypatch,
):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setattr(tips_service, "_client", None)

    response = client.post(
        "/tips",
        json={
            "footprint_data": SAMPLE_FOOTPRINT,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["source"] == "fallback"
    assert "tips" in data
    assert "transport" in data["tips"]


def test_cache_key_is_stable_for_same_data():
    reordered_footprint = {
        "insight": {
            "message": (
                "Transport contributes approximately 56.0% of your footprint. "
                "Prioritize public transport, carpooling, walking, or cycling."
            ),
            "target_footprint": 11.25,
            "potential_savings": 1.25,
            "target_reduction_percent": 10,
            "dominant_percentage": 56.0,
            "dominant_category": "transport",
            "impact_level": "moderate",
        },
        "breakdown": {
            "shopping": 1.0,
            "electricity": 2.5,
            "food": 2.0,
            "transport": 7.0,
        },
        "total_footprint": 12.5,
    }

    assert build_cache_key(SAMPLE_FOOTPRINT) == build_cache_key(
        reordered_footprint
    )


def test_cached_tips_are_returned_as_copy(monkeypatch):
    monkeypatch.setattr(tips_service, "_tips_cache", tips_service.OrderedDict())

    cache_key = build_cache_key(SAMPLE_FOOTPRINT)
    original_result = {
        "tips": "Cached recommendation",
        "source": "gemini",
    }

    cache_tips(cache_key, original_result)

    cached_result = get_cached_tips(cache_key)

    assert cached_result == original_result
    assert cached_result is not original_result


def test_expired_cache_entry_is_removed(monkeypatch):
    monkeypatch.setattr(tips_service, "_tips_cache", tips_service.OrderedDict())
    monkeypatch.setattr(tips_service, "CACHE_TTL_SECONDS", 1)

    cache_key = build_cache_key(SAMPLE_FOOTPRINT)

    tips_service._tips_cache[cache_key] = (
        time.monotonic() - 2,
        {
            "tips": "Expired recommendation",
            "source": "gemini",
        },
    )

    assert get_cached_tips(cache_key) is None
    assert cache_key not in tips_service._tips_cache


def test_repeated_request_uses_cached_gemini_response(monkeypatch):
    monkeypatch.setattr(tips_service, "_tips_cache", tips_service.OrderedDict())

    call_count = {"value": 0}

    class FakeResponse:
        text = "1. First tip\n2. Second tip\n3. Third tip"

    class FakeModels:
        def generate_content(self, **kwargs):
            call_count["value"] += 1
            return FakeResponse()

    class FakeClient:
        models = FakeModels()

    monkeypatch.setattr(
        tips_service,
        "get_gemini_client",
        lambda: FakeClient(),
    )

    first_result = generate_reduction_tips(SAMPLE_FOOTPRINT)
    second_result = generate_reduction_tips(SAMPLE_FOOTPRINT)

    assert first_result == second_result
    assert first_result["source"] == "gemini"
    assert call_count["value"] == 1


def test_tips_endpoint_rejects_invalid_footprint_structure():
    response = client.post(
        "/tips",
        json={
            "footprint_data": {
                "unexpected": "invalid",
            },
        },
    )

    assert response.status_code == 422