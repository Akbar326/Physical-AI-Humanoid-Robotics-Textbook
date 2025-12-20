---
title: "Chapter 1.1: ROS 2 Overview and Installation"
sidebar_position: 1
description: "Understand ROS 2 architecture and set up your development environment"
difficulty: Beginner
time_hours: 3-4
module: 1
---

# Chapter 1.1: ROS 2 Overview and Installation

:::info Chapter Overview
- **Difficulty**: Beginner
- **Time Required**: 3-4 hours
- **Prerequisites**: [Setup Guide](../preface/setup-guide.md)
- **Tools**: ROS 2 Humble, Ubuntu 22.04 (or equivalents)
- **Skills**: Understanding ROS 2 concepts, environment setup
:::

## Learning Objectives

By the end of this chapter, you will be able to:

- [ ] Understand ROS 2 core concepts and architecture
- [ ] Explain the difference between ROS 1 and ROS 2
- [ ] Install and verify ROS 2 Humble on your system
- [ ] Set up your development environment
- [ ] Create and run your first ROS 2 node
- [ ] Debug basic ROS 2 installation issues

## Introduction

**Why This Matters**: ROS 2 is the industry standard for robotics development. Understanding its architecture and having a proper setup is foundational for all robotics work.

**Real-World Application**: Every modern robotics company (Boston Dynamics, NVIDIA, TRI, etc.) uses ROS 2 for their development and deployment.

Think of ROS 2 as the **nervous system of a robot**:
- Just like your nervous system allows different parts of your body to communicate, ROS 2 allows different robot components to communicate
- Your brain sends signals to your muscles → ROS 2 sends commands from a controller to motors
- Your sensory organs provide feedback to your brain → Robot sensors provide data to the control system
- All signals follow standards → All ROS 2 communication follows standard protocols

---

## Part 1: ROS 2 Fundamentals

### What is ROS 2?

**ROS 2 (Robot Operating System 2)** is a flexible framework for writing robot software. It's not an operating system in the traditional sense—it's a middleware that sits on top of Linux, Windows, or macOS and enables robot applications.

**Key Characteristics:**
- **Distributed**: Multiple programs (nodes) communicate over a network
- **Modular**: Build complex robots from simple reusable components
- **Standardized**: Follow common patterns for robotics development
- **Open Source**: Free, community-driven, industry-backed

### The ROS 2 Architecture

#### 1. **The Graph Model**

ROS 2 uses a **computation graph** where everything is a node exchanging messages:

```
┌──────────┐          Topic: /sensor_data          ┌──────────┐
│          │ ──────────────────────────────────►   │          │
│ Sensor   │ (publishes sensor readings)           │ Controller
│ Node     │                                        │ Node
└──────────┘                                        └──────────┘
                ▲                                         │
                │                                         │
                │  Topic: /motor_command                 │
                │  (subscribes to commands)              │
                │                                        ▼
                └────────────────────────────────────────┘
```

**Three main components:**
1. **Nodes**: Individual programs/processes (sensor reader, motor controller, AI algorithm, etc.)
2. **Topics**: Named channels where messages flow between nodes
3. **Messages**: Structured data types (images, positions, velocities, etc.)

#### 2. **Publish-Subscribe Communication**

Nodes communicate asynchronously through topics:

```
Publisher Node          ROS 2 Topic         Subscriber Node
(Sensor)           ("camera/image")      (Image Processor)

  publishes ────►  [message queue]  ────► subscribes
  at 30Hz               on disk           receives at 30Hz
```

**Why this design?**
- Loose coupling: publishers and subscribers don't need to know each other
- Flexible: one publisher can serve many subscribers
- Robust: communication continues even if nodes crash

#### 3. **Middleware: DDS (Data Distribution Service)**

Under the hood, ROS 2 uses **DDS**, an industry standard for distributed systems:

```
┌─ Node A ─┐
│  ROS2    │     DDS Network
│  App     │  ┌──────────────┐
└─────┬────┘  │  Data        │     ┌─ Node B ─┐
      │       │  Distribution│     │  ROS2    │
      └──────►│  Service     │────►│  App     │
              │ (Middleware) │     └──────────┘
              └──────────────┘
```

