---
title: "Chapter 2.1: Introduction to Simulation"
sidebar_position: 1
description: "Understand simulation principles and Gazebo fundamentals"
difficulty: Intermediate
time_hours: 3-4
module: 2
---

# Chapter 2.1: Introduction to Simulation

:::info Chapter Overview
- **Difficulty**: Intermediate
- **Time Required**: 3-4 hours
- **Prerequisites**: Module 1 (ROS 2 Fundamentals)
- **Tools**: Gazebo Fortress, ROS 2 Humble
:::

## Learning Objectives

By the end of this chapter, you will be able to:

- [ ] Understand why simulation is critical in robotics
- [ ] Explain physics simulation principles
- [ ] Navigate Gazebo architecture and components
- [ ] Install and verify Gazebo setup
- [ ] Create and run your first Gazebo world
- [ ] Spawn objects and robots in simulation

## Introduction

**Why This Matters**: Testing robots in the real world is expensive and dangerous:
- **Cost**: Real robots cost $10,000-$1,000,000+
- **Time**: Development cycles are slow without simulation
- **Safety**: Bugs can damage hardware or hurt people
- **Iteration**: Testing changes takes weeks with real hardware

**Simulation solves this**. Before deploying code to a real robot:
1. Test everything in simulation
2. Debug behavior safely
3. Verify performance
4. Optimize algorithms
5. Train machine learning models

**The Reality:**
- Boston Dynamics: 90% development in simulation
- NVIDIA: Sim-to-real transfer learning
- Industry Standard: Gazebo is used by thousands of roboticists

---

## Part 1: Why Simulation Matters

### The Cost of Real-World Testing

```
Scenario: Autonomous mobile robot development

Option A - Real Hardware:
├─ Robot cost: $50,000
├─ Damage from bug: -$5,000 per crash
├─ Per crash repair time: 2 days
├─ Testing one feature: 2 weeks
└─ Total: Too expensive and slow!

Option B - Simulation First:
├─ Simulation cost: $0 (free software!)
├─ Testing one feature: 2 hours
├─ Deploy only after verified
├─ Real-world testing: 1 day for final validation
└─ Total: Fast, safe, and economical!
```

### Types of Simulation

| Type | Use Case | Speed | Accuracy |
|------|----------|-------|----------|
| **Physics Only** | Dynamics testing | ⚡⚡⚡ Very Fast | ⭐⭐⭐ Good |
| **Rendering** | Visual perception | ⚡⚡ Medium | ⭐⭐ Moderate |
| **Photorealistic** | Camera/vision testing | ⚡ Slow | ⭐⭐⭐⭐ Excellent |
| **Hardware-in-Loop** | Real controller testing | ⚡ Slow | ⭐⭐⭐⭐ Excellent |

**Gazebo Fortress** is a **physics + rendering simulator** - perfect balance for most robotics work.

---

## Part 2: Physics Simulation Fundamentals

### How Physics Engines Work

A physics engine simulates real-world physics by:

```
Step 1: Read current state (positions, velocities, forces)
           ↓
Step 2: Apply physics equations (Newton's laws)
           ├─ F = ma (force, mass, acceleration)
           ├─ Gravity: F = m * g
           ├─ Friction: F_friction = μ * F_normal
           └─ Collisions: Detect and respond
           ↓
Step 3: Update positions and velocities
           ↓
Step 4: Detect collisions between objects
           ↓
Step 5: Repeat 60-1000 times per second
```

### Key Physics Concepts

**Mass and Inertia**:
```
Heavy ball: mass = 10 kg
             Takes force to move ↔ Resists rotation
Light ball: mass = 1 kg
             Easy to move ↔ Easy to rotate
```

**Gravity**:
```
On Earth: g = 9.81 m/s² (downward)
Drop a ball: acceleration = 9.81 m/s²
             After 1 sec: velocity = 9.81 m/s
             After 2 sec: velocity = 19.62 m/s
```

