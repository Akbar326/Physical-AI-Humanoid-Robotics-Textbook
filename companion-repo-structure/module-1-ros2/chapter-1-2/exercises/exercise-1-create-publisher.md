# Exercise 2.1: Create a Publisher Node

## Objective
Create a ROS 2 publisher node that publishes custom messages to a topic.

## Prerequisites
- ROS 2 Humble installed
- Basic Python knowledge
- Completed Chapter 1.1

## Steps

### Step 1: Create Package Structure
1. Create a new ROS 2 package directory:
   ```bash
   mkdir -p ~/ros2_ws/src/my_publisher_package
   cd ~/ros2_ws/src/my_publisher_package
   ```

### Step 2: Create the Publisher Script
1. Create a Python file called `my_publisher.py`:
   ```bash
   touch my_publisher.py
   ```

2. Add the publisher code (similar to the example in the chapter)

### Step 3: Make the Script Executable
1. Make the script executable:
   ```bash
   chmod +x my_publisher.py
   ```

### Step 4: Create Package Configuration
1. Create a `package.xml` file with proper metadata
2. Create a `setup.py` file for Python package configuration

### Step 5: Build and Run
1. Navigate to your workspace root:
   ```bash
   cd ~/ros2_ws
   ```

2. Build the package:
   ```bash
   colcon build --packages-select my_publisher_package
   ```

3. Source the workspace:
   ```bash
   source install/setup.bash
   ```

4. Run your publisher:
   ```bash
   ros2 run my_publisher_package my_publisher
   ```

## Expected Output
Your publisher should output messages to the terminal at regular intervals, similar to:
```
[INFO] [1620000000.123456789] [my_publisher]: Publishing: "Hello World: 0"
[INFO] [1620000000.623456789] [my_publisher]: Publishing: "Hello World: 1"
```

## Verification
Use `ros2 topic list` and `ros2 topic echo` to verify your topic is being published.

## Troubleshooting
- Ensure your Python script has the correct shebang line
- Check that your package.xml has proper dependencies listed
- Verify your setup.py has correct entry points defined