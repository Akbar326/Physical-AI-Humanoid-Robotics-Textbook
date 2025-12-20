# Glossary: Physical AI & Humanoid Robotics Textbook

**Date**: 2025-12-19
**Feature**: specs/001-textbook-chapter-specs/
**Status**: Complete

## Overview

This glossary defines key terms used throughout the Physical AI & Humanoid Robotics textbook. Terms are organized by category and include cross-references to relevant chapters.

## Robotics Terms

### A

**Action**
A ROS 2 communication pattern for long-running tasks that provides feedback during execution. Actions extend services with feedback, status, and cancelation capabilities.
*See also: [Chapter 1.4: Actions](/docs/module-1/chapter-1-4)*

**Action Client**
A ROS 2 node that sends goals to an action server and receives feedback during execution.
*See also: [Chapter 1.4: Actions](/docs/module-1/chapter-1-4)*

**Action Server**
A ROS 2 node that accepts goals from action clients, executes long-running tasks, and provides feedback.
*See also: [Chapter 1.4: Actions](/docs/module-1/chapter-1-4)*

### D

**Digital Twin**
A virtual representation of a physical system that mirrors the state and behavior of the real system in real-time. In robotics, digital twins enable simulation-based testing and validation.
*See also: [Module 2: The Digital Twin](/docs/module-2/)*

### G

**Gazebo**
A physics-based simulation engine for robotics that provides realistic sensor simulation and dynamics. Used for testing robot algorithms in virtual environments before deployment on real hardware.
*See also: [Module 2: Gazebo Simulation](/docs/module-2/)*

### M

**Module**
A major division of the textbook covering related topics: Module 1 (ROS 2), Module 2 (Simulation), Module 3 (AI/Isaac), Module 4 (VLA). Each module builds upon the previous ones.
*See also: [Textbook Overview](/docs/)*

### N

**Node**
The fundamental unit of computation in ROS 2. A node is a process that performs computation and communicates with other nodes through topics, services, or actions.
*See also: [Chapter 1.2: Creating Your First ROS 2 Node](/docs/module-1/chapter-1-2)*

### P

**Parameter**
A configuration value in ROS 2 that can be set at runtime. Parameters allow nodes to be configured without recompilation and can be loaded from YAML files.
*See also: [Chapter 1.5: Parameters](/docs/module-1/chapter-1-5)*

**Publisher**
A ROS 2 node that sends messages to a topic. Publishers create a data stream that subscribers can receive.
*See also: [Chapter 1.2: Creating Your First ROS 2 Node](/docs/module-1/chapter-1-2)*

### R

**Robot Operating System (ROS)**
A flexible framework for writing robot software that provides services like hardware abstraction, device drivers, libraries, visualizers, message-passing, and package management.
*See also: [Chapter 1.1: Welcome to ROS 2](/docs/module-1/chapter-1-1)*

**ROS 2**
The second generation of the Robot Operating System, designed for production environments with improved security, real-time capabilities, and distributed computing.
*See also: [Chapter 1.1: Welcome to ROS 2](/docs/module-1/chapter-1-1)*

### S

**Service**
A ROS 2 communication pattern for request-response interactions. Services allow nodes to request specific operations and receive responses.
*See also: [Chapter 1.3: Services](/docs/module-1/chapter-1-3)*

**Service Client**
A ROS 2 node that sends requests to a service server and waits for a response.
*See also: [Chapter 1.3: Services](/docs/module-1/chapter-1-3)*

**Service Server**
A ROS 2 node that receives requests from service clients, processes them, and sends responses.
*See also: [Chapter 1.3: Services](/docs/module-1/chapter-1-3)*

**Subscriber**
A ROS 2 node that receives messages from a topic. Subscribers process data streams published by publishers.
*See also: [Chapter 1.2: Creating Your First ROS 2 Node](/docs/module-1/chapter-1-2)*

### T

**Topic**
A ROS 2 communication channel for streaming messages between nodes. Publishers send messages to topics, and subscribers receive messages from topics.
*See also: [Chapter 1.2: Creating Your First ROS 2 Node](/docs/module-1/chapter-1-2)*

### U

**URDF (Unified Robot Description Format)**
An XML format for representing robot models, including kinematic and dynamic properties, visual meshes, and collision geometries. Used extensively in ROS for robot modeling.
*See also: [Chapter 2.2: Building Your First Robot Model](/docs/module-2/chapter-2-2)*

## AI/ML Concepts

### A

**Action (in Reinforcement Learning)**
The output of an agent that affects the environment and leads to a new state and reward. In robotics, actions often correspond to motor commands.
*See also: [Chapter 3.2: Reinforcement Learning Basics](/docs/module-3/chapter-3-2)*

**Agent**
In reinforcement learning, the entity that learns to make decisions by interacting with an environment to maximize cumulative rewards. In robotics, this could be a control system.
*See also: [Chapter 3.2: Reinforcement Learning Basics](/docs/module-3/chapter-3-2)*

### D

**Deep Learning**
A subset of machine learning using neural networks with multiple layers to learn hierarchical representations of data. Used in robotics for perception and control.
*See also: [Chapter 3.1: Introduction to NVIDIA Isaac Sim](/docs/module-3/chapter-3-1)*

### I

**Inference**
The process of using a trained machine learning model to make predictions on new data. In robotics, inference is often performed in real-time on sensor data.
*See also: [Chapter 3.5: Deploying AI Models to ROS 2](/docs/module-3/chapter-3-5)*

**Isaac Sim**
NVIDIA's robotics simulator for developing and testing AI-based robotics applications. Provides high-fidelity physics simulation and integration with NVIDIA's AI tools.
*See also: [Module 3: Isaac Sim & AI Integration](/docs/module-3/)*

