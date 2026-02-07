"""Recurring task service for handling task recurrence patterns."""

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from sqlmodel import Session

from src.models.task import Task


@dataclass
class RecurrenceConfig:
    """Configuration for a recurrence pattern."""

    pattern: str  # DAILY, WEEKLY, MONTHLY, CUSTOM
    days: list[str] | None = None  # For WEEKLY: MON, TUE, etc.
    day_of_month: int | None = None  # For MONTHLY: 1-31
    interval: int = 1  # For CUSTOM: every N days


WEEKDAY_MAP = {
    "MON": 0,
    "TUE": 1,
    "WED": 2,
    "THU": 3,
    "FRI": 4,
    "SAT": 5,
    "SUN": 6,
}


def parse_recurrence_rule(rule: str) -> RecurrenceConfig | None:
    """Parse a recurrence rule string into configuration.

    Formats:
    - DAILY
    - WEEKLY:MON,WED,FRI
    - MONTHLY:15
    - CUSTOM:7 (every 7 days)
    """
    if not rule:
        return None

    rule = rule.upper().strip()

    if rule == "DAILY":
        return RecurrenceConfig(pattern="DAILY")

    if rule.startswith("WEEKLY:"):
        days_str = rule[7:]
        days = [d.strip() for d in days_str.split(",") if d.strip() in WEEKDAY_MAP]
        if days:
            return RecurrenceConfig(pattern="WEEKLY", days=days)
        return None

    if rule.startswith("MONTHLY:"):
        try:
            day = int(rule[8:])
            if 1 <= day <= 31:
                return RecurrenceConfig(pattern="MONTHLY", day_of_month=day)
        except ValueError:
            pass
        return None

    if rule.startswith("CUSTOM:"):
        try:
            interval = int(rule[7:])
            if interval > 0:
                return RecurrenceConfig(pattern="CUSTOM", interval=interval)
        except ValueError:
            pass
        return None

    return None


def calculate_next_occurrence(task: Task) -> datetime | None:
    """Calculate the next occurrence date based on task's recurrence rule."""
    if not task.recurrence_rule or not task.due_date:
        return None

    config = parse_recurrence_rule(task.recurrence_rule)
    if not config:
        return None

    base_date = task.due_date
    now = datetime.now(UTC)

    # Start from today if due date is in the past
    if base_date < now:
        base_date = now

    if config.pattern == "DAILY":
        return base_date + timedelta(days=1)

    if config.pattern == "WEEKLY" and config.days:
        # Find next matching weekday
        current_weekday = base_date.weekday()
        target_weekdays = sorted([WEEKDAY_MAP[d] for d in config.days])

        # Find next weekday after current
        for wd in target_weekdays:
            if wd > current_weekday:
                days_ahead = wd - current_weekday
                return base_date + timedelta(days=days_ahead)

        # Wrap to next week
        days_ahead = 7 - current_weekday + target_weekdays[0]
        return base_date + timedelta(days=days_ahead)

    if config.pattern == "MONTHLY" and config.day_of_month:
        # Move to next month
        year = base_date.year
        month = base_date.month + 1
        if month > 12:
            month = 1
            year += 1

        day = min(config.day_of_month, 28)  # Safe day to avoid month-end issues
        return base_date.replace(year=year, month=month, day=day)

    if config.pattern == "CUSTOM":
        return base_date + timedelta(days=config.interval)

    return None


def create_next_occurrence(db: Session, completed_task: Task) -> Task | None:
    """Create the next occurrence of a recurring task after completion."""
    if not completed_task.recurrence_rule:
        return None

    next_due = calculate_next_occurrence(completed_task)
    if not next_due:
        return None

    # Create new task with same properties
    new_task = Task(
        user_id=completed_task.user_id,
        title=completed_task.title,
        description=completed_task.description,
        priority=completed_task.priority,
        due_date=next_due,
        reminder_at=_calculate_next_reminder(completed_task, next_due),
        recurrence_rule=completed_task.recurrence_rule,
        parent_task_id=completed_task.id,
        completed=False,
        reminded=False,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def _calculate_next_reminder(task: Task, next_due: datetime) -> datetime | None:
    """Calculate reminder time for next occurrence based on original offset."""
    if not task.reminder_at or not task.due_date:
        return None

    # Calculate the offset between reminder and due date
    offset = task.due_date - task.reminder_at
    return next_due - offset