**Key benefit**: You can have nodes on different computers, and they communicate seamlessly!

#### 4. **ROS 2 Domain IDs**

Each ROS 2 "network" is isolated by a **Domain ID**:

```
Machine A                     Machine B
┌─────────────────┐          ┌─────────────────┐
│ Domain ID = 0   │          │ Domain ID = 1   │
│ ┌─ Node A ┐     │          │ ┌─ Node C ┐     │
│ │          │     │          │ │          │     │
│ └──────────┘     │          │ └──────────┘     │
└─────────────────┘          └─────────────────┘
      ▲                               ▲
      │ Can communicate               │ Cannot communicate
      │ (same Domain ID)              │ (different Domain IDs)
```

### ROS 2 vs ROS 1: What Changed?

| Aspect | ROS 1 | ROS 2 |
|--------|-------|-------|
| **Architecture** | Centralized (rosmaster) | Decentralized (DDS) |
| **Real-time** | Not suitable | Real-time capable |
| **Multi-platform** | Mostly Linux | Linux, Windows, macOS |
| **Security** | Minimal | Built-in authentication |
| **Production Ready** | Research focused | Production focused |
| **Learning Curve** | Moderate | Steeper but clearer |

**Bottom line**: ROS 2 is built for production robots in factories, hospitals, and the real world.

---

## Part 2: Installation and Setup

### Prerequisites Checklist

Before installing ROS 2, verify you have:

- [ ] A computer running **Ubuntu 22.04**, **Windows 10/11 with WSL2**, or **macOS 12+**
- [ ] **Administrator access** on your machine
- [ ] **At least 4GB free disk space**
- [ ] **Stable internet connection** for downloads
- [ ] **~30-45 minutes** for complete installation

### Platform-Specific Installation

#### **Ubuntu 22.04 (Recommended for Beginners)**

:::tip Best Choice
Ubuntu 22.04 is the officially recommended platform. Native support means fewer compatibility issues.
:::

**Step 1: Set up Ubuntu repositories**

```bash
# Add ROS 2 repository
sudo curl -sSL https://repo.ros2.org/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://repo.ros2.org/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Update package index
sudo apt update
```

**Step 2: Install ROS 2 Humble**

```bash
# Install ROS 2 Humble (full desktop installation)
sudo apt install ros-humble-desktop

# This includes:
# - Core ROS 2 libraries
# - RViz (3D visualization tool)
# - Example code and demos
```

**Step 3: Initialize environment**

```bash
# Add ROS 2 to your shell startup
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

# Apply changes
source ~/.bashrc
```

**Step 4: Verify installation**

```bash
# Test basic ROS 2 command
ros2 --version

# Expected output: ROS 2 Humble Hawksbill (release date)
```

#### **Windows 10/11 with WSL2**

:::note WSL2 Required
Windows Subsystem for Linux 2 (WSL2) is required. Windows native support is experimental.
:::

**Step 1: Install WSL2**

```powershell
# Run in PowerShell as Administrator
wsl --install
wsl --set-default-version 2
wsl --install --distribution Ubuntu-22.04

# Restart your computer
```

**Step 2: Inside WSL2 terminal, install ROS 2**

```bash
# Same commands as Ubuntu (see above)
sudo curl -sSL https://repo.ros2.org/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://repo.ros2.org/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update
sudo apt install ros-humble-desktop
```

**Step 3: Update .bashrc in WSL2**

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

#### **macOS 12+ (Experimental)**

:::warning Limited Support
macOS support is experimental. Some features may not work as expected. For learning, Ubuntu 22.04 is strongly recommended.
:::

```bash
# Install using Homebrew
brew install ros

# Or use official installer from ros.org
# https://docs.ros.org/en/humble/Installation/macOS-Install-Binary.html
```

### Understanding Your Installation

After installation, here's what you have:

```
/opt/ros/humble/
├── bin/              # ROS 2 command-line tools (ros2, colcon, etc.)
├── lib/              # ROS 2 libraries
├── include/          # Header files for C++ development
├── share/            # Documentation, examples, data
└── setup.bash        # Environment setup script
```

