# Quick Start Guide: Physical AI & Humanoid Robotics Textbook

**Date**: 2025-12-19
**Feature**: specs/001-textbook-chapter-specs/
**Status**: Complete

## Overview

This guide provides a 30-minute onboarding experience for technical writers contributing to the Physical AI & Humanoid Robotics textbook. By the end of this guide, you will have created your first chapter and run the validation pipeline.

## Prerequisites

Before starting, ensure you have:

- **Git** installed (2.30+)
- **Node.js** 18+ installed
- **npm** or **yarn** package manager
- **Python 3.10+** (for validation scripts)
- **GitHub account** with write access to the repository
- **Basic Markdown knowledge**

## Setup Process

### 1. Clone Repositories

```bash
# Clone the main textbook repository
git clone https://github.com/[your-username]/physical-ai-robotics-textbook.git
cd physical-ai-robotics-textbook

# Clone the companion repository
git clone https://github.com/[your-username]/physical-ai-textbook-assets.git
```

### 2. Install Dependencies

```bash
# Navigate to textbook directory
cd physical-ai-robotics-textbook

# Install Node.js dependencies
npm install
```

### 3. Verify Setup

```bash
# Start local development server
npm start

# Open http://localhost:3000/physical-ai-robotics-textbook/ in your browser
# You should see the textbook landing page
```

## Creating Your First Chapter

### 1. Use the Chapter Template

Copy the chapter template to create your new chapter:

```bash
# For Module 1, Chapter 1.3 (example)
cp docs/chapter-template.md docs/module-1-ros2/1-3-services.md
```

### 2. Fill Required Front-matter

Update the YAML front-matter at the top of your chapter file:

```yaml
---
title: "Chapter 1.3: Services"
sidebar_position: 3
description: "Learn to use services for request-response communication in ROS 2"
difficulty: Beginner-Intermediate
time_hours: 3.5
module: 1
tags: [ros2, services, communication, request-response]
---
```

### 3. Write Chapter Content

Follow the template structure:

1. **Introduction** with learning objectives
2. **Core Concepts** (simple → intermediate → advanced)
3. **Hands-On Exercises** (≥2 with expected outputs)
4. **Code Examples** (≥3 with explanations)
5. **Diagrams** (≥1 with alt text)
6. **Self-Assessment** (≥5 questions)
7. **Connections** to next chapter

### 4. Add Diagrams

Place diagrams in the appropriate module directory:

```bash
# For module 1 diagrams
cp your-diagram.png static/img/module-1/service-request-response.png
```

Reference in your chapter:

```markdown
![Service request-response architecture](/img/module-1/service-request-response.png)
```

### 5. Include Code Examples

For runnable code examples, place them in the companion repository:

```
physical-ai-textbook-assets/
└── module-1-ros2/
    └── chapter-1-3/
        └── code/
            ├── simple_service_server.py
            ├── simple_service_client.py
            └── AddTwoInts.srv
```

Reference in your chapter:

```markdown
```python
# Example service server code
import rclpy
from rclpy.node import Node
# ... rest of code
```
```

## Running Validation

### 1. Build Validation

```bash
# Test that your chapter builds correctly
npm run build
```

### 2. Markdown Linting

```bash
# Check for Markdown style issues
npm run lint
```

### 3. Link Validation

```bash
# Check for broken links
npx markdown-link-check "docs/module-1-ros2/1-3-services.md"
```

### 4. Full Validation Checklist

Before submitting, verify:

- [ ] Chapter builds without errors (`npm run build`)
- [ ] Front-matter has all required fields
- [ ] Learning objectives are specific and measurable
- [ ] At least 2 hands-on exercises with expected outputs
- [ ] At least 3 code examples with explanations
- [ ] At least 1 diagram with descriptive alt text
- [ ] Self-assessment has ≥5 questions
- [ ] All internal links resolve correctly
- [ ] All code examples are syntactically valid
- [ ] Reading level appropriate for target audience
- [ ] Content follows constitution principles

## Creating a Pull Request

### 1. Commit Your Changes

```bash
# Add your new chapter
git add docs/module-1-ros2/1-3-services.md

# Add any new diagrams
git add static/img/module-1/service-request-response.png

# Commit with descriptive message
git commit -m "Add Chapter 1.3: Services

- Cover request-response communication pattern
- Include service server and client examples
- Add exercise for creating custom service"

# Push to your branch
git push origin feature/chapter-1-3-services
```

### 2. Submit Pull Request

1. Go to the repository on GitHub
2. Click "New Pull Request"
3. Select your feature branch
4. Fill the PR template:
   - Title: "Add Chapter 1.3: Services"
   - Description: Summary of changes
   - Checklist: Confirm validation steps completed
   - Reviewers: Tag the textbook maintainers

