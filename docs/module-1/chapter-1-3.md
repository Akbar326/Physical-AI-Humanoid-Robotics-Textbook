---
title: "Chapter 1.3: Publishers and Subscribers"
sidebar_position: 3
description: "Master asynchronous pub-sub communication in ROS 2"
difficulty: Beginner
time_hours: 3-4
module: 1
---

# Chapter 1.3: Publishers and Subscribers

:::info Chapter Overview
- **Difficulty**: Beginner
- **Time Required**: 3-4 hours
- **Prerequisites**: Chapter 1.2
- **Tools**: rclpy, ROS 2 Humble
:::

## Learning Objectives

By the end of this chapter, you will be able to:

- [ ] Understand pub-sub communication patterns
- [ ] Create publishers and subscribers
- [ ] Work with custom message types
- [ ] Handle messages in callbacks
- [ ] Debug communication issues

## Introduction

**Why This Matters**: Publishers and subscribers are the **heart of ROS 2 communication**. Almost everything in robotics is a pub-sub message exchange:
- Sensors publish data → Controllers subscribe to process it
- Planners publish commands → Motors subscribe to execute them
- Feedback loops: Motors publish status → Controllers subscribe to adjust

Understanding pub-sub is understanding ROS 2 itself.

**Real-World Example**: A mobile robot has:
```
LIDAR sensor ──publishes──> /scan topic <──subscribes── Navigation node
                                          ├──publishes──> /cmd_vel
Motor driver ──subscribes─────────────────┘

All communication happens through topics!
```

---

## Part 1: Pub-Sub Fundamentals

### What is Pub-Sub Communication?

**Publish-Subscribe (Pub-Sub)** is a communication pattern where:
- **Publishers** send messages to a named topic
- **Subscribers** receive messages from that topic
- Publishers and subscribers don't know about each other

```
┌────────────┐
│ Publisher  │  "Please send my messages to /temperature"
└──────┬─────┘
       │
       ▼ publishes
  ┌────────────────┐
  │ ROS 2 Topic    │
  │ /temperature   │
  │ Message Queue  │  (messages stored temporarily)
  └────────────────┘
       ▲
       │ subscribes
┌──────┴─────┐
│ Subscriber │  "Give me all /temperature messages"
└────────────┘
```

### Why Pub-Sub is Better Than Direct Communication

**Direct Connection (❌ Bad):**
```
Node A ──send──> Node B
       <──reply─
Both nodes must know each other!
If Node B crashes, Node A breaks.
If Node C also wants the data, add more connections.
```

**Pub-Sub (✅ Good):**
```
Node A ──publishes──> Topic
                       ├─> Node B receives
                       ├─> Node C receives
                       └─> Node D receives
All nodes work independently!
```

### Key Characteristics of Pub-Sub

| Aspect | Detail |
|--------|--------|
| **Decoupling** | Publishers don't know who subscribes |
| **Asynchronous** | Subscribers receive messages when they arrive |
| **Many-to-Many** | One publisher, many subscribers (or vice versa) |
| **Message Queue** | Messages stored if subscriber is slow |
| **Topic-based** | Messages organized by topic names |

---

## Part 2: Creating Publishers

### A Simple Publisher

Let's create a publisher that sends temperature data:

**File: `temperature_publisher.py`**

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32  # Message type for floating-point numbers
import random

class TemperaturePublisher(Node):
    """Simulates a temperature sensor publishing readings"""

    def __init__(self):
        super().__init__('temperature_publisher')

        # Create a publisher
        # Topic: '/temperature'
        # Message type: Float32 (a single floating-point number)
        # Queue size: 10 (how many messages to buffer)
        self.publisher = self.create_publisher(
            Float32,
            '/temperature',
            10
        )

        # Create a timer to publish every 1 second
        self.timer = self.create_timer(1.0, self.publish_temperature)
        self.get_logger().info('Temperature publisher started')

    def publish_temperature(self):
        """Callback function called by timer every 1 second"""
        # Create a Float32 message
        msg = Float32()

        # Simulate a temperature reading between 20-30 degrees
        msg.data = 20.0 + (random.random() * 10.0)

        # Publish the message to the topic
        self.publisher.publish(msg)

        # Log for debugging
        self.get_logger().info(f'Published temperature: {msg.data:.2f}°C')

def main(args=None):
    rclpy.init(args=args)
    node = TemperaturePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Running the Publisher

```bash
# Terminal 1: Run the publisher
python3 temperature_publisher.py

# Expected output:
# [INFO] Temperature publisher started
# [INFO] Published temperature: 24.32°C
# [INFO] Published temperature: 25.18°C
# ...
```

### Checking Published Messages

**In another terminal:**

```bash
# List all active topics
ros2 topic list

# Output:
# /rosout
# /temperature

# View message details
ros2 topic info /temperature

# Output:
# Type: std_msgs/Float32
# Publisher count: 1
# Subscriber count: 0

# Listen to the topic
ros2 topic echo /temperature

# Output:
# data: 24.3199996948
# ---
# data: 25.7839999199
# ---
```

---

## Part 3: Creating Subscribers

### A Simple Subscriber

Now let's create a subscriber that listens to temperature data:

**File: `temperature_subscriber.py`**

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class TemperatureSubscriber(Node):
    """Subscribes to temperature readings and processes them"""

    def __init__(self):
        super().__init__('temperature_subscriber')

        # Create a subscriber
        # Topic: '/temperature' (same as publisher)
        # Message type: Float32
        # Callback: function to call when message arrives
        # Queue size: 10
        self.subscription = self.create_subscription(
            Float32,
            '/temperature',
            self.temperature_callback,
            10
        )

        self.get_logger().info('Temperature subscriber started')

    def temperature_callback(self, msg):
        """
        This function is called EVERY TIME a message arrives on /temperature.
        The message is passed as the 'msg' parameter.
        """
        temperature = msg.data

        # Process the data
        if temperature < 22:
            status = "TOO COLD"
        elif temperature > 28:
            status = "TOO HOT"
        else:
            status = "OK"

        self.get_logger().info(
            f'Temperature: {temperature:.2f}°C [{status}]'
        )

def main(args=None):
    rclpy.init(args=args)
    node = TemperatureSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Running Publisher and Subscriber Together

**Terminal 1: Publisher**
```bash
python3 temperature_publisher.py
```

**Terminal 2: Subscriber**
```bash
python3 temperature_subscriber.py

# Output:
# [INFO] Temperature subscriber started
# [INFO] Temperature: 24.32°C [OK]
# [INFO] Temperature: 25.18°C [OK]
# [INFO] Temperature: 22.50°C [OK]
# [INFO] Temperature: 29.10°C [TOO HOT]
```

**Terminal 3: View topic info**
```bash
ros2 topic info /temperature

# Output:
# Type: std_msgs/Float32
# Publisher count: 1
# Subscriber count: 1
```

Perfect! Your nodes are communicating! 🎉

---

## Part 4: Understanding Message Types

### Standard Message Types

ROS 2 provides many built-in message types:

```python
from std_msgs.msg import String        # Text
from std_msgs.msg import Int32         # Integer
from std_msgs.msg import Float32       # Float
from std_msgs.msg import Bool          # Boolean
from geometry_msgs.msg import Point    # 3D position (x, y, z)
from geometry_msgs.msg import Twist    # Velocity (linear, angular)
from sensor_msgs.msg import Image      # Camera image
from sensor_msgs.msg import LaserScan  # LIDAR data
```

### Common Message Examples

**String message:**
```python
from std_msgs.msg import String

msg = String()
msg.data = "Hello, ROS 2!"
publisher.publish(msg)
```

**Geometry Point:**
```python
from geometry_msgs.msg import Point

msg = Point()
msg.x = 1.0
msg.y = 2.0
msg.z = 3.0
publisher.publish(msg)
```

**Robot Velocity (Twist):**
```python
from geometry_msgs.msg import Twist

msg = Twist()
msg.linear.x = 0.5    # Move forward at 0.5 m/s
msg.angular.z = 0.1   # Rotate at 0.1 rad/s
publisher.publish(msg)
```

### Exploring Message Details