**Key environment variables set by `setup.bash`:**

```bash
# Display your ROS 2 environment
printenv | grep ROS

# Output should show:
# ROS_DISTRO=humble
# ROS_VERSION=2
# ROS_PYTHON_VERSION=3
```

### Create Your Development Workspace

A **workspace** is a folder where you'll keep your ROS 2 projects:

```bash
# Create workspace directory structure
mkdir -p ~/ros2_ws/src

# Navigate to workspace
cd ~/ros2_ws

# Create the build structure
colcon build
```

**After building, always source the workspace:**

```bash
# Add to ~/.bashrc for automatic activation
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc

# Apply changes
source ~/.bashrc
```

**Workspace structure:**

```
ros2_ws/
├── src/              # Your ROS 2 packages go here
├── build/            # Compilation output
├── install/          # Final compiled binaries and libraries
└── log/              # Build log files
```

---

## Part 3: Your First ROS 2 Node

### Understanding Nodes

A **node** is a single executable program in ROS 2. It's the basic unit of computation.

```python
# Every ROS 2 node has this basic structure:
1. Import ROS 2 libraries
2. Create a Node class (inherits from rclpy.node.Node)
3. Define node behavior (publishers, subscribers, timers)
4. Create main() function
5. Spin the node (keep it running)
```

### Creating Your First Publisher

A **publisher** sends messages to a topic. Let's create a simple one:

**File: `my_first_node.py`**

```python
#!/usr/bin/env python3

# Step 1: Import libraries
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

# Step 2: Create node class
class MyFirstPublisher(Node):
    """A simple publisher that broadcasts greetings"""

    def __init__(self):
        super().__init__('my_first_publisher')

        # Create a publisher that sends String messages
        # Topic: '/greeting'
        # Message type: String
        # Queue size: 10 (how many messages to buffer)
        self.publisher = self.create_publisher(
            String,
            '/greeting',
            10
        )

        # Create a timer that calls a function every 1 second
        self.timer = self.create_timer(
            1.0,  # 1 second interval
            self.timer_callback
        )

        self.counter = 0

    def timer_callback(self):
        """This function runs every 1 second"""
        self.counter += 1

        # Create and publish a message
        msg = String()
        msg.data = f'Hello ROS 2! Message #{self.counter}'

        self.publisher.publish(msg)

        # Print to console
        self.get_logger().info(f'Publishing: {msg.data}')

# Step 3: Main function
def main(args=None):
    # Initialize ROS 2
    rclpy.init(args=args)

    # Create an instance of our publisher
    node = MyFirstPublisher()

    # Keep the node running
    rclpy.spin(node)

    # Shutdown gracefully
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Running Your First Node

**In a terminal:**

```bash
# Navigate to wherever you saved the script
cd ~/my_ros2_code

# Make it executable
chmod +x my_first_node.py

# Run the node
python3 my_first_node.py
```

**Expected output:**

```
[INFO] [my_first_publisher]: Publishing: Hello ROS 2! Message #1
[INFO] [my_first_publisher]: Publishing: Hello ROS 2! Message #2
[INFO] [my_first_publisher]: Publishing: Hello ROS 2! Message #3
...
```

:::tip Stopping a Node
Press **Ctrl+C** in the terminal to stop the node.
:::

### Listening to the Topic (Optional: Run in Another Terminal)

To see the node working, open a **second terminal** and listen to its messages:

```bash
# List all active topics
ros2 topic list

# Output:
# /greeting
# /rosout

# Listen to the /greeting topic
ros2 topic echo /greeting
```

**You'll see:**

```
data: Hello ROS 2! Message #1
---
data: Hello ROS 2! Message #2
---
data: Hello ROS 2! Message #3
---
```

Congratulations! You've just created your first ROS 2 publisher! 🎉

---

## Part 4: Hands-On Exercises

### Exercise 1.1: Install ROS 2

**Objective**: Get ROS 2 working on your system

**Steps:**
1. Follow the [Installation and Setup](#installation-and-setup) section for your platform
2. Verify with: `ros2 --version`
3. Check environment: `printenv | grep ROS`

**Expected Result:**
```bash
$ ros2 --version
ROS 2 Humble Hawksbill (12.0.3)

