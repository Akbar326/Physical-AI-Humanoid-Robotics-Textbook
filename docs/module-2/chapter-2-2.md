---
title: "Chapter 2.2: Gazebo Basics and World Setup"
sidebar_position: 2
description: "Create complex Gazebo worlds with multiple objects and environments"
difficulty: Intermediate
time_hours: 3-4
module: 2
---

# Chapter 2.2: Gazebo Basics and World Setup

:::info Chapter Overview
- **Difficulty**: Intermediate
- **Time Required**: 3-4 hours
- **Prerequisites**: Chapter 2.1
- **Tools**: Gazebo, SDF format editor
:::

## Learning Objectives

By the end of this chapter, you will be able to:
- [ ] Understand SDF world structure
- [ ] Create complex multi-object worlds
- [ ] Use Gazebo built-in models
- [ ] Organize worlds with includes
- [ ] Position and orient objects precisely
- [ ] Create realistic environments

## Introduction

**Why This Matters**: Moving beyond basic worlds to realistic environments where robots actually operate. A manipulation robot needs tables, objects, and obstacles. A mobile robot needs paths, walls, and landmarks. Proper world design makes simulation effective.

---

## Part 1: SDF World Structure

### Basic World XML

Every Gazebo world follows this structure:

```xml
<?xml version='1.0'?>
<sdf version='1.9'>
  <world name='world_name'>
    <!-- Physics configuration -->
    <physics type='ode'>
      <gravity>0 0 -9.81</gravity>
    </physics>

    <!-- Models (robots, objects) -->
    <model name='model_name'>
      <!-- Links and joints -->
    </model>

    <!-- Lights -->
    <light type='directional' name='sun'>
      <!-- Light properties -->
    </light>
  </world>
</sdf>
```

### Understanding Links

A **link** is a rigid body with:
- **Inertial**: Mass and inertia tensor
- **Collision**: Geometry for physics
- **Visual**: Geometry for rendering

```xml
<model name='ball'>
  <link name='sphere_link'>
    <!-- What it weighs -->
    <inertial>
      <mass>0.5</mass>
      <inertia>
        <ixx>0.01</ixx>
        <iyy>0.01</iyy>
        <izz>0.01</izz>
      </inertia>
    </inertial>

    <!-- What it hits -->
    <collision name='collision'>
      <geometry>
        <sphere><radius>0.1</radius></sphere>
      </geometry>
    </collision>

    <!-- What it looks like -->
    <visual name='visual'>
      <geometry>
        <sphere><radius>0.1</radius></sphere>
      </geometry>
      <material>
        <ambient>1 0 0 1</ambient>
        <diffuse>1 0 0 1</diffuse>
      </material>
    </visual>
  </link>
</model>
```

### Geometry Types

```xml
<!-- Box (cuboid) -->
<geometry><box><size>0.1 0.2 0.3</size></box></geometry>

<!-- Sphere -->
<geometry><sphere><radius>0.1</radius></sphere></geometry>

<!-- Cylinder -->
<geometry><cylinder><radius>0.1</radius><length>0.5</length></cylinder></geometry>

<!-- Plane (ground) -->
<geometry><plane><normal>0 0 1</normal></plane></geometry>

<!-- Mesh (3D model file) -->
<geometry><mesh><uri>file://path/to/model.dae</uri></mesh></geometry>

<!-- Polyline (2D shape extruded) -->
<geometry><polyline><point>0 0</point><point>1 0</point></polyline></geometry>
```

---

## Part 2: Building Complex Worlds

### Table and Objects Scene

