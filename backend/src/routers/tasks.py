"""Task API endpoints."""

from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, status

from src.database import SessionDep
from src.middleware.auth import CurrentUser, verify_user_access
from src.models.task import Priority, TaskCreate, TaskResponse, TaskUpdate
from src.services import tag_service
from src.services.recurring_service import create_next_occurrence
from src.services.task_service import TaskService

router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])


def _build_task_response(session, task) -> TaskResponse:
    """Build task response with tags."""
    tags = tag_service.get_task_tags(session, task.id)
    response = TaskResponse.model_validate(task)
    response.tags = [{"id": t.id, "name": t.name, "color": t.color} for t in tags]
    return response


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    user_id: str,
    session: SessionDep,
    current_user: CurrentUser,
    status_filter: str | None = Query(None, alias="status"),
    priority: Priority | None = None,
    tag: str | None = None,
    search: str | None = None,
    due_before: datetime | None = None,
    overdue: bool = False,
    sort: str = "created_at",
    order: str = "desc",
) -> list[TaskResponse]:
    """Get all tasks for a user with optional filters."""
    verify_user_access(user_id, current_user)
    service = TaskService(session)
    tasks = service.get_tasks(
        user_id,
        status=status_filter,
        priority=priority,
        tag=tag,
        search=search,
        due_before=due_before,
        overdue=overdue,
        sort=sort,
        order=order,
    )
    return [_build_task_response(session, task) for task in tasks]


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    user_id: str,
    data: TaskCreate,
    session: SessionDep,
    current_user: CurrentUser,
) -> TaskResponse:
    """Create a new task."""
    verify_user_access(user_id, current_user)
    service = TaskService(session)
    task = service.create_task(user_id, data)
    return _build_task_response(session, task)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    user_id: str,
    task_id: int,
    session: SessionDep,
    current_user: CurrentUser,
) -> TaskResponse:
    """Get a specific task by ID."""
    verify_user_access(user_id, current_user)
    service = TaskService(session)
    task = service.get_task(user_id, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return _build_task_response(session, task)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    user_id: str,
    task_id: int,
    data: TaskUpdate,
    session: SessionDep,
    current_user: CurrentUser,
) -> TaskResponse:
    """Update a task's title and/or description."""
    verify_user_access(user_id, current_user)
    service = TaskService(session)
    task = service.update_task(user_id, task_id, data)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return _build_task_response(session, task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    user_id: str,
    task_id: int,
    session: SessionDep,
    current_user: CurrentUser,
) -> None:
    """Delete a task."""
    verify_user_access(user_id, current_user)
    service = TaskService(session)
    if not service.delete_task(user_id, task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )


@router.patch("/{task_id}/complete", response_model=TaskResponse)
def toggle_complete(
    user_id: str,
    task_id: int,
    session: SessionDep,
    current_user: CurrentUser,
) -> TaskResponse:
    """Toggle a task's completion status."""
    verify_user_access(user_id, current_user)
    service = TaskService(session)
    task = service.toggle_complete(user_id, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # If task was completed and has recurrence rule, create next occurrence
    if task.completed and task.recurrence_rule:
        create_next_occurrence(session, task)

    return _build_task_response(session, task)
