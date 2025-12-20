---
title: "Chapter 2.4: Plugins and Custom Simulation"
sidebar_position: 4
description: "Extend Gazebo with custom plugins and behaviors"
difficulty: Advanced
time_hours: 4-5
module: 2
---

# Chapter 2.4: Plugins and Custom Simulation

:::info Chapter Overview
- **Difficulty**: Advanced
- **Time Required**: 4-5 hours
- **Prerequisites**: Chapter 2.3
- **Tools**: C++, CMake, Gazebo SDK, Plugin API
:::

## Learning Objectives

By the end of this chapter, you will be able to:
- [ ] Understand Gazebo plugin architecture
- [ ] Create WorldPlugin implementations
- [ ] Create ModelPlugin implementations
- [ ] Build custom plugins with CMake
- [ ] Load plugins in worlds and robots
- [ ] Implement sensor simulators
- [ ] Add custom physics behaviors
- [ ] Debug plugin issues

## Introduction

**Why This Matters**: Default Gazebo can simulate physics and rendering, but every robot is unique. Some robots need custom sensor behaviors, others need special control logic. **Plugins** let you extend Gazebo without modifying its core code. They run at simulation runtime and can:
- Read sensor data and publish to ROS 2
- Control models based on custom logic
- Implement specialized behaviors
- Simulate custom physics

A plugin transforms Gazebo from a generic simulator into one tailored to your robot.

---

## Part 1: Gazebo Plugin Architecture

### Types of Plugins

Gazebo supports several plugin types:

| Plugin Type | Scope | Use Case |
|-------------|-------|----------|
| **WorldPlugin** | Entire simulation world | Gravity control, global sensors, wind |
| **ModelPlugin** | Single model/robot | Robot-specific behaviors, control |
| **SensorPlugin** | Individual sensor | Custom sensor simulation |
| **SystemPlugin** | Gazebo core | Advanced customization |
| **VisualPlugin** | Rendering/graphics | Visual effects, custom rendering |

### Plugin Lifecycle

```
Gazebo Startup
    ↓
Plugin Constructor
    ↓
OnLoad() - Configure plugin
    ↓
Simulation Running
    ↓
OnUpdate() - Called every physics step (1000x per second for 1ms step)
    ↓
OnReset() - When user resets simulation
    ↓
Plugin Destructor
    ↓
Gazebo Shutdown
```

### Plugin Interfaces

All plugins inherit from a common base class:

```cpp
// All plugins inherit from this
class Plugin
{
    public:
        Plugin() {}
        virtual ~Plugin() {}
        virtual void Load(... _sdf, ...)  = 0;
        virtual void Init() {}
        virtual void Reset() {}
};
```

---

## Part 2: Creating a Simple WorldPlugin

A WorldPlugin can monitor and control the entire simulation.

### Step 1: Create Plugin Header

**File: `include/my_world_plugin.h`**

```cpp
#ifndef MY_WORLD_PLUGIN_H
#define MY_WORLD_PLUGIN_H

#include <gazebo/common/Plugin.hh>
#include <gazebo/physics/World.hh>
#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/float64.hpp>

namespace gazebo {
  class MyWorldPlugin : public WorldPlugin
  {
    public:
        MyWorldPlugin();
        ~MyWorldPlugin();

        // Called when plugin is loaded
        void Load(physics::WorldPtr world, sdf::ElementPtr sdf) override;

        // Called every physics step
        void OnUpdate();

    private:
        // Gazebo components
        physics::WorldPtr world_;
        event::ConnectionPtr update_conn_;

        // ROS 2 components
        std::shared_ptr<rclcpp::Node> ros_node_;
        rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr gravity_pub_;

        // Parameters
        double gravity_z_;
        double wind_strength_;
  };
}

#endif
```

### Step 2: Implement Plugin

**File: `src/my_world_plugin.cpp`**

