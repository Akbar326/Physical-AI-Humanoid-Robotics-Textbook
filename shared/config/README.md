# Configuration Templates

This directory contains reusable configuration templates for the Physical AI & Humanoid Robotics textbook. Use these templates as starting points for your own configurations.

## Overview

| File | Purpose | Format |
|------|---------|--------|
| `robot-base.yaml` | Robot hardware and ROS 2 configuration | YAML |
| `gazebo-world.yaml` | Gazebo simulation world setup | YAML |
| `ros2_launch_template.py` | ROS 2 launch file template | Python |
| `requirements.txt` | Python package dependencies | Text |

---

## 1. Robot Configuration (`robot-base.yaml`)

Complete template for configuring robot hardware, sensors, and ROS 2 parameters.

### Usage

Copy and customize for your robot:

```bash
cp robot-base.yaml my_robot.yaml
# Edit my_robot.yaml with your robot specifications
```

### Key Sections

#### Physical Properties
```yaml
geometry:
  length_m: 0.18
  width_m: 0.16
  height_m: 0.12
  mass_kg: 1.64
```

#### Motion Capabilities
```yaml
motion:
  max_linear_velocity_ms: 0.26
  max_angular_velocity_rads: 2.84
```

#### Sensors
```yaml
sensors:
  lidar:
    enabled: true
    range_m: 3.5
    frequency_hz: 5
  camera:
    enabled: true
    resolution: "1280x720"
    frequency_hz: 30
```

#### ROS 2 Configuration
```yaml
ros2:
  namespace: "/robot"
  domain_id: 0
  topics:
    cmd_vel: "/cmd_vel"
    odom: "/odom"
```

### Example: Loading in Python

```python
from shared.utils import ConfigLoader

# Load robot configuration
robot_config = ConfigLoader.load_yaml("my_robot.yaml")

# Access values
max_speed = ConfigLoader.get_config_value(
    robot_config,
    "motion.max_linear_velocity_ms"
)
print(f"Max speed: {max_speed} m/s")
```

### Example: Using in ROS 2 Node

```python
import rclpy
from shared.utils import ConfigLoader, ROS2Helper

node = ROS2Helper.setup_node("robot_controller")
config = ConfigLoader.load_yaml("my_robot.yaml")

# Set parameters from config
ROS2Helper.set_parameter(
    node,
    "max_speed",
    config['motion']['max_linear_velocity_ms']
)
```

---

## 2. Gazebo World Configuration (`gazebo-world.yaml`)

Complete template for configuring Gazebo simulation worlds.

### Usage

Copy and customize:

```bash
cp gazebo-world.yaml my_world.yaml
# Edit my_world.yaml with your world setup
```

### Key Sections

#### Physics Engine
```yaml
physics:
  engine: "ode"
  real_time_factor: 1.0
  gravity:
    z: -9.81
```

#### Environment
```yaml
environment:
  ambient_light:
    r: 0.3
    g: 0.3
    b: 0.3
  directional_light:
    intensity: 0.8
```

#### Models to Load
```yaml
models:
  ground_plane:
    type: "model"
    uri: "model://ground_plane"
    static: true
```

#### Materials
```yaml
materials:
  concrete:
    friction_mu: 0.5
    density: 2400
```

### Example: Setting Up a World

1. **Start with the template:**
   ```bash
   cp gazebo-world.yaml laboratory.yaml
   ```

2. **Customize physics:**
   ```yaml
   physics:
     gravity:
       z: -9.81
     real_time_factor: 1.0
   ```

3. **Add your models:**
   ```yaml
   models:
     my_robot:
       type: "model"
       uri: "model://my_robot"
       pose:
         x: 0.0
         y: 0.0
         z: 0.0
   ```

4. **Use in Gazebo:**
   ```bash
   gazebo laboratory.yaml
   ```

---

## 3. ROS 2 Launch File (`ros2_launch_template.py`)

Template for Python-based ROS 2 launch files.

### Usage

Copy and customize:

```bash
cp ros2_launch_template.py my_launch.py
# Edit my_launch.py with your nodes and configuration
```

### Key Components

#### Launch Arguments
```python
namespace_arg = DeclareLaunchArgument(
    'namespace',
    default_value='robot',
    description='Namespace for robot nodes'
)
```

#### Creating Nodes
```python
robot_controller_node = Node(
    package='my_package',
    executable='controller',
    namespace=namespace,
    parameters=[config_file],
    remappings=[
        ('/cmd_vel', [namespace, '/cmd_vel']),
    ],
)
```

#### Conditional Execution
```python
condition=IfCondition(use_sim)  # Only run in simulation
```

### Example: Running a Launch File

```bash
# With default arguments
ros2 launch my_package my_launch.py

# With custom arguments
ros2 launch my_package my_launch.py \
    namespace:=my_robot \
    robot_model:=turtlebot3_waffle \
    use_sim:=false
```

### Example: Launch File for Module 1

