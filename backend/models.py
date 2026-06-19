"""Request models used by the Carbon Footprint API."""

from typing import Literal, Optional
from pydantic import BaseModel, Field

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


class FootprintBreakdown(BaseModel):
    transport: float = Field(ge=0)
    food: float = Field(ge=0)
    electricity: float = Field(ge=0)
    shopping: float = Field(ge=0)


class FootprintInsight(BaseModel):
    impact_level: Literal[
        "low",
        "moderate",
        "high",
    ]
    dominant_category: Optional[
        Literal[
            "transport",
            "food",
            "electricity",
            "shopping",
        ]
    ] = None
    dominant_percentage: float = Field(
        ge=0,
        le=100,
    )
    message: str = Field(
        min_length=1,
        max_length=500,
    )


class FootprintResponse(BaseModel):
    total_footprint: float = Field(ge=0)
    breakdown: FootprintBreakdown
    insight: FootprintInsight


class TipsResponse(BaseModel):
    tips: str = Field(
        min_length=1,
        max_length=5000,
    )
    source: Literal[
        "gemini",
        "fallback",
    ]