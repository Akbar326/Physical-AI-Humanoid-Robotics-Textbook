---
sidebar_position: 1
title: "Module 1: ROS 2 Fundamentals"
description: "Learn core ROS 2 concepts, architecture, and development practices"
difficulty: Beginner
time_hours: 19-23
module: 1
---

# Module 1: ROS 2 Fundamentals

## Module Overview

Module 1 provides a comprehensive introduction to ROS 2 (Robot Operating System 2), the industry-standard middleware for robotics development. You'll learn core concepts, development workflows, and best practices that form the foundation for all subsequent modules.

:::info Module At a Glance
- **Duration**: 19-23 hours total
- **Chapters**: 6 chapters with progressive complexity
- **Prerequisites**: Basic Python knowledge, command-line familiarity
- **Learning Level**: Beginner to Intermediate
- **Tools**: ROS 2 Humble, Python 3.10+, colcon build system
- **Platforms**: Ubuntu 22.04, Windows 10/11 (WSL2), macOS 12+
:::

## Chapters in This Module

| Chapter | Title | Duration | Level |
|---------|-------|----------|-------|
| **1.1** | [ROS 2 Overview and Installation](./chapter-1-1.md) | 3-4h | Beginner |
| **1.2** | [Packages and Workspaces](./chapter-1-2.md) | 3-4h | Beginner |
| **1.3** | [Publishers and Subscribers](./chapter-1-3.md) | 3-4h | Beginner |
| **1.4** | [Services and Actions](./chapter-1-4.md) | 3-4h | Intermediate |
| **1.5** | [Parameters and Launch Files](./chapter-1-5.md) | 3-4h | Intermediate |
| **1.6** | [Debugging and Development Tools](./chapter-1-6.md) | 3-4h | Intermediate |

## Module Learning Outcomes

By completing this module, you will be able to:

- **Understand** the ROS 2 architecture and its core concepts
- **Create and manage** ROS 2 packages and workspaces
- **Implement** publisher-subscriber communication patterns
- **Develop** service clients and servers for request-reply patterns
- **Design** action servers for long-running tasks
- **Configure** parameters and launch files for complex systems
- **Debug** ROS 2 applications using built-in tools
- **Apply** ROS 2 best practices in your code

## Core Concepts Covered

- **ROS 2 Middleware**: Graph-based communication architecture
- **Nodes**: Independent processes in the ROS 2 network
- **Topics**: Asynchronous pub-sub communication channels
- **Services**: Synchronous request-reply mechanisms
- **Actions**: Goal-oriented long-running tasks with feedback
- **Parameters**: Runtime-configurable values
- **Launch Files**: Automation for starting complex systems
- **colcon Build System**: Workspace building and dependency management

## What You'll Build

Throughout this module, you'll build progressively more complex applications:

- **Chapter 1.1**: Your first ROS 2 node (publisher and subscriber)
- **Chapter 1.2**: Multi-package workspace with dependencies
- **Chapter 1.3**: Complete pub-sub system with custom message types
- **Chapter 1.4**: Robot simulation controller using services
- **Chapter 1.5**: Configurable robot with parameters and launch files
- **Chapter 1.6**: Debugging tools for complex multi-node systems

## Time Management Tips

**Recommended Weekly Schedule** (assuming ~5 hours/week available):

- **Week 1**: Chapters 1.1 - 1.2 (7-8 hours)
- **Week 2**: Chapters 1.3 - 1.4 (7-8 hours)
- **Week 3**: Chapters 1.5 - 1.6 (5-7 hours)

**For Intensive Learners** (full-time for 1 week):
- Day 1: Chapter 1.1 - 1.2
- Day 2: Chapter 1.3
- Day 3: Chapter 1.4
- Day 4: Chapter 1.5
- Day 5: Chapter 1.6 + Review

## Prerequisites Checklist

Before starting this module, verify you have:

- [ ] Complete system setup from [Setup Guide](../preface/setup-guide.md)
- [ ] Python 3.10 or higher installed
- [ ] ROS 2 Humble installed and working
- [ ] Command-line experience (shell/terminal)
- [ ] Basic Python programming knowledge
- [ ] Git installed for version control
- [ ] Text editor or IDE (VS Code recommended)