```cpp
#include <my_world_plugin.h>
#include <gazebo/physics/physics.hh>

using namespace gazebo;

// Constructor
MyWorldPlugin::MyWorldPlugin()
    : gravity_z_(0.0), wind_strength_(0.0)
{
}

// Destructor
MyWorldPlugin::~MyWorldPlugin()
{
    update_conn_.reset();
}

// Called when plugin loads
void MyWorldPlugin::Load(physics::WorldPtr world, sdf::ElementPtr sdf)
{
    this->world_ = world;

    // Read parameters from SDF
    if (sdf->HasElement("gravity_z")) {
        gravity_z_ = sdf->Get<double>("gravity_z");
    }

    if (sdf->HasElement("wind_strength")) {
        wind_strength_ = sdf->Get<double>("wind_strength");
    }

    // Initialize ROS 2
    if (!rclcpp::ok()) {
        rclcpp::init(0, nullptr);
    }

    ros_node_ = std::make_shared<rclcpp::Node>("world_plugin_node");
    gravity_pub_ = ros_node_->create_publisher<std_msgs::msg::Float64>(
        "world/gravity",
        10
    );

    // Connect update callback
    update_conn_ = event::Events::ConnectWorldUpdateBegin(
        std::bind(&MyWorldPlugin::OnUpdate, this)
    );

    gzmsg << "World plugin loaded successfully" << std::endl;
}

void MyWorldPlugin::OnUpdate()
{
    // This gets called ~1000 times per second
    // (on every physics step for 1ms time step)

    // Read current gravity
    math::Vector3d gravity = world_->Gravity();

    // Publish gravity Z component
    std_msgs::msg::Float64 msg;
    msg.data = gravity.Z();
    gravity_pub_->publish(msg);

    // Optionally modify gravity (e.g., for day/night cycle)
    if (wind_strength_ > 0) {
        // Add some wind effect
        double time = world_->SimTime().Double();
        gravity.X() = wind_strength_ * std::sin(time);
    }
}

// Plugin registration
GZ_REGISTER_WORLD_PLUGIN(MyWorldPlugin)
```

---

## Part 3: Creating a ModelPlugin

ModelPlugins control individual robots/models.

### Step 1: Header

**File: `include/my_robot_plugin.h`**

```cpp
#ifndef MY_ROBOT_PLUGIN_H
#define MY_ROBOT_PLUGIN_H

#include <gazebo/common/Plugin.hh>
#include <gazebo/physics/Model.hh>
#include <gazebo/physics/Link.hh>
#include <gazebo/physics/Joint.hh>
#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <sensor_msgs/msg/joint_state.hpp>

namespace gazebo {
  class MyRobotPlugin : public ModelPlugin
  {
    public:
        MyRobotPlugin();
        ~MyRobotPlugin();

        void Load(physics::ModelPtr model, sdf::ElementPtr sdf) override;
        void OnUpdate();

    private:
        // Callbacks
        void CmdVelCallback(const geometry_msgs::msg::Twist::SharedPtr msg);
        void PublishJointState();

        // Gazebo components
        physics::ModelPtr model_;
        physics::LinkPtr base_link_;
        std::vector<physics::JointPtr> joints_;
        event::ConnectionPtr update_conn_;

        // ROS 2 components
        std::shared_ptr<rclcpp::Node> ros_node_;
        rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr cmd_vel_sub_;
        rclcpp::Publisher<sensor_msgs::msg::JointState>::SharedPtr joint_state_pub_;

        // Control
        double linear_velocity_;
        double angular_velocity_;
        double max_force_;
  };
}

#endif
```

### Step 2: Implementation

**File: `src/my_robot_plugin.cpp`**

