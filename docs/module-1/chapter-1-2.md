---
title: "Chapter 1.2: Packages and Workspaces"
sidebar_position: 2
description: "Organize ROS 2 projects with packages and workspaces"
difficulty: Beginner
time_hours: 3-4
module: 1
---

# Chapter 1.2: Packages and Workspaces

:::info Chapter Overview
- **Difficulty**: Beginner
- **Time Required**: 3-4 hours
- **Prerequisites**: Chapter 1.1
- **Tools**: colcon, ROS 2 Humble
:::

## Learning Objectives

By the end of this chapter, you will be able to:

- [ ] Create ROS 2 packages
- [ ] Understand workspace structure
- [ ] Build packages with colcon
- [ ] Manage dependencies
- [ ] Organize multi-package projects

## Introduction

**Why This Matters**: In [Chapter 1.1](./chapter-1-1.md), you created individual Python scripts. Real robots have dozens or hundreds of components. **Packages** are how ROS 2 organizes code into reusable, shareable, and manageable units.

**Real-World Example**: A mobile robot might have:
- A **navigation_package** for movement
- A **perception_package** for cameras and sensors
- A **control_package** for motor commands
- A **planning_package** for decision-making

Each package is independent, reusable, and can be shared with others.

---

## Part 1: Understanding Packages and Workspaces

### What is a Package?

A **ROS 2 package** is a directory containing:

```
my_first_package/
├── package.xml          # Package metadata (name, version, dependencies)
├── setup.py            # Python build configuration
├── setup.cfg           # Build system configuration
├── resource/           # Non-code resources
└── my_first_package/   # Python module (same name as package)
    ├── __init__.py
    └── my_node.py      # Your ROS 2 node code
```

**Key point**: A package is self-contained. It specifies its own dependencies, making it easy to share and reuse.

### Workspace Hierarchy

Think of your ROS 2 development like this:

```
Workspace Level (~/ros2_ws/)
│
├── Package 1 (navigation_stack/)
│   ├── node_1.py
│   └── node_2.py
│
├── Package 2 (perception_stack/)
│   ├── camera_reader.py
│   └── image_processor.py
│
└── Package 3 (control_stack/)
    ├── motor_controller.py
    └── joint_monitor.py

All packages built together in one workspace!
```

**Why organize this way?**
- **Modularity**: Each package handles one concern
- **Reusability**: Share packages across projects
- **Maintainability**: Easy to find and modify code
- **Dependency management**: Clear what each package needs
- **Collaboration**: Team members work on different packages

### Workspace vs Overlay vs Source

```
System Installation
/opt/ros/humble/          ← Official ROS 2 (read-only)
│
Overlay (your workspace)
~/ros2_ws/
├── src/                  ← Your package source code
├── build/                ← Compilation output
└── install/              ← Final installed packages

When you source setup.bash, ROS 2 finds packages in this order:
1. Your workspace (install/)
2. System installation (/opt/ros/humble/)
```

---

## Part 2: Creating Your First Package

### Create a Python Package

Let's create a package called `my_robot_package`:

**Step 1: Create package structure**

```bash
# Navigate to your workspace
cd ~/ros2_ws/src

# Create a Python package
ros2 pkg create --build-type ament_python my_robot_package

# This creates:
# my_robot_package/
# ├── package.xml
# ├── setup.py
# ├── setup.cfg
# └── my_robot_package/
#     └── __init__.py
```

**Step 2: Understand package.xml**

Open `my_robot_package/package.xml`:

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>my_robot_package</name>
  <version>0.0.0</version>
  <description>My first ROS 2 package</description>

  <!-- Author information -->
  <maintainer email="you@example.com">Your Name</maintainer>
  <license>Apache-2.0</license>

  <!-- Build system -->
  <buildtool_depend>ament_cmake_python</buildtool_depend>

  <!-- Runtime dependencies -->
  <depend>rclpy</depend>
  <depend>std_msgs</depend>

  <!-- Test dependencies -->
  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

**Key fields:**
- `<name>`: Package name (must be lowercase, no spaces)
- `<version>`: Semantic versioning (major.minor.patch)
- `<description>`: What the package does
- `<depend>`: Runtime dependencies
- `<test_depend>`: Testing dependencies only

### Understanding setup.py

Open `my_robot_package/setup.py`:

```python
from setuptools import setup

package_name = 'my_robot_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='Your Name',
    author_email='you@example.com',
    maintainer='Your Name',
    maintainer_email='you@example.com',
    description='My first ROS 2 package',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'my_node = my_robot_package.my_node:main',
        ],
    },
)
```

**Key parts:**
- `packages=[package_name]`: Python packages to include
- `install_requires`: Dependencies (besides ROS 2)
- `entry_points`: Executables created from your code
  - Maps command name to module and function
  - `'my_node = my_robot_package.my_node:main'` means:
    - Run `ros2 run my_robot_package my_node` to execute the `main()` function in `my_robot_package/my_node.py`