### 3. Wait for CI/CD

Your PR will run through the validation pipeline:
- Build validation
- Markdown linting
- Link checking
- Cross-platform testing
- Accessibility validation

## Chapter Template Structure

Use this structure as a reference when creating chapters:

```markdown
---
title: "Chapter X.Y: Title"
sidebar_position: Y
description: "Brief description"
difficulty: Beginner|Intermediate|Advanced
time_hours: float
module: 1|2|3|4
tags: [list, of, tags]
---

# Chapter X.Y: Title

:::info Chapter Overview
- **Difficulty**: Beginner|Intermediate|Advanced
- **Time Required**: X-Y hours
- **Prerequisites**: [Link to prerequisites]
- **Tools**: [List of required tools]
- **Skills**: [What students will learn]
:::

## Learning Objectives

After completing this chapter, you will be able to:
1. [Specific, measurable objective 1]
2. [Specific, measurable objective 2]
3. [Specific, measurable objective 3]

## Prerequisites

Before starting this chapter, you should:
- [ ] Have completed [previous chapter]
- [ ] Have [specific software/tool] installed
- [ ] Understand [specific concept]

## Core Concepts

### Subsection 1: Simple Level

[Explain concept at simple level with examples]

### Subsection 2: Intermediate Level

[Build on simple concept with more detail]

### Subsection 3: Advanced Level

[Advanced applications and considerations]

## Hands-On Exercise 1: [Exercise Name]

### Steps
1. [Step 1 with command/instruction]
2. [Step 2 with command/instruction]
3. [Continue with detailed steps]

### Expected Output
```
[Show what the output should look like]
```

## Hands-On Exercise 2: [Exercise Name]

[Similar structure as Exercise 1]

## Code Examples

### Example 1: [Description]

```python
# Code with inline comments explaining key parts
```

### Example 2: [Description]

```bash
# Command-line example
```

## Diagrams

![Descriptive alt text for accessibility](/img/module-X/diagram-name.png)

*Caption explaining the diagram*

## Troubleshooting

### Common Issue 1
**Problem**: [Description of problem]
**Solution**: [How to fix it]

### Common Issue 2 (OS-Specific)
**Platform**: Windows|macOS|Ubuntu
**Problem**: [Description]
**Solution**: [Platform-specific fix]

## Self-Assessment Checkpoint

1. [Question 1]
2. [Question 2]
3. [Question 3]
4. [Question 4]
5. [Question 5]

*Answers and explanations at end of chapter*

## Connections

- **Next Chapter**: [Link to next chapter with brief explanation]
- **Related Topics**: [Links to related chapters/sections]
- **Real-World Applications**: [How this connects to real robotics]

## References

1. [APA-formatted citation 1]
2. [APA-formatted citation 2]
3. [APA-formatted citation 3]

## Answers to Self-Assessment

1. [Answer to question 1]
2. [Answer to question 2]
3. [Answer to question 3]
4. [Answer to question 4]
5. [Answer to question 5]
```

## Best Practices

### Writing Style
- Use active voice
- Write at Grade 8-12 reading level
- Use specific, measurable language
- Include practical examples
- Provide clear step-by-step instructions

### Technical Accuracy
- Verify all commands work on all platforms
- Test code examples before publishing
- Cite official documentation
- Include version information
- Mention platform-specific differences

### Educational Clarity
- Start with simple concepts before complex ones
- Provide immediate feedback opportunities
- Include common mistakes and how to avoid them
- Use consistent terminology
- Connect new concepts to previous learning

## Getting Help

### Documentation
- [Docusaurus Documentation](https://docusaurus.io/docs)
- [Markdown Guide](https://www.markdownguide.org/)
- [Textbook Style Guide](link-to-style-guide)

### Community
- Open an issue for technical problems
- Join the textbook contributor Discord
- Email the maintainers for content questions

### Troubleshooting Common Issues

**Chapter won't build**: Check for syntax errors in front-matter and Markdown
**Links broken**: Use relative paths for internal links (`/docs/module-1/...`)
**Images not showing**: Verify file paths and image optimization
**Code examples failing**: Test on all target platforms before committing

## Next Steps

After completing this quick start:

1. **Review existing chapters** to understand the style and structure
2. **Choose a chapter to work on** from the roadmap
3. **Create a feature branch** for your work
4. **Follow the validation checklist** before submitting
5. **Join the contributor community** for ongoing support

Congratulations! You're now ready to contribute to the Physical AI & Humanoid Robotics textbook.