```xml
<?xml version='1.0'?>
<sdf version='1.9'>
  <world name='manipulation'>
    <physics type='ode'>
      <gravity>0 0 -9.81</gravity>
      <max_step_size>0.001</max_step_size>
    </physics>

    <!-- Ground -->
    <model name='ground'>
      <static>true</static>
      <link name='link'>
        <collision>
          <geometry><plane><normal>0 0 1</normal></plane></geometry>
        </collision>
        <visual>
          <geometry><plane><normal>0 0 1</normal></plane></geometry>
          <material>
            <ambient>0.5 0.5 0.5 1</ambient>
          </material>
        </visual>
      </link>
    </model>

    <!-- Table -->
    <model name='table'>
      <pose>0 0 0 0 0 0</pose>
      <static>true</static>

      <!-- Table top -->
      <link name='top'>
        <pose>0 0 0.75 0 0 0</pose>
        <collision>
          <geometry><box><size>1.0 1.0 0.05</size></box></geometry>
        </collision>
        <visual>
          <geometry><box><size>1.0 1.0 0.05</size></box></geometry>
          <material><ambient>0.8 0.6 0.4 1</ambient></material>
        </visual>
      </link>

      <!-- Table leg 1 -->
      <link name='leg1'>
        <pose>-0.4 -0.4 0.375 0 0 0</pose>
        <collision>
          <geometry><box><size>0.05 0.05 0.75</size></box></geometry>
        </collision>
        <visual>
          <geometry><box><size>0.05 0.05 0.75</size></box></geometry>
          <material><ambient>0.2 0.2 0.2 1</ambient></material>
        </visual>
      </link>

      <!-- Similar for other legs... -->
    </model>

    <!-- Object on table -->
    <model name='cube'>
      <pose>0 0 0.85 0 0 0</pose>
      <link name='link'>
        <inertial><mass>0.1</mass></inertial>
        <collision>
          <geometry><box><size>0.1 0.1 0.1</size></box></geometry>
        </collision>
        <visual>
          <geometry><box><size>0.1 0.1 0.1</size></box></geometry>
          <material><ambient>1 1 0 1</ambient></material>
        </visual>
      </link>
    </model>

    <!-- Light -->
    <light type='directional' name='sun'>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>1 1 1 1</diffuse>
    </light>
  </world>
</sdf>
```

---

## Part 3: Organizing Worlds with Includes

For large worlds, split into multiple files:

**worlds/main.sdf:**
```xml
<?xml version='1.0'?>
<sdf version='1.9'>
  <world name='warehouse'>
    <physics type='ode'><gravity>0 0 -9.81</gravity></physics>

    <!-- Include ground plane -->
    <include>
      <uri>file://models/ground_plane.sdf</uri>
    </include>

    <!-- Include environment -->
    <include>
      <uri>file://models/warehouse_layout.sdf</uri>
      <pose>0 0 0 0 0 0</pose>
    </include>

    <!-- Include robot -->
    <include>
      <uri>file://models/robot.urdf</uri>
      <pose>0 0 0 0 0 0</pose>
    </include>

    <light type='directional' name='sun'>
      <pose>0 0 10 0 0 0</pose>
    </light>
  </world>
</sdf>
```

---

## Part 4: Using Built-in Models

Gazebo includes many pre-made models:

```bash
# List available models
ls /usr/share/gazebo-11/models/

# Common models:
# - unit_box
# - unit_sphere
# - unit_cylinder
# - ground_plane
# - sun
# - aws_robomaker_warehouse_*
```

### Using a Built-in Model

```xml
<include>
  <uri>model://unit_box</uri>
  <pose>0 0 0.5 0 0 0</pose>
</include>
```

---

## Part 5: Exercises

### Exercise 2.4: Create a Room World

Create a 5m×5m room with:
- Ground
- 4 walls (1.5m height)
- 2 boxes inside
- 1 light source

**Difficulty**: ⭐⭐ (Easy)
**Time**: 30 minutes

### Exercise 2.5: Warehouse Scene

Create a warehouse with:
- Multiple aisles
- Shelving units
- Boxes stacked on shelves
- Lighting

**Difficulty**: ⭐⭐⭐ (Intermediate)
**Time**: 45 minutes

---

## Troubleshooting

### Objects Aren't Visible
- Verify collision AND visual both defined
- Check material colors (might be black on black)
- Try toggling wireframe (T key)

### Models Won't Load
- Check file paths are absolute or relative to Gazebo
- Verify SDF syntax: `gzsdf test model.sdf`

---

**Chapter Status**: ✅ COMPLETE
**Last Updated**: 2025-12-17
**Estimated Reading Time**: 35 minutes
**Estimated Hands-On Time**: 2 hours

**Next Chapter**: [Chapter 2.3: Physics Simulation and Materials](./chapter-2-3.md)