```bash
# Show all fields in a message type
ros2 interface show std_msgs/Float32

# Output:
# std_msgs/Float32 [d41d8cd98f00b204e9800998ecf8427e]
#   float32 data

# For more complex messages
ros2 interface show geometry_msgs/Twist

# Output:
# geometry_msgs/Twist [9f195f1c3e0b3db8d8f1a3f15c3d3f8a]
#   geometry_msgs/Vector3 linear
#     float64 x
#     float64 y
#     float64 z
#   geometry_msgs/Vector3 angular
#     float64 x
#     float64 y
#     float64 z
```

---

## Part 5: Custom Message Types

Sometimes built-in messages aren't enough. Let's create a custom message type.

### Define a Custom Message

Create `RobotStatus.msg` in your package:

**File: `my_robot_package/msg/RobotStatus.msg`**

```
# Custom message for robot status
string robot_name
int32 battery_level
float32 temperature
bool is_moving
```

### Register the Message Type

Update `package.xml`:

```xml
<build_depend>rosidl_default_generators</build_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
```

Create `my_robot_package/CMakeLists.txt`:

```cmake
cmake_minimum_required(VERSION 3.5)
project(my_robot_package)

find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/RobotStatus.msg"
)
```

Update `setup.py`:

```python
from setuptools import setup
from glob import glob
from os.path import join

package_name = 'my_robot_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        # ... existing data files ...
        (join('share', package_name, 'msg'), glob('msg/*.msg')),
    ],
    # ... rest of setup.py ...
)
```

### Use Your Custom Message

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from my_robot_package.msg import RobotStatus

class RobotStatusPublisher(Node):
    def __init__(self):
        super().__init__('robot_status_pub')
        self.publisher = self.create_publisher(RobotStatus, '/robot/status', 10)
        self.timer = self.create_timer(1.0, self.publish_status)

    def publish_status(self):
        msg = RobotStatus()
        msg.robot_name = "RoboBot-1"
        msg.battery_level = 85
        msg.temperature = 42.5
        msg.is_moving = True

        self.publisher.publish(msg)
        self.get_logger().info(f'{msg.robot_name}: Battery {msg.battery_level}%')

def main(args=None):
    rclpy.init(args=args)
    node = RobotStatusPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

## Part 6: Quality of Service (QoS)

QoS settings control how messages are delivered:

### QoS Policy Example

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

# Create a QoS profile
qos_profile = QoSProfile(
    history=HistoryPolicy.KEEP_LAST,  # Keep only latest N messages
    depth=10,                          # Keep 10 latest messages
    reliability=ReliabilityPolicy.RELIABLE  # Wait for delivery confirmation
)

# Use it in publisher
publisher = self.create_publisher(
    Float32,
    '/temperature',
    qos_profile
)

# Or in subscriber
subscription = self.create_subscription(
    Float32,
    '/temperature',
    self.callback,
    qos_profile
)
```

### QoS Settings

| Setting | Options | Use Case |
|---------|---------|----------|
| **Reliability** | RELIABLE, BEST_EFFORT | RELIABLE: sensor data; BEST_EFFORT: video streams |
| **Durability** | TRANSIENT_LOCAL, VOLATILE | TRANSIENT_LOCAL: important config; VOLATILE: sensor streams |
| **History** | KEEP_ALL, KEEP_LAST | KEEP_LAST: use less memory; KEEP_ALL: ensure no loss |
| **Depth** | Integer | How many messages to buffer |

### Preset QoS Profiles

```python
from rclpy.qos import qos_profile_sensor_data
from rclpy.qos import qos_profile_default

# Use preset for sensor data (unreliable, best-effort)
publisher = self.create_publisher(
    Float32,
    '/sensor_data',
    qos_profile_sensor_data
)

# Use default (reliable, keep last 10)
publisher = self.create_publisher(
    Float32,
    '/important_data',
    qos_profile_default
)
```

---

## Part 7: Multi-Node Communication System

Let's build a complete system with multiple nodes:

**System Design:**
```
Sensor Node ────publishes──> /sensor_data  ──┐
                                             ├──> Logger Node
Motor Node ──publishes──> /motor_status ────┤
                                             └──> Visualizer Node
