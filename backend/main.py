
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from calculations import (
    calculate_electricity_footprint,
    calculate_food_footprint,
    calculate_shopping_footprint,
    calculate_transport_footprint,
)
from insights import build_footprint_insight
from models import (
    FootprintRequest,
    FootprintResponse,
    TipsRequest,
    TipsResponse,
)
from tips_service import generate_reduction_tips


load_dotenv()

frontend_url = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173",
)

app = FastAPI(
    title="Carbon Footprint Awareness API",
    description=(
        "API for calculating individual carbon footprints and generating "
        "personalized emission-reduction recommendations."
    ),
    version="2.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        frontend_url,
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.middleware("http")
async def add_security_headers(
    request: Request,
    call_next,
) -> Response:
    """Add defensive HTTP security headers to every API response."""

    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = (
        "camera=(), microphone=(), geolocation=()"
    )

    return response


@app.get("/")
def read_root() -> dict[str, str]:
    """Return a basic API health response."""

    return {
        "message": "Carbon Footprint API",
    }


@app.post(
    "/calculate",
    response_model=FootprintResponse,
)
def calculate_footprint(
    data: FootprintRequest,
) -> dict:
    """Calculate the user's carbon footprint and generate an insight."""

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

    total_footprint = round(
        sum(breakdown.values()),
        3,
    )

    insight = build_footprint_insight(
        total_footprint,
        breakdown,
    )

    return {
        "total_footprint": total_footprint,
        "breakdown": breakdown,
        "insight": insight,
    }


@app.post(
    "/tips",
    response_model=TipsResponse,
)
def get_tips(
    data: TipsRequest,
) -> dict:
    """Generate personalized carbon-reduction recommendations."""

    return generate_reduction_tips(
        data.footprint_data.model_dump(),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )
