"""Context-aware insights for calculated carbon footprints."""

CATEGORY_LABELS = {
    "transport": "Transport",
    "food": "Food",
    "electricity": "Electricity",
    "shopping": "Shopping",
}

CATEGORY_ACTIONS = {
    "transport": (
        "Prioritize public transport, carpooling, walking, or cycling "
        "for your regular journeys."
    ),
    "food": (
        "Start by replacing some high-emission meals with "
        "plant-based alternatives."
    ),
    "electricity": (
        "Reduce unnecessary electricity use and choose "
        "energy-efficient appliances."
    ),
    "shopping": (
        "Buy fewer, longer-lasting products and consider "
        "second-hand alternatives."
    ),
}

REDUCTION_TARGETS = {
        "low": 5,
        "moderate": 10,
        "high": 15,
    }

def get_impact_level(total_footprint: float) -> str:
    """Classify the calculated footprint into a simple awareness level."""

    if total_footprint < 10:
        return "low"

    if total_footprint < 30:
        return "moderate"

    return "high"


def build_footprint_insight(
    total_footprint: float,
    breakdown: dict[str, float],
) -> dict[str, object]:
    """Generate a contextual summary from the footprint breakdown."""

    if not breakdown or total_footprint <= 0:
        return {
            "impact_level": "low",
            "dominant_category": None,
            "dominant_percentage": 0,
            "target_reduction_percent": 0,
            "potential_savings": 0,
            "target_footprint": 0,
            "message": (
                "No significant emissions were recorded for the "
                "provided activities."
            ),
        }

    dominant_category = max(
        breakdown,
        key=breakdown.get,
    )

    dominant_value = breakdown[dominant_category]

    dominant_percentage = round(
        (dominant_value / total_footprint) * 100,
        1,
    )

    category_label = CATEGORY_LABELS.get(
        dominant_category,
        dominant_category.title(),
    )

    action = CATEGORY_ACTIONS.get(
        dominant_category,
        "Focus first on the activity producing the most emissions.",
    )

    impact_level = get_impact_level(total_footprint)

    target_reduction_percent = REDUCTION_TARGETS[
        impact_level
    ]

    potential_savings = round(
        total_footprint
        * target_reduction_percent
        / 100,
        3,
    )

    target_footprint = round(
        total_footprint - potential_savings,
        3,
    )

    return {
    "impact_level": impact_level,
    "dominant_category": dominant_category,
    "dominant_percentage": dominant_percentage,
    "target_reduction_percent": target_reduction_percent,
    "potential_savings": potential_savings,
    "target_footprint": target_footprint,
    "message": (
        f"{category_label} contributes approximately "
        f"{dominant_percentage}% of your footprint. {action}"
    ),
}