```

**File: `sensor_node.py`**

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random

class SensorNode(Node):
    def __init__(self):
        super().__init__('sensor_node')
        self.pub = self.create_publisher(Float32, '/sensor_data', 10)
        self.timer = self.create_timer(0.5, self.read_sensor)

    def read_sensor(self):
        msg = Float32()
        msg.data = 20.0 + (random.random() * 10.0)
        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(SensorNode())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**File: `logger_node.py`**

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class LoggerNode(Node):
    def __init__(self):
        super().__init__('logger_node')
        self.sub = self.create_subscription(Float32, '/sensor_data', self.log_data, 10)

    def log_data(self, msg):
        self.get_logger().info(f'Sensor reading: {msg.data:.2f}')

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(LoggerNode())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Run multiple terminals:**

```bash
# Terminal 1
python3 sensor_node.py

# Terminal 2
python3 logger_node.py

# Terminal 3 (optional, view topics)
ros2 topic list
ros2 topic echo /sensor_data
```

---

## Part 8: Hands-On Exercises

### Exercise 3.1: Create a Simple Publisher

**Objective**: Publish messages to a topic

**Steps:**
1. Create `message_publisher.py`:
   ```python
   #!/usr/bin/env python3
   import rclpy
   from rclpy.node import Node
   from std_msgs.msg import String

   class MyPublisher(Node):
       def __init__(self):
           super().__init__('my_publisher')
           self.pub = self.create_publisher(String, '/my_topic', 10)
           self.timer = self.create_timer(1.0, self.publish)

       def publish(self):
           msg = String()
           msg.data = "Hello, ROS 2!"
           self.pub.publish(msg)
           self.get_logger().info(f'Published: {msg.data}')

   def main(args=None):
       rclpy.init(args=args)
       rclpy.spin(MyPublisher())
       rclpy.shutdown()

   if __name__ == '__main__':
       main()
   ```

2. Run: `python3 message_publisher.py`
3. In another terminal: `ros2 topic echo /my_topic`

**Expected output:**
```
data: Hello, ROS 2!
---
data: Hello, ROS 2!
```

**Difficulty**: ⭐ (Very Easy)
**Time**: 10 minutes

---

### Exercise 3.2: Create a Subscriber

**Objective**: Subscribe to and process messages

**Steps:**
1. Create `message_subscriber.py` that subscribes to `/my_topic`
2. Process the message in callback
3. Run both publisher and subscriber together

**Hint:** Use the code from [Part 3](#creating-subscribers) as reference

**Expected behavior**: Subscriber receives messages as publisher sends them

**Difficulty**: ⭐⭐ (Easy)
**Time**: 15 minutes

---

### Exercise 3.3: Two-Way Communication

**Objective**: Build publish-subscribe system with two nodes communicating

**Create `robot_command_publisher.py`:**
```python
# Publishes robot commands to /cmd_vel topic
# Messages: "forward", "backward", "stop", etc.
```

**Create `robot_controller_subscriber.py`:**
```python
# Subscribes to /cmd_vel and processes commands
# Logs what action the robot is taking
```

**Test it:**
```bash
# Terminal 1: Controller
python3 robot_controller_subscriber.py

# Terminal 2: Command publisher
python3 robot_command_publisher.py

# See both nodes communicate!
```

**Difficulty**: ⭐⭐⭐ (Intermediate)
**Time**: 25 minutes

---

### Mini Lab: Sensor Fusion

Create a system where multiple sensors publish, and one node subscribes to all:

```python
# Sensor 1: Temperature publisher
# Sensor 2: Humidity publisher
# Logger: Subscribes to both and prints readings
```

**Expected output:**
```
Temperature: 25.3°C
Humidity: 60%
Temperature: 24.8°C
Humidity: 61%
```

**Difficulty**: ⭐⭐⭐ (Intermediate)
**Time**: 30 minutes

---

## Part 9: Troubleshooting

### Issue 1: Subscriber Never Receives Messages

**Symptoms**: Subscriber running but no messages in callback

**Causes and Solutions:**

1. **Topic names don't match:**
   ```bash
   # Check topic names exactly
   ros2 topic list
   # Make sure publisher and subscriber use same name
   ```

2. **Publisher hasn't started yet:**
   ```bash
   # Start publisher first, then subscriber
   # Or check with: ros2 topic info /topic_name
   ```

3. **Different ROS domains:**
   ```bash
   # Check domain IDs match
   echo $ROS_DOMAIN_ID
   # Set if needed: export ROS_DOMAIN_ID=0
   ```

---

### Issue 2: Message Type Mismatch

**Error:**
```
Error creating subscription: Type mismatch
```

**Solution:**
```python
# Check types match EXACTLY
from std_msgs.msg import String  # Publisher

