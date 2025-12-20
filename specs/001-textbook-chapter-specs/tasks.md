# Tasks: Physical AI & Humanoid Robotics Textbook

**Input**: Design documents from `/specs/001-textbook-chapter-specs/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md (to be generated), data-model.md (Phase 1)

**Organization**: Tasks are grouped by user story (module) to enable independent chapter development and testing.

**Status**: Ready for Phase 0 research completion and Phase 1 infrastructure setup.

---

## Format: `[ID] [P?] [Story] Description`

- **Checkbox**: `- [ ]` marks incomplete tasks
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., [US1], [US2], [US3], [US4])
- **Description**: Clear action with exact file path

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Docusaurus project initialization, CI/CD, and shared templates

**Checkpoint**: Docusaurus build working, GitHub Actions configured, chapter template ready

### Docusaurus & Build Infrastructure

- [x] T001 Initialize Docusaurus v3.x project with Node.js 18+ in repository root
- [x] T002 [P] Install required Node.js dependencies: Docusaurus, MDX, GitHub Pages plugin, PWA plugin in package.json
- [x] T003 Configure docusaurus.config.js with:
  - Base URL for GitHub Pages deployment
  - Sidebar configuration loader (sidebars.js)
  - Presets for Markdown + MDX support
  - Analytics and search plugins
- [x] T004 Create sidebars.js with 4-module hierarchy:
  - Module 1: ROS 2 (6 chapters)
  - Module 2: Simulation (6 chapters)
  - Module 3: Isaac (5 chapters)
  - Module 4: VLA (6 chapters)
  - Labs and glossary sections
- [x] T005 Set up static/ directory structure:
  - static/img/module-1/, module-2/, module-3/, module-4/ (for diagrams)
  - static/downloads/ (for exercise templates)
- [x] T006 Create docs/index.md landing page with textbook overview and learning path
- [x] T007 Create docs/preface/ directory with 4 files:
  - about.md (book overview and target audience)
  - prerequisites.md (software prerequisites, OS support)
  - how-to-use.md (reading guide for different paths)
  - setup-guide.md (initial setup instructions for all 3 OS)

### GitHub Actions CI/CD Pipeline

- [x] T008 Create .github/workflows/build.yml for:
  - Docusaurus build validation (`npm run build`)
  - Markdown linting (markdownlint configuration)
  - Link checking (link-checker tool)
  - Accessibility validation (Lighthouse score 90+)
  - Syntax validation for code snippets (Python, Bash, YAML, JSON)
- [x] T009 Create .github/workflows/deploy.yml for:
  - Automatic deployment to GitHub Pages on main branch
  - Build artifacts
  - Deployment status check
- [x] T010 Create .github/workflows/cross-platform-test.yml for:
  - Matrix testing: Ubuntu 22.04, Windows 10/11, macOS 12+
  - Code example execution validation (where applicable)
  - Platform-specific installation script tests
- [ ] T011 Configure GitHub branch protection rules:
  - Require PR review before merge to main
  - Require all CI/CD checks pass before merge
  - Dismiss stale PR reviews

### Template & Documentation Standards

- [x] T012 Create docs/chapter-template.md with required sections:
  - Front-matter (title, sidebar_position, description, difficulty, time_hours, module)
  - Introduction (learning objectives, prerequisites)
  - Core Concepts (3 subsections: simple → intermediate → advanced)
  - Hands-On Exercises (≥2 exercises with steps + expected output)
  - Diagrams & Visualizations (≥1 with alt text)
  - Code Examples (≥3 with explanatory comments)
  - Troubleshooting (OS-specific gotchas)
  - Self-Assessment Checkpoint (≥5 questions)
  - Connections (next chapter, related topics)
  - References (APA citations)
  - Validation checklist (embedded)
- [x] T013 Create docs/chapter-validation.md checklist:
  - Technical accuracy verification (claims match official docs)
  - Educational clarity (Grade 8-12 reading level)
  - Practical content percentage (40% minimum)
  - Code example reproducibility (all platforms)
  - Diagram quality and alt text
  - Constitution compliance (all 6 principles)
- [x] T014 Create .mdlintrc (Markdown linting config) with:
  - Heading hierarchy rules (no skipping levels)
  - Line length and list formatting
  - Code block language specification requirement
- [x] T015 [P] Create install scripts in companion repo (shared/install-scripts/):
  - ubuntu-setup.sh (ROS 2 Humble, Gazebo Fortress, Python 3.10)
  - windows-setup.ps1 (PowerShell for Windows 10/11)
  - macos-setup.sh (macOS 12+ setup)
  - Dockerfile (reproducible environment option)

### Companion Repository Setup

- [x] T016 Initialize separate GitHub repository: physical-ai-textbook-assets
- [x] T017 Create root structure in companion repo:
  - module-1-ros2/, module-2-simulation/, module-3-isaac/, module-4-vla/
  - shared/ (install-scripts/, docker/, troubleshooting/)
  - README.md (overview, how to use)
  - LICENSE (choose appropriate license)
- [x] T018 [P] Set up chapter subdirectories in companion repo for all 23 chapters:
  - Each chapter folder: code/, exercises/, solutions/, robot_models/ (if applicable)
  - Example: module-1-ros2/chapter-1-1/code/, module-1-ros2/chapter-1-1/exercises/

**Checkpoint**: Docusaurus builds successfully locally, GitHub Actions workflows created, companion repo initialized. Ready for Phase 2 foundational tasks.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Design artifacts and validation infrastructure that ALL user stories depend on

**⚠️ CRITICAL**: Cannot start chapter creation until this phase is complete

### Design Artifacts & Data Models

- [x] T019 Generate research.md (Phase 0 output) with findings for:
  - Docusaurus v3 sidebar configuration best practices
  - MDX interactive components for education
  - GitHub Actions workflow patterns
  - APA citation management in Markdown
  - URDF/SDF versioning strategy
  - Cross-platform CI/CD matrix testing
  - Docusaurus multi-version support
  - WCAG 2.1 AA accessibility validation
- [x] T020 Create data-model.md with canonical entity definitions:
  - Chapter entity (fields, validation rules)
  - Exercise entity (structure, required elements)
  - Self-Assessment Checkpoint entity (questions, scoring)
  - Diagram entity (file paths, alt text requirements)
  - Code example entity (syntax, platform support)
  - Reference entity (APA format, link validation)
- [x] T021 Create book-architecture.md documenting:
  - Complete Docusaurus directory structure (docs/, static/)
  - Module hierarchy and chapter organization
  - Sidebar configuration details (nesting, ordering)
  - Navigation patterns (previous/next, cross-references)
  - Image organization strategy (static/img/module-X/)
  - Front-matter schema for all chapters
- [x] T022 Create quickstart.md (30-minute writer onboarding):
  - Clone instructions (Docusaurus repo + companion repo)
  - Use chapter template (copy from docs/chapter-template.md)
  - Fill front-matter with chapter metadata
  - Write sections (with progressive disclosure structure)
  - Add code examples (from companion repo or create new)
  - Create diagrams (store in static/img/module-X/)
  - Add APA references
  - Run validation (`npm run build`, link checker, linter)
  - Create PR with validation checklist
  - Review process

### Contracts & Configuration Schemas

- [x] T023 Create contracts/docusaurus-config.json with:
  - Docusaurus version requirement (3.x.x)
  - Node.js version requirement (≥18.0.0)
  - Build command expectation
  - Plugin list (content-docs, search, PWA, ideal-image)
  - Performance targets (build <30s, Lighthouse 90+)
  - Sidebar structure expectations (chapters per module, nesting depth)
- [x] T024 Create contracts/chapter-metadata.json with:
  - Required front-matter fields (title, sidebar_position, description, difficulty, time_hours, module)
  - Optional fields (tags, last_updated, version)
  - Field validation rules (types, patterns, ranges)
  - Example valid chapter metadata
- [x] T025 Create contracts/companion-repo-structure.json with:
  - Module/chapter naming pattern (module-X-{name}/chapter-X.Y/)
  - Required subdirectories (code/, exercises/, solutions/)
  - File naming conventions
  - Validation rules (code must be syntactically valid, solutions provided for all exercises)
  - Cross-platform requirements (all scripts support Ubuntu/Windows/macOS)

### Quality Assurance Framework

- [x] T026 Create .github/config/constitutional-checklist.md with:
  - Technical Accuracy check: Are claims verifiable from official docs?
  - Educational Clarity check: Is reading level Grade 8-12?
  - Modular Architecture check: Can chapter be read independently?
  - Consistency & Quality check: Does tone, terminology, formatting match other chapters?
  - Original Content check: No copy-paste; synthesized from multiple sources?
  - Deployment Readiness check: Compiles in Docusaurus? All links resolve? Images have alt text?
- [x] T027 Create scripts/validate-chapter.py (validation script):
  - Check front-matter completeness
  - Verify heading hierarchy (no skipping levels)
  - Count exercises (≥2 required)
  - Count diagrams (≥1 required)
  - Count code examples (≥3 required)
  - Validate links (internal + external)
  - Check image alt text
  - Estimate reading level (Flesch-Kincaid)
  - Output validation report
- [x] T028 Create docs/quality-gates.md documenting:
  - Pre-merge PR checks (what runs on every PR)
  - Build validation gates
  - Constitutional compliance gates
  - Code example execution gates (per OS)
  - What blocks merge vs. what is warning-only
- [x] T029 Create glossary.md (Docusaurus page) for:
  - Common robotics terms (ROS, node, topic, service, action, etc.)
  - AI/ML concepts (reinforcement learning, model, inference, etc.)
  - Simulation terms (physics engine, URDF, digital twin, etc.)
  - VLA terminology (vision, language, action, multimodal, etc.)
  - Links to chapters where terms are defined in context

### Reusable MDX Components

- [x] T030 [P] Create MDX component: docs/components/Tabs.tsx for:
  - OS-specific tab switching (Ubuntu, Windows, macOS)
  - Difficulty level tabs (Beginner, Intermediate, Advanced)
  - Alternative approaches/implementation tabs
- [x] T031 [P] Create MDX component: docs/components/Callout.tsx for:
  - Info (light blue background)
  - Warning (yellow/orange)
  - Danger (red)
  - Success (green)
  - Custom styling to match Docusaurus theme
- [x] T032 [P] Create MDX component: docs/components/CodeSandbox.tsx for:
  - Embeddable code examples
  - Copy-to-clipboard button
  - Download-code button
- [x] T033 Create docs/components/Exercise.tsx component for:
  - Step-by-step exercise rendering
  - Expected output section
  - "Show solution" toggle

**Checkpoint**: All design artifacts complete, validation framework in place, quality gates documented. Phase 3+ user story work can begin independently.

---

## Phase 3: User Story 1 - Module 1 Chapter Development (Priority: P1) 🎯 MVP

**Goal**: Create 6 complete ROS 2 foundational chapters teaching students from installation through distributed systems. Students can independently learn ROS 2 basics and complete hands-on exercises.

**Independent Test**: Writer creates Chapter 1.1, Docusaurus build succeeds, no broken links, constitution checklist passes, student can complete exercise without external resources.

**Why Priority P1**: Foundation module is critical—students cannot proceed to advanced modules without mastering ROS 2 basics.

### Module 1 Chapter Structure

#### Chapter 1.1: Welcome to ROS 2

- [x] T034 [US1] Create docs/module-1-ros2/1-1-welcome-to-ros2.md with:
  - Front-matter (title, sidebar_position: 1, difficulty: Beginner, time_hours: 2.5)
  - Learning objectives (3-5 specific, measurable skills)
  - Prerequisites (Python 3.10, basic Linux knowledge)
  - Core concepts (3 subsections: What is ROS 2? Why robotics? Why simulation?)
  - Installation section with [Tabs] for Ubuntu/Windows/macOS
  - Verification exercise (running ros2 --version, checking installation)
  - Quick tour of ROS 2 ecosystem (packages, nodes, topics overview)
  - Expected output (successful installation, verified commands)
  - Self-assessment checkpoint (5 questions on ROS 2 basics)
  - Connections (leads to Chapter 1.2: first node)
  - References (official ROS 2 docs, getting started guides)
  - Validation checklist completed
- [x] T035 [P] [US1] Create companion repo code: module-1-ros2/chapter-1-1/code/
  - install_ros2.py (automated installation validator)
  - troubleshooting.md (OS-specific common issues)
- [x] T036 [P] [US1] Create companion repo exercises: module-1-ros2/chapter-1-1/exercises/
  - exercise-1-installation.md (step-by-step install guide)
  - exercise-2-verification.md (verify installation with commands)
- [x] T037 [P] [US1] Create companion repo solutions: module-1-ros2/chapter-1-1/solutions/
  - solutions.md (expected outputs, common mistakes)
- [x] T038 [US1] Create diagram: static/img/module-1/ros2-architecture-overview.png
  - Shows ROS 2 ecosystem (nodes, middleware, tools)
  - Alt text: "Overview of ROS 2 architecture with distributed node communication"
  - Include in Chapter 1.1

#### Chapter 1.2: Creating Your First ROS 2 Node

- [x] T039 [US1] Create docs/module-1-ros2/1-2-first-ros2-node.md with:
  - Front-matter (sidebar_position: 2, difficulty: Beginner, time_hours: 3.5)
  - Learning objectives (publisher/subscriber pattern, node creation, communication)
  - Prerequisites (Chapter 1.1 complete, Python 3.10+)
  - Core concepts (3 subsections: Nodes, Publishers, Subscribers)
  - Hands-on exercises (≥2):
    - Exercise 1: Create publisher node (Python, publishes string messages)
    - Exercise 2: Create subscriber node (listens to publisher)
  - Code examples (≥3):
    - Simple publisher code (with inline comments)
    - Simple subscriber code
    - Launch both together and verify communication
  - Diagrams (≥1): Publisher-Subscriber architecture
  - Expected outputs (terminal output showing messages)
  - Self-assessment checkpoint (5 questions on pub-sub pattern)
  - Connections (leads to Chapter 1.3: services)
  - References (ROS 2 publisher/subscriber tutorials, examples)
- [x] T040 [P] [US1] Create companion repo: module-1-ros2/chapter-1-2/code/
  - simple_publisher.py (runnable publisher example)
  - simple_subscriber.py (runnable subscriber example)
  - package.xml (ROS 2 package configuration)
  - setup.py (Python package setup)
- [x] T041 [P] [US1] Create companion repo: module-1-ros2/chapter-1-2/exercises/
  - exercise-1-create-publisher.md (step-by-step)
  - exercise-2-create-subscriber.md (step-by-step)
- [x] T042 [P] [US1] Create companion repo: module-1-ros2/chapter-1-2/solutions/
  - solutions.md (expected behavior, debugging tips)
- [x] T043 [US1] Create diagram: static/img/module-1/publisher-subscriber-pattern.png
  - Shows publisher and subscriber nodes communicating via topic
  - Alt text: "Publisher and subscriber nodes connected via ROS 2 topic"

#### Chapter 1.3: Services

- [ ] T044 [US1] Create docs/module-1-ros2/1-3-services.md with:
  - Front-matter (sidebar_position: 3, difficulty: Beginner-Intermediate, time_hours: 3.5)
  - Learning objectives (request-response pattern, service servers, clients)
  - Prerequisites (Chapters 1.1-1.2 complete)
  - Core concepts (3 subsections: Request-Response, Service Servers, Service Clients)
  - Hands-on exercises (≥2):
    - Exercise 1: Create service server (processes requests)
    - Exercise 2: Create service client (sends requests)
  - Code examples (≥3): Service definition, server, client
  - Diagrams (≥1): Service call architecture
  - Expected outputs (terminal showing requests/responses)
  - Self-assessment checkpoint (5 questions on services)
  - Connections (leads to Chapter 1.4: actions)
- [ ] T045 [P] [US1] Create companion repo: module-1-ros2/chapter-1-3/code/
  - simple_service_server.py
  - simple_service_client.py
  - AddTwoInts.srv (service definition file)
- [ ] T046 [P] [US1] Create companion repo: module-1-ros2/chapter-1-3/exercises/ & solutions/
  - exercise-1-create-service-server.md
  - exercise-2-create-service-client.md
  - solutions.md
- [ ] T047 [US1] Create diagram: static/img/module-1/service-request-response.png

#### Chapter 1.4: Actions

- [ ] T048 [US1] Create docs/module-1-ros2/1-4-actions.md with:
  - Front-matter (sidebar_position: 4, difficulty: Intermediate, time_hours: 4)
  - Learning objectives (long-running tasks, action servers, clients, feedback)
  - Prerequisites (Chapters 1.1-1.3 complete)
  - Core concepts (3 subsections: Long-Running Tasks, Action Servers, Feedback)
  - Hands-on exercises (≥2):
    - Exercise 1: Create action server (long-running task with feedback)
    - Exercise 2: Create action client (sends goal, receives feedback)
  - Code examples (≥3): Action definition, server, client with feedback
  - Diagrams (≥1): Action architecture with feedback loop
  - Expected outputs (terminal showing goal, feedback, result)
  - Self-assessment checkpoint (5 questions on actions)
  - Connections (leads to Chapter 1.5: parameters)
- [ ] T049 [P] [US1] Create companion repo: module-1-ros2/chapter-1-4/code/
  - fibonacci_action_server.py
  - fibonacci_action_client.py
  - Fibonacci.action (action definition)
- [ ] T050 [P] [US1] Create companion repo: module-1-ros2/chapter-1-4/exercises/ & solutions/
  - exercise-1-create-action-server.md
  - exercise-2-create-action-client.md
  - solutions.md
- [ ] T051 [US1] Create diagram: static/img/module-1/action-server-client-flow.png

#### Chapter 1.5: Parameters

- [ ] T052 [US1] Create docs/module-1-ros2/1-5-parameters.md with:
  - Front-matter (sidebar_position: 5, difficulty: Intermediate, time_hours: 3)
  - Learning objectives (runtime configuration, parameter server, setting/getting parameters)
  - Prerequisites (Chapters 1.1-1.4 complete)
  - Core concepts (3 subsections: What are Parameters? Setting Parameters, Getting Parameters)
  - Hands-on exercises (≥2):
    - Exercise 1: Create node with parameters, modify at runtime
    - Exercise 2: Load parameters from YAML config file
  - Code examples (≥3): Parameter declaration, get, set, YAML config
  - Diagrams (≥1): Parameter server architecture
  - Expected outputs (terminal showing parameter changes)
  - Self-assessment checkpoint (5 questions on parameters)
  - Connections (leads to Chapter 1.6: launch files)
- [ ] T053 [P] [US1] Create companion repo: module-1-ros2/chapter-1-5/code/
  - node_with_parameters.py
  - params.yaml (parameter configuration file)
- [ ] T054 [P] [US1] Create companion repo: module-1-ros2/chapter-1-5/exercises/ & solutions/
  - exercise-1-create-parameterized-node.md
  - exercise-2-load-yaml-config.md
  - solutions.md
- [ ] T055 [US1] Create diagram: static/img/module-1/parameter-server-architecture.png

#### Chapter 1.6: Launch Files

- [ ] T056 [US1] Create docs/module-1-ros2/1-6-launch-files.md with:
  - Front-matter (sidebar_position: 6, difficulty: Intermediate, time_hours: 4)
  - Learning objectives (orchestrating multi-node systems, launch files, reusable configurations)
  - Prerequisites (Chapters 1.1-1.5 complete)
  - Core concepts (3 subsections: Why Launch Files? Launch File Syntax, Complex Orchestration)
  - Hands-on exercises (≥2):
    - Exercise 1: Create launch file for multi-node system
    - Exercise 2: Combine nodes with parameters and launch file
  - Code examples (≥3): Simple launch, launch with substitutions, launch with includes
  - Diagrams (≥1): Launch file execution flow
  - Expected outputs (multi-node system running from single launch command)
  - Self-assessment checkpoint (5 questions on launch files)
  - Module 1 Summary: What students now know (nodes, pub-sub, services, actions, parameters, orchestration)
  - Capstone hint: These skills form foundation for Module 2 (Gazebo/Unity) and beyond
  - Connections (leads to Module 2: simulation)
- [ ] T057 [P] [US1] Create companion repo: module-1-ros2/chapter-1-6/code/
  - multi_node_system.launch.py
  - turtlesim_example.launch.py (Gazebo-style example)
  - bringup_config.yaml
- [ ] T058 [P] [US1] Create companion repo: module-1-ros2/chapter-1-6/exercises/ & solutions/
  - exercise-1-create-launch-file.md
  - exercise-2-combine-systems.md
  - solutions.md
- [ ] T059 [US1] Create diagram: static/img/module-1/launch-file-orchestration.png

### Module 1 Integration & Validation

- [ ] T060 [US1] Create docs/module-1-ros2/index.md (Module 1 landing page):
  - Module overview (what students will learn)
  - Chapter progression (1.1 → 1.6)
  - Prerequisites (Python 3.10, Linux basics)
  - Time estimate (total hours for full module)
  - Tools & software (ROS 2 Humble, Ubuntu 22.04+, Windows 10/11, macOS 12+)
  - How to use (suggested reading order, optional chapters)
  - Module summary (skills mastered after completion)
- [ ] T061 [US1] Validate all Chapter 1 files:
  - Run: npm run build (ensure no Docusaurus errors)
  - Run: link checker (all internal/external links resolve)
  - Run: Markdown linter (heading hierarchy, formatting)
  - Run: scripts/validate-chapter.py for each chapter
  - Constitution checklist (all 6 principles pass for all chapters)
- [ ] T062 [US1] Test all Chapter 1 code examples on Ubuntu 22.04:
  - Clone companion repo
  - Run all Python examples (simple_publisher.py, etc.)
  - Verify expected outputs
- [ ] T063 [US1] Test all Chapter 1 code examples on Windows 10/11:
  - Run install scripts (windows-setup.ps1)
  - Run all Python examples with PowerShell
  - Verify expected outputs
- [ ] T064 [US1] Test all Chapter 1 code examples on macOS 12+:
  - Run install scripts (macos-setup.sh)
  - Run all Python examples with zsh
  - Verify expected outputs

**Checkpoint**: All 6 Module 1 chapters complete, tested on all 3 platforms, constitution-compliant, integrated into Docusaurus, companion repo code working. User Story 1 independently functional. Ready for Module 2.

---

## Phase 4: User Story 2 - Module 2 Chapter Development (Priority: P2)

**Goal**: Create 6 complete simulation chapters teaching Gazebo and Unity integration. Students can build robot models, simulate physics, and visualize with high-fidelity rendering.

**Independent Test**: Writer creates Chapter 2.1, all exercises pass on Ubuntu/Windows/macOS, Gazebo loads models, Unity visualization synchronized.

**Why Priority P2**: Simulation is essential before physical hardware; builds on Module 1 ROS 2 foundation.

**Dependencies**: User Story 1 (Module 1) must be complete—Module 2 chapters assume ROS 2 knowledge.

### Module 2 Chapter Structure

#### Chapter 2.1: Introduction to Robot Simulation

- [ ] T065 [US2] Create docs/module-2-simulation/2-1-intro-simulation.md
  - Front-matter (sidebar_position: 1, difficulty: Beginner, time_hours: 2.5)
  - Learning objectives (simulation concepts, why simulation, Gazebo basics)
  - Prerequisites (Module 1 complete)
  - Core concepts (3 subsections: Why Simulate? Simulation Tools, Gazebo Overview)
  - Installation [Tabs] for Ubuntu/Windows/macOS (Gazebo Fortress)
  - Verification exercise (launch Gazebo, view empty world)
  - Self-assessment checkpoint (5 questions on simulation)
  - Connections (leads to Chapter 2.2: building robot models)
- [ ] T066 [P] [US2] Create companion repo: module-2-simulation/chapter-2-1/code/
  - gazebo_launch.py (launch Gazebo from ROS 2)
  - install_gazebo.sh, install_gazebo.ps1, install_gazebo.sh (macOS)
- [ ] T067 [P] [US2] Create companion repo: module-2-simulation/chapter-2-1/exercises/ & solutions/
  - exercise-1-install-gazebo.md
  - exercise-2-launch-empty-world.md
  - solutions.md
- [ ] T068 [US2] Create diagram: static/img/module-2/gazebo-architecture.png

#### Chapter 2.2: Building Your First Robot Model

- [ ] T069 [US2] Create docs/module-2-simulation/2-2-first-robot-model.md
  - Front-matter (sidebar_position: 2, difficulty: Beginner-Intermediate, time_hours: 4.5)
  - Learning objectives (URDF/SDF, creating robot models, simulation ready robots)
  - Prerequisites (Chapter 2.1 complete)
  - Core concepts (3 subsections: URDF Basics, Building Models, Testing in Gazebo)
  - Hands-on exercises (≥2):
    - Exercise 1: Create simple robot URDF (2-link robot)
    - Exercise 2: Load and verify in Gazebo
  - Code examples (≥3): URDF structure, link definitions, joint definitions
  - Diagrams (≥1): URDF structure visualization
  - Self-assessment checkpoint
  - Connections (leads to Chapter 2.3: adding sensors)
- [ ] T070 [P] [US2] Create companion repo: module-2-simulation/chapter-2-2/robot_models/
  - simple_robot.urdf
  - simple_robot.sdf
  - simple_robot_description.py (load into ROS 2)
- [ ] T071 [P] [US2] Create companion repo: module-2-simulation/chapter-2-2/exercises/ & solutions/
  - exercise-1-create-urdf.md
  - exercise-2-load-in-gazebo.md
  - solutions.md
- [ ] T072 [US2] Create diagram: static/img/module-2/urdf-structure-example.png

#### Chapter 2.3: Adding Sensors to Your Robot

- [ ] T073 [US2] Create docs/module-2-simulation/2-3-adding-sensors.md
  - Front-matter (sidebar_position: 3, difficulty: Intermediate, time_hours: 4)
  - Learning objectives (camera, lidar, IMU sensors in simulation)
  - Prerequisites (Chapter 2.2 complete)
  - Core concepts (3 subsections: Sensor Types, Sensor in URDF, Reading Sensor Data)
  - Hands-on exercises (≥2):
    - Exercise 1: Add camera to robot URDF
    - Exercise 2: Subscribe to camera/lidar topics in ROS 2
  - Code examples (≥3): Sensor URDF, ROS 2 subscriber for sensor data
  - Diagrams (≥1): Sensor integration architecture
  - Self-assessment checkpoint
  - Connections (leads to Chapter 2.4: building worlds)
- [ ] T074 [P] [US2] Create companion repo: module-2-simulation/chapter-2-3/robot_models/
  - robot_with_sensors.urdf
  - camera_plugin.xml
- [ ] T075 [P] [US2] Create companion repo: module-2-simulation/chapter-2-3/code/
  - sensor_subscriber.py (read camera/lidar data)
- [ ] T076 [P] [US2] Create companion repo: module-2-simulation/chapter-2-3/exercises/ & solutions/
- [ ] T077 [US2] Create diagram: static/img/module-2/robot-with-sensors.png

#### Chapter 2.4: Building Worlds in Gazebo

- [ ] T078 [US2] Create docs/module-2-simulation/2-4-building-worlds.md
  - Front-matter (sidebar_position: 4, difficulty: Intermediate, time_hours: 3.5)
  - Learning objectives (custom environments, world files, simulation scenarios)
  - Prerequisites (Chapter 2.3 complete)
  - Core concepts (3 subsections: Gazebo World Format, Adding Objects, Lighting & Physics)
  - Hands-on exercises (≥2):
    - Exercise 1: Create custom world with obstacles
    - Exercise 2: Load robot into custom world
  - Code examples (≥3): World file structure, adding models, configuring physics
  - Diagrams (≥1): World file architecture
  - Self-assessment checkpoint
  - Connections (leads to Chapter 2.5: Unity visualization)
- [ ] T079 [P] [US2] Create companion repo: module-2-simulation/chapter-2-4/worlds/
  - warehouse_world.world
  - office_world.world
  - obstacles.world
- [ ] T080 [P] [US2] Create companion repo: module-2-simulation/chapter-2-4/exercises/ & solutions/
- [ ] T081 [US2] Create diagram: static/img/module-2/gazebo-world-structure.png

#### Chapter 2.5: Unity for Robot Visualization

- [ ] T082 [US2] Create docs/module-2-simulation/2-5-unity-visualization.md
  - Front-matter (sidebar_position: 5, difficulty: Intermediate, time_hours: 4.5)
  - Learning objectives (ROS 2-Unity bridge, real-time visualization, synchronization)
  - Prerequisites (Chapter 2.4 complete, Unity 2022 LTS installed)
  - Core concepts (3 subsections: ROS 2-Unity Communication, Synchronizing Physics, Real-Time Updates)
  - Hands-on exercises (≥2):
    - Exercise 1: Set up ROS 2-Unity bridge
    - Exercise 2: Synchronize Gazebo physics with Unity visualization
  - Code examples (≥3): ROS 2 message structures for Unity, C# subscriber script
  - Diagrams (≥1): ROS 2-Unity architecture
  - [Tabs] for Windows/Linux/macOS Unity setup
  - Self-assessment checkpoint
  - Connections (leads to Chapter 2.6: advanced Unity)
- [ ] T083 [P] [US2] Create companion repo: module-2-simulation/chapter-2-5/code/
  - ros2_unity_bridge.py
  - UnityVisualizerSubscriber.cs (C# script for Unity)
- [ ] T084 [P] [US2] Create companion repo: module-2-simulation/chapter-2-5/exercises/ & solutions/
- [ ] T085 [US2] Create diagram: static/img/module-2/ros2-unity-bridge-architecture.png

#### Chapter 2.6: Advanced Unity Features

- [ ] T086 [US2] Create docs/module-2-simulation/2-6-advanced-unity.md
  - Front-matter (sidebar_position: 6, difficulty: Intermediate-Advanced, time_hours: 4)
  - Learning objectives (interactive visualization, teleoperation, rendering optimization)
  - Prerequisites (Chapter 2.5 complete)
  - Core concepts (3 subsections: Sensor Visualization, Teleoperation UI, Performance Optimization)
  - Hands-on exercises (≥2):
    - Exercise 1: Visualize sensor data in Unity (camera feed overlay)
    - Exercise 2: Add teleoperation UI to control robot
  - Code examples (≥3): Unity UI scripting, real-time sensor rendering, ROS 2 command sending
  - Diagrams (≥1): Advanced visualization architecture
  - Self-assessment checkpoint
  - Module 2 Summary: Digital twin capabilities mastered
  - Connections (leads to Module 3: AI/Isaac)
- [ ] T087 [P] [US2] Create companion repo: module-2-simulation/chapter-2-6/code/
  - AdvancedVisualizerUI.cs (teleoperation UI)
  - SensorOverlay.cs (render camera feed)
- [ ] T088 [P] [US2] Create companion repo: module-2-simulation/chapter-2-6/exercises/ & solutions/
- [ ] T089 [US2] Create diagram: static/img/module-2/advanced-unity-ui.png

### Module 2 Integration & Validation

- [ ] T090 [US2] Create docs/module-2-simulation/index.md (Module 2 landing page)
  - Module overview, prerequisites (Module 1), tools (Gazebo Fortress, Unity 2022)
  - Progression visual showing prerequisites from Module 1
- [ ] T091 [US2] Validate all Chapter 2 files (Docusaurus build, links, Markdown, Constitution checklist)
- [ ] T092 [US2] Test all Chapter 2 code examples on Ubuntu 22.04 (Gazebo + ROS 2 bridge)
- [ ] T093 [US2] Test all Chapter 2 code examples on Windows 10/11 (Unity + ROS 2 bridge)
- [ ] T094 [US2] Test all Chapter 2 code examples on macOS 12+ (Unity on Mac + ROS 2)

**Checkpoint**: All 6 Module 2 chapters complete, tested on all 3 platforms, Gazebo integration verified, Unity bridge functional. User Story 2 independently functional. Ready for Module 3.

---

## Phase 5: User Story 3 - Module 3 Chapter Development (Priority: P3)

**Goal**: Create 5 complete AI chapters teaching NVIDIA Isaac Sim, reinforcement learning, and AI model deployment. Students can train autonomous behaviors in simulation.

**Independent Test**: Writer creates Chapter 3.1, Isaac Sim installs, sample RL environment trains, model deploys to ROS 2.

**Why Priority P3**: AI capabilities require strong ROS 2 and simulation foundations from Modules 1-2.

**Dependencies**: User Stories 1-2 must be complete.

### Module 3 Chapter Structure

#### Chapter 3.1: Introduction to NVIDIA Isaac Sim

- [ ] T095 [US3] Create docs/module-3-isaac/3-1-intro-isaac-sim.md
  - Front-matter (sidebar_position: 1, difficulty: Intermediate, time_hours: 3.5)
  - Learning objectives (Isaac Sim features, AI-ready environments, hardware requirements)
  - Prerequisites (Modules 1-2 complete, GPU: RTX 3060+ or GTX 1060+)
  - Core concepts (3 subsections: Why Isaac Sim? AI Training, Environment Setup)
  - Installation [Tabs] for Linux/Windows/macOS (Isaac Sim 2023.1)
  - Hardware requirements checklist
  - ROS 2 connection verification
  - Self-assessment checkpoint
  - Connections (leads to Chapter 3.2: RL basics)
- [ ] T096 [P] [US3] Create companion repo: module-3-isaac/chapter-3-1/code/
  - isaac_sim_launcher.py
  - check_gpu_availability.py
- [ ] T097 [P] [US3] Create companion repo: module-3-isaac/chapter-3-1/exercises/ & solutions/
- [ ] T098 [US3] Create diagram: static/img/module-3/isaac-sim-architecture.png

#### Chapter 3.2: Reinforcement Learning Basics

- [ ] T099 [US3] Create docs/module-3-isaac/3-2-rl-basics.md
  - Front-matter (sidebar_position: 2, difficulty: Intermediate, time_hours: 4.5)
  - Learning objectives (RL concepts, agent-environment loop, training in Isaac Sim)
  - Prerequisites (Chapter 3.1 complete)
  - Core concepts (3 subsections: RL Fundamentals, Agent-Environment Interaction, Isaac RL Training)
  - Hands-on exercises (≥2):
    - Exercise 1: Train simple navigation task
    - Exercise 2: Monitor training progress and evaluate policy
  - Code examples (≥3): Environment setup, agent configuration, training loop
  - Diagrams (≥1): RL training loop architecture
  - Self-assessment checkpoint
  - Connections (leads to Chapter 3.3: scaling RL)
- [ ] T100 [P] [US3] Create companion repo: module-3-isaac/chapter-3-2/isaac_scenes/
  - simple_navigation_task.usd (USD scene)
  - task_config.yaml
- [ ] T101 [P] [US3] Create companion repo: module-3-isaac/chapter-3-2/code/
  - navigation_agent.py (RL agent)
  - train_navigation.py (training script)
- [ ] T102 [P] [US3] Create companion repo: module-3-isaac/chapter-3-2/exercises/ & solutions/
- [ ] T103 [US3] Create diagram: static/img/module-3/rl-training-loop.png

#### Chapter 3.3: Scaling Up RL Training

- [ ] T104 [US3] Create docs/module-3-isaac/3-3-scaling-rl.md
  - Front-matter (sidebar_position: 3, difficulty: Advanced, time_hours: 5)
  - Learning objectives (parallelization, domain randomization, efficient training)
  - Prerequisites (Chapter 3.2 complete)
  - Core concepts (3 subsections: Parallel Training, Domain Randomization, Optimization)
  - Hands-on exercises (≥2):
    - Exercise 1: Configure parallel environments
    - Exercise 2: Apply domain randomization and train
  - Code examples (≥3): Parallel config, randomization parameters, monitoring multi-worker training
  - Diagrams (≥1): Parallel training architecture
  - Self-assessment checkpoint
  - Connections (leads to Chapter 3.4: manipulation)
- [ ] T105 [P] [US3] Create companion repo: module-3-isaac/chapter-3-3/code/
  - parallel_training.py
  - domain_randomization_config.yaml
- [ ] T106 [P] [US3] Create companion repo: module-3-isaac/chapter-3-3/exercises/ & solutions/
- [ ] T107 [US3] Create diagram: static/img/module-3/parallel-training-architecture.png

#### Chapter 3.4: Robot Manipulation with AI

- [ ] T108 [US3] Create docs/module-3-isaac/3-4-robot-manipulation.md
  - Front-matter (sidebar_position: 4, difficulty: Advanced, time_hours: 5.5)
  - Learning objectives (manipulation tasks, grasping, vision-based control)
  - Prerequisites (Chapter 3.3 complete)
  - Core concepts (3 subsections: Manipulation Tasks, Grasping Policies, Vision Integration)
  - Hands-on exercises (≥2):
    - Exercise 1: Train grasping policy
    - Exercise 2: Test vision-based object identification + grasping
  - Code examples (≥3): Manipulation task definition, grasping reward, vision integration
  - Diagrams (≥1): Manipulation task architecture
  - Self-assessment checkpoint
  - Connections (leads to Chapter 3.5: deployment)
- [ ] T109 [P] [US3] Create companion repo: module-3-isaac/chapter-3-4/isaac_scenes/
  - grasping_task.usd
  - objects_for_grasping.usd
- [ ] T110 [P] [US3] Create companion repo: module-3-isaac/chapter-3-4/code/
  - grasping_agent.py
  - vision_based_grasping.py
- [ ] T111 [P] [US3] Create companion repo: module-3-isaac/chapter-3-4/exercises/ & solutions/
- [ ] T112 [US3] Create diagram: static/img/module-3/grasping-task-architecture.png

#### Chapter 3.5: Deploying AI Models to ROS 2

- [ ] T113 [US3] Create docs/module-3-isaac/3-5-deploying-ai-models.md
  - Front-matter (sidebar_position: 5, difficulty: Advanced, time_hours: 4.5)
  - Learning objectives (model export, inference in ROS 2, sim-to-real considerations)
  - Prerequisites (Chapter 3.4 complete)
  - Core concepts (3 subsections: Model Export, ROS 2 Inference Server, Sim-to-Real Transfer)
  - Hands-on exercises (≥2):
    - Exercise 1: Export trained model to ONNX
    - Exercise 2: Create ROS 2 node that runs inference
  - Code examples (≥3): Model export, ROS 2 inference service, input/output handling
  - Diagrams (≥1): Inference pipeline architecture
  - Module 3 Summary: AI training and deployment capabilities mastered
  - Connections (leads to Module 4: Vision-Language-Action)
  - Self-assessment checkpoint
- [ ] T114 [P] [US3] Create companion repo: module-3-isaac/chapter-3-5/code/
  - export_model.py
  - ros2_inference_server.py
  - model_manager.py
- [ ] T115 [P] [US3] Create companion repo: module-3-isaac/chapter-3-5/exercises/ & solutions/
- [ ] T116 [US3] Create diagram: static/img/module-3/ai-deployment-pipeline.png

### Module 3 Integration & Validation

- [ ] T117 [US3] Create docs/module-3-isaac/index.md (Module 3 landing page)
  - Module overview, prerequisites (Modules 1-2), hardware requirements, tools
- [ ] T118 [US3] Validate all Chapter 3 files (Docusaurus, Constitution checklist)
- [ ] T119 [US3] Test Isaac Sim environments on Linux (GPU, training)
- [ ] T120 [US3] Test Isaac Sim environments on Windows (GPU, training)

**Checkpoint**: All 5 Module 3 chapters complete, tested on Linux/Windows, RL training verified, model deployment to ROS 2 functional. User Story 3 independently functional. Ready for Module 4.

---

## Phase 6: User Story 4 - Module 4 Chapter Development (Priority: P4)

**Goal**: Create 6 complete VLA (Vision-Language-Action) chapters integrating vision, language, and action for natural language robot control. Capstone project demonstrates full system integration.

**Independent Test**: Writer creates Chapter 4.1, student can issue natural language command and see robot execute action in simulation.

**Why Priority P4**: VLA is cutting-edge; requires mastery of all prior modules (1-3).

**Dependencies**: User Stories 1-3 must be complete.

### Module 4 Chapter Structure

#### Chapter 4.1: Introduction to VLA Models

- [ ] T121 [US4] Create docs/module-4-vla/4-1-intro-vla.md
  - Front-matter (sidebar_position: 1, difficulty: Intermediate, time_hours: 3.5)
  - Learning objectives (VLA architecture, vision-language-action components, use cases)
  - Prerequisites (Modules 1-3 complete)
  - Core concepts (3 subsections: What is VLA? Architecture Components, Real-World Applications)
  - Setup & verification (test local LLM, vision model, action executor)
  - Self-assessment checkpoint
  - Connections (leads to Chapter 4.2: vision for robotics)
- [ ] T122 [P] [US4] Create companion repo: module-4-vla/chapter-4-1/code/
  - vla_system_test.py (verify components)
  - local_llm_launcher.py
- [ ] T123 [P] [US4] Create companion repo: module-4-vla/chapter-4-1/exercises/ & solutions/
- [ ] T124 [US4] Create diagram: static/img/module-4/vla-architecture-components.png

#### Chapter 4.2: Vision for Robotics

- [ ] T125 [US4] Create docs/module-4-vla/4-2-vision-robotics.md
  - Front-matter (sidebar_position: 2, difficulty: Intermediate-Advanced, time_hours: 5)
  - Learning objectives (object detection, scene understanding, vision models for robotics)
  - Prerequisites (Chapter 4.1 complete)
  - Core concepts (3 subsections: Computer Vision Basics, Object Detection in Robotics, Scene Understanding)
  - Hands-on exercises (≥2):
    - Exercise 1: Run object detection on robot camera feed
    - Exercise 2: Identify objects and scenes in environment
  - Code examples (≥3): Vision model inference, ROS 2 image integration, result visualization
  - Diagrams (≥1): Vision pipeline architecture
  - Self-assessment checkpoint
  - Connections (leads to Chapter 4.3: language understanding)
- [ ] T126 [P] [US4] Create companion repo: module-4-vla/chapter-4-2/code/
  - object_detection_node.py (YOLOv8 or similar)
  - scene_understanding.py
- [ ] T127 [P] [US4] Create companion repo: module-4-vla/chapter-4-2/exercises/ & solutions/
- [ ] T128 [US4] Create diagram: static/img/module-4/vision-pipeline.png

#### Chapter 4.3: Language Understanding

- [ ] T129 [US4] Create docs/module-4-vla/4-3-language-understanding.md
  - Front-matter (sidebar_position: 3, difficulty: Intermediate-Advanced, time_hours: 5)
  - Learning objectives (speech recognition, NLP, command parsing, accessible LLMs)
  - Prerequisites (Chapter 4.2 complete)
  - Core concepts (3 subsections: Speech-to-Text, Natural Language Processing, Local LLM Options)
  - Hands-on exercises (≥2):
    - Exercise 1: Set up speech recognition (Whisper)
    - Exercise 2: Parse natural language commands with local LLM
  - Code examples (≥3): Whisper for speech-to-text, LLM inference, command extraction
  - Diagrams (≥1): Language processing pipeline
  - [Tabs] for local LLM options (Llama 2, Mistral, etc.)
  - Self-assessment checkpoint
  - Connections (leads to Chapter 4.4: language to actions)
- [ ] T130 [P] [US4] Create companion repo: module-4-vla/chapter-4-3/code/
  - speech_recognizer.py (Whisper)
  - command_parser.py (LLM-based parsing)
  - local_llm_runner.py
- [ ] T131 [P] [US4] Create companion repo: module-4-vla/chapter-4-3/exercises/ & solutions/
- [ ] T132 [US4] Create diagram: static/img/module-4/language-processing-pipeline.png

#### Chapter 4.4: From Language to Actions

- [ ] T133 [US4] Create docs/module-4-vla/4-4-language-to-actions.md
  - Front-matter (sidebar_position: 4, difficulty: Advanced, time_hours: 5.5)
  - Learning objectives (task planning, translating high-level to low-level commands, execution)
  - Prerequisites (Chapter 4.3 complete)
  - Core concepts (3 subsections: Task Planning, Motion Planning, Execution in Simulation)
  - Hands-on exercises (≥2):
    - Exercise 1: Translate "pick up object" to robot motion plan
    - Exercise 2: Execute planned motion in ROS 2 + Gazebo
  - Code examples (≥3): Task planning logic, motion planning integration, ROS 2 action execution
  - Diagrams (≥1): Task planning and execution flow
  - Self-assessment checkpoint
  - Connections (leads to Chapter 4.5: end-to-end VLA)
- [ ] T134 [P] [US4] Create companion repo: module-4-vla/chapter-4-4/code/
  - task_planner.py (high-level to low-level translation)
  - motion_planner.py
  - action_executor.py
- [ ] T135 [P] [US4] Create companion repo: module-4-vla/chapter-4-4/exercises/ & solutions/
- [ ] T136 [US4] Create diagram: static/img/module-4/task-planning-execution-flow.png

#### Chapter 4.5: End-to-End VLA Integration

- [ ] T137 [US4] Create docs/module-4-vla/4-5-end-to-end-vla.md
  - Front-matter (sidebar_position: 5, difficulty: Advanced, time_hours: 6)
  - Learning objectives (full pipeline, voice to robot action, testing and debugging)
  - Prerequisites (Chapter 4.4 complete)
  - Core concepts (3 subsections: Pipeline Architecture, Latency Optimization, Real-World Considerations)
  - Hands-on exercises (≥2):
    - Exercise 1: Connect all components (vision + language + action)
    - Exercise 2: Issue voice commands and observe robot behavior
  - Code examples (≥3): End-to-end pipeline, error handling, logging
  - Diagrams (≥1): Complete VLA system architecture
  - Self-assessment checkpoint
  - Connections (leads to Chapter 4.6: capstone)
- [ ] T138 [P] [US4] Create companion repo: module-4-vla/chapter-4-5/code/
  - vla_pipeline.py (orchestrate all components)
  - error_handler.py
  - performance_monitor.py
- [ ] T139 [P] [US4] Create companion repo: module-4-vla/chapter-4-5/exercises/ & solutions/
- [ ] T140 [US4] Create diagram: static/img/module-4/vla-system-architecture.png

#### Chapter 4.6: Capstone Project

- [ ] T141 [US4] Create docs/module-4-vla/4-6-capstone-project.md
  - Front-matter (sidebar_position: 6, difficulty: Advanced, time_hours: 10-12)
  - Learning objectives (integrate all 4 modules, build complete application, document results)
  - Prerequisites (Chapters 4.1-4.5 complete; all Modules 1-3 mastered)
  - Capstone project brief (e.g., "Build a kitchen robot that responds to voice commands to pick up objects and place them in specified locations")
  - Project requirements:
    - Use ROS 2 for all communication (Module 1 skills)
    - Simulate in Gazebo + visualize in Unity (Module 2 skills)
    - Train/deploy AI model for autonomous behavior (Module 3 skills)
    - Accept natural language commands via VLA (Module 4 skills)
  - Hands-on exercises (≥2):
    - Exercise 1: Design system architecture
    - Exercise 2: Implement and test capstone system
  - Expected deliverables (working system, documentation, demo)
  - Module 4 Summary: State-of-the-art robotics capabilities
  - Textbook Conclusion: Pathway to advanced robotics research, career opportunities, open problems
  - Self-assessment checkpoint (reflection questions on learning journey)
  - References (research papers, industry resources, continuing education)
- [ ] T142 [P] [US4] Create companion repo: module-4-vla/chapter-4-6/code/
  - capstone_skeleton.py (starter template)
  - capstone_example_solution.py (reference implementation)
  - demo_script.py (run complete system)
- [ ] T143 [P] [US4] Create companion repo: module-4-vla/chapter-4-6/exercises/ & solutions/
  - exercise-1-system-design.md
  - exercise-2-implementation.md
  - solutions.md (reference architecture)
- [ ] T144 [US4] Create diagram: static/img/module-4/capstone-system-architecture.png
- [ ] T145 [US4] Create docs/module-4-vla/4-7-further-learning.md (optional advanced topics)
  - Sim-to-real transfer techniques
  - Real robot deployment considerations
  - Research frontiers in VLA
  - Career pathways in robotics + AI

### Module 4 Integration & Validation

- [ ] T146 [US4] Create docs/module-4-vla/index.md (Module 4 landing page)
  - Module overview, prerequisites (Modules 1-3), capstone project preview
- [ ] T147 [US4] Validate all Chapter 4 files (Docusaurus, Constitution checklist)
- [ ] T148 [US4] Test Chapter 4 code examples (speech recognition, LLM, vision integration)
- [ ] T149 [US4] Validate capstone project (all 4 modules integrated, student can complete independently)

**Checkpoint**: All 6 Module 4 chapters complete, tested, capstone project functional. All 4 user stories complete. Textbook fully functional.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements and validations affecting all chapters

### Documentation & Reference Materials

- [ ] T150 Create docs/glossary.md with complete robotics + AI terminology
- [ ] T151 Create docs/resources.md with:
  - Recommended textbooks and papers per module
  - Official documentation links (ROS 2, Gazebo, Isaac Sim, Unity)
  - Community forums and Q&A resources
  - Career resources and advanced learning paths
- [ ] T152 [P] Create docs/troubleshooting.md with:
  - OS-specific installation issues (Ubuntu/Windows/macOS)
  - Common ROS 2 errors and solutions
  - Gazebo/Unity synchronization issues
  - Isaac Sim GPU/performance issues
  - Cross-platform code execution issues
- [ ] T153 Create docs/faq.md (frequently asked questions from chapters)
- [ ] T154 Create docs/errata.md for bug reports and corrections (auto-updated)

### Final Validation & Testing

- [ ] T155 [P] Run full Docusaurus build: npm run build (must complete in <30s)
- [ ] T156 [P] Run full link validation (all internal + external links resolve)
- [ ] T157 [P] Run Markdown linter on all chapters (.mdlintrc compliance)
- [ ] T158 [P] Run code snippet syntax validation (Python, Bash, YAML, JSON)
- [ ] T159 [P] Run Lighthouse accessibility scan (target: 90+ score)
- [ ] T160 Validate all 23 chapters against Constitution checklist (all 6 principles)
- [ ] T161 Cross-check all chapter connections (1.1→1.2→...→4.6 progression coherent)
- [ ] T162 Verify companion repo mirrors textbook structure (all code present, organized correctly)

### Code Quality & Performance

- [ ] T163 [P] Verify all Python code examples:
  - Static syntax check (pylint/flake8)
  - No hardcoded credentials or secrets
  - Example runs on Ubuntu 22.04 without external setup
- [ ] T164 [P] Optimize all images in static/img/:
  - JPEG/PNG optimization (lossless or acceptable lossy)
  - Target: all images <500KB (total <50MB)
  - Responsive sizing (include @2x variants)
- [ ] T165 [P] Verify all diagrams:
  - Alt text present and descriptive (≥20 chars)
  - File names descriptive and organized per module
  - Format consistent (PNG, SVG, or specified in naming)

### GitHub Pages Deployment & CI/CD

- [ ] T166 Test GitHub Pages build: `npm run build && npm run serve` locally
- [ ] T167 Verify GitHub Actions workflows:
  - Build workflow runs on every PR
  - Deploy workflow runs on merge to main
  - All checks pass (build, links, Markdown, accessibility, constitutional)
- [ ] T168 Set up GitHub Pages domain (if custom domain used)
- [ ] T169 Create deployment runbook (how to publish new version, rollback, etc.)
- [ ] T170 Configure GitHub Discussions for reader Q&A (optional)

### Team Documentation & Onboarding

- [ ] T171 Create CONTRIBUTING.md guide:
  - How to add new chapters
  - Chapter template usage
  - Review process
  - Validation checklist before PR
- [ ] T172 Create MAINTAINERS.md with roles and responsibilities
- [ ] T173 Create VERSION.md documenting:
  - Targeted software versions (ROS 2 Humble, Gazebo Fortress, etc.)
  - Content version history
  - Breaking changes between versions
- [ ] T174 Create ROADMAP.md for future content:
  - Planned Module 5 (real robot hardware)
  - Planned upgrade guides (ROS 2 Jazzy, Unity 2023, Isaac 2024)
  - Community contribution opportunities
- [ ] T175 Record short onboarding video (5 min):
  - How to use textbook for self-study
  - How to use for classroom teaching
  - Capstone project setup walkthrough

### Final Checklist & Sign-Off

- [ ] T176 [P] Verify all 23 chapters present and complete
- [ ] T177 [P] Verify all 23 chapters compile in Docusaurus
- [ ] T178 [P] Verify all companion code examples run on all 3 platforms
- [ ] T179 [P] Verify all 23 chapters pass Constitution compliance
- [ ] T180 [P] Verify GitHub Pages live and accessible
- [ ] T181 [P] Verify all CI/CD checks passing on main branch
- [ ] T182 Create final release notes (v1.0.0) summarizing:
  - 23 chapters across 4 modules
  - Total estimated learning time (e.g., 120-150 hours)
  - System requirements and software versions
  - Companion code and robot models
  - Known limitations and future work
- [ ] T183 [P] Announce textbook on robotics communities and social media
- [ ] T184 Create feedback survey (for future improvements)

**Checkpoint**: Textbook fully validated, deployed, documented. Ready for publication and community use.

---

## Dependencies & Execution Order

### Phase Dependencies

| Phase | Description | Blocks |
|-------|-------------|--------|
| **Phase 1** | Setup (Docusaurus, CI/CD, templates) | All other phases |
| **Phase 2** | Foundational (Design artifacts, contracts, quality framework) | All user stories |
| **Phase 3** | User Story 1 - Module 1 (ROS 2 chapters) | US2, US3, US4 (prerequisite) |
| **Phase 4** | User Story 2 - Module 2 (Simulation) | US3, US4 (prerequisite) |
| **Phase 5** | User Story 3 - Module 3 (AI/Isaac) | US4 (prerequisite) |
| **Phase 6** | User Story 4 - Module 4 (VLA + Capstone) | Polish phase |
| **Phase 7** | Polish & Cross-Cutting Concerns | Deployment |

### User Story Prerequisites

- **US1 (Module 1)**: Depends only on Phase 2 (Foundational) → Can start immediately after Phase 2
- **US2 (Module 2)**: Depends on US1 completion (students need ROS 2 foundation)
- **US3 (Module 3)**: Depends on US1 + US2 completion (needs ROS 2 + simulation skills)
- **US4 (Module 4)**: Depends on US1 + US2 + US3 completion (capstone requires all prior modules)

### Parallel Opportunities

**Team of 4 developers** (suggested allocation):

1. **Developer 1**: Phase 1 (Setup) + Phase 2 (Foundational)
2. Once Phase 1-2 complete, **split team**:
   - **Developer 1**: Module 1 (US1)
   - **Developer 2**: Start Phase 2 Foundational items 2-3 in parallel + then assist US1
   - **Developer 3**: Assist US1 testing (cross-platform validation)
3. After US1 complete:
   - **Developer 1**: Module 2 (US2) writing
   - **Developer 2**: Module 2 companion code
   - **Developer 3**: Module 2 cross-platform testing
   - **Developer 4**: Start Module 3 research
4. Continue pattern for US3 and US4

**Realistic timeline** (single developer):
- Phase 1: 1 week
- Phase 2: 2 weeks
- Phase 3 (US1): 4-5 weeks
- Phase 4 (US2): 4-5 weeks
- Phase 5 (US3): 3-4 weeks
- Phase 6 (US4): 5-6 weeks
- Phase 7 (Polish): 1-2 weeks
- **Total**: ~20-25 weeks (5-6 months)

---

## Parallel Example: Phase 1 Setup

**Tasks that can run in parallel**:
```
T002: Install Node.js dependencies
T003: Configure docusaurus.config.js
T005: Set up static/ directory structure
T010: Create GitHub Actions build workflow
T015: Create install scripts (Ubuntu/Windows/macOS)
```

**Run in sequence after parallels complete**:
```
T001: Initialize Docusaurus
→ T004: Create sidebars.js
→ T006: Create landing page
→ T007: Create preface/
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

