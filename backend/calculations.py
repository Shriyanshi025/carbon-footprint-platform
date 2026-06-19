"""Carbon-footprint calculation utilities."""

TRANSPORT_EMISSION_FACTORS = {
    "car": 0.17,
    "bus": 0.08,
    "train": 0.04,
    "plane": 0.25,
    "motorcycle": 0.1,
}

FOOD_EMISSION_FACTORS = {
    "red_meat": 27,
    "white_meat": 7,
    "fish": 6,
    "dairy": 1,
    "vegan": 0.5,
}

ELECTRICITY_EMISSION_FACTOR = 0.475

SHOPPING_EMISSION_FACTORS = {
    "electronics": 0.5,
    "clothing": 0.2,
    "groceries": 0.1,
    "other": 0.3,
}


def calculate_transport_footprint(
    distance: float,
    vehicle_type: str,
) -> float:
    """Calculate transport emissions in kilograms of CO2e."""

    return distance * TRANSPORT_EMISSION_FACTORS[vehicle_type]


def calculate_food_footprint(
    food_type: str,
    consumption: float,
) -> float:
    """Calculate food emissions in kilograms of CO2e."""

    return consumption * FOOD_EMISSION_FACTORS[food_type]


def calculate_electricity_footprint(kwh: float) -> float:
    """Calculate electricity emissions in kilograms of CO2e."""

    return kwh * ELECTRICITY_EMISSION_FACTOR


def calculate_shopping_footprint(
    amount_spent: float,
    category: str,
) -> float:
    """Calculate shopping emissions in kilograms of CO2e."""

    return amount_spent * SHOPPING_EMISSION_FACTORS[category]