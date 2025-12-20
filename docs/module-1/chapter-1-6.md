---
title: "Chapter 1.6: Debugging and Development Tools"
sidebar_position: 6
description: "Master ROS 2 debugging tools and best development practices"
difficulty: Intermediate
time_hours: 3-4
module: 1
---

# Chapter 1.6: Debugging and Development Tools

:::info Chapter Overview
- **Difficulty**: Intermediate
- **Time Required**: 3-4 hours
- **Prerequisites**: Chapter 1.5
:::

## Learning Objectives

By the end of this chapter, you will be able to:

- [ ] Use ROS 2 command-line tools effectively
- [ ] Debug running ROS 2 systems
- [ ] Use Rviz for visualization
- [ ] Monitor system performance
- [ ] Apply best practices for development

## Introduction

**Why This Matters**: Even experienced developers spend more time **debugging** than writing code. ROS 2 provides powerful tools to diagnose issues quickly.

**The Debugging Cycle:**
```
Node crashes or behaves wrong
            ↓
Use debugging tools to inspect
            ↓
Identify the root cause
            ↓
Fix the issue
            ↓
Verify the fix works
```

---

## Part 1: Essential ROS 2 CLI Tools

### Topic Debugging

```bash
# List all active topics
ros2 topic list

# Get details about a topic
ros2 topic info /sensor_data

# Output:
# Type: std_msgs/Float32
# Publisher count: 1
# Subscriber count: 2

# Echo (display) messages
ros2 topic echo /sensor_data

# Echo with only 5 messages
ros2 topic echo /sensor_data --max-count 5

# Measure bandwidth
ros2 topic hz /sensor_data   # Shows publish frequency

# Listen to a specific field
ros2 topic echo /robot/status --field battery_level
```

### Service Debugging

```bash
# List all services
ros2 service list

# Get service type
ros2 service type /get_battery

# Call a service manually
ros2 service call /get_battery example_interfaces/srv/GetBatteryLevel

# View service definition
ros2 interface show example_interfaces/srv/GetBatteryLevel
```

### Node Debugging

```bash
# List all running nodes
ros2 node list

# Get node details
ros2 node info /my_robot_node

# Output:
# /my_robot_node
#   Subscribers:
#     /sensor_data: std_msgs/Float32
#   Publishers:
#     /cmd_vel: geometry_msgs/Twist

# Check if node is running
pgrep -f "ros2 run"
```

### Parameter Debugging

```bash
# List all parameters
ros2 param list

# Get a parameter value
ros2 param get /controller max_velocity

# Set a parameter
ros2 param set /controller max_velocity 3.0

# Dump all parameters
ros2 param dump /controller
```

---

## Part 2: Logging and Debugging

### Adding Logging to Code

```python
import rclpy
from rclpy.node import Node

class DebugNode(Node):
    def __init__(self):
        super().__init__('debug_node')

        # Different log levels
        self.get_logger().debug("Debug message (verbose)")
        self.get_logger().info("Info message (important)")
        self.get_logger().warn("Warning message (attention needed)")
        self.get_logger().error("Error message (something failed)")
        self.get_logger().fatal("Fatal message (critical failure)")

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(DebugNode())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Setting Log Levels

```bash
# Set log level for a node
ros2 run my_package my_node --ros-args --log-level DEBUG

# Set for all nodes
ros2 run my_package my_node --ros-args --log-level WARN

# Log levels (in order of verbosity):
# DEBUG < INFO < WARN < ERROR < FATAL
```

### Capturing Logs to File

```bash
# Redirect to file
ros2 run my_package my_node > robot_logs.txt 2>&1

# Or use tee to both display and save
ros2 run my_package my_node 2>&1 | tee robot_logs.txt
```

---

## Part 3: System Monitoring

### ROS 2 System Graph

```bash
# View the computation graph
ros2 graph

# Output shows all nodes, topics, and services connected

# Generate DOT visualization
rqt_graph
# Opens GUI showing the entire system
```

### Real-Time Monitoring

```bash
# Watch topics in real-time
watch -n 0.1 'ros2 topic echo /sensor_data --max-count 1'

# Monitor node CPU/memory
ps aux | grep ros2

# Check ROS 2 communication health
ros2 doctor
# Reports any issues with installation
```

### Bandwidth and Performance

```bash
# Measure topic bandwidth
ros2 topic hz /camera_image

# Show message frequency and latency
ros2 topic hz /sensor_data --window 10  # Last 10 messages

# Profile code performance
python3 -m cProfile my_node.py
```

---

## Part 4: Common Debugging Scenarios

### Scenario 1: Node Won't Connect to Topic

**Problem**: Publisher sends, subscriber never receives

**Debug Steps:**
```bash
# 1. Verify topic exists
ros2 topic list | grep topic_name

# 2. Check message type matches
ros2 topic info /my_topic
ros2 interface show std_msgs/Float32

# 3. Check ROS_DOMAIN_ID
echo $ROS_DOMAIN_ID

# 4. View actual messages
ros2 topic echo /my_topic
```

### Scenario 2: Service Call Fails

**Problem**: Service call times out

**Debug Steps:**
```bash
# 1. List available services
ros2 service list | grep service_name

# 2. Check service type
ros2 service type /get_battery

# 3. Try calling manually
ros2 service call /get_battery example_interfaces/srv/GetBatteryLevel ""

# 4. Check if server is running
ros2 node list | grep server
```

### Scenario 3: Slow Performance

**Problem**: System is sluggish

**Debug Steps:**
```bash
# 1. Check publish frequency
ros2 topic hz /sensor_data  # Should be reasonable