**Friction**:
```
Smooth surface (ice):    friction = low  → slides far
Rough surface (carpet):  friction = high → stops quickly
```

**Collision**:
```
Object A hits Object B:
├─ Is collision detected? (bounding box overlap)
├─ Calculate collision response
├─ Apply forces to both objects
└─ Update velocities

If no collision detection: objects pass through each other!
```

### Time Stepping

The physics engine runs at discrete time steps:

```
Real time: ─────────────────────────────────── (continuous)

Simulation: ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌
             (60-1000 updates per second)

Update rate: Usually 1000 Hz (0.001 second steps)
```

**Important**: Smaller time steps = more accurate but slower.

---

## Part 3: Gazebo Architecture

### What is Gazebo?

**Gazebo** is an open-source 3D robot simulator featuring:
- **Physics Engine**: Accurate simulation of forces, collisions, friction
- **Rendering Engine**: 3D graphics for visualization
- **Sensor Simulation**: Cameras, LIDAR, IMU, GPS, etc.
- **Plugin System**: Custom code for complex behaviors
- **ROS 2 Integration**: Native support for ROS 2 nodes

### Gazebo Components

```
┌─ Gazebo Client (GUI)
│  ├─ 3D Viewport (what you see)
│  ├─ Model inspector
│  └─ Simulation controls
│
├─ Gazebo Server (Physics)
│  ├─ Physics engine (ODE, Bullet, DART)
│  ├─ Collision detection
│  ├─ Sensor simulation
│  └─ Plugins
│
└─ Your ROS 2 Node
   ├─ Publishes commands
   └─ Subscribes to sensor data

All communicate via DDS (from Module 1)
```

### Gazebo File Formats

**SDF (Simulation Description Format)**:
```xml
<?xml version='1.0'?>
<sdf version='1.9'>
  <world name='default'>
    <physics type='ode'>
      <gravity>0 0 -9.81</gravity>
    </physics>

    <model name='ground_plane'>
      <!-- Model definition -->
    </model>
  </world>
</sdf>
```

**URDF (Unified Robot Description Format)**:
- Older format, still widely used
- Defines robot structure (links, joints)
- Can be converted to SDF

**DAE (COLLADA)**:
- 3D model format for meshes
- Contains geometry and textures

---

## Part 4: Setting Up Gazebo

### Installation

**Ubuntu 22.04 (Recommended)**:
```bash
# Install Gazebo Fortress
sudo apt-get update
sudo apt-get install gazebo

# Verify installation
gazebo --version
# Output: Gazebo version 6.x.x
```

**Check Dependencies**:
```bash
# You should have:
source /opt/ros/humble/setup.bash  # ROS 2 sourced

# Test Gazebo with ROS 2
gazebo
# Should open GUI with empty world
```

### Verify Installation

Create `test_gazebo.sh`:

```bash
#!/bin/bash

echo "=== Gazebo Installation Verification ==="

# 1. Check Gazebo
echo "1. Gazebo version:"
gazebo --version

# 2. Check ROS 2
echo "2. ROS 2 environment:"
echo "   ROS_DISTRO=$ROS_DISTRO"

# 3. Check Gazebo-ROS bridge
ros2 pkg list | grep gazebo_ros
echo "   gazebo_ros found: $?"

# 4. Test Gazebo launch
echo "3. Testing Gazebo launch (will open GUI)..."
timeout 5 gazebo /opt/ros/humble/share/gazebo_ros/launch/test.sdf &
wait $!

echo "=== Verification Complete ==="
```

Run it:
```bash
bash test_gazebo.sh
```

---

## Part 5: Your First Gazebo World

### Creating a Simple World

**File: `my_first_world.world`** (SDF format):

