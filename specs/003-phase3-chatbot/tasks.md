# Tasks: Phase III - AI-Powered Chatbot

**Feature Branch**: `003-phase3-chatbot`
**Created**: 2026-02-07
**Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

---

## Phase Overview

Add AI-powered conversational interface using:
- OpenAI Agents SDK for AI orchestration
- MCP Server for task tool exposure
- OpenAI ChatKit for frontend chat UI
- Conversation persistence in PostgreSQL

**Total Tasks**: 32 | **Estimated Complexity**: High

---

## Epic 1: Database Models for Conversations

### Task 1.1: Create Conversation Model
**Priority**: P0 | **Type**: Implementation | **Depends on**: None

Create SQLModel for conversation entity.

**Acceptance Criteria**:
- [ ] Create `backend/src/models/conversation.py`
- [ ] Define Conversation with id, user_id, created_at, updated_at
- [ ] Add user_id index
- [ ] Export from models/__init__.py

**Test Cases**:
```
TC-1.1.1: Conversation model validates user_id required
TC-1.1.2: Conversation auto-generates timestamps
```

---

### Task 1.2: Create Message Model
**Priority**: P0 | **Type**: Implementation | **Depends on**: 1.1

Create SQLModel for message entity.

**Acceptance Criteria**:
- [ ] Create `backend/src/models/message.py`
- [ ] Define Message with id, conversation_id, role, content, created_at
- [ ] Add role enum validation (user, assistant)
- [ ] Add conversation_id foreign key and index
- [ ] Export from models/__init__.py

**Test Cases**:
```
TC-1.2.1: Message validates role is 'user' or 'assistant'
TC-1.2.2: Message validates content is required
TC-1.2.3: Message validates conversation_id exists
```

---

### Task 1.3: Create Database Migration
**Priority**: P0 | **Type**: Implementation | **Depends on**: 1.1, 1.2

Add Alembic migration for new tables.

**Acceptance Criteria**:
- [ ] Create migration for conversations table
- [ ] Create migration for messages table
- [ ] Add indexes and foreign keys
- [ ] Test migration up and down

**Test Cases**:
```
TC-1.3.1: Migration creates both tables
TC-1.3.2: Rollback removes tables cleanly
```

---

## Epic 2: MCP Server Implementation

### Task 2.1: Create MCP Server Structure
**Priority**: P0 | **Type**: Implementation | **Depends on**: None

Set up MCP Server module structure.

**Acceptance Criteria**:
- [ ] Create `backend/src/mcp/__init__.py`
- [ ] Create `backend/src/mcp/server.py` with server setup
- [ ] Create `backend/src/mcp/tools.py` for tool definitions
- [ ] Add MCP SDK dependency to pyproject.toml

**Test Cases**:
```
TC-2.1.1: MCP module imports without errors
TC-2.1.2: Server initializes correctly
```

---

### Task 2.2: Implement add_task Tool
**Priority**: P0 | **Type**: Implementation | **Depends on**: 2.1

Create MCP tool for adding tasks.

**Acceptance Criteria**:
- [ ] Define add_task tool with title and description parameters
- [ ] Implement handler that calls TaskService.create_task
- [ ] Return created task details in response
- [ ] Handle validation errors

**Test Cases**:
```
TC-2.2.1: add_task creates task with title only
TC-2.2.2: add_task creates task with title and description
TC-2.2.3: add_task rejects empty title
```

---

### Task 2.3: Implement list_tasks Tool
**Priority**: P0 | **Type**: Implementation | **Depends on**: 2.1

Create MCP tool for listing tasks.

**Acceptance Criteria**:
- [ ] Define list_tasks tool with optional status filter
- [ ] Implement handler that calls TaskService.get_tasks
- [ ] Filter by status (all, pending, completed)
- [ ] Return formatted task list

**Test Cases**:
```
TC-2.3.1: list_tasks returns all tasks
TC-2.3.2: list_tasks with status="pending" filters correctly
TC-2.3.3: list_tasks with status="completed" filters correctly
TC-2.3.4: list_tasks returns empty list message when no tasks
```

---

### Task 2.4: Implement complete_task Tool
**Priority**: P0 | **Type**: Implementation | **Depends on**: 2.1

Create MCP tool for toggling task completion.

**Acceptance Criteria**:
- [ ] Define complete_task tool with task_id parameter
- [ ] Implement handler that calls TaskService.toggle_complete
- [ ] Return updated task status
- [ ] Handle task not found error

**Test Cases**:
```
TC-2.4.1: complete_task toggles pending to completed
TC-2.4.2: complete_task toggles completed to pending
TC-2.4.3: complete_task returns error for invalid ID
```

