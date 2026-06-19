
from typing import Literal
from pydantic import BaseModel, Field
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import google.genai as genai
import os
from dotenv import load_dotenv

load_dotenv()

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        frontend_url,
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

# Gemini AI configuration
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.get("/")
def read_root():
    return {"message": "Carbon Footprint API"}

class TransportData(BaseModel):
    distance: float = Field(
        ge=0,
        le=100000,
        description="Distance travelled in kilometres",
    )
    vehicle_type: Literal[
        "car",
        "bus",
        "train",
        "plane",
        "motorcycle",
    ]


class FoodData(BaseModel):
    food_type: Literal[
        "red_meat",
        "white_meat",
        "fish",
        "dairy",
        "vegan",
    ]
    consumption: float = Field(
        ge=0,
        le=10000,
        description="Food consumption in kilograms",
    )


class ElectricityData(BaseModel):
    kwh: float = Field(
        ge=0,
        le=1000000,
        description="Electricity consumption in kilowatt-hours",
    )


class ShoppingData(BaseModel):
    amount_spent: float = Field(
        ge=0,
        le=10000000,
        description="Amount spent",
    )
    category: Literal[
        "electronics",
        "clothing",
        "groceries",
        "other",
    ]


class FootprintRequest(BaseModel):
    transport: TransportData
    food: FoodData
    electricity: ElectricityData
    shopping: ShoppingData


class TipsRequest(BaseModel):
    footprint_data: dict

# Carbon footprint calculation logic
def calculate_transport_footprint(distance, vehicle_type):
    # Emission factors (kg CO2e per km)
    emission_factors = {
        "car": 0.17,
        "bus": 0.08,
        "train": 0.04,
        "plane": 0.25,
        "motorcycle": 0.1
    }
    return distance * emission_factors.get(vehicle_type, 0)

def calculate_food_footprint(food_type, consumption):
    # Emission factors (kg CO2e per kg)
    emission_factors = {
        "red_meat": 27,
        "white_meat": 7,
        "fish": 6,
        "dairy": 1,
        "vegan": 0.5
    }
    return consumption * emission_factors.get(food_type, 0)

def calculate_electricity_footprint(kwh):
    # Average emission factor (kg CO2e per kWh)
    emission_factor = 0.475
    return kwh * emission_factor

def calculate_shopping_footprint(amount_spent, category):
    # Emission factors (kg CO2e per dollar spent) - highly simplified
    emission_factors = {
        "electronics": 0.5,
        "clothing": 0.2,
        "groceries": 0.1,
        "other": 0.3
    }
    return amount_spent * emission_factors.get(category, 0)


@app.post("/calculate")
def calculate_footprint(data: FootprintRequest):
    transport_footprint = calculate_transport_footprint(
        data.transport.distance,
        data.transport.vehicle_type,
    )

    food_footprint = calculate_food_footprint(
        data.food.food_type,
        data.food.consumption,
    )

    electricity_footprint = calculate_electricity_footprint(
        data.electricity.kwh,
    )

    shopping_footprint = calculate_shopping_footprint(
        data.shopping.amount_spent,
        data.shopping.category,
    )

    breakdown = {
        "transport": round(transport_footprint, 3),
        "food": round(food_footprint, 3),
        "electricity": round(electricity_footprint, 3),
        "shopping": round(shopping_footprint, 3),
    }

    total_footprint = round(sum(breakdown.values()), 3)

    return {
        "total_footprint": total_footprint,
        "breakdown": breakdown,
    }

@app.post("/tips")
def get_tips(data: TipsRequest):
    footprint_data = data.footprint_data
    breakdown = footprint_data.get("breakdown", {})

    fallback_tips = []

    if breakdown:
        highest_category = max(breakdown, key=breakdown.get)

        category_tips = {
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

        fallback_tips.append(
            f"Your largest footprint source is {highest_category}. "
            f"{category_tips.get(highest_category, '')}"
        )

    fallback_tips.extend([
        "Track your activities regularly and set a small weekly carbon-reduction target.",
        "Choose reusable products and avoid unnecessary single-use packaging.",
    ])

    try:
        prompt = f"""
        Based on this carbon footprint information:
        {footprint_data}

        Give exactly 3 practical and personalized carbon reduction tips.
        Keep each tip short, specific, and easy to follow.
        """

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        return {
            "tips": response.text,
            "source": "gemini",
        }

    except Exception as error:
        print(f"Gemini tips unavailable: {error}")

        return {
            "tips": "\n\n".join(
                f"{index + 1}. {tip}"
                for index, tip in enumerate(fallback_tips[:3])
            ),
            "source": "fallback",
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