```python
def generate_launch_description():
    # Nodes for publisher/subscriber example
    publisher_node = Node(
        package='module_1',
        executable='publisher',
        name='talker',
    )

    subscriber_node = Node(
        package='module_1',
        executable='subscriber',
        name='listener',
    )

    return LaunchDescription([
        publisher_node,
        subscriber_node,
    ])
```

### Example: Launch File for Module 2

```python
def generate_launch_description():
    # Gazebo world
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('gazebo_ros'),
            '/launch/gazebo.launch.py'
        ]),
        launch_arguments={'world': 'my_world.yaml'}
    )

    # Robot spawner
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'robot', '-file', 'robot.urdf'],
    )

    return LaunchDescription([
        gazebo,
        spawn_robot,
    ])
```

---

## 4. Python Dependencies (`requirements.txt`)

Python package requirements for all modules.

### Installation

```bash
# Install all dependencies
pip install -r requirements.txt

# Or install specific subset
pip install numpy matplotlib PyYAML  # Core packages
```

### Key Dependencies

- **Scientific Computing**: numpy, scipy, pandas
- **Visualization**: matplotlib, plotly, seaborn
- **Configuration**: PyYAML, jsonschema
- **Computer Vision**: opencv-python, scikit-image
- **Machine Learning**: torch, transformers (Module 4)
- **Development**: pytest, black, flake8

### GPU Support (Optional)

For GPU acceleration:

```bash
# PyTorch with CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# TensorFlow with GPU support
pip install tensorflow-gpu
```

### Virtual Environment Setup

```bash
# Create virtual environment
python3 -m venv robotics_env

# Activate
source robotics_env/bin/activate  # Linux/macOS
# or
robotics_env\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## Using Templates in Your Projects

### Step 1: Copy the Template

```bash
cd my_project
cp /path/to/shared/config/robot-base.yaml config/my_robot.yaml
```

### Step 2: Customize

Edit the copied file for your specific needs:

```yaml
robot:
  name: "my_custom_robot"
  type: "holonomic"
  # ... customize other fields
```

### Step 3: Load and Use

```python
from shared.utils import ConfigLoader

config = ConfigLoader.load_yaml("config/my_robot.yaml")
# Use config in your application
```

### Step 4: Validate

```python
from shared.utils import ConfigLoader

# Validate required fields
is_valid = ConfigLoader.validate_config(
    config,
    required_keys=['robot', 'ros2', 'sensors']
)
```

---

## Configuration Best Practices

1. **Use version control**: Track configuration changes in git
2. **Document changes**: Add comments explaining custom modifications
3. **Validate early**: Check configuration validity at startup
4. **Use defaults**: Provide sensible defaults in templates
5. **Separate concerns**: Keep hardware, ROS 2, and sim configs separate
6. **Parameter naming**: Use consistent naming conventions

### Example: Configuration with Comments

```yaml
robot:
  name: "my_robot"
  # Using custom motor model with higher torque
  motors:
    left_wheel:
      type: "brushless_dc"
      nominal_voltage_v: 24.0  # Upgraded from 12V
      max_current_a: 2.0
```

---

## Troubleshooting

### "File not found" error
- Verify path is correct (absolute or relative)
- Check file exists: `ls config/robot.yaml`

### YAML parsing error
- Verify YAML syntax (check indentation, no tabs)
- Use: `python -c "import yaml; yaml.safe_load(open('file.yaml'))"`

### ROS 2 parameter mismatch
- Validate parameter types match expected
- Check namespace configuration

### Gazebo model not found
- Verify model URI is correct
- Check model is in Gazebo model path: `echo $GAZEBO_MODEL_PATH`

---

## Advanced Topics

### Configuration Inheritance

```python
# Load base configuration
base_config = ConfigLoader.load_yaml("base.yaml")

# Load overrides
overrides = ConfigLoader.load_yaml("overrides.yaml")

# Merge
config = ConfigLoader.merge_configs(base_config, overrides)
```

### Environment Variable Substitution

```yaml
# In config file
robot:
  model_path: "${ROBOT_MODELS_PATH}/my_robot"

# In Python
import os
path = config['robot']['model_path'].replace(
    "${ROBOT_MODELS_PATH}",
    os.environ.get('ROBOT_MODELS_PATH', '/default/path')
)
```

### Dynamic Configuration

```python
# Generate configuration programmatically
config = {
    'robot': {
        'name': 'robot_' + str(i),
        'namespace': f'/robot_{i}',
    }
    for i in range(4)  # Create 4 robot configs
}
```

---

## See Also

- Module 1: ROS 2 configuration usage
- Module 2: Gazebo world setup
- `shared/utils/config_loader.py`: Configuration utilities
- Textbook chapters for specific use cases

---

**Last Updated**: 2025-12-16
**Status**: Ready for use
**Compatibility**: ROS 2 Humble, Gazebo Fortress, Python 3.10+
