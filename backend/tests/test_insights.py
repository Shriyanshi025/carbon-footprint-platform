import pytest

from insights import (
    build_footprint_insight,
    get_impact_level,
)


@pytest.mark.parametrize(
    ("total_footprint", "expected_level"),
    [
        (0, "low"),
        (9.99, "low"),
        (10, "moderate"),
        (29.99, "moderate"),
        (30, "high"),
        (100, "high"),
    ],
)
def test_impact_level_boundaries(
    total_footprint,
    expected_level,
):
    assert get_impact_level(total_footprint) == expected_level


def test_insight_identifies_dominant_category():
    breakdown = {
        "transport": 6.0,
        "food": 2.0,
        "electricity": 1.0,
        "shopping": 1.0,
    }

    insight = build_footprint_insight(
        total_footprint=10.0,
        breakdown=breakdown,
    )

    assert insight["impact_level"] == "moderate"
    assert insight["dominant_category"] == "transport"
    assert insight["dominant_percentage"] == pytest.approx(60.0)
    assert "Transport contributes" in insight["message"]
    assert insight["target_reduction_percent"] == 10
    assert insight["potential_savings"] == pytest.approx(1.0)
    assert insight["target_footprint"] == pytest.approx(9.0)


def test_zero_footprint_returns_safe_insight():
    insight = build_footprint_insight(
        total_footprint=0,
        breakdown={
            "transport": 0,
            "food": 0,
            "electricity": 0,
            "shopping": 0,
        },
    )

    assert insight == {
        "impact_level": "low",
        "dominant_category": None,
        "dominant_percentage": 0,
        "message": (
            "No significant emissions were recorded for the "
            "provided activities."
        ),
        "target_reduction_percent": 0,
        "potential_savings": 0,
        "target_footprint": 0,
    }


def test_dominant_percentage_is_rounded():
    insight = build_footprint_insight(
        total_footprint=3.0,
        breakdown={
            "transport": 1.0,
            "food": 1.0,
            "electricity": 1.0,
            "shopping": 0.0,
        },
    )

    assert insight["dominant_percentage"] == pytest.approx(33.3)