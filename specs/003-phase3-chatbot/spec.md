# Feature Specification: Phase III - AI-Powered Chatbot

**Feature Branch**: `003-phase3-chatbot`
**Created**: 2026-02-07
**Status**: Draft
**Points**: 200

## Overview

Transform the web application into an AI-powered conversational interface. Users interact with a chatbot to manage their tasks using natural language. The system uses OpenAI Agents SDK for AI logic and MCP (Model Context Protocol) Server to expose task tools.

## Architecture

```
┌─────────────────┐     ┌──────────────────────────────────┐     ┌─────────────┐
│  ChatKit UI     │────▶│  FastAPI Server                  │     │   Neon DB   │
│  (Frontend)     │     │  ├─ /api/chat endpoint           │     │  - tasks    │
│                 │◀────│  ├─ OpenAI Agents SDK            │◀───▶│  - convos   │
│                 │     │  └─ MCP Server (Task Tools)      │     │  - messages │
└─────────────────┘     └──────────────────────────────────┘     └─────────────┘
```

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Natural Language Task Creation (Priority: P1)

As a user, I want to create tasks by typing natural language so that I don't need to navigate forms.

**Why this priority**: Core chatbot functionality that replaces the form-based UI.

**Independent Test**: User types "Add a task to buy groceries" and a task titled "Buy groceries" is created.

**Acceptance Scenarios**:

1. **Given** I'm in the chat, **When** I type "Add a task to buy groceries", **Then** a task "Buy groceries" is created
2. **Given** I'm in the chat, **When** I type "Create task: Call mom at 5pm", **Then** a task with title "Call mom at 5pm" is created
3. **Given** I'm in the chat, **When** I type "Add task", **Then** the bot asks for task details
4. **Given** I create a task via chat, **When** I refresh the tasks page, **Then** I see the new task

---

### User Story 2 - View Tasks via Chat (Priority: P1)

As a user, I want to ask the chatbot to show my tasks so that I can see my todo list conversationally.

**Why this priority**: Essential for users to see their tasks through the chat interface.

**Independent Test**: User types "Show my tasks" and sees a formatted list of their tasks.

**Acceptance Scenarios**:

1. **Given** I have 3 tasks, **When** I ask "Show my tasks", **Then** I see all 3 tasks listed
2. **Given** I have no tasks, **When** I ask "What are my tasks?", **Then** the bot says I have no tasks
3. **Given** I have tasks, **When** I ask "Show pending tasks", **Then** I see only incomplete tasks
4. **Given** I have tasks, **When** I ask "Show completed tasks", **Then** I see only completed tasks

---

### User Story 3 - Complete Tasks via Chat (Priority: P1)

As a user, I want to mark tasks complete by telling the chatbot so that I can update status conversationally.

**Why this priority**: Core task management through natural language.

**Independent Test**: User types "Mark task 1 as complete" and the task is marked complete.

**Acceptance Scenarios**:

1. **Given** I have task #1, **When** I say "Complete task 1", **Then** task 1 is marked complete
2. **Given** I have task "Buy groceries", **When** I say "I finished buying groceries", **Then** that task is marked complete
3. **Given** task 1 is complete, **When** I say "Uncomplete task 1", **Then** it's marked incomplete
4. **Given** invalid task ID, **When** I say "Complete task 999", **Then** the bot says task not found

---

### User Story 4 - Delete Tasks via Chat (Priority: P2)

As a user, I want to delete tasks by telling the chatbot so that I can remove items conversationally.

**Why this priority**: Secondary but necessary functionality.

**Independent Test**: User types "Delete task 1" and the task is removed.

**Acceptance Scenarios**:

1. **Given** I have task #1, **When** I say "Delete task 1", **Then** task 1 is deleted
2. **Given** I say "Delete task 1", **When** the bot confirms, **Then** I can say "yes" to proceed
3. **Given** invalid task ID, **When** I say "Delete task 999", **Then** the bot says task not found

---

### User Story 5 - Update Tasks via Chat (Priority: P2)

