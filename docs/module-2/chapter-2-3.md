---
title: "Chapter 2.3: Physics Simulation and Materials"
sidebar_position: 3
description: "Master physics engines, material properties, and realistic physical interactions"
difficulty: Intermediate
time_hours: 4-5
module: 2
---

# Chapter 2.3: Physics Simulation and Materials

:::info Chapter Overview
- **Difficulty**: Intermediate
- **Time Required**: 4-5 hours
- **Prerequisites**: Chapter 2.2
- **Tools**: Gazebo, physics engines, material databases
:::

## Learning Objectives

By the end of this chapter, you will be able to:
- [ ] Understand different physics engines and their tradeoffs
- [ ] Configure physics engine parameters effectively
- [ ] Define realistic material properties
- [ ] Handle collisions and contact dynamics
- [ ] Simulate friction and damping
- [ ] Calibrate simulations to match real-world behavior
- [ ] Debug physics issues

## Introduction

**Why This Matters**: Physics simulation is only useful if it's **accurate**. A gripper simulated with wrong friction will behave completely differently than the real robot. A ball with incorrect density will bounce unpredictably. Proper physics configuration is the difference between simulation that helps and simulation that misleads.

**The Physics Reality Gap**:
```
Sim-to-Real Transfer Success depends on:
  - Accurate material properties (friction, density, restitution)
  - Correct physics engine choice (speed vs accuracy tradeoff)
  - Proper collision detection and contact response
  - Realistic damping and energy dissipation
  - Environmental effects (gravity, time stepping)
```

---

## Part 1: Physics Engines in Gazebo

### Available Physics Engines

Gazebo supports multiple physics engines, each with different characteristics:

| Engine | Speed | Accuracy | Stability | Best For |
|--------|-------|----------|-----------|----------|
| **ODE** | Fast | Medium | Good | Real-time simulation, wheeled robots |
| **Bullet** | Very Fast | Medium | Excellent | Many collisions, stability-critical |
| **DART** | Medium | High | Good | Humanoids, articulated systems |
| **Simbody** | Medium | Very High | Excellent | Bio-mechanical systems |

### ODE (Open Dynamics Engine)

**Advantages:**
- Fast, suitable for real-time control
- Stable for most robotics applications
- Good contact dynamics
- Well-integrated with ROS

**Disadvantages:**
- Less accurate than DART/Simbody
- Can have numerical errors with very high forces

**Configuration:**
```xml
<physics type='ode'>
  <!-- Gravity -->
  <gravity>0 0 -9.81</gravity>

  <!-- Time stepping -->
  <max_step_size>0.001</max_step_size>
  <real_time_factor>1.0</real_time_factor>
  <real_time_update_rate>1000</real_time_update_rate>

  <!-- Solver -->
  <ode>
    <solver>
      <type>quick</type>
      <iters>50</iters>
      <sor>1.3</sor>
    </solver>
    <constraints>
      <cfm>0.0</cfm>
      <erp>0.2</erp>
      <contact_max_correcting_vel>100</contact_max_correcting_vel>
      <contact_surface_layer>0.001</contact_surface_layer>
    </constraints>
  </ode>
</physics>
```

### Bullet Physics

**Advantages:**
- Extremely stable with many bodies
- Good for large environments
- Handles soft bodies

**Disadvantages:**
- Less real-time friendly
- Can be slower than ODE

**Configuration:**
```xml
<physics type='bullet'>
  <gravity>0 0 -9.81</gravity>
  <max_step_size>0.001</max_step_size>
  <bullet>
    <solver>
      <type>sequential_impulse</type>
      <iters>50</iters>
    </solver>
  </bullet>
</physics>
```

### DART (Dynamic Animation and Robotics Toolkit)

**Advantages:**
- High accuracy for articulated systems
- Excellent for humanoid robots
- More realistic joint dynamics
- Better constraint handling

**Disadvantages:**
- Slower than ODE
- More computationally expensive

**Configuration:**
```xml
<physics type='dart'>
  <gravity>0 0 -9.81</gravity>
  <max_step_size>0.001</max_step_size>
  <dart>
    <solver>
      <type>dantzig</type>
    </solver>
  </dart>
</physics>
```

