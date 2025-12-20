# Data Model: Physical AI & Humanoid Robotics Textbook

**Date**: 2025-12-19
**Feature**: specs/001-textbook-chapter-specs/
**Status**: Complete

## Overview

This document defines the canonical data model for the Physical AI & Humanoid Robotics textbook, including entity definitions, validation rules, and schema specifications.

## Chapter Entity

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | Yes | Unique identifier in format "module.chapter" (e.g., "1.1", "3.5") |
| title | string | Yes | Human-readable chapter title |
| module | integer | Yes | Module number (1-4) |
| difficulty | enum | Yes | One of: Beginner, Intermediate, Advanced |
| estimated_hours | float | Yes | Time required in hours (1.0-12.0) |
| learning_objectives | list[string] | Yes | 3-6 measurable learning objectives |
| prerequisites | list[string] | Yes | List of prerequisite chapter IDs |
| tools_required | list[object] | Yes | List of required tools with versions |
| sections | list[Section] | Yes | Content sections |
| exercises | list[Exercise] | Yes | Minimum 2 exercises per chapter |
| self_assessment | Checkpoint | Yes | Self-assessment questions |
| diagrams | list[Diagram] | Yes | Minimum 1 diagram per chapter |
| code_examples | list[CodeSnippet] | Yes | Minimum 3 code examples per chapter |
| references | list[Citation] | Yes | APA-formatted references |
| connections | object | Yes | Navigation connections to other chapters |

### Validation Rules

- `title` must match pattern: `[A-Za-z\s\-:\'\(\)]+`
- `estimated_hours` must be between 1.0 and 12.0
- `learning_objectives` must have 3-6 items
- `exercises` must have ≥2 items
- `diagrams` must have ≥1 item
- `code_examples` must have ≥3 items
- All code must be syntactically valid
- All diagrams must have alt text ≥20 characters
- All references must be verifiable (links resolve)

## Exercise Entity

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Exercise title |
| step_count | integer | Yes | Number of steps (5-15) |
| steps | list[string] | Yes | List of step-by-step instructions |
| expected_output | string | Yes | Description of expected result |
| time_estimate | integer | Yes | Time in minutes |
| os_support | list[enum] | Yes | List of supported OS: Ubuntu, Windows, macOS |
| solution_ref | string | Yes | Reference to solution location |

### Validation Rules

- All steps must be actionable commands or clear procedures
- Expected output must be concrete and observable
- Code examples in steps must be runnable
- Step count must be between 5 and 15

## Self-Assessment Checkpoint Entity

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| questions | list[object] | Yes | List of question objects |
| passing_score | float | Yes | Minimum score required (0.0-1.0) |
| verifies_concepts | list[string] | Yes | Concepts verified by this checkpoint |

### Question Object Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| question | string | Yes | The question text |
| answer | string | Yes | The correct answer |
| hints | list[string] | No | Optional hints |

### Validation Rules

- Must have at least 5 questions
- Questions must be verifiable from chapter content (no external knowledge required)
- All answers must be unambiguous

## Diagram Entity

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| file | string | Yes | File path (static/img/module-X/...) |
| alt_text | string | Yes | Alternative text for accessibility |
| caption | string | No | Optional caption |
| type | enum | Yes | Type: node_graph, architecture, data_flow, screenshot, world_layout |

### Validation Rules

- Alt text must be present and descriptive (≥20 characters)
- File must exist and be optimized for web
- Type must match diagram content

## Code Snippet Entity

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| language | string | Yes | Code language (python, bash, yaml, etc.) |
| content | string | Yes | The code content |
| description | string | Yes | Explanation of what the code does |
| os_support | list[enum] | Yes | Supported operating systems |
| expected_output | string | No | Expected output when run |

### Validation Rules

- Code must be syntactically valid for the specified language
- Must be runnable on specified operating systems
- If expected_output provided, must match actual output

## Citation Entity

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| type | enum | Yes | Type: book, article, webpage, documentation, paper |
| title | string | Yes | Title of the cited work |
| authors | list[string] | Yes | List of authors |
| year | integer | Yes | Publication year |
| url | string | No | URL if available |
| publisher | string | No | Publisher information |
| doi | string | No | DOI if available |

### Validation Rules

- Must follow APA 7th edition format
- URLs must be resolvable
- All required fields for citation type must be present

## Front Matter Schema

Each chapter markdown file must include this YAML front matter:

```yaml
---
title: "Chapter X.Y: Title"
sidebar_position: Y
description: "Brief description"
difficulty: Beginner|Intermediate|Advanced
time_hours: float
module: 1|2|3|4
tags: [list, of, tags]
---
```

## Validation Checklist

For each chapter, verify:

- [ ] All required fields present and valid
- [ ] Minimum content requirements met (2+ exercises, 1+ diagrams, 3+ code examples)
- [ ] Learning objectives are specific and measurable
- [ ] Exercises have clear steps and expected outputs
- [ ] Diagrams have descriptive alt text
- [ ] Code examples are syntactically valid
- [ ] References follow APA format
- [ ] Self-assessment has ≥5 questions
- [ ] Prerequisites are properly linked
- [ ] Accessibility requirements met

## Example Chapter Data

```json
{
  "id": "1.1",
  "title": "Welcome to ROS 2",
  "module": 1,
  "difficulty": "Beginner",
  "estimated_hours": 2.5,
  "learning_objectives": [
    "Explain the purpose of ROS 2 in robotics development",
    "Install ROS 2 Humble on your operating system",
    "Run your first ROS 2 command successfully"
  ],
  "prerequisites": [],
  "tools_required": [
    {
      "name": "ROS 2",
      "version": "Humble Hawksbill",
      "os": ["Ubuntu", "Windows", "macOS"]
    }
  ],
  "exercises": [
    {
      "title": "Install ROS 2",
      "step_count": 8,
      "steps": ["Download ROS 2 Humble...", "Run installation script..."],
      "expected_output": "Successful installation with ros2 command available",
      "time_estimate": 45,
      "os_support": ["Ubuntu", "Windows", "macOS"],
      "solution_ref": "solution.md"
    }
  ],
  "self_assessment": {
    "questions": [
      {
        "question": "What does ROS stand for?",
        "answer": "Robot Operating System",
        "hints": ["It's an acronym", "Used in robotics"]
      }
    ],
    "passing_score": 0.8,
    "verifies_concepts": ["ROS 2 basics"]
  },
  "diagrams": [
    {
      "file": "static/img/module-1/ros2-architecture.png",
      "alt_text": "Diagram showing ROS 2 architecture with nodes, topics, and services",
      "caption": "ROS 2 architecture overview",
      "type": "architecture"
    }
  ],
  "code_examples": [
    {
      "language": "bash",
      "content": "ros2 --version",
      "description": "Check ROS 2 installation",
      "os_support": ["Ubuntu", "Windows", "macOS"],
      "expected_output": "ros2 humble"
    }
  ],
  "references": [
    {
      "type": "documentation",
      "title": "ROS 2 Installation Guide",
      "authors": ["Open Robotics"],
      "year": 2025,
      "url": "https://docs.ros.org/"
    }
  ],
  "connections": {
    "next_chapter": "1.2",
    "related_chapters": ["1.2", "1.3"]
  }
}
```