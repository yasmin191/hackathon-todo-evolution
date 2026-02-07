"""Tag API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.database import get_session
from src.models.tag import TagCreate, TagResponse, TagUpdate, TaskTagsUpdate
from src.services import tag_service

router = APIRouter(prefix="/api", tags=["tags"])


@router.get("/{user_id}/tags", response_model=list[TagResponse])
def list_tags(user_id: str, db: Session = Depends(get_session)) -> list[TagResponse]:
    """Get all tags for a user."""
    tags = tag_service.get_tags(db, user_id)
    return [TagResponse.model_validate(t) for t in tags]


@router.post(
    "/{user_id}/tags", response_model=TagResponse, status_code=status.HTTP_201_CREATED
)
def create_tag(
    user_id: str, tag_data: TagCreate, db: Session = Depends(get_session)
) -> TagResponse:
    """Create a new tag."""
    try:
        tag = tag_service.create_tag(db, user_id, tag_data)
        return TagResponse.model_validate(tag)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}/tags/{tag_id}", response_model=TagResponse)
def get_tag(
    user_id: str, tag_id: int, db: Session = Depends(get_session)
) -> TagResponse:
    """Get a specific tag by ID."""
    tag = tag_service.get_tag_by_id(db, user_id, tag_id)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return TagResponse.model_validate(tag)


@router.put("/{user_id}/tags/{tag_id}", response_model=TagResponse)
def update_tag(
    user_id: str, tag_id: int, tag_data: TagUpdate, db: Session = Depends(get_session)
) -> TagResponse:
    """Update a tag."""
    try:
        tag = tag_service.update_tag(db, user_id, tag_id, tag_data)
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
            )
        return TagResponse.model_validate(tag)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{user_id}/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(user_id: str, tag_id: int, db: Session = Depends(get_session)) -> None:
    """Delete a tag."""
    if not tag_service.delete_tag(db, user_id, tag_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )


@router.post("/{user_id}/tasks/{task_id}/tags", status_code=status.HTTP_200_OK)
def add_tags_to_task(
    user_id: str,
    task_id: int,
    tag_data: TaskTagsUpdate,
    db: Session = Depends(get_session),
) -> dict:
    """Add tags to a task."""
    # Verify tags belong to user
    for tag_id in tag_data.tag_ids:
        tag = tag_service.get_tag_by_id(db, user_id, tag_id)
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Tag {tag_id} not found"
            )

    tag_service.add_tags_to_task(db, task_id, tag_data.tag_ids)
    return {"message": "Tags added successfully"}


@router.delete(
    "/{user_id}/tasks/{task_id}/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT
)
def remove_tag_from_task(
    user_id: str, task_id: int, tag_id: int, db: Session = Depends(get_session)
) -> None:
    """Remove a tag from a task."""
    if not tag_service.remove_tag_from_task(db, task_id, tag_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag association not found"
        )