### Choosing Your Physics Engine

**Use ODE when:**
- Building wheeled mobile robots
- Need real-time performance
- Objects are rigid and well-defined

**Use Bullet when:**
- Many bodies in simulation (100+)
- Need maximum stability
- Complex stacked objects

**Use DART when:**
- Building humanoid robots
- Need accurate joint dynamics
- Articulated systems with many DOFs

---

## Part 2: Material Properties

### Understanding Material Properties

Every material in Gazebo is defined by these properties:

```xml
<material>
  <!-- Appearance -->
  <ambient>R G B A</ambient>
  <diffuse>R G B A</diffuse>
  <specular>R G B A</specular>

  <!-- Physics -->
  <friction>
    <mu>0.3</mu>           <!-- Friction coefficient (static) -->
    <mu2>0.3</mu2>         <!-- Friction coefficient (kinetic) -->
    <fdir1>1 0 0</fdir1>   <!-- Friction direction -->
    <slip1>0.0</slip1>     <!-- Slip (0 = no slip) -->
    <slip2>0.0</slip2>
  </friction>

  <restitution>0.5</restitution>  <!-- Bounciness (0 = no bounce, 1 = perfect) -->
</material>
```

### Common Material Friction Coefficients

| Material Pair | Friction (μ) | Notes |
|---------------|-------------|-------|
| **Rubber on concrete** | 0.7-0.9 | High grip, wheeled robots |
| **Metal on metal** | 0.15-0.25 | Low friction, sliding |
| **Plastic on plastic** | 0.2-0.5 | Medium, depends on surface |
| **Rubber on wood** | 0.25-0.5 | Moderate grip |
| **Ice (extremely smooth)** | 0.02-0.05 | Very low friction |
| **Robot gripper on object** | 0.4-0.8 | Needs tuning per gripper |

### Density and Mass

**Never hardcode mass!** Instead, define density and let Gazebo calculate mass:

```xml
<model name='steel_cube'>
  <link name='body'>
    <!-- Inertia calculated from geometry and density -->
    <inertial>
      <density>7850</density>  <!-- kg/m³ for steel -->
    </inertial>

    <!-- OR explicitly set mass -->
    <inertial>
      <mass>5.0</mass>
      <inertia>
        <ixx>0.042</ixx>
        <iyy>0.042</iyy>
        <izz>0.042</izz>
      </inertia>
    </inertial>

    <collision><geometry><box><size>0.1 0.1 0.1</size></box></geometry></collision>
    <visual><geometry><box><size>0.1 0.1 0.1</size></box></geometry></visual>
  </link>
</model>
```

### Common Material Densities

| Material | Density (kg/m³) |
|----------|-----------------|
| Aluminum | 2,700 |
| Steel | 7,850 |
| Wood | 500-900 |
| Plastic (ABS) | 1,050 |
| Rubber | 920 |
| Water | 1,000 |

---

## Part 3: Collision and Contact Configuration

### Surface Contact Parameters

When two objects collide, Gazebo uses these parameters:

```xml
<surface>
  <friction>
    <mu>0.5</mu>
    <mu2>0.5</mu2>
  </friction>

  <!-- Bounciness -->
  <restitution>0.3</restitution>

  <!-- Energy absorption -->
  <bounce>
    <restitution_threshold>0.001</restitution_threshold>
  </bounce>

  <!-- Contact dynamics -->
  <contact>
    <collide_without_contact>false</collide_without_contact>
    <collide_without_contact_bitmask>1</collide_without_contact_bitmask>
    <ode>
      <soft_cfm>0.0</soft_cfm>
      <soft_erp>0.2</soft_erp>
      <kp>1000000.0</kp>
      <kd>100.0</kd>
      <max_vel>0.01</max_vel>
      <min_depth>0.0</min_depth>
    </ode>
  </contact>
</surface>
```

### Contact Parameters Explained