As a user, I want to update task details via chat so that I can modify tasks conversationally.

**Why this priority**: Important for task management but less frequent.

**Independent Test**: User types "Rename task 1 to 'Updated title'" and the task title changes.

**Acceptance Scenarios**:

1. **Given** I have task #1, **When** I say "Rename task 1 to 'New title'", **Then** the title is updated
2. **Given** I have task #1, **When** I say "Add description to task 1: more details", **Then** description is added
3. **Given** invalid task ID, **When** I try to update task 999, **Then** the bot says task not found

---

### User Story 6 - Conversation Persistence (Priority: P1)

As a user, I want my chat history saved so that I can see previous conversations.

**Why this priority**: Essential for user experience and context continuity.

**Independent Test**: User has a conversation, refreshes the page, and sees the previous messages.

**Acceptance Scenarios**:

1. **Given** I sent messages, **When** I refresh, **Then** I see my previous messages
2. **Given** I'm a new user, **When** I open chat, **Then** I see a welcome message
3. **Given** I have multiple conversations, **When** I view history, **Then** I see all past messages

---

### Edge Cases

- What if user types gibberish? Bot responds with helpful guidance
- What if user asks non-task questions? Bot politely redirects to task management
- What if API call fails? Bot shows error and suggests retry
- What if user references task by name but multiple match? Bot asks for clarification
- What if session expires during chat? Redirect to login with message

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a chat endpoint that accepts natural language input
- **FR-002**: System MUST use OpenAI Agents SDK for processing user intent
- **FR-003**: System MUST expose task operations via MCP Server tools
- **FR-004**: System MUST persist conversations and messages in database
- **FR-005**: System MUST maintain user context across chat messages
- **FR-006**: System MUST integrate with existing Phase II task API
- **FR-007**: Frontend MUST use OpenAI ChatKit for the chat UI
- **FR-008**: System MUST handle task operations: add, list, complete, delete, update
- **FR-009**: Chat endpoint MUST be stateless (state persisted to DB)
- **FR-010**: System MUST provide clear, conversational responses

### MCP Tools Required

| Tool | Purpose | Parameters |
|------|---------|------------|
| add_task | Create a new task | user_id, title, description? |
| list_tasks | Get all tasks | user_id, status? (all/pending/completed) |
| get_task | Get task by ID | user_id, task_id |
| complete_task | Toggle completion | user_id, task_id |
| delete_task | Remove a task | user_id, task_id |
| update_task | Modify task | user_id, task_id, title?, description? |

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/chat | Process chat message and return response |
| GET | /api/conversations | List user's conversations |
| GET | /api/conversations/{id}/messages | Get messages in conversation |

### Key Entities

- **Conversation**: Chat session
  - `id`: Unique identifier
  - `user_id`: Owner
  - `created_at`: Start timestamp
  - `updated_at`: Last activity

- **Message**: Chat message
  - `id`: Unique identifier
  - `conversation_id`: Parent conversation
  - `role`: "user" | "assistant"
  - `content`: Message text
  - `created_at`: Timestamp

### Natural Language Examples

| User Says | Agent Action |
|-----------|--------------|
| "Add a task to buy groceries" | add_task(title="Buy groceries") |
| "Show me all my tasks" | list_tasks(status="all") |
| "What do I need to do?" | list_tasks(status="pending") |
| "Mark task 3 as complete" | complete_task(task_id=3) |
| "I finished buying groceries" | complete_task (by title match) |
| "Delete the grocery task" | delete_task (by title match) |
| "Rename task 1 to 'Call mom'" | update_task(task_id=1, title="Call mom") |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Chat response time under 3 seconds for 95% of requests
- **SC-002**: All 5 task operations work via natural language
- **SC-003**: Conversation history persists across page refreshes
- **SC-004**: Bot correctly interprets 90%+ of common task commands
- **SC-005**: Graceful error handling with helpful messages
- **SC-006**: Chat UI is responsive and mobile-friendly
- **SC-007**: MCP tools correctly map to existing task API