$ printenv | grep ROS
ROS_DISTRO=humble
ROS_VERSION=2
ROS_PYTHON_VERSION=3
```

**Difficulty**: ⭐ (Very Easy)
**Time**: 30-45 minutes

---

### Exercise 1.2: Create Your Development Workspace

**Objective**: Set up a proper workspace structure

**Steps:**
1. Create workspace: `mkdir -p ~/ros2_ws/src`
2. Build it: `cd ~/ros2_ws && colcon build`
3. Source it: `source ~/ros2_ws/install/setup.bash`
4. Verify: `echo $AMENT_PREFIX_PATH`

**Expected Result:**
```bash
$ echo $AMENT_PREFIX_PATH
/home/username/ros2_ws/install:/opt/ros/humble/install
```

**Difficulty**: ⭐ (Very Easy)
**Time**: 10 minutes

---

### Exercise 1.3: Modify and Run Your First Node

**Objective**: Understand node code by modifying it

**Steps:**
1. Copy the `my_first_node.py` code from [Part 3](#your-first-ros-2-node)
2. Save it as `~/my_first_publisher.py`
3. Run it: `python3 ~/my_first_publisher.py`
4. In another terminal, listen: `ros2 topic echo /greeting`

**Modifications to try:**
- Change the timer interval from 1.0 to 2.0 seconds
- Change the message text
- Add a counter to the message (already done in the example!)

**Expected Result:**
Messages publishing every 1 second, visible in both terminals.

**Difficulty**: ⭐⭐ (Easy)
**Time**: 15 minutes

---

### Mini Lab: Create a Simple Subscriber

**Objective**: Learn to receive messages from a topic

**Create file: `my_first_subscriber.py`**

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MyFirstSubscriber(Node):
    """A simple subscriber that listens to greetings"""

    def __init__(self):
        super().__init__('my_first_subscriber')

        # Create a subscriber
        self.subscription = self.create_subscription(
            String,
            '/greeting',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        """This function is called every time a message arrives"""
        self.get_logger().info(f'I heard: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = MyFirstSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**To use:**
1. Run the publisher: `python3 my_first_publisher.py`
2. In another terminal, run the subscriber: `python3 my_first_subscriber.py`
3. Watch both nodes communicate!

**Difficulty**: ⭐⭐ (Easy)
**Time**: 20 minutes

---

## Part 5: Troubleshooting

### Issue 1: `ros2: command not found`

**Cause**: ROS 2 environment not loaded

**Solution:**
```bash
# Source the ROS 2 setup script
source /opt/ros/humble/setup.bash

# Verify
ros2 --version
```

**For permanent fix:**
```bash
# Add to ~/.bashrc
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

### Issue 2: `ModuleNotFoundError: No module named 'rclpy'`

**Cause**: Python environment doesn't have ROS 2 Python libraries

**Solution:**
```bash
# Verify ROS 2 is sourced
echo $ROS_DISTRO

# If empty, source ROS 2:
source /opt/ros/humble/setup.bash

# Then run your script
python3 my_first_node.py
```

---

### Issue 3: Node Doesn't Start / Port Already in Use

**Cause**: Another ROS 2 process using the same name or domain ID

**Solution:**
```bash
# Kill all Python ROS 2 processes
killall python3

# Or use a different domain ID
export ROS_DOMAIN_ID=1
python3 my_first_node.py

# Or give the node a unique name
# (modify the node creation line in your code)
```

---

### Issue 4: Installation Hangs on Ubuntu

**Cause**: Package manager waiting for input

**Solution:**
```bash
# Use non-interactive mode
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y ros-humble-desktop

# Or press Enter/accept prompts during installation
```

---

### Issue 5: WSL2 Can't Display RViz (Windows)

**Cause**: WSL2 has no native display server

