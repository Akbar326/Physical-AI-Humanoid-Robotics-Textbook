# Exercise 2.2: Create a Subscriber Node

## Objective
Create a ROS 2 subscriber node that listens to messages from a publisher node.

## Prerequisites
- ROS 2 Humble installed
- Basic Python knowledge
- Completed Exercise 2.1 (Publisher Node)
- Understanding of ROS 2 topics

## Steps

### Step 1: Create the Subscriber Script
1. In the same package directory as your publisher, create `my_subscriber.py`:
   ```bash
   touch my_subscriber.py
   ```

2. Add the subscriber code (similar to the example in the chapter)

### Step 2: Update Package Configuration
1. Ensure your `package.xml` includes any additional dependencies
2. Verify your `setup.py` includes the new subscriber script in entry points

### Step 3: Rebuild the Package
1. Navigate to your workspace root:
   ```bash
   cd ~/ros2_ws
   ```

2. Rebuild the package:
   ```bash
   colcon build --packages-select my_publisher_package
   ```

3. Source the workspace:
   ```bash
   source install/setup.bash
   ```

### Step 4: Test Publisher-Subscriber Communication
1. Open a new terminal and start your publisher:
   ```bash
   ros2 run my_publisher_package my_publisher
   ```

2. In another terminal, start your subscriber:
   ```bash
   ros2 run my_publisher_package my_subscriber
   ```

3. Verify that the subscriber receives messages from the publisher

### Step 5: Experiment with Parameters
1. Modify the message content in your publisher
2. Change the publishing frequency
3. Create multiple subscribers to the same topic

## Expected Output
When both nodes are running, the subscriber terminal should display:
```
[INFO] [1620000000.123456789] [my_subscriber]: I heard: "Hello World: 0"
[INFO] [1620000000.623456789] [my_subscriber]: I heard: "Hello World: 1"
```

## Verification
- Messages from publisher appear in subscriber terminal
- Both nodes show up in `ros2 node list`
- Topic shows up in `ros2 topic list` and has proper type

## Advanced Exercise (Optional)
Create a third node that acts as both a publisher and subscriber (relay node).