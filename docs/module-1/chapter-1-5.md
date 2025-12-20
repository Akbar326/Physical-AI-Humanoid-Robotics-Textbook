---
title: "Chapter 1.5: Parameters and Launch Files"
sidebar_position: 5
description: "Configure complex ROS 2 systems with parameters and launch files"
difficulty: Intermediate
time_hours: 3-4
module: 1
---

# Chapter 1.5: Parameters and Launch Files

:::info Chapter Overview
- **Difficulty**: Intermediate
- **Time Required**: 3-4 hours
- **Prerequisites**: Chapter 1.4
:::

## Learning Objectives

By the end of this chapter, you will be able to:

- [ ] Use ROS 2 parameters effectively
- [ ] Create launch files
- [ ] Manage complex multi-node systems
- [ ] Pass arguments to launch files
- [ ] Debug launch issues

## Introduction

**Why This Matters**: Real robots don't have hardcoded values. They need **configuration**:
- Sensor calibration values change per robot
- Motor speeds differ between models
- Network settings vary by environment

**Parameters** store these values. **Launch files** start multiple nodes with proper configuration.

---

## Part 1: ROS 2 Parameters

### What Are Parameters?

Parameters are **runtime configuration values** for nodes:

```python
# Instead of hardcoding:
WHEEL_RADIUS = 0.1      # ❌ Hard to change

# Use parameters:
self.get_parameter('wheel_radius')  # ✅ Easy to change
```

### Setting Parameters

**From command line:**
```bash
ros2 run my_package my_node --ros-args -p wheel_radius:=0.15
```

**In Python node:**
```python
self.declare_parameter('wheel_radius', 0.1)  # Default value
value = self.get_parameter('wheel_radius').value
```

**From YAML file:**
```yaml
my_package:
  my_node:
    ros__parameters:
      wheel_radius: 0.1
      max_speed: 2.0
      enable_debug: true
```

### Exercise Example

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

class ConfigurableBot(Node):
    def __init__(self):
        super().__init__('configurable_bot')

        # Declare parameters with defaults
        self.declare_parameter('robot_name', 'Robot')
        self.declare_parameter('max_velocity', 1.0)
        self.declare_parameter('debug_mode', False)

        # Get parameters
        self.robot_name = self.get_parameter('robot_name').value
        self.max_velocity = self.get_parameter('max_velocity').value
        self.debug = self.get_parameter('debug_mode').value

        self.get_logger().info(
            f'Robot: {self.robot_name}, '
            f'Max Speed: {self.max_velocity} m/s'
        )

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(ConfigurableBot())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Run with parameters:**
```bash
ros2 run my_package configurable_bot \
  --ros-args \
  -p robot_name:="TurtleBot3" \
  -p max_velocity:=2.5 \
  -p debug_mode:=true
```

---

## Part 2: Launch Files

### What Are Launch Files?

Launch files **start multiple nodes** with one command:

Instead of:
```bash
# Terminal 1
ros2 run pkg1 node1

# Terminal 2
ros2 run pkg2 node2 --ros-args -p param:=value

# Terminal 3
ros2 run pkg3 node3
```

Do this:
```bash
ros2 launch my_package system.launch.py
```

### Creating a Launch File

**File: `my_robot_package/launch/robot_system.launch.py`**

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Node 1: Sensor reader
        Node(
            package='sensor_package',
            executable='camera_node',
            name='camera',
            parameters=[{'frame_rate': 30}]
        ),

        # Node 2: Controller
        Node(
            package='control_package',
            executable='motor_controller',
            name='controller',
            parameters=[{'max_speed': 2.0}]
        ),

        # Node 3: Visualizer
        Node(
            package='viz_package',
            executable='rviz',
            name='visualizer'
        ),
    ])