**Deliverable**: Module 1 (ROS 2) fully functional and publishable

1. Complete Phase 1: Setup (✅ Docusaurus + GitHub Actions working)
2. Complete Phase 2: Foundational (✅ Design artifacts, validation framework)
3. Complete Phase 3: US1 - Module 1 (✅ All 6 ROS 2 chapters written, tested, published)
4. **STOP and VALIDATE**: Test MVP independently
5. Deploy to GitHub Pages and announce: "Physical AI & Humanoid Robotics Textbook - Module 1 (ROS 2) now live!"

**MVP Success Criteria**:
- All 6 Module 1 chapters compile and publish
- All code examples run on Ubuntu/Windows/macOS
- Students can complete Chapter 1.6 launch files exercise independently
- GitHub Pages live and Lighthouse 90+

### Incremental Delivery Strategy

After MVP, add modules incrementally:

1. **Release 1.0.0** (MVP): Module 1 only (ROS 2)
2. **Release 1.1.0** (2-3 weeks later): Add Module 2 (Simulation/Gazebo/Unity)
3. **Release 1.2.0** (3-4 weeks later): Add Module 3 (AI/Isaac)
4. **Release 2.0.0** (3-4 weeks later): Add Module 4 (VLA + Capstone)

Each release:
- Adds new module chapters
- Includes upgrade guides for software versions
- Fixes errata from community feedback
- Improves accessibility/readability based on reader feedback