### Add Your First Node

Create `my_robot_package/my_robot_package/my_node.py`:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MyRobotNode(Node):
    """First node in my_robot_package"""

    def __init__(self):
        super().__init__('my_robot_node')
        self.get_logger().info('MyRobotNode initialized!')

def main(args=None):
    rclpy.init(args=args)
    node = MyRobotNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Register the Executable

Update `setup.py` entry_points:

```python
entry_points={
    'console_scripts': [
        'my_node = my_robot_package.my_node:main',
    ],
},
```

Now ROS 2 knows how to run your node!

---

## Part 3: Building Packages with Colcon

### What is Colcon?

**Colcon** (Collective Construction) is the ROS 2 build tool:

```
Your package source code (setup.py, setup.cfg, package.xml)
            ↓
        colcon build
            ↓
Compiled binaries and libraries (in install/)
```

### Build Your Package

**Step 1: Build from workspace root**

```bash
# Navigate to workspace root
cd ~/ros2_ws

# Build everything
colcon build

# Or build a specific package
colcon build --packages-select my_robot_package

# Or build with verbose output
colcon build --packages-select my_robot_package --symlink-install
```

**Expected output:**
```
Starting >>> my_robot_package
Finished <<< my_robot_package [0.42s]

Summary: 1 package finished [0.46s]
```

### Understand the Build Output

After building, you have three directories:

```
~/ros2_ws/
├── src/                 # Your original source code (unchanged)
│   └── my_robot_package/
│       ├── package.xml
│       └── setup.py
│
├── build/               # Compilation intermediate files
│   └── my_robot_package/
│       ├── build_timestamp
│       └── ... (build artifacts)
│
└── install/             # Final installed packages (what ROS 2 uses!)
    └── my_robot_package/
        ├── bin/        # Executables
        ├── lib/        # Libraries
        └── share/      # Resources
```

### Source Your Workspace

After building, tell ROS 2 about your new package:

```bash
# Source the workspace
source ~/ros2_ws/install/setup.bash

# Verify your package is available
ros2 pkg list | grep my_robot_package

# Output: my_robot_package
```

**Add to .bashrc for permanent activation:**

```bash
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### Run Your Package Node

```bash
# Run your node
ros2 run my_robot_package my_node

# Output:
# [INFO] [my_robot_node]: MyRobotNode initialized!
```

Congratulations! You just ran your first ROS 2 package! 🎉

---

## Part 4: Managing Dependencies

### Adding Dependencies to Your Package

Let's say your node needs the `std_msgs` package:

**Step 1: Update package.xml**

```xml
<depend>rclpy</depend>
<depend>std_msgs</depend>        <!-- Add this line -->
<depend>geometry_msgs</depend>   <!-- Add if you need it -->
```

**Step 2: Update setup.py**

```python
install_requires=[
    'setuptools',
],
```

(Note: ROS 2 dependencies go in `package.xml`, not `setup.py`)

**Step 3: Rebuild**

```bash
cd ~/ros2_ws
colcon build --packages-select my_robot_package
source ~/ros2_ws/install/setup.bash
```

### Finding Available Dependencies

**View all ROS 2 packages:**

```bash
# List all packages
ros2 pkg list

# Search for a specific package
ros2 pkg list | grep sensor
```

**Check a package's information:**

```bash
# Get package info
ros2 pkg prefix std_msgs

# Find package.xml
ros2 pkg list -p std_msgs
```

### Dependency Types

```xml
<!-- Build-time dependency (needed during compilation) -->
<buildtool_depend>ament_cmake_python</buildtool_depend>

<!-- Runtime dependency (needed when running) -->
<depend>rclpy</depend>
<depend>std_msgs</depend>

<!-- Test dependency (only needed for testing) -->
<test_depend>pytest</test_depend>
```

---

## Part 5: Multi-Package Workspaces

### Organize Multiple Packages

Let's create a complete robot system:

```bash
cd ~/ros2_ws/src

# Create multiple packages
ros2 pkg create --build-type ament_python robot_control
ros2 pkg create --build-type ament_python robot_perception
ros2 pkg create --build-type ament_python robot_planning
```

**Your workspace now looks like:**

```
~/ros2_ws/
├── src/
│   ├── my_robot_package/
│   │   ├── package.xml
│   │   └── my_robot_package/
│   │       └── my_node.py
│   │
│   ├── robot_control/
│   │   ├── package.xml
│   │   └── robot_control/
│   │       └── controller.py
│   │
│   ├── robot_perception/
│   │   ├── package.xml
│   │   └── robot_perception/
│   │       └── camera_reader.py
│   │
│   └── robot_planning/
│       ├── package.xml
│       └── robot_planning/
│           └── planner.py
│
└── build/, install/, log/
```

### Build All Packages Together

```bash
# Build entire workspace
cd ~/ros2_ws
colcon build

