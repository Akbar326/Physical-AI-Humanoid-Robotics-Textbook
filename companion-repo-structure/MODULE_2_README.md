# Module 2: Gazebo Simulation - Code Examples & Exercises

**Time**: 21-26 hours | **Chapters**: 6 | **Difficulty**: Intermediate to Advanced

This directory contains all code examples, exercises, and solutions for **Module 2: Gazebo Simulation** of the Physical AI & Humanoid Robotics textbook.

---

## Quick Links

| Chapter | Topic | Time | Files |
|---------|-------|------|-------|
| [2.1](chapter-2-1/) | Introduction to Simulation | 3-4h | Examples, Exercises |
| [2.2](chapter-2-2/) | Gazebo Basics and World Setup | 3-4h | Worlds, Examples |
| [2.3](chapter-2-3/) | Physics Simulation and Materials | 3-4h | Physics configs |
| [2.4](chapter-2-4/) | Plugins and Custom Simulation | 3-4h | Plugin examples |
| [2.5](chapter-2-5/) | Interfacing Robots with Gazebo | 3-4h | Robot control |
| [2.6](chapter-2-6/) | Advanced Simulation Techniques | 3-4h | Optimization |

---

## Learning Objectives

After completing this module, you will be able to:

- ✅ Understand simulation principles and physics engines
- ✅ Create and configure Gazebo worlds
- ✅ Model robot physics with realistic properties
- ✅ Develop custom Gazebo plugins
- ✅ Integrate ROS 2 nodes with Gazebo
- ✅ Optimize simulations for performance

---

## Prerequisites

- Complete **Module 1: ROS 2 Fundamentals**
- Gazebo Fortress installed
- ROS 2 Humble configured
- Basic understanding of physics concepts

---

## Getting Started

### 1. Setup Gazebo

```bash
# Ensure Gazebo is installed
gazebo --version

# Start Gazebo server
gzserver &

# Launch example world
gazebo worlds/empty.world
```

### 2. Run First Example

```bash
cd module-2/chapter-2-1/examples
python3 spawn_robot.py
```

### 3. Follow Chapters Sequentially

Each chapter builds physics and control concepts:

1. **Ch 2.1**: Basic simulation concepts
2. **Ch 2.2**: World creation and objects
3. **Ch 2.3**: Physics configuration
4. **Ch 2.4**: Custom behaviors
5. **Ch 2.5**: Robot control from ROS 2
6. **Ch 2.6**: Performance optimization

---

## Chapter Breakdown

### Chapter 2.1: Introduction to Simulation

**Topics**: Why simulation matters, Gazebo architecture

**Files**:
- `examples/first_world.world` - Basic Gazebo world
- `examples/spawn_robot.py` - Spawn robot in world
- `config/` - Gazebo configuration

**Quick Start**:
```bash
cd chapter-2-1/examples
gazebo first_world.world &
python3 spawn_robot.py
```

### Chapter 2.2: Gazebo Basics and World Setup

**Topics**: World files (SDF), models, rendering

**Files**:
- `worlds/lab_environment.world` - Laboratory world
- `models/` - Robot and object models
- `examples/load_world.py` - World management

**Quick Start**:
```bash
gazebo worlds/lab_environment.world
```

### Chapter 2.3: Physics Simulation and Materials

**Topics**: Physics engines, materials, friction, mass

**Files**:
- `config/physics_*.yaml` - Physics configurations
- `examples/physics_demo.py` - Physics demonstration
- `materials/` - Material definitions

**Quick Start**:
```bash
cd chapter-2-3/examples
python3 physics_demo.py
```

### Chapter 2.4: Plugins and Custom Simulation

**Topics**: Gazebo plugins, C++ programming, custom behaviors

**Files**:
- `plugins/` - Custom plugin source code
- `examples/plugin_demo.py` - Using plugins
- `CMakeLists.txt` - Build configuration

**Quick Start**:
```bash
cd chapter-2-4/
mkdir build && cd build
cmake ..
make
```

### Chapter 2.5: Interfacing Robots with Gazebo

**Topics**: ROS 2 integration, robot control, sensor simulation

**Files**:
- `examples/gazebo_ros_control.py` - Robot control
- `launch/gazebo_robot.launch.py` - Launch file
- `config/robot.urdf` - Robot definition