- **cfm (Constraint Force Mixing)**: Adds "softness" to contacts (0 = hard, higher = softer)
- **erp (Error Reduction Parameter)**: How quickly errors are corrected (0.2 = typical)
- **kp (Spring stiffness)**: How hard objects push back (higher = stiffer)
- **kd (Damping)**: Energy dissipation in contact (higher = more damping)

---

## Part 4: Complete Physics World Example

```xml
<?xml version='1.0'?>
<sdf version='1.9'>
  <world name='physics_demo'>
    <!-- ODE physics engine -->
    <physics type='ode'>
      <gravity>0 0 -9.81</gravity>
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>

      <ode>
        <solver>
          <type>quick</type>
          <iters>50</iters>
          <sor>1.3</sor>
        </solver>
        <constraints>
          <cfm>0.0</cfm>
          <erp>0.2</erp>
          <contact_max_correcting_vel>100</contact_max_correcting_vel>
        </constraints>
      </ode>
    </physics>

    <!-- Ground plane -->
    <model name='ground'>
      <static>true</static>
      <link name='link'>
        <collision>
          <geometry><plane><normal>0 0 1</normal></plane></geometry>
          <surface>
            <friction><mu>0.8</mu></friction>
          </surface>
        </collision>
        <visual>
          <geometry><plane><normal>0 0 1</normal></plane></geometry>
          <material><ambient>0.5 0.5 0.5 1</ambient></material>
        </visual>
      </link>
    </model>

    <!-- Steel ball (high density, low friction) -->
    <model name='steel_ball'>
      <pose>0 0 2 0 0 0</pose>
      <link name='body'>
        <inertial>
          <density>7850</density>
        </inertial>
        <collision>
          <geometry><sphere><radius>0.05</radius></sphere></geometry>
          <surface>
            <friction>
              <mu>0.1</mu>
              <mu2>0.1</mu2>
            </friction>
            <restitution>0.5</restitution>
          </surface>
        </collision>
        <visual>
          <geometry><sphere><radius>0.05</radius></sphere></geometry>
          <material><ambient>0.8 0.8 0.8 1</ambient></material>
        </visual>
      </link>
    </model>

    <!-- Rubber ball (low density, high friction, bouncy) -->
    <model name='rubber_ball'>
      <pose>1 0 2 0 0 0</pose>
      <link name='body'>
        <inertial>
          <density>920</density>
        </inertial>
        <collision>
          <geometry><sphere><radius>0.05</radius></sphere></geometry>
          <surface>
            <friction>
              <mu>0.7</mu>
              <mu2>0.7</mu2>
            </friction>
            <restitution>0.9</restitution>
          </surface>
        </collision>
        <visual>
          <geometry><sphere><radius>0.05</radius></geometry>
          <material><ambient>1 0 0 1</ambient></material>
        </visual>
      </link>
    </model>

    <!-- Slippery surface (icy) -->
    <model name='ice_block'>
      <pose>0 1 0.5 0 0 0</pose>
      <static>true</static>
      <link name='body'>
        <collision>
          <geometry><box><size>1 1 0.1</size></box></geometry>
          <surface>
            <friction>
              <mu>0.02</mu>
              <mu2>0.02</mu2>
            </friction>
            <restitution>0.2</restitution>
          </surface>
        </collision>
        <visual>
          <geometry><box><size>1 1 0.1</size></box></geometry>
          <material><ambient>0.7 1 1 1</ambient></material>
        </visual>
      </link>
    </model>

    <light type='directional' name='sun'>
      <pose>0 0 10 0 0 0</pose>
    </light>
  </world>
</sdf>
```

---

## Part 5: Damping and Energy Dissipation

### Linear and Angular Damping

Objects lose energy naturally through damping:

```xml
<link name='body'>
  <inertial>
    <mass>1.0</mass>
    <!-- Damping reduces motion over time -->
    <linear_damping>0.04</linear_damping>
    <angular_damping>0.04</angular_damping>
  </inertial>

  <collision><geometry><box><size>0.1 0.1 0.1</size></box></geometry></collision>
  <visual><geometry><box><size>0.1 0.1 0.1</size></box></geometry></visual>
</link>
```

