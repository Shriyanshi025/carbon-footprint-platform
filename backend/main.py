
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import google.genai as genai
import os
from dotenv import load_dotenv

from calculations import (
    calculate_electricity_footprint,
    calculate_food_footprint,
    calculate_shopping_footprint,
    calculate_transport_footprint,
)

from models import FootprintRequest, TipsRequest

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