```xml
<?xml version='1.0'?>
<sdf version='1.9'>
  <world name='default'>
    <!-- Physics engine -->
    <physics type='ode'>
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
      <gravity>0 0 -9.81</gravity>
    </physics>

    <!-- Ground plane -->
    <model name='ground_plane'>
      <static>true</static>
      <link name='link'>
        <collision name='collision'>
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>100 100</size>
            </plane>
          </geometry>
        </collision>
        <visual name='visual'>
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>100 100</size>
            </plane>
          </geometry>
          <material>
            <ambient>0.8 0.8 0.8 1</ambient>
            <diffuse>0.8 0.8 0.8 1</diffuse>
            <specular>0.8 0.8 0.8 1</specular>
          </material>
        </visual>
      </link>
    </model>

    <!-- A simple box -->
    <model name='box'>
      <pose>0 0 0.5 0 0 0</pose>
      <link name='link'>
        <inertial>
          <mass>1.0</mass>
          <inertia>
            <ixx>0.1</ixx>
            <iyy>0.1</iyy>
            <izz>0.1</izz>
          </inertia>
        </inertial>
        <collision name='collision'>
          <geometry>
            <box>
              <size>0.2 0.2 0.2</size>
            </box>
          </geometry>
        </collision>
        <visual name='visual'>
          <geometry>
            <box>
              <size>0.2 0.2 0.2</size>
            </box>
          </geometry>
          <material>
            <ambient>1 0 0 1</ambient>
            <diffuse>1 0 0 1</diffuse>
            <specular>1 0 0 1</specular>
          </material>
        </visual>
      </link>
    </model>

    <!-- Light source -->
    <light type='directional' name='sun'>
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <attenuation>
        <range>1000</range>
        <constant>0.9</constant>
        <linear>0.01</linear>
        <quadratic>0.001</quadratic>
      </attenuation>
      <direction>-0.5 0.1 -0.9</direction>
    </light>
  </world>
</sdf>
```

### Running Your First World

```bash
# Launch Gazebo with your world
gazebo my_first_world.world

# Or from ROS 2
gazebo /path/to/my_first_world.world
```

**What You'll See:**
- Ground plane (gray checkerboard)
- Red box floating above ground
- Box falls due to gravity
- Bounces on ground with physics

Congratulations! You've simulated physics! 🎉

---

## Part 6: Understanding the Gazebo GUI

When Gazebo opens, you'll see:

```
┌─────────────────────────────────────────┐
│  [File] [Edit] [View] [Camera] [Tools]  │
├─────────────────────────────────────────┤
│                                         │
│          3D Viewport                    │ ├─ Model List (right)
│  (your simulation here)                 │ │ ├─ ground_plane
│                                         │ │ ├─ box
│                                         │ │ └─ sun
│                                         │ │
│                                         │ ├─ Property Inspector
│                                         │ │ (shows selected object)
│                                         │
└─────────────────────────────────────────┘
```

### Useful Keyboard Controls

```
Mouse Controls:
- Left Click + Drag:     Rotate view
- Middle Click + Drag:   Pan camera
- Right Click + Drag:    Zoom
- Scroll Wheel:          Zoom in/out

Keyboard:
- R:    Reset simulation
- P:    Pause/Resume
- C:    Toggle collision visualization
- T:    Toggle transparency
- W:    Move selected object
- E:    Rotate selected object
- Q:    Exit
```

### Spawning Objects Dynamically

Instead of hardcoding objects in the world file, spawn them from code:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from gazebo_msgs.srv import SpawnEntity
from gazebo_msgs.srv import DeleteEntity

