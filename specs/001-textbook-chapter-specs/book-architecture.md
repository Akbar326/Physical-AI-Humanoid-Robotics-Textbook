# Book Architecture: Physical AI & Humanoid Robotics Textbook

**Date**: 2025-12-19
**Feature**: specs/001-textbook-chapter-specs/
**Status**: Complete

## Overview

This document defines the complete architecture for the Physical AI & Humanoid Robotics textbook project, including directory structure, module organization, and technical implementation details.

## Directory Structure

### Primary Repository (Docusaurus Site)

```
physical-ai-robotics-textbook/
├── docs/
│   ├── index.md                           # Landing page
│   ├── preface/                           # Preface materials
│   │   ├── about.md
│   │   ├── prerequisites.md
│   │   ├── how-to-use.md
│   │   └── setup-guide.md
│   ├── module-1-ros2/                     # The Robotic Nervous System
│   │   ├── index.md
│   │   ├── 1-1-welcome-to-ros2.md
│   │   ├── 1-2-first-ros2-node.md
│   │   ├── 1-3-services.md
│   │   ├── 1-4-actions.md
│   │   ├── 1-5-parameters.md
│   │   └── 1-6-launch-files.md
│   ├── module-2-simulation/               # The Digital Twin
│   │   ├── index.md
│   │   ├── 2-1-intro-simulation.md
│   │   ├── 2-2-first-robot-model.md
│   │   ├── 2-3-adding-sensors.md
│   │   ├── 2-4-building-worlds.md
│   │   ├── 2-5-unity-visualization.md
│   │   └── 2-6-advanced-unity.md
│   ├── module-3-isaac/                    # The AI-Robot Brain
│   │   ├── index.md
│   │   ├── 3-1-intro-isaac-sim.md
│   │   ├── 3-2-rl-basics.md
│   │   ├── 3-3-scaling-rl.md
│   │   ├── 3-4-robot-manipulation.md
│   │   └── 3-5-deploying-ai-models.md
│   ├── module-4-vla/                      # Vision-Language-Action
│   │   ├── index.md
│   │   ├── 4-1-intro-vla.md
│   │   ├── 4-2-vision-robotics.md
│   │   ├── 4-3-language-understanding.md
│   │   ├── 4-4-language-to-actions.md
│   │   ├── 4-5-end-to-end-vla.md
│   │   └── 4-6-capstone-project.md
│   ├── labs/                              # Advanced lab exercises
│   │   ├── index.md
│   │   ├── lab-1-ros2-debug.md
│   │   ├── lab-2-gazebo-advanced.md
│   │   ├── lab-3-isaac-training.md
│   │   └── lab-4-vla-integration.md
│   ├── chapter-template.md                # Reusable chapter template
│   ├── chapter-validation.md              # Validation checklist
│   ├── glossary.md                        # Common terminology
│   └── resources.md                       # Additional references
├── static/
│   ├── img/
│   │   ├── module-1/                      # ROS 2 diagrams
│   │   ├── module-2/                      # Simulation diagrams
│   │   ├── module-3/                      # AI/Isaac diagrams
│   │   └── module-4/                      # VLA diagrams
│   └── downloads/                         # Exercise templates and solutions
├── src/
│   ├── css/custom.css                     # Custom styling
│   └── components/                        # Custom MDX components
│       ├── Tabs.tsx
│       ├── Callout.tsx
│       ├── CodeSandbox.tsx
│       └── Exercise.tsx
├── .github/
│   └── workflows/                         # GitHub Actions CI/CD
│       ├── build.yml
│       ├── deploy.yml
│       └── cross-platform-test.yml
├── docusaurus.config.js                   # Main Docusaurus configuration
├── sidebars.js                           # Navigation structure
├── package.json                          # Dependencies and scripts
├── .gitignore                           # Git ignore patterns
├── .mdlintrc                           # Markdown linting rules
└── README.md                           # Project overview
```

### Companion Repository (Code & Assets)

