"""Task API endpoints."""

from fastapi import APIRouter, HTTPException, status

from src.database import SessionDep
from src.middleware.auth import CurrentUser, verify_user_access
from src.models.task import TaskCreate, TaskResponse, TaskUpdate
from src.services.task_service import TaskService

router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    user_id: str,
    session: SessionDep,
    current_user: CurrentUser,
) -> list[TaskResponse]:
    """Get all tasks for a user."""
    verify_user_access(user_id, current_user)
    service = TaskService(session)
    tasks = service.get_tasks(user_id)
    return [TaskResponse.model_validate(task) for task in tasks]


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
    return TaskResponse.model_validate(task)


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
    return TaskResponse.model_validate(task)


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
    return TaskResponse.model_validate(task)


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
    return TaskResponse.model_validate(task)