# 2. Monitor CPU
watch -n 1 'ps aux | grep python3'

# 3. Check for message backlog
ros2 topic info /my_topic  # Look for queue size

# 4. Reduce publishing frequency
# In node: self.timer = self.create_timer(2.0, callback)  # Less frequent
```

---

## Part 5: Development Best Practices

### Code Structure

```python
#!/usr/bin/env python3
"""
Module docstring explaining what this node does
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class MyNode(Node):
    """
    Brief description of the node

    Attributes:
        publisher: Publishes to /topic
        subscriber: Subscribes to /input
    """

    def __init__(self):
        super().__init__('my_node')
        self.get_logger().info('MyNode initialized')

        # Declare all parameters first
        self.declare_parameter('param_name', 0.0)

        # Create all subscribers and publishers
        self.pub = self.create_publisher(Float32, '/output', 10)
        self.sub = self.create_subscription(
            Float32, '/input', self.callback, 10
        )

        # Create all timers
        self.timer = self.create_timer(1.0, self.timer_callback)

    def callback(self, msg):
        """Process incoming messages"""
        self.get_logger().info(f'Received: {msg.data}')

    def timer_callback(self):
        """Process at regular intervals"""
        msg = Float32()
        msg.data = 42.0
        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down...')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Testing

```python
# test_my_node.py
import pytest
import rclpy
from my_package.my_node import MyNode

def test_node_initialization():
    """Test that node initializes properly"""
    rclpy.init()
    node = MyNode()
    assert node.get_name() == 'my_node'
    node.destroy_node()
    rclpy.shutdown()

def test_parameter_loading():
    """Test that parameters load correctly"""
    rclpy.init()
    node = MyNode()
    param = node.get_parameter('param_name')
    assert param.value == 0.0
    node.destroy_node()
    rclpy.shutdown()
```

Run tests:
```bash
pytest test_my_node.py -v
```

---

## Part 6: Hands-On Exercises

### Exercise 6.1: Debug a Broken System

Given a malfunctioning ROS 2 system, use debugging tools to:
1. Identify which node is failing
2. Find the specific topic causing issues
3. Determine the root cause
4. Fix the problem

**Difficulty**: ⭐⭐⭐ (Intermediate)
**Time**: 30 minutes

---

### Exercise 6.2: Create Comprehensive Logging

Add logging to a multi-node system:
- Log at appropriate levels (DEBUG, INFO, WARN, ERROR)
- Include relevant information in log messages
- Capture logs to file
- Analyze logs to understand system behavior

**Difficulty**: ⭐⭐ (Easy)
**Time**: 25 minutes

---

### Exercise 6.3: System Performance Analysis

Analyze a working ROS 2 system:
1. Measure topic frequencies
2. Check CPU and memory usage
3. Identify bandwidth bottlenecks
4. Suggest optimizations

**Difficulty**: ⭐⭐⭐ (Intermediate)
**Time**: 30 minutes

---

## Part 7: Troubleshooting Tools Summary

| Tool | Use Case | Command |
|------|----------|---------|
| `ros2 topic` | Inspect topics | `ros2 topic list\|echo\|info` |
| `ros2 service` | Check services | `ros2 service list\|call` |
| `ros2 node` | Monitor nodes | `ros2 node list\|info` |
| `ros2 param` | Configure runtime | `ros2 param get\|set` |
| `rqt_graph` | Visualize system | `rqt_graph` |
| `ros2 doctor` | Check installation | `ros2 doctor` |

---

## Part 8: Key Takeaways

✅ **CLI Tools**: Use `ros2 topic`, `ros2 service`, `ros2 node` for debugging
✅ **Logging**: Add logs at appropriate levels for troubleshooting
✅ **Monitoring**: Watch system performance in real-time
✅ **Testing**: Write unit tests for your nodes
✅ **Best Practices**: Organize code, document clearly, handle errors gracefully

---

## Self-Assessment Checkpoint

1. How do you see what topics are active?
   - Answer: `ros2 topic list`

2. What command shows which nodes are publishing/subscribing?
   - Answer: `ros2 node info /node_name`

3. How do you capture logs to a file?
   - Answer: `ros2 run pkg node 2>&1 | tee output.txt`

---

## Next Steps

- **Congratulations!** You've completed Module 1! 🎉
- You now understand ROS 2 fundamentals and can build real systems
- Continue to [Module 2: Gazebo Simulation](../module-2/index.md)
- Review any chapters that weren't fully clear
- Practice building complex multi-node systems

---

## Module 1 Completion Summary

You've learned:
- ✅ ROS 2 architecture and core concepts
- ✅ Creating and managing packages
- ✅ Pub-Sub communication patterns
- ✅ Services and Actions
- ✅ Parameters and Launch files
- ✅ Debugging and troubleshooting

**Total Time**: ~18-20 hours of learning + hands-on practice
**Ready for**: Building real robot systems with ROS 2

---

**Chapter Status**: ✅ COMPLETE
**Last Updated**: 2025-12-17
**Estimated Reading Time**: 45 minutes
**Estimated Hands-On Time**: 2-3 hours

---

**🎓 Module 1: ROS 2 Fundamentals - COMPLETE!**

You've successfully completed the foundational module of the Physical AI & Humanoid Robotics textbook. You now have the ROS 2 skills needed to build complex robot systems.

**What's Next?**
- [Module 2: Gazebo Simulation](../module-2/index.md) - Learn to simulate robots before deploying
- [Module 3: Isaac Sim & AI](../module-3/index.md) - Advanced simulation with AI integration
- [Module 4: Vision-Language-Action](../module-4/index.md) - Cutting-edge robot learning