```
physical-ai-textbook-assets/
├── README.md                             # Companion repo overview
├── LICENSE                              # License information
├── module-1-ros2/                       # ROS 2 code and assets
│   ├── chapter-1-1/
│   │   ├── code/
│   │   │   ├── install_ros2.py
│   │   │   └── troubleshooting.md
│   │   ├── exercises/
│   │   │   ├── exercise-1-installation.md
│   │   │   └── exercise-2-verification.md
│   │   └── solutions/
│   │       └── solutions.md
│   ├── chapter-1-2/
│   │   ├── code/
│   │   │   ├── simple_publisher.py
│   │   │   ├── simple_subscriber.py
│   │   │   ├── package.xml
│   │   │   └── setup.py
│   │   ├── exercises/
│   │   └── solutions/
│   └── [1-3 through 1-6...]
├── module-2-simulation/                  # Simulation code and assets
│   ├── chapter-2-1/
│   │   ├── code/
│   │   ├── robot_models/
│   │   ├── worlds/
│   │   ├── exercises/
│   │   └── solutions/
│   └── [2-2 through 2-6...]
├── module-3-isaac/                     # Isaac code and assets
│   ├── chapter-3-1/
│   │   ├── isaac_scenes/
│   │   ├── code/
│   │   ├── configs/
│   │   ├── exercises/
│   │   └── solutions/
│   └── [3-2 through 3-5...]
├── module-4-vla/                       # VLA code and assets
│   ├── chapter-4-1/
│   │   ├── code/
│   │   ├── models/
│   │   ├── exercises/
│   │   └── solutions/
│   └── [4-2 through 4-6...]
└── shared/                            # Shared utilities
    ├── install-scripts/
    │   ├── ubuntu-setup.sh
    │   ├── windows-setup.ps1
    │   └── macos-setup.sh
    ├── docker/
    │   └── Dockerfile
    └── troubleshooting/
        └── platform-specific.md
```

## Module Hierarchy and Organization

### Module 1: The Robotic Nervous System (ROS 2)
- **Focus**: Foundation of distributed robotics systems
- **Chapters**: 6 chapters (1.1-1.6)
- **Learning Path**: Installation → Nodes → Communication → Orchestration
- **Prerequisites**: Basic Python knowledge
- **Tools**: ROS 2 Humble, colcon, rclpy/rclcpp

### Module 2: The Digital Twin (Simulation)
- **Focus**: Physics-based simulation and visualization
- **Chapters**: 6 chapters (2.1-2.6)
- **Learning Path**: Gazebo → Robot Models → Sensors → Worlds → Unity
- **Prerequisites**: Module 1 (ROS 2)
- **Tools**: Gazebo Fortress, Unity 2022 LTS, URDF/SDF

### Module 3: The AI-Robot Brain (AI/Isaac)
- **Focus**: AI for robotics, reinforcement learning
- **Chapters**: 5 chapters (3.1-3.5)
- **Learning Path**: Isaac Sim → RL Basics → Scaling → Manipulation → Deployment
- **Prerequisites**: Modules 1-2
- **Tools**: NVIDIA Isaac Sim 2023.1, reinforcement learning frameworks

### Module 4: Vision-Language-Action (VLA)
- **Focus**: End-to-end intelligent robotics systems
- **Chapters**: 6 chapters (4.1-4.6)
- **Learning Path**: VLA Concepts → Vision → Language → Action → Integration → Capstone
- **Prerequisites**: Modules 1-3
- **Tools**: Vision models, language models, action execution systems

## Navigation Patterns

### Sidebar Configuration (sidebars.js)
- **Primary Navigation**: Module-based categories
- **Secondary Navigation**: Chapter lists within modules
- **Tertiary Navigation**: In-page TOC for long chapters
- **Cross-references**: "Next Chapter", "See Also" links

### Front-matter Schema
Each chapter uses consistent front-matter:

```yaml
---
title: "Chapter X.Y: Title"
sidebar_position: Y
description: "Brief description for SEO"
difficulty: "Beginner|Intermediate|Advanced"
time_hours: float
module: 1|2|3|4
tags: [list, of, tags]
---
```

## Image Organization Strategy

