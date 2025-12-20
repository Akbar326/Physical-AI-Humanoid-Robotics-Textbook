# Shared Utilities Module

This directory contains reusable Python utilities for the Physical AI & Humanoid Robotics textbook. These utilities simplify common tasks across ROS 2, Gazebo, Isaac Sim, and data visualization.

## Utilities Overview

### 1. ROS 2 Helpers (`ros2_helpers.py`)

Common utilities for ROS 2 development.

**Key Classes & Methods**:
- `ROS2Helper.setup_node()` - Initialize ROS 2 nodes
- `ROS2Helper.list_topics()` - Discover available topics
- `ROS2Helper.list_services()` - Discover available services
- `ROS2Helper.get_parameter()` / `set_parameter()` - Manage parameters
- `ROS2Helper.create_publisher()` - Create publishers
- `ROS2Helper.create_subscriber()` - Create subscribers
- `ROS2Helper.wait_for_service()` - Wait for service availability

**Usage Example**:
```python
from shared.utils import ROS2Helper

# Create a node
node = ROS2Helper.setup_node("my_robot_controller")

# List topics
topics = ROS2Helper.list_topics()
print(f"Available topics: {topics}")

# Get/set parameters
speed = ROS2Helper.get_parameter(node, "max_speed", default=1.0)
ROS2Helper.set_parameter(node, "max_speed", 2.0)

# Create publisher
from geometry_msgs.msg import Twist
publisher = ROS2Helper.create_publisher(node, "/cmd_vel", Twist)

# Create subscriber
def callback(msg):
    print(f"Received: {msg}")

from std_msgs.msg import String
subscriber = ROS2Helper.create_subscriber(
    node, "/topic", String, callback)
```

---

### 2. Gazebo Helpers (`gazebo_utils.py`)

Utilities for Gazebo simulation control and queries.

**Key Classes & Methods**:
- `GazeboHelper.spawn_model()` - Spawn models in simulation
- `GazeboHelper.delete_model()` - Remove models
- `GazeboHelper.get_world_state()` - Query world state
- `GazeboHelper.get_world_models()` - List models in world
- `GazeboHelper.get_model_state()` - Get model pose/velocity
- `GazeboHelper.reset_simulation()` - Reset world to initial state
- `GazeboHelper.pause_simulation()` / `unpause_simulation()`
- `GazeboHelper.set_physics_properties()` - Configure physics engine
- `GazeboHelper.apply_force_to_model()` - Apply forces during simulation
- `GazeboHelper.get_contact_info()` - Get collision/contact info

**Usage Example**:
```python
from shared.utils import GazeboHelper

# Spawn a robot
success = GazeboHelper.spawn_model(
    "robot1",
    "/path/to/robot.sdf",
    position=(1.0, 2.0, 0.0),
    orientation=(0.0, 0.0, 0.785)
)

# Get world state
state = GazeboHelper.get_world_state()
print(f"Sim time: {state['sim_time']}")

# Get all models
models = GazeboHelper.get_world_models()
print(f"Models: {models}")

# Get specific model state
robot_state = GazeboHelper.get_model_state("robot1")
if robot_state:
    print(f"Position: {robot_state['pose']['position']}")

# Configure physics
GazeboHelper.set_physics_properties(
    gravity=(0.0, 0.0, -9.81),
    time_step=0.001,
    max_update_rate=1000.0
)

# Apply force
GazeboHelper.apply_force_to_model(
    "robot1",
    force=(10.0, 0.0, 0.0),
    duration=1.0
)
```

---

### 3. Visualization Utilities (`visualization.py`)

Tools for plotting and visualizing robotics data.

**Key Classes & Methods**:
- `Visualizer.plot_trajectory()` - Plot 2D paths
- `Visualizer.plot_joint_angles()` - Plot joint angle data
- `Visualizer.plot_performance_metrics()` - Plot system performance
- `Visualizer.visualize_point_cloud()` - 3D point cloud visualization
- `Visualizer.create_animation()` - Create animated videos
- `Visualizer.visualize_robot_state()` - Show robot configuration
- `Visualizer.compare_trajectories()` - Compare multiple paths
- `Visualizer.heatmap_2d()` - Create 2D heatmaps

**Usage Example**:
```python
from shared.utils import Visualizer

# Plot trajectory
positions = [(0, 0), (1, 1), (2, 0), (3, 1)]
Visualizer.plot_trajectory(
    positions,
    title="Robot Path",
    save_path="/tmp/trajectory.png"
)

# Plot joint angles
joint_data = [
    [0.0, 0.0, 0.0],
    [0.1, 0.2, -0.1],
    [0.3, 0.5, -0.3],
]
joint_names = ["shoulder", "elbow", "wrist"]
Visualizer.plot_joint_angles(
    joint_data,
    joint_names,
    title="Arm Movement"
)

# Plot performance
metrics = {
    "latency_ms": [1.0, 1.2, 1.1],
    "cpu_percent": [25, 30, 28],
}
Visualizer.plot_performance_metrics(metrics)

# Visualize 3D point cloud
points = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
Visualizer.visualize_point_cloud(points, colors)

# Compare trajectories
trajectories = {
    "planned": [(0, 0), (1, 1), (2, 0)],
    "executed": [(0, 0), (1.05, 0.95), (1.95, 0.05)],
}
Visualizer.compare_trajectories(trajectories)
```

