# Module 1: ROS 2 Fundamentals - Code Examples & Exercises

**Time**: 19-23 hours | **Chapters**: 6 | **Difficulty**: Beginner to Intermediate

This directory contains all code examples, exercises, and solutions for **Module 1: ROS 2 Fundamentals** of the Physical AI & Humanoid Robotics textbook.

---

## Quick Links

| Chapter | Topic | Time | Files |
|---------|-------|------|-------|
| [1.1](chapter-1-1/) | ROS 2 Overview and Installation | 3-4h | Examples, Exercises, Solutions |
| [1.2](chapter-1-2/) | Packages and Workspaces | 3-4h | Examples, Exercises, Solutions |
| [1.3](chapter-1-3/) | Publishers and Subscribers | 3-4h | Examples, Exercises, Solutions |
| [1.4](chapter-1-4/) | Services and Actions | 3-4h | Examples, Exercises, Solutions |
| [1.5](chapter-1-5/) | Parameters and Launch Files | 3-4h | Examples, Exercises, Solutions |
| [1.6](chapter-1-6/) | Debugging and Development Tools | 3-4h | Examples, Exercises, Solutions |

---

## Learning Objectives

After completing this module, you will be able to:

- ✅ Understand ROS 2 architecture and core concepts
- ✅ Create and manage ROS 2 packages and workspaces
- ✅ Implement publisher-subscriber communication
- ✅ Design service clients and servers
- ✅ Configure parameters and launch files
- ✅ Debug ROS 2 systems using command-line tools

---

## Getting Started

### 1. Start with Chapter 1.1

```bash
# Navigate to first chapter
cd module-1/chapter-1-1/

# Read the chapter README
cat README.md

# Run the first example
python3 examples/my_first_node.py
```

### 2. Work Through Progressively

Each chapter builds on the previous one:

1. **Ch 1.1**: Your first node (publisher/subscriber)
2. **Ch 1.2**: Multiple packages in a workspace
3. **Ch 1.3**: Message types and topics
4. **Ch 1.4**: Request-reply patterns
5. **Ch 1.5**: Configuration and automation
6. **Ch 1.6**: Debugging techniques

### 3. Try the Exercises

```bash
# Go to chapter directory
cd chapter-1-3/exercises

# Read exercise README
cat README.md

# Start with exercise template
python3 exercise1.py

# Check the solution when stuck
cat ../solutions/exercise1_solution.py
```

---

## Chapter Breakdown

### Chapter 1.1: ROS 2 Overview and Installation

**Concepts**: ROS 2 architecture, DDS middleware, graph-based systems

**Files**:
- `examples/my_first_node.py` - Basic ROS 2 publisher
- `examples/simple_subscriber.py` - Basic ROS 2 subscriber
- `exercises/` - Create your first node

**Quick Start**:
```bash
cd chapter-1-1/examples
python3 my_first_node.py
```

### Chapter 1.2: Packages and Workspaces

**Concepts**: Package structure, dependencies, colcon build system

**Files**:
- `examples/package_structure.py` - Package organization
- `exercises/` - Create multi-package workspace

**Quick Start**:
```bash
cd chapter-1-2/examples
python3 package_structure.py
```

### Chapter 1.3: Publishers and Subscribers

**Concepts**: Topic-based communication, message types, callbacks

**Files**:
- `examples/publisher.py` - Topic publisher
- `examples/subscriber.py` - Topic subscriber
- `examples/custom_messages.py` - Custom message types
- `exercises/` - Build multi-node system

**Quick Start** (requires 2 terminals):
```bash
# Terminal 1
cd chapter-1-3/examples
python3 publisher.py

# Terminal 2
cd chapter-1-3/examples
python3 subscriber.py
```

### Chapter 1.4: Services and Actions

**Concepts**: Request-reply patterns, asynchronous operations, goals

**Files**:
- `examples/service_server.py` - Service implementation
- `examples/service_client.py` - Service caller
- `examples/action_server.py` - Action server
- `examples/action_client.py` - Action client

**Quick Start** (requires 2 terminals):
```bash
# Terminal 1
cd chapter-1-4/examples
python3 service_server.py

# Terminal 2
cd chapter-1-4/examples
python3 service_client.py
```

### Chapter 1.5: Parameters and Launch Files

**Concepts**: Runtime configuration, launch files, parameterization

**Files**:
- `examples/parameters.py` - Parameter usage
- `examples/launch_example.py` - Launch file
- `config/robot.yaml` - Configuration file
- `exercises/` - Create launch system