## Learning Resources

### Primary Resources
- Textbook chapters (detailed implementations)
- Code examples in companion repository
- Hands-on exercises with solutions
- Self-assessment checkpoints in each chapter

### Supplementary Resources
- [Official ROS 2 Documentation](https://docs.ros.org/en/humble/)
- [ROS 2 Humble Release Notes](https://docs.ros.org/en/humble/Releases/Release-Humble-Hawksbill.html)
- [ROS 2 API Documentation](https://docs.ros.org/en/humble/API-Docs.html)
- [colcon Build System](https://colcon.readthedocs.io/)

## Key Technologies

| Technology | Version | Purpose |
|-----------|---------|---------|
| **ROS 2** | Humble | Core robotics middleware |
| **Python** | 3.10+ | Primary programming language |
| **colcon** | Latest | Build and test system |
| **ament** | Latest | Build system backend |
| **rclpy** | Humble | ROS 2 Python client library |

## Module Projects

### Hands-On Project: Robot Command Center
Design and implement a multi-node ROS 2 system that:
- Receives movement commands from a publisher
- Controls a simulated robot via services
- Reports robot status through subscribers
- Uses parameters for configuration
- Implements debugging and logging

This project combines all skills learned in Module 1 and prepares you for Module 2.

## Next Steps

### After Completing This Module:
1. Review the module summary and self-assessment
2. Complete the hands-on project
3. Practice with the companion repository exercises
4. Proceed to [Module 2: Gazebo Simulation](../module-2/)

### Skills Transfer:
The ROS 2 skills from this module apply to:
- Gazebo simulation (Module 2)
- Isaac Sim development (Module 3)
- Robot control systems (Module 4)
- Real-world robot deployments

## Getting Help

### If You Get Stuck:
1. **Check chapter troubleshooting** - See "Troubleshooting Guide" section
2. **Review code examples** - Run and understand example code
3. **Check companion repository** - View solutions and additional examples
4. **Verify installation** - Re-run setup script to verify environment
5. **Open an issue** - Provide error message, OS, and reproduction steps

### Common Issues by Chapter:
- **Ch 1.1-1.2**: Installation or PATH issues → See setup guide
- **Ch 1.3**: Message type or import errors → Check package.xml
- **Ch 1.4**: Service definition or call errors → Verify .srv files
- **Ch 1.5**: Parameter or launch file syntax → Check YAML formatting
- **Ch 1.6**: Tool not found or permission denied → Verify installation

## Quick Start Command

To get started immediately after setup:

```bash
# 1. Source ROS 2
source /opt/ros/humble/setup.bash

# 2. Create workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws

# 3. Clone companion repository
git clone https://github.com/physical-ai-lab/ai-humanoid-robotics-code.git code

# 4. Start with Module 1 examples
cd code/module-1/chapter-1.1/examples

# 5. Run first example
python3 my_first_node.py
```

## Module Completion Checklist

Ensure you've completed all of these before moving to Module 2:

- [ ] All 6 chapters read and understood
- [ ] All code examples run successfully on your system
- [ ] All exercises completed
- [ ] Self-assessment checkpoint passed (5/5 or 4/5)
- [ ] Hands-on project completed and working
- [ ] No outstanding errors or warnings
- [ ] Ready to learn Module 2: Gazebo Simulation

## Estimated Workload

| Activity | Hours | Cumulative |
|----------|-------|-----------|
| Chapter 1.1-1.2 | 7-8 | 7-8 |
| Chapter 1.3-1.4 | 7-8 | 14-16 |
| Chapter 1.5-1.6 | 5-7 | 19-23 |

**Total Module Time**: 19-23 hours

---

**Module Status**: Content ready for implementation
**Last Updated**: 2025-12-16
**Next Module**: [Module 2: Gazebo Simulation](../module-2/index.md)

**Questions?** See [How to Use This Textbook](../preface/how-to-use.md) or open an issue on GitHub.