```cpp
#include <my_robot_plugin.h>
#include <gazebo/physics/physics.hh>

using namespace gazebo;

MyRobotPlugin::MyRobotPlugin()
    : linear_velocity_(0.0), angular_velocity_(0.0), max_force_(10.0)
{
}

MyRobotPlugin::~MyRobotPlugin()
{
    update_conn_.reset();
}

void MyRobotPlugin::Load(physics::ModelPtr model, sdf::ElementPtr sdf)
{
    this->model_ = model;

    // Get base link
    base_link_ = model_->GetLink("base_link");
    if (!base_link_) {
        gzwarn << "Could not find base_link" << std::endl;
        return;
    }

    // Get all joints
    for (unsigned int i = 0; i < model_->GetJointCount(); ++i) {
        joints_.push_back(model_->GetJoint(i));
    }

    // Read parameters from SDF
    if (sdf->HasElement("max_force")) {
        max_force_ = sdf->Get<double>("max_force");
    }

    // Initialize ROS 2
    if (!rclcpp::ok()) {
        rclcpp::init(0, nullptr);
    }

    std::string robot_name = model_->GetName();
    ros_node_ = std::make_shared<rclcpp::Node>(robot_name + "_plugin");

    // Create ROS publishers and subscribers
    cmd_vel_sub_ = ros_node_->create_subscription<geometry_msgs::msg::Twist>(
        robot_name + "/cmd_vel",
        10,
        std::bind(&MyRobotPlugin::CmdVelCallback, this, std::placeholders::_1)
    );

    joint_state_pub_ = ros_node_->create_publisher<sensor_msgs::msg::JointState>(
        robot_name + "/joint_states",
        10
    );

    // Connect update callback
    update_conn_ = event::Events::ConnectWorldUpdateBegin(
        std::bind(&MyRobotPlugin::OnUpdate, this)
    );

    gzmsg << "Robot plugin loaded for: " << robot_name << std::endl;
}

void MyRobotPlugin::CmdVelCallback(const geometry_msgs::msg::Twist::SharedPtr msg)
{
    linear_velocity_ = msg->linear.x;
    angular_velocity_ = msg->angular.z;
}

void MyRobotPlugin::OnUpdate()
{
    // Apply forces to base link
    ignition::math::Vector3d force(linear_velocity_ * max_force_, 0, 0);
    base_link_->AddForce(force);

    // Apply torque
    ignition::math::Vector3d torque(0, 0, angular_velocity_ * max_force_);
    base_link_->AddTorque(torque);

    // Publish joint states
    PublishJointState();
}

void MyRobotPlugin::PublishJointState()
{
    auto msg = std::make_unique<sensor_msgs::msg::JointState>();
    msg->header.stamp = rclcpp::Clock().now();
    msg->header.frame_id = "world";

    for (const auto& joint : joints_) {
        msg->name.push_back(joint->GetName());
        msg->position.push_back(joint->Position());
        msg->velocity.push_back(joint->GetVelocity(0));
        // Effort would require getting joint torques
    }

    joint_state_pub_->publish(*msg);
}

GZ_REGISTER_MODEL_PLUGIN(MyRobotPlugin)
```

---

## Part 4: Building Plugins with CMake

### CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.5)
project(my_gazebo_plugins)

# C++ standard
set(CMAKE_CXX_STANDARD 17)

# Find required packages
find_package(gazebo REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(Ignition-Math REQUIRED)

# Include directories
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${GAZEBO_INCLUDE_DIRS}
)

# Link directories
link_directories(${GAZEBO_LIBRARY_DIRS})

# World plugin
add_library(my_world_plugin SHARED
    src/my_world_plugin.cpp
)

ament_target_dependencies(my_world_plugin
    gazebo
    rclcpp
    std_msgs
)

target_link_libraries(my_world_plugin
    ${GAZEBO_LIBRARIES}
    Ignition-Math::Ignition-Math
)

# Robot plugin
add_library(my_robot_plugin SHARED
    src/my_robot_plugin.cpp
)

ament_target_dependencies(my_robot_plugin
    gazebo
    rclcpp
    geometry_msgs
    sensor_msgs
)

target_link_libraries(my_robot_plugin
    ${GAZEBO_LIBRARIES}
    Ignition-Math::Ignition-Math
)

# Install plugins
install(TARGETS
    my_world_plugin
    my_robot_plugin
    DESTINATION lib
)

# Install headers
install(DIRECTORY include/
    DESTINATION include
)
```

### Build Commands

```bash
# Create build directory
mkdir build && cd build

# Configure
cmake ..

# Build
make

# Install
sudo make install

