from pydantic import BaseModel, ConfigDict, Field


class IdentityCreate(BaseModel):
    display_name: str = Field(min_length=1, max_length=100, examples=["Sebastian"])

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "display_name": "Sebastian",
            }
        }
    )


class IdentityProfileUpdate(BaseModel):
    cold_sensitivity: float | None = Field(default=None, ge=0, le=1, examples=[0.8])
    heat_sensitivity: float | None = Field(default=None, ge=0, le=1, examples=[0.4])
    comfort_priority: float | None = Field(default=None, ge=0, le=1, examples=[0.9])
    style_priority: float | None = Field(default=None, ge=0, le=1, examples=[0.6])

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "cold_sensitivity": 0.8,
                "heat_sensitivity": 0.4,
                "comfort_priority": 0.9,
                "style_priority": 0.6,
            }
        }
    )


class IdentityProfileResponse(BaseModel):
    cold_sensitivity: float = Field(examples=[0.5])
    heat_sensitivity: float = Field(examples=[0.5])
    comfort_priority: float = Field(examples=[0.5])
    style_priority: float = Field(examples=[0.5])


class IdentityResponse(BaseModel):
    public_id: str = Field(examples=["550e8400-e29b-41d4-a716-446655440000"])
    display_name: str = Field(examples=["Sebastian"])
    profile: IdentityProfileResponse