### M

**Model**
In AI/ML, a mathematical representation learned from data that can make predictions or decisions. In robotics, models can represent robot dynamics, sensor characteristics, or environment properties.
*See also: [Chapter 3.5: Deploying AI Models to ROS 2](/docs/module-3/chapter-3-5)*

### P

**Policy**
In reinforcement learning, a strategy that defines the behavior of an agent by mapping states to actions. Policies can be deterministic or stochastic.
*See also: [Chapter 3.2: Reinforcement Learning Basics](/docs/module-3/chapter-3-2)*

### R

**Reinforcement Learning (RL)**
A machine learning paradigm where an agent learns to make decisions by receiving rewards or penalties based on its actions. Used in robotics for autonomous behavior learning.
*See also: [Chapter 3.2: Reinforcement Learning Basics](/docs/module-3/chapter-3-2)*

**Reward**
In reinforcement learning, the feedback signal that indicates the desirability of an action. The agent learns to maximize cumulative rewards over time.
*See also: [Chapter 3.2: Reinforcement Learning Basics](/docs/module-3/chapter-3-2)*

### T

**Training**
The process of adjusting model parameters using data to improve performance. In robotics, models may be trained in simulation before deployment.
*See also: [Chapter 3.2: Reinforcement Learning Basics](/docs/module-3/chapter-3-2)*

## Simulation Terms

### D

**Digital Twin**
A virtual representation of a physical system that mirrors the state and behavior of the real system in real-time. In robotics, digital twins enable simulation-based testing and validation.
*See also: [Module 2: The Digital Twin](/docs/module-2/)*

### G

**Gazebo**
A physics-based simulation engine for robotics that provides realistic sensor simulation and dynamics. Used for testing robot algorithms in virtual environments before deployment on real hardware.
*See also: [Module 2: Gazebo Simulation](/docs/module-2/)*

### P

**Physics Engine**
Software that simulates the physical properties and interactions of objects, including gravity, friction, collisions, and dynamics. Essential for realistic robotics simulation.
*See also: [Chapter 2.1: Introduction to Robot Simulation](/docs/module-2/chapter-2-1)*

### S

**SDF (Simulation Description Format)**
An XML format for describing robots, objects, and environments for simulation. Alternative to URDF, often used in Gazebo simulation environments.
*See also: [Chapter 2.2: Building Your First Robot Model](/docs/module-2/chapter-2-2)*

**Simulation**
The process of creating a virtual representation of a real system to study its behavior under various conditions. In robotics, simulation allows testing without physical hardware.
*See also: [Chapter 2.1: Introduction to Robot Simulation](/docs/module-2/chapter-2-1)*

## VLA (Vision-Language-Action) Terms

### A

**Action (in VLA)**
The physical or motor response generated by a VLA system based on visual and linguistic input. Represents the "A" in Vision-Language-Action.
*See also: [Chapter 4.4: From Language to Actions](/docs/module-4/chapter-4-4)*

### L

**Language Understanding**
The ability of a VLA system to process and comprehend natural language commands or descriptions. Represents the "L" in Vision-Language-Action.
*See also: [Chapter 4.3: Language Understanding](/docs/module-4/chapter-4-3)*

### V

**Vision**
The ability of a VLA system to process and understand visual information from cameras or sensors. Represents the "V" in Vision-Language-Action.
*See also: [Chapter 4.2: Vision for Robotics](/docs/module-4/chapter-4-2)*

**Vision-Language-Action (VLA)**
A unified system that integrates visual perception, language understanding, and physical action to create robots capable of responding to natural language commands with appropriate physical behaviors.
*See also: [Module 4: Vision-Language-Action Models](/docs/module-4/)*

## Cross-References

### By Chapter
- **Module 1 Glossary Terms**: [Chapter 1.1](/docs/module-1/chapter-1-1), [Chapter 1.2](/docs/module-1/chapter-1-2), [Chapter 1.3](/docs/module-1/chapter-1-3), [Chapter 1.4](/docs/module-1/chapter-1-4), [Chapter 1.5](/docs/module-1/chapter-1-5), [Chapter 1.6](/docs/module-1/chapter-1-6)
- **Module 2 Glossary Terms**: [Chapter 2.1](/docs/module-2/chapter-2-1), [Chapter 2.2](/docs/module-2/chapter-2-2), [Chapter 2.3](/docs/module-2/chapter-2-3), [Chapter 2.4](/docs/module-2/chapter-2-4), [Chapter 2.5](/docs/module-2/chapter-2-5), [Chapter 2.6](/docs/module-2/chapter-2-6)
- **Module 3 Glossary Terms**: [Chapter 3.1](/docs/module-3/chapter-3-1), [Chapter 3.2](/docs/module-3/chapter-3-2), [Chapter 3.3](/docs/module-3/chapter-3-3), [Chapter 3.4](/docs/module-3/chapter-3-4), [Chapter 3.5](/docs/module-3/chapter-3-5)
- **Module 4 Glossary Terms**: [Chapter 4.1](/docs/module-4/chapter-4-1), [Chapter 4.2](/docs/module-4/chapter-4-2), [Chapter 4.3](/docs/module-4/chapter-4-3), [Chapter 4.4](/docs/module-4/chapter-4-4), [Chapter 4.5](/docs/module-4/chapter-4-5), [Chapter 4.6](/docs/module-4/chapter-4-6)

### By Topic
- **ROS 2 Fundamentals**: [Module 1](/docs/module-1/)
- **Simulation**: [Module 2](/docs/module-2/)
- **AI/Isaac**: [Module 3](/docs/module-3/)
- **VLA Systems**: [Module 4](/docs/module-4/)