# Verify
ls /usr/local/lib/libmy_*plugin.so
```

---

## Part 5: Loading Plugins in Worlds

### In SDF World File

**File: `world_with_plugin.sdf`**

```xml
<?xml version='1.0'?>
<sdf version='1.9'>
  <world name='plugin_world'>
    <!-- Load world plugin -->
    <plugin
        filename='libmy_world_plugin.so'
        name='my_world_plugin'>
      <gravity_z>-9.81</gravity_z>
      <wind_strength>0.5</wind_strength>
    </plugin>

    <!-- Ground plane -->
    <model name='ground'>
      <static>true</static>
      <link name='link'>
        <collision>
          <geometry><plane><normal>0 0 1</normal></plane></geometry>
        </collision>
        <visual>
          <geometry><plane><normal>0 0 1</normal></plane></geometry>
          <material><ambient>0.5 0.5 0.5 1</ambient></material>
        </visual>
      </link>
    </model>

    <!-- Robot with plugin -->
    <model name='my_robot'>
      <pose>0 0 0.5 0 0 0</pose>

      <!-- Load robot plugin -->
      <plugin
          filename='libmy_robot_plugin.so'
          name='my_robot_plugin'>
        <max_force>10.0</max_force>
      </plugin>

      <!-- Robot body -->
      <link name='base_link'>
        <inertial><mass>5.0</mass></inertial>
        <collision>
          <geometry><box><size>0.5 0.5 0.3</size></box></geometry>
        </collision>
        <visual>
          <geometry><box><size>0.5 0.5 0.3</size></box></geometry>
          <material><ambient>1 0 0 1</ambient></material>
        </visual>
      </link>

      <!-- Joints if needed -->
    </model>

    <light type='directional' name='sun'>
      <pose>0 0 10 0 0 0</pose>
    </light>
  </world>
</sdf>
```

---

## Part 6: Sensor Plugin Example

Simulating a custom sensor:

```cpp
class CustomSensorPlugin : public SensorPlugin
{
    public:
        void Load(sensors::SensorPtr sensor, sdf::ElementPtr sdf) override;
        void OnUpdate();

    private:
        sensors::SensorPtr sensor_;
        event::ConnectionPtr update_conn_;
        rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr pub_;
};

void CustomSensorPlugin::Load(sensors::SensorPtr sensor, sdf::ElementPtr sdf)
{
    sensor_ = sensor;

    // Get update rate
    double rate = sensor_->UpdateRate();

    // Create ROS publisher
    ros_node_ = std::make_shared<rclcpp::Node>("custom_sensor");
    pub_ = ros_node_->create_publisher<std_msgs::msg::Float32>(
        "sensor/reading",
        10
    );

    // Connect to update event
    update_conn_ = event::Events::ConnectSensorUpdate(
        std::bind(&CustomSensorPlugin::OnUpdate, this)
    );
}

void CustomSensorPlugin::OnUpdate()
{
    // Generate simulated sensor data
    std_msgs::msg::Float32 msg;
    msg.data = 42.0;  // Your sensor logic here
    pub_->publish(msg);
}

GZ_REGISTER_SENSOR_PLUGIN(CustomSensorPlugin)
```

---

## Part 7: Hands-On Exercises

### Exercise 4.1: Simple WorldPlugin

Create a WorldPlugin that:
1. Publishes current simulation time to ROS 2 topic `/world/time`
2. Reads wind parameters from SDF
3. Applies a wind force to objects (optional)

**Difficulty**: ⭐⭐⭐ (Intermediate)
**Time**: 45 minutes

---

### Exercise 4.2: Robot Control Plugin

Create a ModelPlugin that:
1. Subscribes to `/robot/cmd_vel` (Twist messages)
2. Applies forces to robot base link
3. Publishes joint states on `/robot/joint_states`

**Difficulty**: ⭐⭐⭐⭐ (Advanced)
**Time**: 60 minutes

---

### Exercise 4.3: Custom Sensor

Create a SensorPlugin that simulates:
1. A temperature sensor
2. Publishes temperature based on robot proximity
3. Visualize in RViz

**Difficulty**: ⭐⭐⭐⭐ (Advanced)
**Time**: 50 minutes

---

## Part 8: Troubleshooting Plugins

### Issue 1: Plugin Won't Load

**Error**: `Error loading plugin`

**Solutions:**
```bash
# Check plugin path
export GAZEBO_PLUGIN_PATH=$GAZEBO_PLUGIN_PATH:/usr/local/lib

# Verify plugin exists
ls -la /usr/local/lib/libmy_*plugin.so

# Check library dependencies
ldd /usr/local/lib/libmy_robot_plugin.so