---

### 4. Configuration Loader (`config_loader.py`)

Load and manage configuration files in various formats.

**Key Classes & Methods**:
- `ConfigLoader.load_yaml()` - Load YAML files
- `ConfigLoader.load_json()` - Load JSON files
- `ConfigLoader.load_config()` - Auto-detect and load config
- `ConfigLoader.validate_config()` - Validate against schema
- `ConfigLoader.merge_configs()` - Merge configurations
- `ConfigLoader.save_config()` - Save configuration to file
- `ConfigLoader.get_config_value()` - Get nested values

**Usage Example**:
```python
from shared.utils import ConfigLoader

# Load YAML configuration
robot_config = ConfigLoader.load_yaml("robot_config.yaml")

# Load JSON configuration
settings = ConfigLoader.load_json("settings.json")

# Auto-detect and load
config = ConfigLoader.load_config("config.yaml")

# Validate configuration
is_valid = ConfigLoader.validate_config(
    config,
    required_keys=["robot", "speed"],
    type_schema={"robot": str, "speed": float}
)

# Merge configurations
base = {"speed": 0.5, "debug": False}
override = {"speed": 1.0}
merged = ConfigLoader.merge_configs(base, override)
# Result: {"speed": 1.0, "debug": False}

# Get nested value using dot notation
speed = ConfigLoader.get_config_value(
    config,
    "robot.motor.max_speed",
    default=1.0
)

# Save configuration
ConfigLoader.save_config(config, "output.yaml", format="yaml")
```

---

## Installation & Setup

### Prerequisites

```bash
# Core requirements
python3 -m pip install PyYAML

# For visualization
python3 -m pip install matplotlib numpy

# ROS 2 (if using ROS2Helper)
source /opt/ros/humble/setup.bash
```

### Adding to Your Project

```python
# Add to Python path
import sys
sys.path.insert(0, '/path/to/shared')

# Import utilities
from utils import ROS2Helper, GazeboHelper, Visualizer, ConfigLoader
```

---

## Usage in Chapters

### Example: Module 1 - ROS 2 Pub/Sub

```python
from shared.utils import ROS2Helper
from std_msgs.msg import String

# Create node
node = ROS2Helper.setup_node("talker")

# Create publisher
publisher = ROS2Helper.create_publisher(node, "/chatter", String)

# Publish messages
msg = String()
msg.data = "Hello, World!"
publisher.publish(msg)
```

### Example: Module 2 - Gazebo Simulation

```python
from shared.utils import GazeboHelper

# Spawn robot
GazeboHelper.spawn_model(
    "turtlebot",
    "/models/turtlebot3_burger/model.sdf",
    position=(0.0, 0.0, 0.0)
)

# Check world
models = GazeboHelper.get_world_models()
print(f"Models: {models}")

# Get robot state
state = GazeboHelper.get_model_state("turtlebot")
print(f"Robot position: {state['pose']['position']}")
```

### Example: Module 3 - Visualization

```python
from shared.utils import Visualizer

# Load trajectory data
trajectory = load_trajectory_from_file("trajectory.csv")

# Plot it
Visualizer.plot_trajectory(
    trajectory,
    title="Robot Trajectory",
    save_path="/tmp/viz.png"
)
```

### Example: Module 4 - Configuration

```python
from shared.utils import ConfigLoader

# Load robot config
config = ConfigLoader.load_config("vla_robot.yaml")

# Get parameters
max_speed = ConfigLoader.get_config_value(
    config,
    "locomotion.max_speed",
    default=1.0
)

# Validate before use
if ConfigLoader.validate_config(
    config,
    required_keys=["model_name", "checkpoint_path"]
):
    print("Config is valid, proceeding...")
```

---

## Testing Utilities

Run tests for utilities:

```bash
# Test all utilities
python3 -m pytest shared/utils/ -v

# Test specific module
python3 -m pytest shared/utils/test_ros2_helpers.py -v
```

---

## Contributing

When adding new utilities:

1. Add comprehensive docstrings
2. Include usage examples
3. Add error handling and logging
4. Update this README
5. Add unit tests
6. Ensure backward compatibility

---

## Troubleshooting

### "ImportError: rclpy not installed"
**Solution**: Install ROS 2:
```bash
source /opt/ros/humble/setup.bash
```

### "ModuleNotFoundError: No module named 'yaml'"
**Solution**: Install PyYAML:
```bash
pip install PyYAML
```

### Gazebo services not available
**Solution**: Ensure Gazebo is running:
```bash
gazebo &
```

### Visualization not displaying
**Solution**: Ensure matplotlib backend is set:
```bash
export MPLBACKEND=TkAgg
```

---

## License

Part of the Physical AI & Humanoid Robotics textbook (MIT License)

## Questions?

See the relevant chapter in the textbook or open an issue on GitHub.

---

**Last Updated**: 2025-12-16
**Status**: Ready for use in all modules