**Quick Start**:
```bash
cd chapter-1-5/examples
python3 parameters.py --params config/robot.yaml
```

### Chapter 1.6: Debugging and Development Tools

**Concepts**: ROS 2 CLI tools, debugging, profiling, logging

**Files**:
- `examples/debug_example.py` - Debugging demo
- `examples/logging.py` - Logging best practices
- `scripts/debug.sh` - Debugging commands
- `exercises/` - Debug complex systems

**Quick Start**:
```bash
cd chapter-1-6/examples
python3 debug_example.py
```

---

## File Organization

### `examples/`
Complete, working implementations demonstrating concepts.

```bash
# Run an example
cd chapter-1-3/examples
python3 publisher.py

# Understanding the code
cat publisher.py     # Read the code
head -n 20 publisher.py  # See just the beginning
```

### `exercises/`
Templates for you to complete.

```bash
# Start an exercise
cd chapter-1-3/exercises
cat exercise1.py     # See what needs implementing
python3 exercise1.py # Test your implementation
```

### `solutions/`
Reference implementations (check only after attempting!).

```bash
# Compare with solution
cd chapter-1-3/solutions
diff ../exercises/exercise1.py exercise1_solution.py
```

---

## Common Tasks

### Run All Examples

```bash
# Run examples from all chapters
for chapter in chapter-1-{1..6}; do
  echo "=== $chapter ==="
  python3 $chapter/examples/*.py
done
```

### Check Chapter Progress

```bash
# See what's in each chapter
for chapter in chapter-1-{1..6}; do
  echo "=== $chapter ==="
  ls $chapter/examples/
  ls $chapter/exercises/
  ls $chapter/solutions/
done
```

### Run Tests

```bash
# Run tests for module
pytest tests/

# Run tests for specific chapter
pytest tests/chapter-1-1_test.py -v
```

---

## Prerequisites

### Required
- Python 3.10+
- ROS 2 Humble installed and sourced
- Basic command-line experience

### Recommended
- VS Code or similar editor
- `rclpy` library (installed with ROS 2)

### Setup

```bash
# Source ROS 2
source /opt/ros/humble/setup.bash

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r ../../requirements.txt
```

---

## Learning Resources

### From This Repository
- [Examples](chapter-1-3/examples/) - Working code
- [Exercises](chapter-1-3/exercises/) - Practice problems
- [Solutions](chapter-1-3/solutions/) - Reference implementations

### From Main Textbook
- Full explanations: [textbook/module-1/](https://github.com/physical-ai-lab/ai-humanoid-robotics)
- Learning guides: [textbook/module-1/index.md](https://github.com/physical-ai-lab/ai-humanoid-robotics)

### Official Documentation
- [ROS 2 Humble Docs](https://docs.ros.org/en/humble/)
- [ROS 2 Tutorials](https://docs.ros.org/en/humble/Tutorials.html)
- [rclpy API](https://docs.ros.org/en/humble/API-Docs.html)

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'rclpy'"
```bash
# Source ROS 2
source /opt/ros/humble/setup.bash
python3 script.py
```

### "Node name already in use"
```bash
# Different ROS domains
export ROS_DOMAIN_ID=1
python3 script.py
```

### "Topic not found"
```bash
# List available topics
ros2 topic list
ros2 topic echo /topic_name
```

### More help
See [Troubleshooting Guide](../../docs/TROUBLESHOOTING.md)

---

## Module Projects

### Project 1: Robot Command Center

Build a multi-node ROS 2 system with:
- Command receiver (subscriber)
- Robot controller (service)
- Status publisher
- Parameter configuration
- Launch file automation

**Files**: `projects/robot_command_center/`
**Time**: 3-4 hours
**Skills**: All Chapter 1 concepts

---

## Next Steps

After completing Module 1:

1. ✅ Review all exercises and solutions
2. ✅ Complete the module project
3. ✅ Practice with your own ROS 2 packages
4. → Proceed to [Module 2: Gazebo Simulation](../module-2/)

---

## Tips for Success

1. **Run all examples**: Don't just read, execute the code
2. **Modify examples**: Experiment with parameters
3. **Attempt exercises first**: Try before checking solutions
4. **Use ROS 2 tools**: Practice with `ros2 topic`, `ros2 service`, etc.
5. **Debug systematically**: Use logging and command-line tools

---

## Contributing

Found issues or want to add examples? See [CONTRIBUTING.md](../../CONTRIBUTING.md)

---

**Happy learning! 🤖**

**Last Updated**: 2025-12-16 | **Status**: Ready for use
