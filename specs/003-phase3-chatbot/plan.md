# Implementation Plan: Phase III - AI-Powered Chatbot

**Branch**: `003-phase3-chatbot` | **Date**: 2026-02-07 | **Spec**: [spec.md](spec.md)

## Summary

Add a conversational AI interface to the todo application using OpenAI Agents SDK and MCP Server. Users can manage tasks through natural language in a chat interface built with OpenAI ChatKit.

## Technical Context

**AI/ML Stack**:
- OpenAI Agents SDK - Agent orchestration
- MCP SDK - Tool server implementation
- OpenAI API - GPT-4 for language understanding

**Backend Additions**:
- MCP Server with task tools
- Chat endpoint integrating Agents SDK
- Conversation/Message models

**Frontend**:
- OpenAI ChatKit integration
- Chat page with message history

## Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                         Frontend (Next.js)                          │
│  ┌──────────────────┐                                               │
│  │   ChatKit UI     │  ◄──────── OpenAI ChatKit Component           │
│  │   /chat page     │                                               │
│  └────────┬─────────┘                                               │
└───────────┼─────────────────────────────────────────────────────────┘
            │ POST /api/chat
            ▼
┌────────────────────────────────────────────────────────────────────┐
│                         Backend (FastAPI)                           │
│                                                                     │
│  ┌──────────────────┐    ┌───────────────────┐                     │
│  │  Chat Router     │───▶│  OpenAI Agents    │                     │
│  │  /api/chat       │    │  SDK Runner       │                     │
│  └──────────────────┘    └─────────┬─────────┘                     │
│                                    │                                │
│                          ┌─────────▼─────────┐                     │
│                          │    MCP Server     │                     │
│                          │  (Task Tools)     │                     │
│                          │  - add_task       │                     │
│                          │  - list_tasks     │                     │
│                          │  - complete_task  │                     │
│                          │  - delete_task    │                     │
│                          │  - update_task    │                     │
│                          └─────────┬─────────┘                     │
│                                    │                                │
│  ┌──────────────────┐    ┌─────────▼─────────┐                     │
│  │  Conversation    │◄───│   Task Service    │                     │
│  │  Service         │    │   (Phase II)      │                     │
│  └────────┬─────────┘    └───────────────────┘                     │
└───────────┼─────────────────────────────────────────────────────────┘
            │
            ▼
┌────────────────────────────────────────────────────────────────────┐
│                      Neon PostgreSQL                                │
│  ┌───────────┐  ┌───────────────┐  ┌──────────────┐                │
│  │   tasks   │  │ conversations │  │   messages   │                │
│  └───────────┘  └───────────────┘  └──────────────┘                │
└────────────────────────────────────────────────────────────────────┘
```

## Project Structure

```
backend/
├── src/
│   ├── main.py              # Add chat router
│   ├── models/
│   │   ├── task.py          # Existing
│   │   ├── conversation.py  # NEW: Conversation model
│   │   └── message.py       # NEW: Message model
│   ├── routers/
│   │   ├── tasks.py         # Existing
│   │   └── chat.py          # NEW: Chat endpoint
│   ├── services/
│   │   ├── task_service.py  # Existing
│   │   └── chat_service.py  # NEW: Conversation handling
│   └── mcp/                 # NEW: MCP Server
│       ├── __init__.py
│       ├── server.py        # MCP Server setup
│       └── tools.py         # Task tool definitions
├── tests/
│   ├── test_chat.py         # NEW: Chat tests
│   └── test_mcp_tools.py    # NEW: MCP tool tests

frontend/
├── src/
│   ├── app/
│   │   └── chat/            # NEW: Chat page
│   │       └── page.tsx
│   └── components/
│       └── ChatInterface.tsx # NEW: ChatKit wrapper
```

## Database Schema Additions

```sql
-- Conversations table
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);

-- Messages table
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
```

## MCP Tool Definitions

```python
# Tool schemas for MCP Server
TASK_TOOLS = [
    {
        "name": "add_task",
        "description": "Create a new task for the user",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Task title"},
                "description": {"type": "string", "description": "Optional task description"}
            },
            "required": ["title"]
        }
    },
    {
        "name": "list_tasks",
        "description": "Get all tasks for the user",
        "parameters": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["all", "pending", "completed"],
                    "description": "Filter by status"
                }
            }
        }
    },
    {
        "name": "complete_task",
        "description": "Mark a task as complete or incomplete",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "Task ID to toggle"}
            },
            "required": ["task_id"]
        }
    },
    {
        "name": "delete_task",
        "description": "Delete a task",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "Task ID to delete"}
            },
            "required": ["task_id"]
        }
    },
    {
        "name": "update_task",
        "description": "Update a task's title or description",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "Task ID to update"},
                "title": {"type": "string", "description": "New title"},
                "description": {"type": "string", "description": "New description"}
            },
            "required": ["task_id"]
        }
    }
]
```

## Agent System Prompt

```
You are a helpful task management assistant. You help users manage their todo list through natural conversation.

You have access to the following tools:
- add_task: Create a new task
- list_tasks: View tasks (can filter by status)
- complete_task: Mark a task as complete/incomplete
- delete_task: Remove a task
- update_task: Change a task's title or description

Guidelines:
1. Be conversational and friendly
2. Confirm actions after they're completed
3. When listing tasks, format them clearly with IDs
4. If a user's request is ambiguous, ask for clarification
5. For task references by name, try to match the closest task
6. Keep responses concise but helpful

Examples:
- User: "Add a task to buy milk" → Use add_task with title "Buy milk"
- User: "What do I need to do?" → Use list_tasks with status "pending"
- User: "I'm done with task 3" → Use complete_task with task_id 3
```

## Chat API Request/Response

### Request
```json
POST /api/chat
{
    "message": "Add a task to buy groceries",
    "conversation_id": null  // null for new conversation
}
```

### Response
```json
{
    "response": "I've added 'Buy groceries' to your task list. Is there anything else you'd like to add?",
    "conversation_id": 1,
    "message_id": 2
}
```

## Environment Variables

```bash
# Add to backend/.env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo-preview
```

## Dependencies

### Backend
```toml
# Add to pyproject.toml
"openai>=1.0.0"
"openai-agents-sdk>=0.1.0"  # Or actual package name
"mcp>=0.1.0"                # MCP SDK
```

### Frontend
```json
// Add to package.json
"@openai/chatkit": "^0.1.0"  // Or actual package name
```

## Implementation Order

1. **Database Models** - Conversation and Message entities
2. **MCP Server** - Tool definitions and handlers
3. **Chat Service** - Conversation management
4. **Agents Integration** - OpenAI Agents SDK setup
5. **Chat Router** - API endpoint
6. **Frontend Chat UI** - ChatKit integration
7. **Testing** - End-to-end chat flow

## Complexity Tracking

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| AI Provider | OpenAI | Hackathon requirement |
| Agent Framework | OpenAI Agents SDK | Hackathon requirement |
| Tool Protocol | MCP | Hackathon requirement |
| Chat UI | OpenAI ChatKit | Hackathon requirement |
| Conversation Storage | PostgreSQL | Reuse existing DB |
