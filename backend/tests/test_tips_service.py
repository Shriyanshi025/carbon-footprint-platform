from fastapi.testclient import TestClient

import tips_service
from main import app
from tips_service import (
    build_fallback_tips,
    build_gemini_prompt,
    generate_reduction_tips,
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