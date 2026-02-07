# Tasks: Phase I - In-Memory Python Console Todo App

**Input**: Design documents from `/specs/001-phase1-console-app/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/cli-interface.md, research.md, quickstart.md

**Tests**: Included per Constitution Principle III (Test-First Development)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Create project structure and configure development environment

- [x] T001 Create project directory structure per plan.md (src/, tests/, src/models/, src/services/, src/cli/)
- [x] T002 Initialize Python project with pyproject.toml for UV package manager
- [x] T003 [P] Create src/__init__.py with package metadata
- [x] T004 [P] Create src/models/__init__.py
- [x] T005 [P] Create src/services/__init__.py
- [x] T006 [P] Create src/cli/__init__.py
- [x] T007 [P] Create tests/__init__.py
- [x] T008 [P] Create tests/unit/__init__.py
- [x] T009 [P] Create tests/integration/__init__.py
- [x] T010 [P] Configure pytest in pyproject.toml with test settings
- [x] T011 Create tests/conftest.py with shared fixtures for TaskService

**Checkpoint**: Project structure ready, pytest configured, UV environment set up

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T012 Create custom exceptions in src/exceptions.py (TaskNotFoundError, ValidationError)
- [x] T013 Create Task dataclass in src/models/task.py with fields: id, title, description, completed, created_at
- [x] T014 Create TaskService class skeleton in src/services/task_service.py with in-memory storage dict and next_id counter
- [x] T015 [P] Create output formatters in src/cli/formatters.py (format_task, format_task_list, format_error, format_success)
- [x] T016 Create menu display and input handling in src/cli/menu.py (display_menu, get_user_choice, get_task_id_input)
- [x] T017 Create main entry point in src/main.py with main loop skeleton and menu integration

**Checkpoint**: Foundation ready - Task model exists, TaskService skeleton in place, CLI menu displays

---

## Phase 3: User Story 1 - Add New Task (Priority: P1)

**Goal**: Users can add a new task with title and optional description

**Independent Test**: User launches app, adds task "Buy groceries" with description, sees confirmation with ID

### Tests for User Story 1

- [x] T018 [P] [US1] Create unit test for Task creation in tests/unit/test_task.py
- [x] T019 [P] [US1] Create unit test for TaskService.add_task() in tests/unit/test_task_service.py
- [x] T020 [P] [US1] Create unit test for title validation (empty, too long) in tests/unit/test_task_service.py

### Implementation for User Story 1

- [x] T021 [US1] Implement Task dataclass validation in src/models/task.py (title required, max 500 chars)
- [x] T022 [US1] Implement TaskService.add_task() method in src/services/task_service.py
- [x] T023 [US1] Implement add_task CLI handler in src/cli/menu.py (prompt for title, description)
- [x] T024 [US1] Wire add_task handler to main menu option 1 in src/main.py

**Checkpoint**: User Story 1 complete - users can add tasks via menu option 1

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Users can view all tasks with ID, title, description, and completion status

**Independent Test**: After adding 3 tasks, user selects view and sees formatted list with status indicators

### Tests for User Story 2

- [x] T025 [P] [US2] Create unit test for TaskService.list_tasks() in tests/unit/test_task_service.py
- [x] T026 [P] [US2] Create unit test for format_task_list() with tasks in tests/unit/test_formatters.py
- [x] T027 [P] [US2] Create unit test for format_task_list() with empty list in tests/unit/test_formatters.py

### Implementation for User Story 2

- [x] T028 [US2] Implement TaskService.list_tasks() method in src/services/task_service.py
- [x] T029 [US2] Implement format_task() for single task display in src/cli/formatters.py
- [x] T030 [US2] Implement format_task_list() with status counts in src/cli/formatters.py
- [x] T031 [US2] Implement view_tasks CLI handler in src/cli/menu.py
- [x] T032 [US2] Wire view_tasks handler to main menu option 2 in src/main.py

**Checkpoint**: User Stories 1 AND 2 complete - users can add and view tasks

---

## Phase 5: User Story 3 - Mark Task Complete/Incomplete (Priority: P2)

**Goal**: Users can toggle task completion status by ID

**Independent Test**: Add task, mark complete, verify status changes in task list

### Tests for User Story 3

- [x] T033 [P] [US3] Create unit test for TaskService.toggle_complete() in tests/unit/test_task_service.py
- [x] T034 [P] [US3] Create unit test for toggle on non-existent task (TaskNotFoundError) in tests/unit/test_task_service.py

### Implementation for User Story 3

- [x] T035 [US3] Implement TaskService.get_task() method in src/services/task_service.py
- [x] T036 [US3] Implement TaskService.toggle_complete() method in src/services/task_service.py
- [x] T037 [US3] Implement toggle_complete CLI handler in src/cli/menu.py
- [x] T038 [US3] Wire toggle_complete handler to main menu option 3 in src/main.py

**Checkpoint**: User Stories 1, 2, AND 3 complete - users can add, view, and complete tasks

---

## Phase 6: User Story 4 - Update Task (Priority: P2)

**Goal**: Users can update a task's title and/or description by ID

**Independent Test**: Add task with typo, update title, verify change in task list

### Tests for User Story 4

- [x] T039 [P] [US4] Create unit test for TaskService.update_task() in tests/unit/test_task_service.py
- [x] T040 [P] [US4] Create unit test for update with partial fields (only title, only description) in tests/unit/test_task_service.py
- [x] T041 [P] [US4] Create unit test for update on non-existent task in tests/unit/test_task_service.py

### Implementation for User Story 4

- [x] T042 [US4] Implement TaskService.update_task() method in src/services/task_service.py
- [x] T043 [US4] Implement update_task CLI handler in src/cli/menu.py (show current, prompt for new values)
- [x] T044 [US4] Wire update_task handler to main menu option 4 in src/main.py

**Checkpoint**: User Stories 1-4 complete - users can add, view, complete, and update tasks

---

## Phase 7: User Story 5 - Delete Task (Priority: P3)

**Goal**: Users can delete a task by ID with confirmation

**Independent Test**: Add task, delete with confirmation, verify no longer in list

### Tests for User Story 5

- [x] T045 [P] [US5] Create unit test for TaskService.delete_task() in tests/unit/test_task_service.py
- [x] T046 [P] [US5] Create unit test for delete on non-existent task in tests/unit/test_task_service.py

### Implementation for User Story 5

- [x] T047 [US5] Implement TaskService.delete_task() method in src/services/task_service.py
- [x] T048 [US5] Implement delete_task CLI handler with confirmation in src/cli/menu.py
- [x] T049 [US5] Wire delete_task handler to main menu option 5 in src/main.py

**Checkpoint**: All 5 user stories complete - full CRUD functionality implemented

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T050 [P] Implement exit handler for menu option 6 in src/main.py
- [x] T051 [P] Add input validation for menu choice (1-6 only) in src/cli/menu.py
- [x] T052 [P] Add input validation for task ID (positive integer) in src/cli/menu.py
- [x] T053 Create integration test for full workflow in tests/integration/test_cli_workflow.py
- [x] T054 [P] Add welcome banner on startup in src/main.py
- [x] T055 Run all tests and verify 100% pass rate
- [x] T056 Run quickstart.md validation (manual verification)

---

## Implementation Complete

**Status**: All 56 tasks completed
**Tests**: 49 tests passing (100%)
**Date**: 2026-02-07

---

## Task Summary

| Phase | Task Count | Stories | Status |
|-------|------------|---------|--------|
| Phase 1: Setup | 11 | - | COMPLETE |
| Phase 2: Foundational | 6 | - | COMPLETE |
| Phase 3: US1 Add | 7 | US1 | COMPLETE |
| Phase 4: US2 View | 8 | US2 | COMPLETE |
| Phase 5: US3 Complete | 6 | US3 | COMPLETE |
| Phase 6: US4 Update | 6 | US4 | COMPLETE |
| Phase 7: US5 Delete | 5 | US5 | COMPLETE |
| Phase 8: Polish | 7 | - | COMPLETE |
| **TOTAL** | **56** | **5** | **COMPLETE** |