---

### Task 2.5: Implement delete_task Tool
**Priority**: P1 | **Type**: Implementation | **Depends on**: 2.1

Create MCP tool for deleting tasks.

**Acceptance Criteria**:
- [ ] Define delete_task tool with task_id parameter
- [ ] Implement handler that calls TaskService.delete_task
- [ ] Return success confirmation
- [ ] Handle task not found error

**Test Cases**:
```
TC-2.5.1: delete_task removes existing task
TC-2.5.2: delete_task returns error for invalid ID
```

---

### Task 2.6: Implement update_task Tool
**Priority**: P1 | **Type**: Implementation | **Depends on**: 2.1

Create MCP tool for updating tasks.

**Acceptance Criteria**:
- [ ] Define update_task tool with task_id, title, description parameters
- [ ] Implement handler that calls TaskService.update_task
- [ ] Support partial updates
- [ ] Handle task not found error

**Test Cases**:
```
TC-2.6.1: update_task updates title only
TC-2.6.2: update_task updates description only
TC-2.6.3: update_task updates both fields
TC-2.6.4: update_task returns error for invalid ID
```

---

### Task 2.7: Create MCP Tool Tests
**Priority**: P1 | **Type**: Test | **Depends on**: 2.2-2.6

Comprehensive tests for all MCP tools.

**Acceptance Criteria**:
- [ ] Create `backend/tests/test_mcp_tools.py`
- [ ] Test each tool with valid inputs
- [ ] Test error handling for each tool
- [ ] Test user isolation

**Test Cases**:
```
TC-2.7.1: All tools work with valid inputs
TC-2.7.2: All tools handle errors gracefully
TC-2.7.3: Tools respect user isolation
```

---

## Epic 3: OpenAI Agents SDK Integration

### Task 3.1: Add OpenAI Dependencies
**Priority**: P0 | **Type**: Setup | **Depends on**: None

Add OpenAI packages to backend.

**Acceptance Criteria**:
- [ ] Add openai to pyproject.toml
- [ ] Add openai-agents (or agents-sdk) package
- [ ] Add OPENAI_API_KEY to config
- [ ] Add OPENAI_MODEL to config (default: gpt-4-turbo)

**Test Cases**:
```
TC-3.1.1: Dependencies install without errors
TC-3.1.2: Config loads API key from environment
```

---

### Task 3.2: Create Agent Configuration
**Priority**: P0 | **Type**: Implementation | **Depends on**: 3.1, 2.1

Configure OpenAI Agent with system prompt and tools.

**Acceptance Criteria**:
- [ ] Create `backend/src/agents/__init__.py`
- [ ] Create `backend/src/agents/task_agent.py`
- [ ] Define system prompt for task management
- [ ] Register MCP tools with agent
- [ ] Configure model and parameters

**Test Cases**:
```
TC-3.2.1: Agent initializes with correct prompt
TC-3.2.2: Agent has access to all MCP tools
```

---

### Task 3.3: Implement Agent Runner
**Priority**: P0 | **Type**: Implementation | **Depends on**: 3.2

Create service to run agent with user messages.

**Acceptance Criteria**:
- [ ] Create agent runner function
- [ ] Accept user message and conversation context
- [ ] Execute agent with tools
- [ ] Return agent response
- [ ] Handle API errors gracefully

**Test Cases**:
```
TC-3.3.1: Runner processes simple message
TC-3.3.2: Runner handles tool calls
TC-3.3.3: Runner handles API errors
```

---

## Epic 4: Chat Service and API

### Task 4.1: Create Conversation Service
**Priority**: P0 | **Type**: Implementation | **Depends on**: 1.1, 1.2

Implement conversation management.

**Acceptance Criteria**:
- [ ] Create `backend/src/services/conversation_service.py`
- [ ] Implement create_conversation(user_id)
- [ ] Implement get_conversation(user_id, conversation_id)
- [ ] Implement get_conversations(user_id)
- [ ] Implement add_message(conversation_id, role, content)
- [ ] Implement get_messages(conversation_id)

**Test Cases**:
```
TC-4.1.1: create_conversation returns new conversation
TC-4.1.2: get_conversation returns existing conversation
TC-4.1.3: get_conversations returns user's conversations only
TC-4.1.4: add_message creates message in conversation
TC-4.1.5: get_messages returns messages in order
```

---

### Task 4.2: Create Chat Router
**Priority**: P0 | **Type**: Implementation | **Depends on**: 3.3, 4.1

Implement chat API endpoint.

**Acceptance Criteria**:
- [ ] Create `backend/src/routers/chat.py`
- [ ] Implement POST /api/chat endpoint
- [ ] Accept message and optional conversation_id
- [ ] Create new conversation if needed
- [ ] Save user message to database
- [ ] Run agent and get response
- [ ] Save assistant message to database
- [ ] Return response with conversation_id

**Test Cases**:
```
TC-4.2.1: New chat creates conversation
TC-4.2.2: Existing conversation_id reuses conversation
TC-4.2.3: Messages are persisted to database
TC-4.2.4: Response includes conversation_id
```

---

### Task 4.3: Create Conversations List Endpoint
**Priority**: P1 | **Type**: Implementation | **Depends on**: 4.1

Implement conversation history endpoint.

**Acceptance Criteria**:
- [ ] Implement GET /api/conversations
- [ ] Return user's conversations
- [ ] Include message count and last message preview
- [ ] Order by updated_at descending

**Test Cases**:
```
TC-4.3.1: Returns user's conversations only
TC-4.3.2: Includes conversation metadata
TC-4.3.3: Orders by most recent first
```

---

### Task 4.4: Create Messages Endpoint
**Priority**: P1 | **Type**: Implementation | **Depends on**: 4.1

Implement message history endpoint.

**Acceptance Criteria**:
- [ ] Implement GET /api/conversations/{id}/messages
- [ ] Return all messages in conversation
- [ ] Verify user owns conversation
- [ ] Order by created_at ascending

**Test Cases**:
```
TC-4.4.1: Returns messages for owned conversation
TC-4.4.2: Returns 404 for other user's conversation
TC-4.4.3: Messages in chronological order
```

---

### Task 4.5: Register Chat Router
**Priority**: P0 | **Type**: Implementation | **Depends on**: 4.2

Wire up chat router in main app.

**Acceptance Criteria**:
- [ ] Import chat router in main.py
- [ ] Include router with appropriate prefix
- [ ] Add to OpenAPI tags

**Test Cases**:
```
TC-4.5.1: Chat endpoints accessible
TC-4.5.2: OpenAPI docs include chat endpoints
```

---

### Task 4.6: Create Chat API Tests
**Priority**: P1 | **Type**: Test | **Depends on**: 4.2-4.4

End-to-end tests for chat API.

**Acceptance Criteria**:
- [ ] Create `backend/tests/test_chat_api.py`
- [ ] Test chat message flow
- [ ] Test conversation persistence
- [ ] Test authentication requirements
- [ ] Mock OpenAI API calls

**Test Cases**:
```
TC-4.6.1: Chat requires authentication
TC-4.6.2: Chat creates and stores messages
TC-4.6.3: Conversation history persists
```

---

## Epic 5: Frontend Chat UI

### Task 5.1: Install ChatKit Dependencies
**Priority**: P0 | **Type**: Setup | **Depends on**: None

Add OpenAI ChatKit to frontend.

**Acceptance Criteria**:
- [ ] Research actual ChatKit package name (may be different)
- [ ] Install ChatKit or alternative chat UI library
- [ ] Configure any required providers

**Test Cases**:
```
TC-5.1.1: Package installs without errors
TC-5.1.2: ChatKit components importable
```

---

### Task 5.2: Create Chat API Client
**Priority**: P0 | **Type**: Implementation | **Depends on**: None

Add chat methods to API client.

**Acceptance Criteria**:
- [ ] Add sendMessage(conversationId, message) to api.ts
- [ ] Add getConversations() to api.ts
- [ ] Add getMessages(conversationId) to api.ts
- [ ] Handle streaming responses if supported

**Test Cases**:
```
TC-5.2.1: sendMessage calls correct endpoint
TC-5.2.2: getConversations returns list
TC-5.2.3: getMessages returns message history
```

---

### Task 5.3: Create ChatInterface Component
**Priority**: P0 | **Type**: Implementation | **Depends on**: 5.1, 5.2

Build main chat UI component.

**Acceptance Criteria**:
- [ ] Create `frontend/src/components/ChatInterface.tsx`
- [ ] Display message history
- [ ] Input field for new messages
- [ ] Send button and enter-to-send
- [ ] Loading state during API call
- [ ] Auto-scroll to new messages

**Test Cases**:
```
TC-5.3.1: Messages display correctly
TC-5.3.2: User can send messages
TC-5.3.3: Loading state shows during API call
TC-5.3.4: Auto-scrolls on new message
```

---

### Task 5.4: Create Chat Page
**Priority**: P0 | **Type**: Implementation | **Depends on**: 5.3

Build the chat page with routing.

