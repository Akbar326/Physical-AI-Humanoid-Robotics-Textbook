<!--
Sync Impact Report - Constitution Update

VERSION CHANGE: 0.0.0 → 1.0.0 (Initial ratification)

PRINCIPLES DEFINED:
- Technical Accuracy & Verifiability
- Educational Clarity
- Modular Architecture
- Consistency & Quality
- Original Content
- Deployment Readiness

SECTIONS ADDED:
- Core Principles (6 principles)
- Content Standards (writing, citation, examples, code quality)
- Docusaurus Requirements (structure, formatting, deployment)
- Governance

TEMPLATES STATUS:
✅ plan-template.md - Reviewed, constitution check section will reference these principles
✅ spec-template.md - Reviewed, aligns with user story and requirements structure
✅ tasks-template.md - Reviewed, aligns with phased implementation approach
✅ phr-template.prompt.md - Reviewed, compatible with PHR creation workflow

FOLLOW-UP TODOS:
- None - all placeholders filled, no deferred items

RATIONALE FOR MAJOR VERSION (1.0.0):
- First ratification of constitution
- Establishes foundational governance structure
- Defines all core principles from scratch
-->

# AI-Driven Book Creation Constitution

## Core Principles

### I. Technical Accuracy & Verifiability

**Rule**: All factual claims about AI, Web technologies, Robotics, and Physical AI MUST be verifiable from reliable sources.

**Requirements**:
- Every technical assertion must be backed by authoritative sources (academic papers, official documentation, industry standards)
- Claims about AI capabilities, limitations, or implementations must reflect current state-of-the-art (as of January 2025)
- No speculative statements presented as facts
- When emerging technologies are discussed, clearly distinguish between proven capabilities and experimental features

**Rationale**: The book's value depends on technical credibility. Inaccurate information undermines learning and can mislead students building on this foundation.

### II. Educational Clarity

**Rule**: Content MUST be accessible to learners at Grade 8-12 reading level while maintaining expert-level depth.

**Requirements**:
- Complex concepts broken down into progressive explanations (simple → intermediate → advanced)
- Technical jargon introduced with clear definitions before use
- Abstract concepts paired with concrete examples or analogies
- Each chapter assumes only knowledge from previous chapters (no hidden prerequisites)
- At least 40% of content must include examples, diagrams, code snippets, or step-by-step breakdowns

**Rationale**: Balancing accessibility with depth ensures the book serves both beginners building foundations and advanced learners seeking mastery.

### III. Modular Architecture

**Rule**: Book structure MUST align with Docusaurus architecture (pages, sections, sidebars) and support independent chapter navigation.

**Requirements**:
- Each chapter is a standalone Docusaurus document with proper front-matter
- Chapters organized into logical sections (Preface, Core Concepts, Applied Topics, Labs, Glossary)
- Sidebar navigation reflects learning progression
- Cross-references use Docusaurus link syntax for maintainability
- Each module can be read independently or as part of the full sequence

**Rationale**: Modular design enables flexible learning paths, easier maintenance, and scalable content expansion without breaking existing structure.

### IV. Consistency & Quality

**Rule**: All content MUST maintain consistent tone, terminology, formatting, and quality standards across chapters.

**Requirements**:
- Terminology: Use consistent terms for concepts (define once, use everywhere)
- Tone: Educational, practical, encouraging (avoid condescending or overly casual language)
- Formatting: Standardized heading hierarchy (H1 for chapter, H2 for major sections, H3 for subsections)
- Code style: Consistent syntax highlighting, naming conventions, and comment style
- Citations: APA format inline + reference list per chapter (where applicable)

**Rationale**: Consistency builds reader trust and reduces cognitive load, allowing focus on learning rather than decoding presentation variations.

### V. Original Content

**Rule**: All content MUST be original, transformed, and free from plagiarism.

**Requirements**:
- No copy-pasted content from external sources (even with attribution)
- Concepts explained in the author's own words after synthesis from multiple sources
- Examples and code snippets created specifically for this book (not reproduced from tutorials)
- When referencing external work, provide proper citation and transformative analysis

