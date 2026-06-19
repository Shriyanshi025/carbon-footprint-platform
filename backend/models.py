"""Request models used by the Carbon Footprint API."""

from typing import Literal

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
    