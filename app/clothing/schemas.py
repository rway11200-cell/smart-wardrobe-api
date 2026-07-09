from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ClothingStatus = Literal["clean", "worn", "laundry", "unavailable", "repair"]


class ClothingCategoryResponse(BaseModel):
    name: str
    layer_type: str
    required_for_outfit: bool
    display_order: int


class ClothingColorResponse(BaseModel):
    name: str
    hex_code: str | None = None
    display_order: int


class ClothingItemCreate(BaseModel):
    category_name: str = Field(min_length=1, max_length=80, examples=["top"])
    name: str = Field(min_length=1, max_length=120, examples=["Black hoodie"])
    color: str | None = Field(default=None, max_length=80, examples=["black"])
    material: str | None = Field(default=None, max_length=100, examples=["cotton"])
    image_url: str | None = Field(default=None, max_length=500, examples=["https://example.com/hoodie.jpg"])
    warmth_rating: float = Field(default=0.5, ge=0, le=1, examples=[0.75])
    comfort_rating: float = Field(default=0.5, ge=0, le=1, examples=[0.9])
    formality_rating: float = Field(default=0.5, ge=0, le=1, examples=[0.3])
    rain_rating: float = Field(default=0.0, ge=0, le=1, examples=[0.2])
    wind_rating: float = Field(default=0.0, ge=0, le=1, examples=[0.4])
    current_status: ClothingStatus = Field(default="clean", examples=["clean"])

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "category_name": "top",
                "name": "Black hoodie",
                "color": "black",
                "material": "cotton",
                "image_url": "https://example.com/hoodie.jpg",
                "warmth_rating": 0.75,
                "comfort_rating": 0.9,
                "formality_rating": 0.3,
                "rain_rating": 0.2,
                "wind_rating": 0.4,
                "current_status": "clean",
            }
        }
    )


class ClothingItemUpdate(BaseModel):
    category_name: str | None = Field(default=None, min_length=1, max_length=80, examples=["outerwear"])
    name: str | None = Field(default=None, min_length=1, max_length=120, examples=["Black hoodie"])
    color: str | None = Field(default=None, max_length=80, examples=["black"])
    material: str | None = Field(default=None, max_length=100, examples=["cotton"])
    image_url: str | None = Field(default=None, max_length=500, examples=["https://example.com/hoodie.jpg"])
    warmth_rating: float | None = Field(default=None, ge=0, le=1, examples=[0.75])
    comfort_rating: float | None = Field(default=None, ge=0, le=1, examples=[0.9])
    formality_rating: float | None = Field(default=None, ge=0, le=1, examples=[0.3])
    rain_rating: float | None = Field(default=None, ge=0, le=1, examples=[0.2])
    wind_rating: float | None = Field(default=None, ge=0, le=1, examples=[0.4])


class ClothingItemStatusUpdate(BaseModel):
    current_status: ClothingStatus = Field(examples=["laundry"])

    model_config = ConfigDict(json_schema_extra={"example": {"current_status": "laundry"}})


class ClothingItemResponse(BaseModel):
    id: int
    category_name: str
    name: str
    color: str | None = None
    material: str | None = None
    image_url: str | None = None
    warmth_rating: float
    comfort_rating: float
    formality_rating: float
    rain_rating: float
    wind_rating: float
    current_status: str
    is_active: bool
    last_worn_at: datetime | None = None
    created_at: datetime
    updated_at: datetime | None = None