```

### Running a Launch File

```bash
ros2 launch my_robot_package robot_system.launch.py
```

**Output:**
```
[INFO] Launching robot system...
[camera-1] [INFO] Camera node started
[controller-1] [INFO] Motor controller started
[visualizer-1] [INFO] RViz started
```

All nodes start together!

### Launch File with Arguments

```python
from launch import LaunchDescription, LaunchContext
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Declare arguments
    robot_model_arg = DeclareLaunchArgument(
        'robot_model',
        default_value='turtlebot3_burger',
        description='Robot model'
    )

    max_speed_arg = DeclareLaunchArgument(
        'max_speed',
        default_value='2.0',
        description='Maximum velocity'
    )

    return LaunchDescription([
        robot_model_arg,
        max_speed_arg,

        Node(
            package='robot_package',
            executable='controller',
            name='controller',
            parameters=[{
                'robot_model': LaunchConfiguration('robot_model'),
                'max_speed': LaunchConfiguration('max_speed')
            }]
        ),
    ])
```

**Run with arguments:**
```bash
ros2 launch my_package robot.launch.py \
  robot_model:=turtlebot3_waffle \
  max_speed:=3.0
```

---

## Part 3: Parameter Files

### YAML Parameter Files

**File: `config/robot_params.yaml`**

```yaml
robot_controller:
  ros__parameters:
    # Motor configuration
    wheel_radius: 0.1
    track_width: 0.2
    max_linear_velocity: 2.0
    max_angular_velocity: 1.57

    # Sensor configuration
    imu_publish_rate: 50
    lidar_scan_rate: 10

    # Debug
    verbose_logging: true
```

**Load in launch file:**

```python
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    config_path = PathJoinSubstitution([
        get_package_share_directory('my_package'),
        'config',
        'robot_params.yaml'
    ])

    return LaunchDescription([
        Node(
            package='robot_package',
            executable='controller',
            name='controller',
            parameters=[config_path]
        ),
    ])
```

---

## Part 4: Hands-On Exercises

### Exercise 5.1: Create Parameterized Node

Create a node that accepts parameters:
- robot_name
- base_speed
- enable_logging

**Difficulty**: ⭐⭐ (Easy)
**Time**: 20 minutes

---

### Exercise 5.2: Launch Multiple Nodes

Create a launch file that starts:
1. A sensor simulator
2. A controller
3. A logger

All with appropriate parameters.

**Difficulty**: ⭐⭐⭐ (Intermediate)
**Time**: 30 minutes

---

### Exercise 5.3: Parameter File

Create a YAML configuration for a robot system with:
- Motor parameters
- Sensor calibration
- Control gains
- Debug settings

**Difficulty**: ⭐⭐ (Easy)
**Time**: 15 minutes

---

## Part 5: Troubleshooting

### Issue 1: Parameter Not Found

**Error**: `Parameter 'wheel_radius' not found`

**Solution**:
```python
# Make sure to declare it first
self.declare_parameter('wheel_radius', 0.1)
```

---

### Issue 2: Launch File Not Found

```bash
# Verify launch file exists
ls -la my_package/launch/

# Use absolute path if needed
ros2 launch /full/path/to/launch.py
```

---

### Issue 3: Nodes Not Starting

Check launch file syntax. Use:
```bash
ros2 launch my_package robot.launch.py --show-args
```

---

## Part 6: Key Takeaways

✅ **Parameters**: Runtime configuration values
✅ **Launch Files**: Start multiple nodes together
✅ **YAML Config**: Store parameters in files
✅ **Arguments**: Pass values to launch files

---

## Self-Assessment Checkpoint

1. How do you set a parameter at runtime?
   - Answer: `ros2 run pkg node --ros-args -p param:=value`

2. What's the benefit of launch files?
   - Answer: Start multiple nodes with one command instead of multiple terminals

3. How do you load parameters from a YAML file?
   - Answer: Use `parameters=[config_path]` in Node()

---

## Next Steps

- Continue to [Chapter 1.6: Debugging and Development Tools](./chapter-1-6.md)
- Create launch files for your multi-node systems
- Experiment with parameters and configuration files

---

**Chapter Status**: ✅ COMPLETE
**Last Updated**: 2025-12-17
**Estimated Reading Time**: 40 minutes
**Estimated Hands-On Time**: 1-2 hours