**Quick Start** (3 terminals):
```bash
# Terminal 1: Gazebo
gazebo &

# Terminal 2: Robot
cd chapter-2-5/examples
python3 gazebo_ros_control.py

# Terminal 3: Control
ros2 publish /cmd_vel geometry_msgs/Twist "linear: {x: 0.5}"
```

### Chapter 2.6: Advanced Simulation Techniques

**Topics**: Optimization, large-scale simulation, performance tuning

**Files**:
- `examples/optimization.py` - Performance tips
- `config/` - Optimization configurations
- `benchmarks/` - Performance benchmarks

**Quick Start**:
```bash
cd chapter-2-6/examples
python3 optimization.py
```

---

## Project: Simulated Robot Navigation

Build a complete navigation simulation:

**Scope**:
- Multi-room laboratory world
- Mobile robot with sensors
- Obstacle detection and avoidance
- ROS 2 navigation stack integration

**Files**: `projects/robot_navigation/`
**Time**: 4-5 hours
**Skills**: All Module 2 concepts

---

## World Files

### Available Worlds

```
worlds/
├── empty.world              # Minimal world
├── lab_environment.world    # Laboratory setup
├── warehouse.world          # Warehouse scenario
└── outdoor.world           # Outdoor environment
```

### Creating Custom Worlds

```bash
# Copy template
cp worlds/empty.world worlds/my_world.world

# Edit in Gazebo
gazebo -e worlds/my_world.world

# Or edit as SDF text file
gedit worlds/my_world.world
```

---

## Models

### Built-in Models

```bash
# List available models
ls /usr/share/gazebo/models/

# Use in worlds
<include>
  <uri>model://box</uri>
  <pose>0 0 0.5 0 0 0</pose>
</include>
```

### Custom Models

Create in `models/`:

```
models/my_robot/
├── model.sdf
├── model.config
└── meshes/
    └── robot.dae
```

---

## Common Tasks

### Launch with ROS 2

```bash
cd chapter-2-5
ros2 launch launch/gazebo_robot.launch.py
```

### Get Robot State

```bash
# From Python
from shared.utils import GazeboHelper
state = GazeboHelper.get_model_state("robot")

# From Command Line
ros2 service call /gazebo/get_model_state gazebo_msgs/srv/GetModelState
```

### Apply Forces

```python
from shared.utils import GazeboHelper

GazeboHelper.apply_force_to_model(
    "robot",
    force=(10.0, 0.0, 0.0),
    duration=1.0
)
```

### Monitor Performance

```bash
# Check simulation statistics
rostopic echo /gazebo/performance_metrics

# Monitor physics step time
python3 -c "import gazebo; print(gazebo.get_stats())"
```

---

## Troubleshooting

### "Gazebo not found"
```bash
# Install Gazebo
sudo apt-get install gazebo-classic
# or for Gazebo Garden/Harmonic
sudo apt-get install gz-garden
```

### "libgazebo_ros plugins not found"
```bash
source /opt/ros/humble/setup.bash
```

### Slow simulation
- Reduce real-time factor: `<real_time_update_rate>10</real_time_update_rate>`
- Simplify models
- Reduce sensor frequencies
- See Chapter 2.6 for optimization

### Model not spawning
- Check model path is correct
- Verify .sdf syntax is valid
- Use `gzsdf` to validate:
  ```bash
  gzsdf test model.sdf
  ```

---

## Resources

### From This Repository
- [Examples](chapter-2-1/examples/) - Working code
- [World Files](chapter-2-2/worlds/) - SDF worlds
- [Models](models/) - Robot definitions

### Official Documentation
- [Gazebo Documentation](https://gazebosim.org/)
- [SDF Format](http://sdformat.org/)
- [ROS 2 Gazebo](https://docs.ros.org/en/humble/Tutorials/Advanced/Gazebo/Gazebo.html)

---

## Performance Tips

1. **Use simplified geometries** instead of meshes when possible
2. **Reduce contact point** detection (`max_contacts`)
3. **Adjust physics update rate** based on needs
4. **Disable unused sensors** when not needed
5. **Use real-time factor** < 1.0 for headless operation

---

## Next Steps

After completing Module 2:

1. ✅ Review all simulations
2. ✅ Complete navigation project
3. ✅ Optimize your world
4. → Proceed to [Module 3: Isaac Sim & AI](../module-3/)

---

**Happy simulating! 🎮**

**Last Updated**: 2025-12-16