# Subscriber must use same type
self.create_subscription(String, '/topic', callback, 10)  # ✅ Correct

# Not this:
self.create_subscription(Float32, '/topic', callback, 10)  # ❌ Wrong type!
```

---

### Issue 3: Callback Never Called

**Symptoms**: Subscriber created but callback never executes

**Solution:**
```python
# Make sure you're SPINNING the node!
rclpy.spin(node)  # ✅ This is required

# Without spin, callbacks don't fire!
```

---

### Issue 4: High CPU Usage

**Symptoms**: CPU usage spikes when nodes communicate

**Solution:**
```python
# Increase timer intervals (slower publishing)
self.timer = self.create_timer(2.0, callback)  # 2 seconds instead of 0.1

# Use appropriate QoS settings
from rclpy.qos import qos_profile_sensor_data
pub = self.create_publisher(msg_type, topic, qos_profile_sensor_data)
```

---

## Part 10: Key Takeaways

### What You Learned

✅ **Pub-Sub Communication:**
- Publishers send, subscribers receive
- Decoupled: publishers and subscribers don't know each other
- Asynchronous: subscribers get messages when available

✅ **Implementation:**
- `create_publisher()` to send messages
- `create_subscription()` to receive messages
- Callbacks are called when messages arrive

✅ **Message Types:**
- Use built-in types: String, Float32, Point, Twist, etc.
- Create custom messages for specific needs
- Access fields: `msg.data`, `msg.x`, `msg.robot_name`, etc.

✅ **Quality of Service:**
- RELIABLE vs BEST_EFFORT
- KEEP_LAST vs KEEP_ALL
- Important for robustness

### Why This Matters

- **Decoupling**: Your sensor node doesn't need to know about the controller
- **Scalability**: Add more subscribers without changing publisher
- **Flexibility**: Change message types by updating definitions
- **Robustness**: QoS settings prevent message loss in critical systems

### Common Patterns

**Sensor Publishing:**
```python
# Publish at regular intervals
self.timer = self.create_timer(0.1, self.publish)
```

**Message Processing:**
```python
# Process each message as it arrives
self.sub = self.create_subscription(MsgType, '/topic', self.callback, 10)
```

**Multi-Subscriber System:**
```python
# Multiple nodes subscribe to same topic
self.sub1 = self.create_subscription(MsgType, '/data', callback1, 10)
self.sub2 = self.create_subscription(MsgType, '/data', callback2, 10)
```

---

## Self-Assessment Checkpoint

Before proceeding, verify you understand:

:::note Self-Check
1. **Conceptual**: What's the main difference between pub-sub and direct node-to-node communication?
   - Answer: Pub-sub decouples nodes; publishers and subscribers don't know each other

2. **Practical**: How do you create a publisher for Float32 messages?
   ```python
   self.pub = self.create_publisher(Float32, '/topic', 10)
   ```

3. **Callback**: When is a subscription callback called?
   - Answer: Every time a message arrives on the subscribed topic

4. **Message Types**: Name three common message types
   - Answer: String, Float32, Geometry Point (or others from std_msgs, geometry_msgs, sensor_msgs)

5. **Debugging**: Your subscriber isn't receiving messages. What's the most likely cause?
   - Answer: Topic names don't match exactly (case-sensitive!)
:::

---

## Next Steps

- **Ready for more?** Continue to [Chapter 1.4: Services and Actions](./chapter-1-4.md)
- **Want to practice more?** Create multi-node communication systems
- **Need help?** See [Troubleshooting](#part-9-troubleshooting) section
- **Questions?** Check [Module 1 Overview](./index.md) for learning resources

---

**Chapter Status**: ✅ COMPLETE
**Last Updated**: 2025-12-17
**Estimated Reading Time**: 50 minutes
**Estimated Hands-On Time**: 2-3 hours