# Rebuild if needed
cd build && cmake .. && make && sudo make install
```

---

### Issue 2: ROS 2 Initialization Fails

**Problem**: Plugin can't initialize ROS 2 node

**Solution:**
```cpp
// Check if ROS already initialized
if (!rclcpp::ok()) {
    rclcpp::init(0, nullptr);
}

// Verify ROS_DOMAIN_ID is set
ros_node_ = std::make_shared<rclcpp::Node>("plugin_node");
```

---

### Issue 3: Plugin Crashes on Update

**Problem**: OnUpdate() crashes or causes segmentation fault

**Solutions:**
- Add null pointer checks:
```cpp
void MyPlugin::OnUpdate()
{
    if (!model_ || !world_) return;
    // Safe to use model_ and world_ now
}
```

- Use proper locking for shared resources
- Avoid blocking operations in OnUpdate() (it runs 1000x per second!)

---

## Part 9: Best Practices

### Performance

1. **Minimize work in OnUpdate()**
   - It runs ~1000 times per second
   - Do expensive work only when needed

2. **Use efficient data structures**
   ```cpp
   // Cache frequently accessed objects
   physics::LinkPtr base_link_;  // Cache in Load()

   void OnUpdate() {
       // Reuse cached pointer
       base_link_->GetWorldPose();
   }
   ```

3. **Publish at appropriate rates**
   ```cpp
   // Don't publish every OnUpdate() call
   static unsigned int counter = 0;
   if (++counter % 100 == 0) {  // Publish every 100 steps
       publisher_->publish(msg);
   }
   ```

### Code Quality

```cpp
// Good plugin structure
class MyPlugin : public ModelPlugin
{
    private:
        // Gazebo components - listed first
        physics::ModelPtr model_;
        physics::LinkPtr link_;
        event::ConnectionPtr conn_;

        // ROS components
        std::shared_ptr<rclcpp::Node> ros_node_;
        rclcpp::Publisher<...>::SharedPtr pub_;
        rclcpp::Subscription<...>::SharedPtr sub_;

        // Control parameters
        double max_force_;
        double update_rate_;

        // State variables
        double last_update_time_;
};
```

### Documentation

```cpp
/**
 * MyRobotPlugin - Controls robot locomotion
 *
 * Parameters from SDF:
 *   - max_force: Maximum force to apply (default: 10.0)
 *   - update_rate: Hz to publish at (default: 50)
 *
 * Subscribed Topics:
 *   - /robot/cmd_vel (geometry_msgs::msg::Twist)
 *
 * Published Topics:
 *   - /robot/joint_states (sensor_msgs::msg::JointState)
 */
```

---

## Part 10: Key Takeaways

✅ **Plugin Types**: WorldPlugin, ModelPlugin, SensorPlugin for different scopes
✅ **Lifecycle**: Load → OnUpdate → Reset → Destructor
✅ **ROS Integration**: Plugins bridge Gazebo and ROS 2 perfectly
✅ **Performance**: OnUpdate runs frequently; keep it efficient
✅ **Build System**: CMake integration with ROS 2

---

## Self-Assessment Checkpoint

1. **What's the difference between WorldPlugin and ModelPlugin?**
   - Answer: WorldPlugin operates on entire simulation, ModelPlugin on single model

2. **How often does OnUpdate() get called?**
   - Answer: Once per physics step (~1000/second for 1ms step)

3. **How do you pass parameters to plugins from SDF?**
   - Answer: Use `<plugin>` tags with child elements read in Load()

4. **Why should you avoid blocking operations in OnUpdate()?**
   - Answer: It runs frequently and would slow down simulation significantly

5. **How do you register a plugin so Gazebo can find it?**
   - Answer: Use GZ_REGISTER_WORLD_PLUGIN() or GZ_REGISTER_MODEL_PLUGIN() macro

---

## Next Steps

- Continue to [Chapter 2.5: Interfacing Robots with Gazebo](./chapter-2-5.md)
- Build custom plugins for your specific robot
- Integrate ROS 2 control interfaces
- Profile plugin performance

---

**Chapter Status**: ✅ COMPLETE
**Last Updated**: 2025-12-17
**Estimated Reading Time**: 55 minutes
**Estimated Hands-On Time**: 2-3 hours

**Next Chapter**: [Chapter 2.5: Interfacing Robots with Gazebo](./chapter-2-5.md)