### Damping Values Guide

| Damping | Effect | Use Case |
|---------|--------|----------|
| 0.0 | No damping, endless motion | Space environments (unrealistic) |
| 0.01-0.05 | Minimal damping | Light, free-moving objects |
| 0.1-0.2 | Moderate damping | Typical wheeled robots |
| 0.3-0.5 | High damping | Heavy objects, friction-rich |

---

## Part 6: Hands-On Exercises

### Exercise 3.1: Physics Engine Comparison

Create three worlds with the same scene using different physics engines:

1. ODE engine world
2. Bullet engine world
3. DART engine world

Drop 10 boxes from height and measure:
- Time to settle
- Final rest stability
- Computational speed

**Difficulty**: ⭐⭐⭐ (Intermediate)
**Time**: 45 minutes

---

### Exercise 3.2: Material Property Tuning

Create a gripper grasping scenario:
1. Define gripper pads with different friction values
2. Spawn an object (e.g., a can)
3. Simulate grasping with various friction coefficients
4. Find the minimum friction needed to hold the object

**Difficulty**: ⭐⭐⭐ (Intermediate)
**Time**: 40 minutes

---

### Exercise 3.3: Friction Measurement

Create a friction experiment:
1. Build an inclined plane (adjustable angle)
2. Spawn boxes with different materials (wood, rubber, metal)
3. Find the angle at which each slides
4. Calculate friction coefficient: μ = tan(θ)

Python script for angle adjustment:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from gazebo_msgs.srv import SetEntityPose
from geometry_msgs.msg import Pose
import math

class FrictionExperiment(Node):
    def __init__(self):
        super().__init__('friction_experiment')
        self.set_pose_client = self.create_client(
            SetEntityPose,
            '/gazebo/set_entity_state'
        )
        while not self.set_pose_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for Gazebo service...')

    def incline_plane(self, angle_degrees):
        """Rotate plane to specified angle"""
        angle_rad = math.radians(angle_degrees)

        pose = Pose()
        pose.position.x = 0.0
        pose.position.y = 0.0
        pose.position.z = 0.0

        # Rotation around Y axis
        q = self.euler_to_quaternion(0, angle_rad, 0)
        pose.orientation.x = q[0]
        pose.orientation.y = q[1]
        pose.orientation.z = q[2]
        pose.orientation.w = q[3]

        request = SetEntityPose.Request()
        request.entity_name = 'incline_plane'
        request.pose = pose

        self.set_pose_client.call_async(request)
        self.get_logger().info(f'Incline angle: {angle_degrees}°')

    @staticmethod
    def euler_to_quaternion(roll, pitch, yaw):
        """Convert Euler angles to quaternion"""
        cr, cp, cy = [math.cos(x/2) for x in [roll, pitch, yaw]]
        sr, sp, sy = [math.sin(x/2) for x in [roll, pitch, yaw]]

        return [
            sr*cp*cy - cr*sp*sy,
            cr*sp*cy + sr*cp*sy,
            cr*cp*sy - sr*sp*cy,
            cr*cp*cy + sr*sp*sy
        ]

def main(args=None):
    rclpy.init(args=args)
    node = FrictionExperiment()

    # Test angles from 0 to 60 degrees
    for angle in range(0, 61, 5):
        node.incline_plane(angle)
        rclpy.spin_once(node, timeout_sec=1.0)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Difficulty**: ⭐⭐⭐ (Intermediate)
**Time**: 50 minutes

---

## Part 7: Troubleshooting Physics Issues

### Issue 1: Objects Fall Through Surfaces

**Problem**: Objects penetrate collision geometry

**Causes:**
- Time step too large
- Collision geometry doesn't match visual
- Static objects not properly flagged

**Solutions:**
```xml
<!-- Reduce time step -->
<max_step_size>0.0001</max_step_size>

<!-- Increase contact surface layer -->
<contact_surface_layer>0.005</contact_surface_layer>

<!-- Ensure static objects are marked -->
<model name='ground'>
  <static>true</static>
```

---

### Issue 2: Jittering or Exploding Objects

