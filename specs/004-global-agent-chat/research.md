# Research: Global Agent-Only Chat

## Decision: Docusaurus Global Component Implementation
**Rationale**: To make the chatbot UI visible on every page of the textbook site, the most appropriate approach is to use Docusaurus' Root component which wraps all pages. This ensures the chat UI appears consistently across all pages without requiring individual page modifications.

**Alternatives considered**:
1. Layout wrapper component - requires modifying each layout individually
2. MDX global component - limited to MDX pages only
3. Custom theme integration - complex and potentially fragile
4. Root component approach - chosen as it's officially supported by Docusaurus for global UI elements

## Decision: Agent-Only API Integration
**Rationale**: Remove all references to basic RAG `/query` endpoint and exclusively use `/agent-query` endpoint. This simplifies the frontend logic while meeting the requirement for agent-only functionality.

**Alternatives considered**:
1. Keep both endpoints with UI toggle - violates requirement to remove basic RAG
2. Conditional endpoint based on config - adds unnecessary complexity
3. Single endpoint approach - chosen as it's simpler and meets requirements

## Decision: Fixed Position UI Design
**Rationale**: Implement the chat UI as a fixed-position component (e.g., bottom-right corner) that remains visible during scrolling and navigation. This provides consistent access to the chat functionality.

**Alternatives considered**:
1. Floating sidebar - might interfere with content layout
2. Top navigation bar - might compete with existing navigation
3. Fixed bottom-right position - chosen as it's non-intrusive and commonly used for chat widgets

## Decision: React State Management
**Rationale**: Use React hooks (useState, useEffect) for local state management of the chat component. This keeps the implementation simple and follows React best practices.

**Alternatives considered**:
1. Redux/store - overkill for simple UI state
2. Context API - unnecessary complexity for isolated component
3. Local hooks - chosen as it's simpler and sufficient for requirements

## Decision: Error Handling Strategy
**Rationale**: Implement appropriate error handling for network failures and backend unavailability. Provide user-friendly messages when the agent service is unavailable.

**Alternatives considered**:
1. Silent failures - poor user experience
2. Generic error messages - not informative enough
3. Detailed error feedback - chosen as it provides good UX while being informative