**Acceptance Criteria**:
- [ ] Create `frontend/src/app/chat/page.tsx`
- [ ] Require authentication
- [ ] Load existing conversation or start new
- [ ] Include header with navigation
- [ ] Responsive layout

**Test Cases**:
```
TC-5.4.1: Page requires authentication
TC-5.4.2: Loads conversation history
TC-5.4.3: Responsive on mobile
```

---

### Task 5.5: Add Chat Navigation
**Priority**: P1 | **Type**: Implementation | **Depends on**: 5.4

Add navigation to chat from tasks page.

**Acceptance Criteria**:
- [ ] Add "Chat" button/link on tasks page
- [ ] Add "Tasks" button/link on chat page
- [ ] Update layout with consistent navigation

**Test Cases**:
```
TC-5.5.1: Can navigate from tasks to chat
TC-5.5.2: Can navigate from chat to tasks
```

---

### Task 5.6: Style Chat UI
**Priority**: P1 | **Type**: Implementation | **Depends on**: 5.3

Apply consistent styling to chat.

**Acceptance Criteria**:
- [ ] Style message bubbles (user vs assistant)
- [ ] Match app color scheme
- [ ] Responsive design
- [ ] Typing indicator animation

**Test Cases**:
```
TC-5.6.1: User messages styled distinctly
TC-5.6.2: Assistant messages styled distinctly
TC-5.6.3: Responsive on mobile
```

---

## Epic 6: Integration and Testing

### Task 6.1: End-to-End Chat Flow Test
**Priority**: P1 | **Type**: Test | **Depends on**: 4.5, 5.4

Test complete chat workflow.

**Acceptance Criteria**:
- [ ] Test adding task via chat
- [ ] Test listing tasks via chat
- [ ] Test completing task via chat
- [ ] Verify task appears in tasks page

**Test Cases**:
```
TC-6.1.1: Add task via chat, see in task list
TC-6.1.2: Complete task via chat, status updates
TC-6.1.3: Delete task via chat, removed from list
```

---

### Task 6.2: Error Handling Tests
**Priority**: P1 | **Type**: Test | **Depends on**: 4.5

Test error scenarios.

**Acceptance Criteria**:
- [ ] Test invalid task references
- [ ] Test API failures
- [ ] Test malformed requests
- [ ] Verify user-friendly error messages

**Test Cases**:
```
TC-6.2.1: Invalid task ID shows helpful error
TC-6.2.2: API timeout shows retry option
TC-6.2.3: Malformed input handled gracefully
```

---

### Task 6.3: Update Documentation
**Priority**: P2 | **Type**: Documentation | **Depends on**: 6.1

Document Phase III features.

**Acceptance Criteria**:
- [ ] Update README with chat feature
- [ ] Document chat API endpoints
- [ ] Add chat-specific environment variables
- [ ] Update architecture diagram

**Test Cases**:
```
TC-6.3.1: README includes chat setup
TC-6.3.2: API docs complete
```

---

## Task Dependency Graph

```
1.1 ── 1.2 ── 1.3
       │
2.1 ──┬── 2.2
      ├── 2.3
      ├── 2.4
      ├── 2.5
      └── 2.6 ── 2.7

3.1 ── 3.2 ── 3.3
              │
4.1 ──────────┼── 4.2 ── 4.5 ── 6.1
              │    │            │
              │   4.3           6.2
              │   4.4           │
              │    │            6.3
              │   4.6
              │
5.1 ── 5.3 ── 5.4 ── 5.5
       │            │
5.2 ───┘           5.6
```

---

## Implementation Order

### Wave 1: Foundation (Tasks 1.1-1.3, 2.1, 3.1)
Database models, MCP structure, OpenAI setup.

### Wave 2: MCP Tools (Tasks 2.2-2.7)
Implement all task tools.

### Wave 3: Agent (Tasks 3.2-3.3)
Configure and run AI agent.

### Wave 4: Chat API (Tasks 4.1-4.6)
Backend chat endpoints.

### Wave 5: Frontend (Tasks 5.1-5.6)
Chat UI components.

### Wave 6: Integration (Tasks 6.1-6.3)
Testing and documentation.

---

## Summary

| Epic | Tasks | Priority Mix |
|------|-------|--------------|
| 1. Database Models | 3 | P0: 3 |
| 2. MCP Server | 7 | P0: 5, P1: 2 |
| 3. Agents SDK | 3 | P0: 3 |
| 4. Chat API | 6 | P0: 3, P1: 3 |
| 5. Frontend Chat | 6 | P0: 4, P1: 2 |
| 6. Integration | 3 | P1: 2, P2: 1 |
| **Total** | **28** | P0: 18, P1: 9, P2: 1 |
