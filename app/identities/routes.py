from uuid import UUID

from fastapi import APIRouter, HTTPException, Path, status

from app.identities import service
from app.identities.api_schema import IdentityCreate, IdentityProfileUpdate, IdentityResponse

router = APIRouter(prefix="/identities", tags=["Identities"])


@router.post("", response_model=IdentityResponse, status_code=status.HTTP_201_CREATED)
def create_identity(identity: IdentityCreate):
    return service.create_identity(identity)


@router.get("/{public_id}", response_model=IdentityResponse)
def get_identity(public_id: UUID = Path(..., examples=["550e8400-e29b-41d4-a716-446655440000"])):
    try:
        return service.get_identity(str(public_id))
    except service.IdentityNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Identity not found")


@router.patch("/{public_id}/profile", response_model=IdentityResponse)
def update_identity_profile(
    profile: IdentityProfileUpdate,
    public_id: UUID = Path(..., examples=["550e8400-e29b-41d4-a716-446655440000"]),
):
    changes = profile.model_dump(exclude_unset=True)

    if not changes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

    try:
        return service.update_identity_profile(str(public_id), changes)
    except service.IdentityNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Identity not found")
