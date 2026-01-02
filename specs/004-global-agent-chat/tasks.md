---
description: "Task list for global agent-only chat implementation"
---

# Tasks: Global Agent-Only Chat

**Input**: Design documents from `/specs/004-global-agent-chat/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are included as requested in the feature specification for verifying UI display and agent responses.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `src/`, `static/`, `docusaurus.config.js` at repository root
- **React components**: `src/components/GlobalChat/`
- **Docusaurus theme**: `src/theme/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create directory structure for GlobalChat component in src/components/GlobalChat/
- [x] T002 [P] Create CSS module file for GlobalChat styling in src/components/GlobalChat/GlobalChat.module.css
- [x] T003 [P] Create API service file for agent communication in src/components/GlobalChat/ChatService.js

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create GlobalChat React component in src/components/GlobalChat/GlobalChat.jsx
- [x] T005 [P] Implement basic UI structure with message display and input field
- [x] T006 [P] Add state management hooks for chat messages and UI state
- [x] T007 Create API service function to call /agent-query endpoint
- [x] T008 Configure error handling for API communication

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---
## Phase 3: User Story 1 - Global Chat Access (Priority: P1) 🎯 MVP

**Goal**: Create a persistent chat UI that appears on every page of the textbook site, with fixed positioning and basic functionality.

**Independent Test**: Can be fully tested by loading any textbook page and verifying the chat UI appears in a consistent location with full functionality to send messages to the agent backend.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T009 [P] [US1] Create component test to verify chat UI appears on page load in src/components/GlobalChat/__tests__/GlobalChat.test.js
- [x] T010 [P] [US1] Create integration test to verify message submission functionality

### Implementation for User Story 1

- [x] T011 [P] [US1] Update Docusaurus Root component to include GlobalChat in src/theme/Root.js
- [x] T012 [US1] Implement fixed positioning styling for chat UI in GlobalChat.module.css
- [x] T013 [US1] Add responsive design for mobile and desktop in GlobalChat.module.css
- [x] T014 [US1] Implement message display functionality in GlobalChat.jsx
- [x] T015 [US1] Implement input field and send button functionality in GlobalChat.jsx
- [x] T016 [US1] Add API call integration to send messages to /agent-query endpoint

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---
## Phase 4: User Story 2 - Agent-Only Functionality (Priority: P1)

**Goal**: Ensure the chat UI exclusively uses agent-enhanced functionality and removes any basic RAG integration.

**Independent Test**: Can be fully tested by sending queries and verifying they are processed only through the agent-enhanced endpoint, not the basic RAG endpoint.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [x] T017 [P] [US2] Create test to verify API calls go only to /agent-query endpoint
- [x] T018 [P] [US2] Create test to verify no calls are made to /query endpoint

### Implementation for User Story 2

- [x] T019 [P] [US2] Remove any references to /query endpoint from ChatService.js
- [x] T020 [US2] Remove any basic RAG functionality from GlobalChat.jsx
- [x] T021 [US2] Update API service to only call /agent-query endpoint
- [x] T022 [US2] Remove any toggle or configuration for basic RAG mode
- [x] T023 [US2] Update error handling to be specific to agent-only functionality

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---
## Phase 5: User Story 3 - Consistent UI Experience (Priority: P2)

**Goal**: Ensure the chatbot UI maintains consistent styling and behavior across all textbook pages.

**Independent Test**: Can be tested by navigating between different textbook pages and verifying the chat UI looks and behaves the same on all pages.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [x] T024 [P] [US3] Create test to verify UI styling consistency across different page contexts
- [x] T025 [P] [US3] Create test to verify chat state persistence during navigation

### Implementation for User Story 3

- [x] T026 [P] [US3] Ensure UI styling matches Docusaurus theme in GlobalChat.module.css
- [x] T027 [US3] Add state persistence for chat across page navigation
- [x] T028 [US3] Implement proper z-index and layering to avoid UI conflicts
- [x] T029 [US3] Add keyboard accessibility features
- [x] T030 [US3] Implement proper focus management and ARIA attributes

**Checkpoint**: All user stories should now be independently functional

---
## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T031 [P] Add loading indicators during agent response in GlobalChat.jsx
- [x] T032 [P] Add proper error handling and user feedback for API failures
- [x] T033 Add empty state and welcome message for initial chat state
- [x] T034 [P] Add typing indicators for agent responses
- [x] T035 Update docusaurus.config.js if needed for any new configurations
- [x] T036 [P] Documentation updates in docs/
- [x] T037 Run quickstart.md validation
- [x] T038 Test edge cases like network errors, empty messages, and long responses

---
## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---
## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Create component test to verify chat UI appears on page load in src/components/GlobalChat/__tests__/GlobalChat.test.js"
Task: "Create integration test to verify message submission functionality"

# Launch all implementation tasks for User Story 1 together:
Task: "Update Docusaurus Root component to include GlobalChat in src/theme/Root.js"
Task: "Implement fixed positioning styling for chat UI in GlobalChat.module.css"
Task: "Add responsive design for mobile and desktop in GlobalChat.module.css"
```

---
## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---
## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence