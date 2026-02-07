# CLI Interface Contract: Phase I - Console Todo App

**Date**: 2026-02-07
**Feature**: 001-phase1-console-app

## Overview

This document specifies the command-line interface for the Phase I Todo App. The app uses a menu-driven interface where users select numbered options.

---

## Main Menu

### Display Format

```
╔══════════════════════════════════╗
║         TODO APP - Phase I       ║
╠══════════════════════════════════╣
║  1. Add Task                     ║
║  2. View All Tasks               ║
║  3. Mark Task Complete/Incomplete║
║  4. Update Task                  ║
║  5. Delete Task                  ║
║  6. Exit                         ║
╚══════════════════════════════════╝

Enter your choice (1-6): 
```

### Menu Options

| Option | Action | Maps to FR |
|--------|--------|------------|
| 1 | Add new task | FR-001, FR-002 |
| 2 | View all tasks | FR-003 |
| 3 | Toggle task completion | FR-004 |
| 4 | Update task details | FR-005 |
| 5 | Delete task | FR-006 |
| 6 | Exit application | FR-010 |

---

## Command Flows

### 1. Add Task

**Input Flow**:
```
Enter your choice (1-6): 1

=== Add New Task ===
Enter task title: Buy groceries
Enter description (optional, press Enter to skip): Milk, eggs, bread

✓ Task created: #1 - Buy groceries
```

**Error Cases**:
```
Enter task title: 
✗ Error: Title is required

Enter task title: [500+ characters]
✗ Error: Title must be 500 characters or less
```

**Response Format**:
- Success: `✓ Task created: #{id} - {title}`
- Error: `✗ Error: {message}`

---

### 2. View All Tasks

**Output Format (with tasks)**:
```
Enter your choice (1-6): 2

=== Your Tasks ===

#1 [ ] Buy groceries
      Milk, eggs, bread

#2 [x] Call mom
      Wish her happy birthday

#3 [ ] Finish homework

────────────────────
Total: 3 tasks (1 completed, 2 pending)
```

**Output Format (empty)**:
```
Enter your choice (1-6): 2

=== Your Tasks ===

No tasks found. Add your first task!
```

**Display Elements**:
- `[ ]` = Pending task
- `[x]` = Completed task
- Description indented under title (if present)
- Summary line with counts

---

### 3. Mark Task Complete/Incomplete

**Input Flow**:
```
Enter your choice (1-6): 3

=== Toggle Task Completion ===
Enter task ID: 1

✓ Task #1 marked as completed
```

**Toggle Behavior**:
- If task is pending → mark as completed
- If task is completed → mark as pending (incomplete)

**Response Messages**:
- Pending → Completed: `✓ Task #{id} marked as completed`
- Completed → Pending: `✓ Task #{id} marked as pending`

**Error Cases**:
```
Enter task ID: 999
✗ Error: Task not found: #999

Enter task ID: abc
✗ Error: Invalid ID: please enter a number
```

---

### 4. Update Task

**Input Flow**:
```
Enter your choice (1-6): 4

=== Update Task ===
Enter task ID: 1

Current task: #1 - Buy grocries
Current description: Milk, eggs

Enter new title (press Enter to keep current): Buy groceries
Enter new description (press Enter to keep current): Milk, eggs, bread

✓ Task #1 updated successfully
```

**Behavior**:
- Empty input for title = keep current title
- Empty input for description = keep current description
- New title = update title
- New description = update description

**Error Cases**:
```
Enter task ID: 999
✗ Error: Task not found: #999

Enter new title: [empty when current is also empty - edge case]
# This is allowed - title remains unchanged
```

---

### 5. Delete Task

**Input Flow**:
```
Enter your choice (1-6): 5

=== Delete Task ===
Enter task ID: 1

Are you sure you want to delete "#1 - Buy groceries"? (y/n): y

✓ Task deleted: #1
```

**Confirmation**:
- `y` or `Y` = proceed with deletion
- `n`, `N`, or any other input = cancel deletion

**Cancellation**:
```
Are you sure you want to delete "#1 - Buy groceries"? (y/n): n

Deletion cancelled.
```

**Error Cases**:
```
Enter task ID: 999
✗ Error: Task not found: #999
```

---

### 6. Exit

**Output**:
```
Enter your choice (1-6): 6

Thank you for using Todo App. Goodbye!
```

**Behavior**:
- Display farewell message
- Exit application gracefully (exit code 0)

---

## Error Handling

### Standard Error Format

```
✗ Error: {specific error message}
```

### Error Messages

| Condition | Message |
|-----------|---------|
| Empty title | "Title is required" |
| Title too long | "Title must be 500 characters or less" |
| Task not found | "Task not found: #{id}" |
| Invalid ID format | "Invalid ID: please enter a number" |
| Invalid menu choice | "Invalid choice. Please enter 1-6." |

---

## Input Validation

### Menu Choice
- Accept: 1, 2, 3, 4, 5, 6
- Reject: Any other input
- Response: "Invalid choice. Please enter 1-6."

### Task ID
- Accept: Positive integers (1, 2, 3, ...)
- Reject: Non-numeric, zero, negative
- Response: "Invalid ID: please enter a number"

### Title
- Accept: 1-500 characters, any UTF-8 content
- Reject: Empty string, >500 characters
- Response: Appropriate validation message

### Description
- Accept: Any string including empty (optional field)
- No rejection cases

---

## Session Behavior

### Startup
```
╔══════════════════════════════════╗
║         TODO APP - Phase I       ║
║    Welcome! Your tasks await.    ║
╚══════════════════════════════════╝
```

### Loop
- After each operation, return to main menu
- Clear feedback after each action
- No screen clearing (preserve history for reference)

### Data Persistence
- All tasks lost on exit (in-memory only)
- No warning about data loss on exit (expected behavior)
