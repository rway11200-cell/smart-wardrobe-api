from uuid import UUID

from fastapi import APIRouter, HTTPException, Path, status

from app.clothing import service
from app.clothing.schemas import (
    ClothingCategoryResponse,
    ClothingColorResponse,
    ClothingItemCreate,
    ClothingItemResponse,
    ClothingItemStatusUpdate,
    ClothingItemUpdate,
)

router = APIRouter(tags=["Clothing"])


def _handle_clothing_error(error: Exception):
    if isinstance(error, service.IdentityNotFoundError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Identity not found")
    if isinstance(error, service.ClothingCategoryNotFoundError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clothing category not found")
    if isinstance(error, service.ClothingItemNotFoundError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clothing item not found")
    if isinstance(error, service.InvalidClothingUpdateError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    raise error


@router.get("/clothing-categories", response_model=list[ClothingCategoryResponse])
def list_clothing_categories():
    return service.list_categories()


@router.get("/clothing-colors", response_model=list[ClothingColorResponse])
def list_clothing_colors():
    return service.list_colors()


@router.post(
    "/identities/{public_id}/clothing-items",
    response_model=ClothingItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_clothing_item(
    item: ClothingItemCreate,
    public_id: UUID = Path(..., examples=["11111111-1111-4111-8111-111111111111"]),
):
    try:
        return service.create_item(str(public_id), item)
    except Exception as error:
        _handle_clothing_error(error)


@router.get("/identities/{public_id}/clothing-items", response_model=list[ClothingItemResponse])
def list_clothing_items(
    public_id: UUID = Path(..., examples=["11111111-1111-4111-8111-111111111111"]),
):
    try:
        return service.list_items(str(public_id))
    except Exception as error:
        _handle_clothing_error(error)


@router.get("/identities/{public_id}/clothing-items/{item_id}", response_model=ClothingItemResponse)
def get_clothing_item(
    item_id: int = Path(..., ge=1, examples=[1]),
    public_id: UUID = Path(..., examples=["11111111-1111-4111-8111-111111111111"]),
):
    try:
        return service.get_item(str(public_id), item_id)
    except Exception as error:
        _handle_clothing_error(error)


@router.patch("/identities/{public_id}/clothing-items/{item_id}", response_model=ClothingItemResponse)
def update_clothing_item(
    item: ClothingItemUpdate,
    item_id: int = Path(..., ge=1, examples=[1]),
    public_id: UUID = Path(..., examples=["11111111-1111-4111-8111-111111111111"]),
):
    changes = item.model_dump(exclude_unset=True)

    if not changes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

    try:
        return service.update_item(str(public_id), item_id, changes)
    except Exception as error:
        _handle_clothing_error(error)


@router.patch("/identities/{public_id}/clothing-items/{item_id}/status", response_model=ClothingItemResponse)
def update_clothing_item_status(
    status_update: ClothingItemStatusUpdate,
    item_id: int = Path(..., ge=1, examples=[1]),
    public_id: UUID = Path(..., examples=["11111111-1111-4111-8111-111111111111"]),
):
    try:
        return service.update_item_status(str(public_id), item_id, status_update.current_status)
    except Exception as error:
        _handle_clothing_error(error)


@router.delete("/identities/{public_id}/clothing-items/{item_id}")
def delete_clothing_item(
    item_id: int = Path(..., ge=1, examples=[1]),
    public_id: UUID = Path(..., examples=["11111111-1111-4111-8111-111111111111"]),
):
    try:
        return service.delete_item(str(public_id), item_id)
    except Exception as error:
        _handle_clothing_error(error)