class SpawnObjectNode(Node):
    def __init__(self):
        super().__init__('spawn_object')

        # Create spawn service client
        self.spawn_client = self.create_client(
            SpawnEntity,
            '/spawn_entity'
        )

        # Wait for service
        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for spawn service...')

    def spawn_box(self, name, x, y, z):
        """Spawn a box at (x, y, z)"""

        # SDF model of a box
        sdf_xml = '''<?xml version='1.0'?>
<sdf version='1.9'>
  <model name='%s'>
    <link name='link'>
      <inertial>
        <mass>1.0</mass>
        <inertia>
          <ixx>0.1</ixx>
          <iyy>0.1</iyy>
          <izz>0.1</izz>
        </inertia>
      </inertial>
      <collision name='collision'>
        <geometry>
          <box><size>0.2 0.2 0.2</size></box>
        </geometry>
      </collision>
      <visual name='visual'>
        <geometry>
          <box><size>0.2 0.2 0.2</size></box>
        </geometry>
        <material>
          <ambient>0 1 0 1</ambient>
          <diffuse>0 1 0 1</diffuse>
        </material>
      </visual>
    </link>
  </model>
</sdf>''' % name

        # Create request
        request = SpawnEntity.Request()
        request.name = name
        request.xml = sdf_xml
        request.robot_namespace = ''
        request.initial_pose.position.x = float(x)
        request.initial_pose.position.y = float(y)
        request.initial_pose.position.z = float(z)

        # Send request
        future = self.spawn_client.call_async(request)
        self.get_logger().info(f'Spawning {name} at ({x}, {y}, {z})')

def main(args=None):
    rclpy.init(args=args)
    node = SpawnObjectNode()

    # Spawn a few boxes
    node.spawn_box('box1', 0.0, 0.0, 1.0)
    node.spawn_box('box2', 1.0, 0.0, 1.0)
    node.spawn_box('box3', 0.0, 1.0, 1.0)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**To Use:**
1. Start Gazebo: `gazebo my_first_world.world`
2. In another terminal: `python3 spawn_objects.py`
3. Watch boxes appear in the simulation!

---

## Part 7: Hands-On Exercises

### Exercise 2.1: Launch Gazebo

**Objective**: Get Gazebo running

**Steps:**
1. Open terminal
2. Source ROS 2: `source /opt/ros/humble/setup.bash`
3. Launch Gazebo: `gazebo`
4. Verify it opens without errors
5. Close Gazebo: Press Q or close window

**Expected Result**: Gazebo opens with empty world

**Difficulty**: ⭐ (Very Easy)
**Time**: 5 minutes

---

### Exercise 2.2: Create Your Own World File

**Objective**: Write a world with multiple objects

**Steps:**
1. Create `my_world.world` with:
   - Ground plane
   - 3-4 objects (boxes, spheres, cylinders)
   - Light source
   - Gravity enabled

2. Launch: `gazebo my_world.world`

3. Observe objects fall and interact

**Expected Behavior**: Objects fall due to gravity, collide realistically

**Difficulty**: ⭐⭐ (Easy)
**Time**: 20 minutes