---

## Success Criteria Summary

| Metric | Target | Verification |
|--------|--------|--------------|
| **Chapters** | 23 total (6+6+5+6) | Count in docs/, all in sidebars.js |
| **Build Time** | <30 seconds | npm run build with timing |
| **Docusaurus Compilation** | 100% success | npm run build passes on main |
| **Broken Links** | 0 external, 0 internal | link-checker report |
| **Code Examples** | 100% runnable on all 3 OS | Test matrix results |
| **Lighthouse Score** | 90+ | Lighthouse audit report |
| **Constitution Compliance** | 100% of chapters | Checklist pass rate |
| **Exercises** | ≥2 per chapter | Count in each chapter |
| **Diagrams** | ≥1 per chapter + alt text | static/img/ inventory |
| **Companion Repo** | Code for all chapters | module-X/chapter-X-Y/ sync |
| **Reference Platform** | Ubuntu 22.04, Windows 10/11, macOS 12+ | Tested and documented |
| **GitHub Pages** | Live and responsive | https://[user].github.io/[repo]/ |
| **CI/CD** | All checks passing on main | GitHub Actions dashboard |
| **Documentation** | Glossary, FAQ, Troubleshooting, Resources | docs/ files present |
| **Maintainability** | CONTRIBUTING.md, MAINTAINERS.md, ROADMAP.md | Onboarding docs present |

---

## Total Task Count

- **Phase 1 (Setup)**: 18 tasks
- **Phase 2 (Foundational)**: 11 tasks
- **Phase 3 (US1 - Module 1)**: 26 tasks
- **Phase 4 (US2 - Module 2)**: 26 tasks
- **Phase 5 (US3 - Module 3)**: 22 tasks
- **Phase 6 (US4 - Module 4)**: 25 tasks
- **Phase 7 (Polish)**: 35 tasks

**TOTAL: 163 tasks**

---

## Notes

- Each task is specific and actionable
- File paths are absolute and concrete
- Dependencies clearly marked
- [P] tasks can run in parallel (different files, no dependencies within phases)
- [Story] labels enable independent story development
- Each user story is independently testable and completable
- Validation checkpoints prevent quality regressions
- Team can stop at any checkpoint to deploy/demo

---

**Task Generation Status**: ✅ **READY FOR EXECUTION**

This task list is immediately executable. Developers can begin with Phase 1 setup, and work through phases sequentially or parallelize with appropriate team structure. Each task is scoped to a specific, verifiable deliverable.

