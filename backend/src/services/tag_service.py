"""Tag service for CRUD operations."""

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from src.models.tag import Tag, TagCreate, TagUpdate, TaskTag


def create_tag(db: Session, user_id: str, tag_data: TagCreate) -> Tag:
    """Create a new tag for a user."""
    tag = Tag(user_id=user_id, name=tag_data.name, color=tag_data.color)
    db.add(tag)
    try:
        db.commit()
        db.refresh(tag)
        return tag
    except IntegrityError:
        db.rollback()
        raise ValueError(f"Tag '{tag_data.name}' already exists for this user")


def get_tags(db: Session, user_id: str) -> list[Tag]:
    """Get all tags for a user."""
    stmt = select(Tag).where(Tag.user_id == user_id).order_by(Tag.name)
    return list(db.exec(stmt).all())


def get_tag_by_id(db: Session, user_id: str, tag_id: int) -> Tag | None:
    """Get a specific tag by ID."""
    stmt = select(Tag).where(Tag.id == tag_id, Tag.user_id == user_id)
    return db.exec(stmt).first()


def get_tag_by_name(db: Session, user_id: str, name: str) -> Tag | None:
    """Get a tag by name."""
    stmt = select(Tag).where(Tag.user_id == user_id, Tag.name == name)
    return db.exec(stmt).first()


def update_tag(
    db: Session, user_id: str, tag_id: int, tag_data: TagUpdate
) -> Tag | None:
    """Update an existing tag."""
    tag = get_tag_by_id(db, user_id, tag_id)
    if not tag:
        return None

    update_data = tag_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(tag, key, value)

    try:
        db.commit()
        db.refresh(tag)
        return tag
    except IntegrityError:
        db.rollback()
        raise ValueError(f"Tag '{tag_data.name}' already exists for this user")


def delete_tag(db: Session, user_id: str, tag_id: int) -> bool:
    """Delete a tag and all its associations."""
    tag = get_tag_by_id(db, user_id, tag_id)
    if not tag:
        return False

    # Delete tag associations first
    stmt = select(TaskTag).where(TaskTag.tag_id == tag_id)
    associations = db.exec(stmt).all()
    for assoc in associations:
        db.delete(assoc)

    db.delete(tag)
    db.commit()
    return True


def add_tags_to_task(db: Session, task_id: int, tag_ids: list[int]) -> None:
    """Add tags to a task."""
    for tag_id in tag_ids:
        # Check if association already exists
        stmt = select(TaskTag).where(
            TaskTag.task_id == task_id, TaskTag.tag_id == tag_id
        )
        existing = db.exec(stmt).first()
        if not existing:
            task_tag = TaskTag(task_id=task_id, tag_id=tag_id)
            db.add(task_tag)
    db.commit()


def remove_tag_from_task(db: Session, task_id: int, tag_id: int) -> bool:
    """Remove a tag from a task."""
    stmt = select(TaskTag).where(TaskTag.task_id == task_id, TaskTag.tag_id == tag_id)
    task_tag = db.exec(stmt).first()
    if not task_tag:
        return False
    db.delete(task_tag)
    db.commit()
    return True


def get_task_tags(db: Session, task_id: int) -> list[Tag]:
    """Get all tags for a task."""
    stmt = (
        select(Tag)
        .join(TaskTag, Tag.id == TaskTag.tag_id)
        .where(TaskTag.task_id == task_id)
        .order_by(Tag.name)
    )
    return list(db.exec(stmt).all())


def get_or_create_tag(
    db: Session, user_id: str, name: str, color: str = "#6366f1"
) -> Tag:
    """Get existing tag or create new one."""
    tag = get_tag_by_name(db, user_id, name)
    if tag:
        return tag
    return create_tag(db, user_id, TagCreate(name=name, color=color))