**Rationale**: Original content ensures copyright compliance, demonstrates understanding, and provides unique value beyond aggregating existing resources.

### VI. Deployment Readiness

**Rule**: All content MUST be deployment-ready for GitHub Pages via Docusaurus build process.

**Requirements**:
- All chapters compile without errors in Docusaurus build (`npm run build` succeeds)
- No broken internal or external links
- All images referenced have valid paths and alt text
- Front-matter includes required metadata (title, sidebar position, description)
- Markdown follows CommonMark/GFM specification
- MDX components (if used) are properly imported and syntactically correct

**Rationale**: Deployment-ready content ensures the book is always publishable and functional, avoiding technical debt and broken reader experiences.

## Content Standards

### Writing Quality

- **Clarity**: Sentences under 25 words average; paragraphs under 150 words
- **Active Voice**: Prefer active constructions ("The system processes data" not "Data is processed by the system")
- **Concrete Examples**: Abstract principles must be illustrated with specific, runnable examples
- **Progressive Disclosure**: Introduce simple version first, then add complexity

### Citation & Attribution

- **Format**: APA style (Author, Year) inline citations
- **Sources**: Peer-reviewed papers, official documentation, authoritative industry publications
- **Reference Lists**: Each chapter includes bibliography for cited sources
- **Code Attribution**: Original code snippets require no attribution; adapted code must cite source

### Examples & Code Quality

- **Runnable Code**: All code examples must be syntactically correct and executable
- **Minimal Examples**: Strip unnecessary complexity; focus on concept being taught
- **Comments**: Explain "why" not "what" (code shows what; comments explain rationale)
- **Testing**: Complex examples should include test cases or expected output

## Docusaurus Requirements

### Structure

```text
docs/
├── index.md                  # Landing/Introduction
├── preface/
│   └── *.md
├── chapter-01-foundations/
│   └── *.md
├── chapter-02-ai-basics/
│   └── *.md
├── labs/
│   └── *.md
└── glossary.md
```

### Front-Matter

Every Markdown file must include:

```yaml
---
title: "Chapter Title"
sidebar_position: 1
description: "Brief chapter summary"
---
```

### Formatting Standards

- **Headings**: No skipping levels (H1 → H2 → H3, never H1 → H3)
- **Code Blocks**: Always specify language (```python, ```javascript, ```bash)
- **Links**: Use relative paths for internal links (`[Chapter 2](../chapter-02/intro.md)`)
- **Images**: Store in `static/img/`, reference as `/img/filename.png`

### Deployment

- **Build Validation**: Run `npm run build` before any commit to main branch
- **Link Checking**: Validate all links resolve correctly (no 404s)
- **GitHub Pages**: Deploy via GitHub Actions to `gh-pages` branch
- **Accessibility**: All images have descriptive alt text; color contrast meets WCAG AA

## Governance

### Amendment Process

1. **Proposal**: Document proposed changes with rationale
2. **Impact Analysis**: Identify affected content, templates, and workflows
3. **Review**: Minimum 24-hour review period for significant changes
4. **Approval**: Explicit approval required before implementation
5. **Migration**: Update all dependent artifacts (templates, existing chapters)

### Version Policy

- **MAJOR**: Breaking changes to principles (removes guarantees, changes scope)
- **MINOR**: New principles added or existing principles materially expanded
- **PATCH**: Clarifications, examples, formatting, typo fixes

### Compliance

- All content creation must reference this constitution for quality gates
- Pull requests must include constitution compliance checklist
- Constitution supersedes conflicting guidance in other documents
- Spec-Kit-Plus quality checks validate adherence to these principles

### Complexity Justification

Any deviation from these principles (e.g., exceeding reading level, omitting examples, breaking modular structure) MUST be explicitly justified in the relevant spec, plan, or ADR with:
- Why the principle cannot be followed
- What specific problem requires the deviation
- What alternatives were considered and rejected

**Version**: 1.0.0 | **Ratified**: 2025-12-04 | **Last Amended**: 2025-12-04