**Problem**: Physics becomes unstable, objects shake violently

**Causes:**
- Too-high forces
- Incompatible material properties
- High solver iterations needed

**Solutions:**
```xml
<!-- Increase solver iterations -->
<ode>
  <solver>
    <iters>100</iters>  <!-- Default is 50 -->
  </solver>
</ode>

<!-- Reduce spring stiffness -->
<contact>
  <ode>
    <kp>1000000.0</kp>  <!-- Lower if unstable -->
  </ode>
</contact>
```

---

### Issue 3: Objects Slide When They Shouldn't

**Problem**: High-friction objects still slip unexpectedly

**Causes:**
- Friction coefficient too low
- Contact point issues
- Solver not converging

**Solutions:**
```xml
<!-- Increase friction -->
<surface>
  <friction>
    <mu>0.9</mu>
    <mu2>0.9</mu2>
  </friction>
</surface>

<!-- Reduce slip -->
<friction>
  <slip1>0.0</slip1>
  <slip2>0.0</slip2>
</friction>
```

---

## Part 8: Physics Best Practices

### For Accurate Sim-to-Real Transfer

1. **Measure real materials**
   ```bash
   # Experimentally determine friction
   # Use inclined plane test like Exercise 3.3
   ```

2. **Use correct densities**
   - Look up material properties
   - Cross-check with actual robot weights
   - Document all material assumptions

3. **Start conservative**
   - Use ODE for robotics (proven track record)
   - Keep time step at 1ms or smaller
   - Test with real-world calibration

4. **Debug systematically**
   - Compare sim vs real behavior
   - Identify one parameter at a time
   - Document changes and results

### Physics Configuration Template

```xml
<?xml version='1.0'?>
<sdf version='1.9'>
  <world name='physics_template'>
    <!-- ODE engine - reliable for robotics -->
    <physics type='ode'>
      <gravity>0 0 -9.81</gravity>
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
      <real_time_update_rate>1000</real_time_update_rate>

      <ode>
        <solver>
          <type>quick</type>
          <iters>50</iters>
          <sor>1.3</sor>
        </solver>
        <constraints>
          <cfm>0.0</cfm>
          <erp>0.2</erp>
          <contact_max_correcting_vel>100</contact_max_correcting_vel>
          <contact_surface_layer>0.001</contact_surface_layer>
        </constraints>
      </ode>
    </physics>

    <!-- Your models here -->

    <light type='directional' name='sun'>
      <pose>0 0 10 0 0 0</pose>
    </light>
  </world>
</sdf>
```

---

## Part 9: Key Takeaways

✅ **Physics Engines**: ODE for speed, DART for accuracy, Bullet for stability
✅ **Materials**: Define friction, density, and restitution realistically
✅ **Contacts**: Tune collision parameters for your specific use case
✅ **Damping**: Add realistic energy dissipation
✅ **Calibration**: Always validate against real-world measurements

---

## Self-Assessment Checkpoint

1. **What physics engine should you use for a humanoid robot?**
   - Answer: DART (high accuracy for articulated systems)

2. **What does a friction coefficient of 0.5 mean?**
   - Answer: Moderate grip; typical for rubber or plastic surfaces

3. **How do you make an object heavier without changing its size?**
   - Answer: Increase its density or explicitly set mass in inertial tag

4. **What happens if your time step is too large?**
   - Answer: Objects can fall through surfaces and physics becomes unstable

5. **Which parameter controls bounciness: friction or restitution?**
   - Answer: Restitution (0=no bounce, 1=perfect bounce)

---

## Next Steps

- Continue to [Chapter 2.4: Plugins and Custom Simulation](./chapter-2-4.md)
- Experiment with different material combinations
- Create a physics calibration experiment for your robot
- Compare simulation vs real-world behavior

---

**Chapter Status**: ✅ COMPLETE
**Last Updated**: 2025-12-17
**Estimated Reading Time**: 50 minutes
**Estimated Hands-On Time**: 2-3 hours

**Next Chapter**: [Chapter 2.4: Plugins and Custom Simulation](./chapter-2-4.md)
