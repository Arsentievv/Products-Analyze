from fastapi import APIRouter, Body, Depends, HTTPException, status
from src.tracking import schemas
from src.tracking.services import ProductTrackService
from typing import Annotated
from src.tracking.dependencies import get_track_service
from src.products.exceptions import ProductNotFoundError
from src.users.exceptions import UserNotFoundError
from src.tracking.exceptions import ProductTrackNotFoundError


router = APIRouter(prefix="/tracks", tags=["tracks"])


@router.post(
    "/create",
    response_model=schemas.ProductTrackSchema,
    status_code=status.HTTP_201_CREATED,
    description="Создание отслеживания."
)
async def create_track(
        track_service: Annotated[ProductTrackService, Depends(get_track_service)],
        user_id: int = Body(),
        product_id: int = Body()
):
    try:
        track = await track_service.create_track(user_id, product_id)
        return track
    except UserNotFoundError as e:
        raise HTTPException(
            detail=e.detail,
            status_code=status.HTTP_404_NOT_FOUND
        )
    except ProductNotFoundError as e:
        raise HTTPException(
            detail=e.detail,
            status_code=status.HTTP_404_NOT_FOUND
        )


@router.get(
    "/ID/{track_id}",
    response_model=schemas.ProductTrackSchema,
    status_code=status.HTTP_200_OK,
    description="Получение отслеживания по ID."
)
async def get_track_by_id(
        track_service: Annotated[ProductTrackService, Depends(get_track_service)],
        track_id: int
):
    try:
        track = await track_service.get_track_by_id(track_id)
        return track
    except ProductTrackNotFoundError as e:
        raise HTTPException(
            detail=e.detail,
            status_code=status.HTTP_404_NOT_FOUND
        )


@router.get(
    "/all",
    response_model=list[schemas.ProductTrackSchema],
    status_code=status.HTTP_200_OK,
    description="Получение всех отслеживаний."
)
async def get_all_tracks(
        track_service: Annotated[ProductTrackService, Depends(get_track_service)]
):
    tracks = await track_service.get_all_tracks()
    return tracks


@router.delete(
    "/{track_id}/delete",
    status_code=status.HTTP_200_OK,
    description="Удалить отслеживание."
)
async def delete_track(
        track_service: Annotated[ProductTrackService, Depends(get_track_service)],
        track_id: int
):
    try:
        await track_service.delete_track(track_id)
        return {"status": f"ID {track_id} deleted"}
    except ProductTrackNotFoundError as e:
        raise HTTPException(
            detail=e.detail,
            status_code=status.HTTP_404_NOT_FOUND
        )