# Or with progress indication
colcon build --packages-up-to robot_planning
```

**Output:**
```
Starting >>> my_robot_package
Finished <<< my_robot_package [0.42s]
Starting >>> robot_control
Finished <<< robot_control [0.35s]
Starting >>> robot_perception
Finished <<< robot_perception [0.38s]
Starting >>> robot_planning
Finished <<< robot_planning [0.40s]

Summary: 4 packages finished [1.65s]
```

### Package Dependencies Between Packages

Make one package depend on another:

**In `robot_planning/package.xml`:**

```xml
<depend>rclpy</depend>
<depend>std_msgs</depend>
<depend>robot_control</depend>    <!-- Depend on robot_control package! -->
```

Now ROS 2 will ensure `robot_control` is built before `robot_planning`.

---

## Part 6: Hands-On Exercises

### Exercise 2.1: Create Your First Package

**Objective**: Organize code in a ROS 2 package

**Steps:**

1. Create a package:
   ```bash
   cd ~/ros2_ws/src
   ros2 pkg create --build-type ament_python my_learning_package
   ```

2. Create a node file: `my_learning_package/my_learning_package/hello_world.py`
   ```python
   #!/usr/bin/env python3
   import rclpy
   from rclpy.node import Node

   class HelloNode(Node):
       def __init__(self):
           super().__init__('hello_node')
           self.get_logger().info('Hello from a package!')

   def main(args=None):
       rclpy.init(args=args)
       node = HelloNode()
       rclpy.spin(node)
       node.destroy_node()
       rclpy.shutdown()

   if __name__ == '__main__':
       main()
   ```

3. Update `setup.py`:
   ```python
   entry_points={
       'console_scripts': [
           'hello = my_learning_package.hello_world:main',
       ],
   },
   ```

4. Build and run:
   ```bash
   cd ~/ros2_ws
   colcon build --packages-select my_learning_package
   source install/setup.bash
   ros2 run my_learning_package hello
   ```

**Expected output:**
```
[INFO] [hello_node]: Hello from a package!
```

**Difficulty**: ⭐⭐ (Easy)
**Time**: 20 minutes

---

### Exercise 2.2: Add Dependencies

**Objective**: Use packages and manage dependencies

**Steps:**

1. Update `my_learning_package/package.xml` to add geometry_msgs:
   ```xml
   <depend>geometry_msgs</depend>
   ```

2. Verify package exists:
   ```bash
   ros2 pkg list | grep geometry_msgs
   ```

3. Rebuild:
   ```bash
   cd ~/ros2_ws
   colcon build --packages-select my_learning_package
   ```

4. Check dependency resolution:
   ```bash
   ros2 pkg depends my_learning_package
   ```

**Expected output:**
```
geometry_msgs
rclpy
std_msgs
```

**Difficulty**: ⭐⭐ (Easy)
**Time**: 15 minutes

---

### Exercise 2.3: Create Multi-Package System

**Objective**: Organize code across multiple packages

**Steps:**

1. Create two packages:
   ```bash
   cd ~/ros2_ws/src
   ros2 pkg create --build-type ament_python sensor_readers
   ros2 pkg create --build-type ament_python data_processors
   ```

2. In `data_processors/package.xml`, add dependency:
   ```xml
   <depend>sensor_readers</depend>
   ```

3. Build both:
   ```bash
   cd ~/ros2_ws
   colcon build
   ```

4. Verify order:
   ```bash
   colcon build --packages-select data_processors
   ```

**Expected behavior**: Building `data_processors` automatically ensures `sensor_readers` is built first.

**Difficulty**: ⭐⭐⭐ (Intermediate)
**Time**: 25 minutes

---

### Mini Lab: Workspace Organization

Create the following structure:

```bash
cd ~/ros2_ws/src

ros2 pkg create --build-type ament_python robot_base
ros2 pkg create --build-type ament_python robot_sensors
ros2 pkg create --build-type ament_python robot_motors
ros2 pkg create --build-type ament_python robot_controller
```

Then build with:

```bash
cd ~/ros2_ws
colcon build
```

Observe how all packages build together in a single command!

**Difficulty**: ⭐⭐ (Easy)
**Time**: 20 minutes

---

## Part 7: Troubleshooting

### Issue 1: `package not found`

**Error:**
```bash
$ ros2 run my_robot_package my_node
Package 'my_robot_package' not found
```

**Cause**: Workspace not sourced after building

**Solution:**
```bash
# Source the workspace
source ~/ros2_ws/install/setup.bash