**Solution**:
- Install an X server on Windows: [VcXsrv](https://sourceforge.net/projects/vcxsrv/)
- Or use Windows 11 native WSLg (newer versions have built-in display support)
- For now, use command-line tools only (`ros2 topic echo`, etc.)

---

## Part 6: Using Shared Utilities

Once you're comfortable with basic nodes, you can use the shared utilities from this textbook:

### ROS 2 Helper Functions

The companion repository includes `shared/utils/ros2_helpers.py` with useful functions:

```python
from shared.utils import ROS2Helper

# Setup a node easily
node = ROS2Helper.setup_node('my_node')

# List all topics
topics = ROS2Helper.list_topics()

# Get a parameter
param_value = ROS2Helper.get_parameter(node, 'my_param', default=5)

# Create publisher with one line
pub = ROS2Helper.create_publisher(node, '/my_topic', String, 10)
```

You'll use these extensively in [Chapter 1.3: Publishers and Subscribers](./chapter-1-3.md).

---

## Part 7: Key Takeaways

### Summary

✅ **What You Learned:**

1. **ROS 2 is a distributed middleware** for robot software development
2. **The graph model**: nodes communicate through topics asynchronously
3. **DDS provides the networking layer** - you don't need to think about it
4. **Nodes are individual programs** that do specific tasks
5. **Publishers send messages, subscribers receive them**
6. **Installation takes 30-45 minutes** and is straightforward on Ubuntu
7. **A minimal node requires 50-100 lines of Python code**

### Why This Matters

Understanding these fundamentals is critical because:
- Every subsequent chapter builds on this foundation
- You'll recognize the same patterns (publishers, subscribers) in complex systems
- Multi-robot systems, real-world applications, and research all use these basics
- 80% of ROS 2 debugging comes from understanding the graph model

### Next Steps

You now know:
- ✅ How ROS 2 works conceptually
- ✅ How to install it
- ✅ How to write and run a simple node

**Next chapter** ([Chapter 1.2: Packages and Workspaces](./chapter-1-2.md)) will teach you how to organize your code professionally using ROS 2 packages.

---

## Self-Assessment Checkpoint

Before proceeding, answer these questions:

:::note Self-Check Questions
1. **Conceptual**: What's the main difference between ROS 1 and ROS 2?
   - A) ROS 2 is for Python only
   - B) ROS 2 is decentralized and production-focused
   - C) ROS 2 doesn't need installation
   - **Answer**: B

2. **Architecture**: In the ROS 2 graph model, what's the role of a topic?
   - A) Run the entire robot system
   - B) A named channel where messages flow between nodes
   - C) A configuration file
   - **Answer**: B

3. **Practical**: How do you make ROS 2 commands available after a fresh terminal?
   - A) Reinstall ROS 2
   - B) Add `source /opt/ros/humble/setup.bash` to ~/.bashrc
   - C) Set an environment variable
   - **Answer**: B

4. **Code Understanding**: In the publisher code, what does `self.create_timer(1.0, callback)` do?
   - A) Wait 1 second before starting
   - B) Call the callback function every 1 second
   - C) Create a 1-second timeout
   - **Answer**: B

5. **Debugging**: You get `ros2: command not found`. What's the most likely cause?
   - A) ROS 2 is broken
   - B) ROS 2 environment hasn't been sourced in this terminal
   - C) You need to reinstall
   - **Answer**: B

6. **Advanced**: Why does ROS 2 use DDS instead of a centralized server like ROS 1?
   - A) DDS is faster to code
   - B) DDS enables distributed, scalable, production-ready systems
   - C) There's no real reason
   - **Answer**: B
:::

**Scoring:**
- 6/6: Excellent! Ready for Chapter 1.2
- 5/6: Very good, but review any section you struggled with
- 4/6 or less: Review the Core Concepts section before proceeding

---

## Next Steps

- **Ready for more?** Continue to [Chapter 1.2: Packages and Workspaces](./chapter-1-2.md)
- **Want to practice more?** Modify the exercises and experiment
- **Need help?** See [Troubleshooting](#troubleshooting) section
- **Questions?** Check [Module 1 Overview](./index.md) for learning resources

---

**Chapter Status**: ✅ COMPLETE
**Last Updated**: 2025-12-17
**Estimated Reading Time**: 45 minutes
**Estimated Hands-On Time**: 2-3 hours
