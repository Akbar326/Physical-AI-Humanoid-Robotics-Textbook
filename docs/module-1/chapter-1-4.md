---
title: "Chapter 1.4: Services and Actions"
sidebar_position: 4
description: "Implement synchronous and asynchronous request-reply patterns"
difficulty: Intermediate
time_hours: 3-4
module: 1
---

# Chapter 1.4: Services and Actions

:::info Chapter Overview
- **Difficulty**: Intermediate
- **Time Required**: 3-4 hours
- **Prerequisites**: Chapter 1.3
:::

## Learning Objectives

By the end of this chapter, you will be able to:

- [ ] Understand services and actions
- [ ] Create service servers and clients
- [ ] Implement action servers and clients
- [ ] Handle long-running tasks
- [ ] Deal with timeouts and errors

## Introduction

**Why This Matters**: Not all communication is pub-sub. Sometimes you need **request-reply**:
- A controller needs to **ask** the motor to move to position 45° and **wait** for confirmation
- A planner needs to **request** a path and **receive** the result
- A system needs to **call** a configuration service and **get** the response

**Services** (synchronous) and **Actions** (asynchronous) handle these patterns.

---

## Part 1: Services vs Pub-Sub vs Actions

### Communication Patterns Comparison

```
Pub-Sub (Chapter 1.3):
Publisher ──► Topic ──► Subscriber
One-way, asynchronous, fire-and-forget
Best for: Sensors → streaming data

Service (This chapter):
Client ──► Request ──► Server
         ◄── Response ◄──
Synchronous, request-reply
Best for: Quick queries, configuration

Action (This chapter):
Client ──► Goal ──► Server
       ◄── Feedback ◄──
       ◄── Result ◄──
Asynchronous with progress updates
Best for: Long-running tasks
```

### When to Use Each

| Pattern | Use Case | Example |
|---------|----------|---------|
| **Pub-Sub** | Streaming data | Sensor readings, camera frames |
| **Service** | Quick request-reply | Get battery level, check status |
| **Action** | Long task with feedback | Move arm to position, take photo |

---

## Part 2: Understanding Services

### Service Basics

A **service** is:
- **Request-Reply**: Client sends request, server responds
- **Synchronous**: Client waits for answer
- **Single exchange**: One request, one response

```
Client                 Service
  │                      │
  ├─ (1) Send Request ──→│
  │   "What is battery?"  │
  │                      │
  │                    (2) Process
  │                      │
  ├─ (3) Receive Reply ←──│
  │   "Battery: 85%"      │
  │                      │
```

### Service Definition

Services use `.srv` files that define request and response:

**File: `my_robot_package/srv/GetBatteryLevel.srv`**

```
# Request (client sends)
---
# Response (server sends)
int32 battery_level
bool is_charging
```

The `---` separates request from response.

---

## Part 3: Creating a Service Server

**File: `battery_server.py`**

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.srv import GetBatteryLevel

class BatteryServer(Node):
    """Service server that provides battery status"""

    def __init__(self):
        super().__init__('battery_server')

        # Create a service
        self.service = self.create_service(
            GetBatteryLevel,
            'get_battery_level',
            self.handle_battery_request
        )
        self.get_logger().info('Battery service ready')
        self.battery_level = 85

    def handle_battery_request(self, request, response):
        """Called when client makes a request"""
        # Generate response
        response.battery_level = self.battery_level
        response.is_charging = False

        self.get_logger().info(
            f'Battery requested: returning {response.battery_level}%'
        )
        return response

def main(args=None):
    rclpy.init(args=args)
    node = BatteryServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

## Part 4: Creating a Service Client

**File: `battery_client.py`**

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.srv import GetBatteryLevel
import time

class BatteryClient(Node):
    """Service client that requests battery status"""

    def __init__(self):
        super().__init__('battery_client')

        # Create a client
        self.client = self.create_client(
            GetBatteryLevel,
            'get_battery_level'
        )

        # Wait for service to be available
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting...')

        self.get_logger().info('Service available!')

    def send_request(self):
        """Make a service request"""
        request = GetBatteryLevel.Request()

        # Send request and wait for response
        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        response = future.result()
        self.get_logger().info(
            f'Battery Level: {response.battery_level}% '
            f'(Charging: {response.is_charging})'
        )
        return response

def main(args=None):
    rclpy.init(args=args)
    node = BatteryClient()
    response = node.send_request()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Running Service-Client Example

**Terminal 1: Server**
```bash
python3 battery_server.py
# [INFO] Battery service ready
```

**Terminal 2: Client**
```bash
python3 battery_client.py
# [INFO] Service available!
# [INFO] Battery Level: 85% (Charging: False)
```

---

## Part 5: Understanding Actions

### Action Basics

An **action** is for long-running tasks:
- **Asynchronous**: Client sends goal and continues
- **Feedback**: Server sends progress updates
- **Cancellable**: Client can cancel mid-task

```
Client                   Action
  │                        │
  ├─ (1) Send Goal ───────→│
  │   "Move to 90°"        │
  │                       (2) Processing...
  ├─ (3) Receive Feedback ←│
  │   "Now at 45°"         │
  ├─ (4) Receive Feedback ←│
  │   "Now at 90°"         │
  │                        │
  ├─ (5) Receive Result ───←─
  │   "Success"            │
```

### Action Definition

**File: `my_robot_package/action/MoveArm.action`**

