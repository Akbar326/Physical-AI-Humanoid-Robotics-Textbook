# Implementation Plan: Global Agent-Only Chat

**Branch**: `004-global-agent-chat` | **Date**: 2026-01-02 | **Spec**: specs/004-global-agent-chat/spec.md
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

## Summary

Implement a global chatbot UI that appears on every page of the Docusaurus textbook site, using only agent-enhanced functionality (sending queries exclusively to `/agent-query` endpoint). This involves creating a persistent React component that integrates with the Docusaurus layout system and removing all basic RAG functionality.

## Technical Context

**Language/Version**: JavaScript/React, Docusaurus v3.x
**Primary Dependencies**: React, Docusaurus framework, existing backend API
**Storage**: Browser local storage for chat history (optional)
**Testing**: Jest for unit tests, manual testing for UI integration
**Target Platform**: Web browser, responsive design for mobile/desktop
**Project Type**: Web application with React components
**Performance Goals**: <500ms response time for UI interactions, minimal impact on page load
**Constraints**: Must work with existing Docusaurus theme, minimal styling changes, persistent across page navigation
**Scale/Scope**: Single global component, works across all textbook pages

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Technical Accuracy & Verifiability**: Implementation will use standard Docusaurus patterns and React best practices
- **Educational Clarity**: UI will be intuitive and provide clear feedback to users
- **Modular Architecture**: Component will be modular and reusable across the site
- **Consistency & Quality**: UI will match Docusaurus theme and maintain consistent styling
- **Original Content**: Component implementation will be original code
- **Deployment Readiness**: Component will be compatible with Docusaurus build process

## Project Structure

### Documentation (this feature)

```text
specs/004-global-agent-chat/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── components/
│   └── GlobalChat/
│       ├── GlobalChat.jsx        # Main chat component
│       ├── GlobalChat.module.css # Component styling
│       └── ChatService.js        # API interaction logic
└── theme/
    └── Root.js                 # Global layout wrapper

# Update existing files
docusaurus.config.js           # Configuration updates
package.json                  # Dependencies if needed
```

**Structure Decision**: Single project with React component approach. The GlobalChat component will be integrated into the Docusaurus theme via the Root component to ensure it appears on every page.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [N/A] | [N/A] | [N/A] |

## Phase 0: Research Complete
- [x] Research.md created with technology decisions and rationale
- [x] All NEEDS CLARIFICATION items resolved

## Phase 1: Design & Contracts Complete
- [x] Data-model.md created with entities and relationships
- [x] API contracts created in /contracts/ directory
- [x] Quickstart.md created with implementation guide
- [x] Agent context updated (not applicable for manual process)
- [x] Constitution Check re-evaluated and passed