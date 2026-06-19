import pytest
from fastapi.testclient import TestClient

from main import (
    app,
    calculate_electricity_footprint,
    calculate_food_footprint,
    calculate_shopping_footprint,
    calculate_transport_footprint,
)

client = TestClient(app)


def test_transport_calculation():
    result = calculate_transport_footprint(10, "car")
    assert result == pytest.approx(1.7)


def test_food_calculation():
    result = calculate_food_footprint("vegan", 2)
    assert result == pytest.approx(1.0)


def test_electricity_calculation():
    result = calculate_electricity_footprint(10)
    assert result == pytest.approx(4.75)


def test_shopping_calculation():
    result = calculate_shopping_footprint(20, "clothing")
    assert result == pytest.approx(4.0)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Carbon Footprint API"
    }


def test_calculate_endpoint_with_valid_data():
    payload = {
        "transport": {
            "distance": 10,
            "vehicle_type": "car",
        },
        "food": {
            "food_type": "vegan",
            "consumption": 1,
        },
        "electricity": {
            "kwh": 5,
        },
        "shopping": {
            "amount_spent": 10,
            "category": "other",
        },
    }

    response = client.post("/calculate", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["total_footprint"] == 7.575
    assert data["breakdown"] == {
        "transport": 1.7,
        "food": 0.5,
        "electricity": 2.375,
        "shopping": 3.0,
    }
    assert data["insight"]["impact_level"] == "low"
    assert data["insight"]["dominant_category"] == "shopping"
    assert data["insight"]["dominant_percentage"] == pytest.approx(39.6)
    assert "Shopping contributes" in data["insight"]["message"]


def test_calculate_endpoint_rejects_negative_values():
    payload = {
        "transport": {
            "distance": -10,
            "vehicle_type": "car",
        },
        "food": {
            "food_type": "vegan",
            "consumption": 1,
        },
        "electricity": {
            "kwh": 5,
        },
        "shopping": {
            "amount_spent": 10,
            "category": "other",
        },
    }

    response = client.post("/calculate", json=payload)

    assert response.status_code == 422


def test_calculate_endpoint_rejects_invalid_vehicle():
    payload = {
        "transport": {
            "distance": 10,
            "vehicle_type": "spaceship",
        },
        "food": {
            "food_type": "vegan",
            "consumption": 1,
        },
        "electricity": {
            "kwh": 5,
        },
        "shopping": {
            "amount_spent": 10,
            "category": "other",
        },
    }

    response = client.post("/calculate", json=payload)

    assert response.status_code == 422