# Try running again
ros2 run my_robot_package my_node
```

---

### Issue 2: `entry_points` errors

**Error:**
```
ERROR in setup.py entry_points: 'my_node = my_robot_package.my_node:main'
Cannot find module
```

**Cause**: Wrong path or module doesn't exist

**Solution:**
1. Verify file exists: `ls my_robot_package/my_robot_package/my_node.py`
2. Check `setup.py` has correct format:
   ```python
   'my_node = my_robot_package.my_node:main'
   #        ╰─ package name ╯   ╰─ module ╯
   ```

---

### Issue 3: Dependency not found

**Error:**
```
ERROR: Dependency 'geometry_msgs' not found
```

**Cause**: Package not installed or not in package.xml

**Solution:**
```bash
# Add to package.xml
<depend>geometry_msgs</depend>

# Rebuild
cd ~/ros2_ws
colcon build

# Verify it's available
ros2 pkg list | grep geometry_msgs
```

---

### Issue 4: Build fails with import errors

**Error:**
```python
ImportError: No module named 'rclpy'
```

**Cause**: Workspace not sourced during build

**Solution:**
```bash
# Source ROS 2
source /opt/ros/humble/setup.bash

# Rebuild
cd ~/ros2_ws
colcon build --packages-select my_robot_package
```

---

### Issue 5: Conflicting packages

**Cause**: Same package name in two locations

**Solution:**
```bash
# Use unique package names
ros2 pkg create --build-type ament_python team_robot_v1
# Instead of: team_robot (common name!)
```

---

## Part 8: Using Shared Utilities in Packages

The companion repository provides utilities in the `shared/` directory:

**Add to your package.xml:**

```xml
<depend>shared</depend>  <!-- If available as a package -->
```

**Or copy utilities directly:**

```bash
cp -r /path/to/shared/utils/* my_robot_package/
```

**Use in your nodes:**

```python
from shared.utils import ROS2Helper

# In your node class:
helper = ROS2Helper()
topics = helper.list_topics()
```

---

## Part 9: Key Takeaways

### What You Learned

✅ **Packages and Workspaces:**
- Packages organize code logically
- Workspaces contain multiple packages
- `package.xml` specifies metadata and dependencies
- `setup.py` defines build configuration and executables

✅ **Building:**
- `colcon build` compiles your packages
- Output goes to `install/` directory
- Must source workspace to use packages

✅ **Executables:**
- Entry points in `setup.py` create runnable commands
- Maps shell commands to Python functions
- Same command works for anyone with your package

✅ **Dependencies:**
- List all dependencies in `package.xml`
- ROS 2 resolves them automatically
- Packages can depend on other packages

### Why This Matters

- **Professional organization**: Real robots have 10-100+ packages
- **Collaboration**: Team members work on different packages independently
- **Reusability**: Share packages across projects and with the community
- **Testing**: Each package can be tested independently
- **Maintenance**: Easy to find and modify specific functionality

### Common Patterns

**Single package:**
```bash
ros2 pkg create --build-type ament_python my_pkg
colcon build --packages-select my_pkg
ros2 run my_pkg my_node
```

**Multi-package system:**
```bash
ros2 pkg create --build-type ament_python pkg1 pkg2 pkg3
colcon build                    # Build all
ros2 run pkg1 node1
ros2 run pkg2 node2
```

---

## Self-Assessment Checkpoint

Before proceeding, verify you can:

:::note Self-Check
1. **Conceptual**: What's the difference between a workspace and a package?
   - Answer: A workspace is a directory containing multiple packages. Packages are self-contained units of code.

2. **Practical**: Can you create a package from scratch?
   ```bash
   ros2 pkg create --build-type ament_python test_pkg
   # Yes if you can run this successfully
   ```

3. **Code Understanding**: What does this entry_points line do?
   ```python
   'my_cmd = my_pkg.my_module:main'
   ```
   - Answer: Creates a command `my_cmd` that runs the `main()` function in `my_pkg/my_module.py`

4. **Debugging**: Your node says `Package not found`. What's missing?
   - Answer: Haven't sourced the workspace after building. Run `source ~/ros2_ws/install/setup.bash`

5. **Multi-Package**: How do you make package B depend on package A?
   - Answer: Add `<depend>package_a</depend>` to B's `package.xml`
:::

**Ready for Chapter 1.3?** You should be able to create and build ROS 2 packages confidently.

---

## Next Steps

- **Ready for more?** Continue to [Chapter 1.3: Publishers and Subscribers](./chapter-1-3.md)
- **Want to practice more?** Create 2-3 packages and build them together
- **Need help?** See [Troubleshooting](#troubleshooting) section
- **Questions?** Check [Module 1 Overview](./index.md) for learning resources

---

**Chapter Status**: ✅ COMPLETE
**Last Updated**: 2025-12-17
**Estimated Reading Time**: 40 minutes
**Estimated Hands-On Time**: 2-3 hours