**Hint**: Reference the example in [Part 5](#part-5-your-first-gazebo-world)

---

### Exercise 2.3: Spawn Objects Programmatically

**Objective**: Dynamically spawn objects from Python

**Steps:**
1. Create `spawn_demo.py` from the example in [Part 6](#spawning-objects-dynamically)
2. Start Gazebo: `gazebo`
3. In another terminal, run: `python3 spawn_demo.py`
4. Watch boxes appear in the simulation

**Expected Output:**
```
[INFO] Waiting for spawn service...
[INFO] Spawning box1 at (0.0, 0.0, 1.0)
[INFO] Spawning box2 at (1.0, 0.0, 1.0)
[INFO] Spawning box3 at (0.0, 1.0, 1.0)
```

**Difficulty**: ⭐⭐⭐ (Intermediate)
**Time**: 25 minutes

---

### Mini Lab: Physics Experimentation

Create different scenarios to understand physics:

```bash
# Test 1: Different masses
# Spawn light ball (mass=0.1) and heavy ball (mass=10)
# Drop both - watch heavy one fall faster? (No! Both fall same)

# Test 2: Different friction
# Create surfaces with friction=0 (ice) and friction=1 (carpet)
# Slide a box across both

# Test 3: Initial velocity
# Spawn ball with initial velocity
# Watch it move and interact with obstacles
```

**Difficulty**: ⭐⭐⭐ (Intermediate)
**Time**: 30 minutes

---

## Part 8: Troubleshooting

### Issue 1: Gazebo Won't Launch

**Error:**
```
gazebo: command not found
```

**Solution:**
```bash
# Install Gazebo
sudo apt-get install gazebo

# Or verify installation
which gazebo

# If still not found, check PATH
echo $PATH
```

---

### Issue 2: ROS 2 Not Found in Gazebo

**Error:**
```
gazebo_ros extension not found
```

**Solution:**
```bash
# Make sure to source ROS 2 BEFORE launching Gazebo
source /opt/ros/humble/setup.bash
gazebo
```

---

### Issue 3: Objects Fall Through Ground Plane

**Cause**: No collision geometry on ground plane

**Solution:**
```xml
<!-- Ensure ground plane has collision -->
<model name='ground_plane'>
  <static>true</static>
  <link name='link'>
    <collision name='collision'>
      <geometry>
        <plane>
          <normal>0 0 1</normal>
          <size>100 100</size>
        </plane>
      </geometry>
    </collision>
    <!-- ... visual ... -->
  </link>
</model>
```

---

### Issue 4: Simulation Very Slow

**Cause**: Physics timestep too small or rendering heavy

**Solution:**
```xml
<physics type='ode'>
  <max_step_size>0.01</max_step_size>  <!-- Increase from 0.001 -->
  <real_time_factor>0.5</real_time_factor>  <!-- Allow slower than realtime -->
</physics>
```

---

### Issue 5: Spawn Service Not Available

**Error:**
```
Waiting for spawn service... (never completes)
```

**Cause**: Gazebo not running or ROS 2 bridge not loaded

**Solution:**
```bash
# Start Gazebo first
gazebo &

# Then run spawn script
python3 spawn_objects.py

# Or use ROS 2 launch file (Chapter 2.5)
```

---

## Part 9: Key Takeaways

### What You Learned

✅ **Why Simulation**: Safe, fast, and cost-effective development
✅ **Physics Basics**: Gravity, forces, collisions, time stepping
✅ **Gazebo Architecture**: Client-server, plugins, ROS 2 integration
✅ **SDF Format**: XML description of worlds and objects
✅ **Spawning Objects**: Dynamically create entities in simulation
✅ **GUI Controls**: Navigate and interact with the 3D environment

### Key Concepts to Remember

```
Physics Simulation = Gravity + Collisions + Forces
                   updated every millisecond
                   produces realistic motion

Gazebo = Physics Engine + 3D Rendering + ROS 2 Bridge
       = Everything you need to test robots
```

### Why This Matters

- **Safe**: Test dangerous behaviors without risk
- **Fast**: Iterate in seconds, not weeks
- **Repeatable**: Same initial conditions → same results
- **Scalable**: Simulate 100 robots at once
- **Transferable**: Skills transfer to real robots

---

## Self-Assessment Checkpoint

Before proceeding, verify you understand:

:::note Self-Check
1. **Conceptual**: Why is simulation better than real-world testing?
   - Answer: Safer, faster, cheaper, easier to iterate

2. **Physics**: What determines how fast an object falls?
   - Answer: Gravity (not mass!). Time. All objects accelerate at 9.81 m/s²

3. **Practical**: How do you launch Gazebo with a custom world?
   - Answer: `gazebo my_world.world`

4. **Architecture**: What are the three main Gazebo components?
   - Answer: Physics engine, rendering engine, plugin system

5. **Programming**: How do you spawn an object from Python?
   - Answer: Create SpawnEntity service client and call it with SDF model
:::

---

## Next Steps

- **Ready for more?** Continue to [Chapter 2.2: Gazebo Basics and World Setup](./chapter-2-2.md)
- **Want to experiment?** Create different world files with various objects
- **Need help?** See [Troubleshooting](#part-8-troubleshooting) section
- **Questions?** Check [Module 2 Overview](./index.md) for resources

---

**Chapter Status**: ✅ COMPLETE
**Last Updated**: 2025-12-17
**Estimated Reading Time**: 50 minutes
**Estimated Hands-On Time**: 2-3 hours