```
# Goal (client sends)
float32 target_angle
---
# Result (final response)
bool success
string message
---
# Feedback (progress updates)
float32 current_angle
int32 percentage_complete
```

---

## Part 6: Creating an Action Server

**File: `arm_server.py`**

```python
#!/usr/bin/env python3

import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from example_interfaces.action import Fibonacci
import time

class ArmActionServer(Node):
    """Simulates moving a robot arm"""

    def __init__(self):
        super().__init__('arm_action_server')

        self.action_server = ActionServer(
            self,
            Fibonacci,
            'move_arm',
            self.execute_callback
        )

    def execute_callback(self, goal_handle):
        """Called when client sends a goal"""
        self.get_logger().info(f'Executing goal: {goal_handle.request.target}')

        # Simulate moving arm to angle
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.current_angle = 0.0

        for i in range(int(goal_handle.request.target)):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                return Fibonacci.Result()

            # Simulate movement
            feedback_msg.current_angle = float(i)
            feedback_msg.percentage_complete = int((i / goal_handle.request.target) * 100)
            goal_handle.publish_feedback(feedback_msg)

            time.sleep(0.1)

        # Send result
        result = Fibonacci.Result()
        result.success = True
        result.message = f'Moved to {goal_handle.request.target}°'
        goal_handle.succeed()

        return result

def main(args=None):
    rclpy.init(args=args)
    node = ArmActionServer()
    executor = MultiThreadedExecutor()
    rclpy.spin(node, executor=executor)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

## Part 7: Creating an Action Client

**File: `arm_client.py`**

```python
#!/usr/bin/env python3

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from example_interfaces.action import Fibonacci

class ArmActionClient(Node):
    """Requests arm movement"""

    def __init__(self):
        super().__init__('arm_action_client')
        self.action_client = ActionClient(self, Fibonacci, 'move_arm')

    def send_goal(self, target):
        """Send movement goal to action server"""
        # Wait for server
        if not self.action_client.wait_for_server(timeout_sec=5.0):
            self.get_logger().error('Action server not available!')
            return

        # Create goal
        goal_msg = Fibonacci.Goal()
        goal_msg.target = target

        # Send goal
        self.get_logger().info(f'Sending goal: move to {target}°')
        self.send_goal_future = self.action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        self.send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        """Called when server accepts/rejects goal"""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected!')
            return

        self.get_logger().info('Goal accepted!')
        self.result_future = goal_handle.get_result_async()
        self.result_future.add_done_callback(self.result_callback)

    def feedback_callback(self, feedback_msg):
        """Called when server sends feedback"""
        feedback = feedback_msg.feedback
        self.get_logger().info(
            f'Progress: {feedback.percentage_complete}% '
            f'(Angle: {feedback.current_angle}°)'
        )

    def result_callback(self, future):
        """Called when action completes"""
        result = future.result().result
        self.get_logger().info(
            f'Action complete: {result.success} - {result.message}'
        )

def main(args=None):
    rclpy.init(args=args)
    node = ArmActionClient()
    node.send_goal(90.0)

    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

## Part 8: Hands-On Exercises

### Exercise 4.1: Create a Simple Service

**Objective**: Implement a request-reply pattern

Create `calculator_server.py` that provides an **Add** service:
- Request: two numbers
- Response: sum

Build and test with a client node.

**Difficulty**: ⭐⭐ (Easy)
**Time**: 20 minutes

---

### Exercise 4.2: Service Client

Create `calculator_client.py` that:
1. Waits for service availability
2. Sends request (5 + 3)
3. Receives and prints result

**Expected output**: `Result: 8`

**Difficulty**: ⭐⭐ (Easy)
**Time**: 15 minutes

---

### Exercise 4.3: Long-Running Action

Create an action server that simulates a **download** task:
- Goal: filename to download
- Feedback: bytes downloaded, percentage
- Result: success status, total size

Create corresponding client that:
- Sends goal
- Displays feedback progress
- Shows final result

**Difficulty**: ⭐⭐⭐ (Intermediate)
**Time**: 30 minutes

---

## Part 9: Troubleshooting

### Issue 1: Service Not Found

**Solution**:
```bash
# Check if service is available
ros2 service list

# If missing, verify server is running
ps aux | grep server
```

---

### Issue 2: Service Timeout

```python
# Increase timeout
self.client.wait_for_service(timeout_sec=10.0)  # 10 second timeout
```

---

### Issue 3: Action Client Doesn't Receive Feedback

**Solution**:
- Verify `feedback_callback` is registered
- Check action server is publishing feedback

---

## Part 10: Key Takeaways

✅ **Services**: Synchronous request-reply for simple queries
✅ **Actions**: Asynchronous long-running tasks with feedback
✅ **Callbacks**: Handle responses, feedback, and results
✅ **Error Handling**: Always check for success/failure

---

## Self-Assessment Checkpoint

1. When should you use a **Service** vs **Topic**?
   - Answer: Service for request-reply, topic for streaming data

2. Can a client cancel a service request after sending it?
   - Answer: No, services are synchronous

3. What's the difference between action feedback and result?
   - Answer: Feedback is progress updates, result is final outcome

---

## Next Steps

- Continue to [Chapter 1.5: Parameters and Launch Files](./chapter-1-5.md)
- Practice services and actions in combination
- See [Troubleshooting](#part-9-troubleshooting) for issues

---

**Chapter Status**: ✅ COMPLETE
**Last Updated**: 2025-12-17
**Estimated Reading Time**: 45 minutes
**Estimated Hands-On Time**: 2-3 hours