### Directory Structure
- `static/img/module-1/`: ROS 2 diagrams and screenshots
- `static/img/module-2/`: Simulation and Gazebo images
- `static/img/module-3/`: Isaac Sim and AI visualizations
- `static/img/module-4/`: VLA system diagrams

### Naming Convention
- `concept-overview.png`: High-level concept diagrams
- `architecture-flow.png`: System architecture diagrams
- `code-screenshot.png`: Code examples as images
- `simulation-output.png`: Gazebo/Unity screenshots

### Accessibility Requirements
- Alt text: ≥20 characters, descriptive of content
- Captions: Optional but encouraged for complex diagrams
- File size: Optimized for web (≤500KB per image)

## Front-matter Schema for All Chapters

### Required Fields
- `title`: Human-readable title
- `sidebar_position`: Position within module sidebar
- `description`: SEO-friendly description
- `difficulty`: Educational difficulty level
- `time_hours`: Estimated completion time
- `module`: Module number (1-4)

### Optional Fields
- `tags`: Array of topic tags for search
- `last_updated`: Last modification date
- `version`: Content version (if versioned)

## Technical Implementation Details

### Docusaurus Configuration (docusaurus.config.js)
- **Base URL**: `/physical-ai-robotics-textbook/` for GitHub Pages
- **Presets**: Classic preset with docs, blog (disabled), theme
- **Plugins**: Search, PWA, ideal image, client redirects
- **Themes**: Custom CSS, syntax highlighting for Python/Bash/YAML

### Build Performance Targets
- **Build time**: <30 seconds
- **Lighthouse score**: >90 for accessibility/performance
- **Page load**: <2 seconds on good network

### Cross-Platform Support
- **Ubuntu 22.04**: Primary development platform
- **Windows 10/11**: WSL2 support for ROS 2, native for other tools
- **macOS 12+**: Native support for all tools except some GPU-dependent features

## Quality Assurance Framework

### Content Validation
- **Technical Accuracy**: All claims verifiable from official documentation
- **Educational Clarity**: Grade 8-12 reading level
- **Modular Architecture**: Chapters readable independently
- **Consistency**: Uniform terminology and formatting
- **Original Content**: Synthesized from multiple sources, no copy-paste
- **Deployment Readiness**: All links resolve, images load, builds succeed

### Automated Checks
- **Build Validation**: `npm run build` succeeds
- **Link Checking**: All internal and external links resolve
- **Markdown Linting**: Style and syntax compliance
- **Code Syntax**: Python/Bash/YAML code blocks are valid
- **Accessibility**: Alt text, heading hierarchy, color contrast

## Component Architecture

### MDX Components (src/components/)
- **Tabs.tsx**: OS-specific instruction tabs
- **Callout.tsx**: Informational, warning, and danger callouts
- **CodeSandbox.tsx**: Interactive code examples
- **Exercise.tsx**: Structured exercise rendering with solutions

### Custom Styling (src/css/custom.css)
- **Module Cards**: Grid layout for module overviews
- **Progress Indicators**: Visual progress tracking
- **Code Themes**: Custom syntax highlighting
- **Responsive Design**: Mobile-friendly layouts

## Deployment Architecture

### GitHub Pages
- **Source**: `main` branch of primary repository
- **Build**: GitHub Actions workflow on push to main
- **Target**: `gh-pages` branch with static site
- **Domain**: `[username].github.io/physical-ai-robotics-textbook`

### CI/CD Pipeline
- **Build Workflow**: Validates build, linting, links
- **Deploy Workflow**: Automatic deployment on main branch
- **Cross-Platform Workflow**: Tests on Ubuntu, Windows, macOS
- **Security Workflow**: Scans for secrets and vulnerabilities

## Data Flow and Integration

### Textbook ↔ Companion Repository
- **Code Examples**: Maintained separately, referenced in textbook
- **Robot Models**: URDF/SDF files in companion, referenced in textbook
- **Exercise Solutions**: Separate from exercises, accessible after attempt
- **Install Scripts**: Shared across both repositories

### Content Synchronization
- **Version Alignment**: Textbook and companion repo versions aligned
- **API Compatibility**: Code examples match documented software versions
- **Dependency Management**: Clear version requirements in both repos