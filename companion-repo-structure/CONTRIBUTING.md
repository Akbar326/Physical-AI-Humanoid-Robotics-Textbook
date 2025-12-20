# Contributing to Physical AI & Humanoid Robotics Code Repository

Thank you for your interest in contributing! This document provides guidelines for contributing code examples, exercises, and improvements to this repository.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## How to Contribute

### Reporting Issues

Found a bug? Please open a GitHub issue with:

1. **Clear Title**: Concise description of the problem
2. **Environment**: OS, Python version, ROS 2 version
3. **Steps to Reproduce**: How to trigger the issue
4. **Expected vs Actual**: What should happen vs what happens
5. **Error Message**: Full error trace if available
6. **Attempted Solutions**: What you've tried

**Example**:
```
Title: ImportError when running chapter-1-1 example

Environment:
- OS: Ubuntu 22.04
- Python: 3.10.11
- ROS 2: Humble
- Platform: Native (not WSL)

Steps:
1. cd module-1/chapter-1-1/examples
2. python3 my_first_node.py

Error:
ModuleNotFoundError: No module named 'rclpy'

Attempted:
- source /opt/ros/humble/setup.bash
- pip install rclpy
```

### Suggesting Enhancements

Have an idea? Open an issue with the `enhancement` label:

1. **Motivation**: Why this enhancement matters
2. **Proposed Solution**: Your suggested approach
3. **Alternatives Considered**: Other options
4. **Additional Context**: Links, images, etc.

### Adding New Code Examples

Want to add an example? Here's the process:

#### 1. Fork the Repository

```bash
git clone https://github.com/YOUR-USERNAME/ai-humanoid-robotics-code.git
cd ai-humanoid-robotics-code
git checkout -b feature/add-example-name
```

#### 2. Create Your Example

Follow this structure:

```
module-X/chapter-X-Y/examples/
├── my_example.py        # Your example code
├── README.md           # Explanation
└── data/              # If needed
    └── sample_data.txt
```

#### 3. Write Clear Code

**Style Guide**:
```python
#!/usr/bin/env python3
"""
Module docstring explaining what this example does.
Related textbook: Chapter X.Y: [Title]
"""

import logging
from typing import Optional

# Configure logging
logger = logging.getLogger(__name__)


class MyRobotController:
    """
    Clear class docstring with purpose and usage.

    Example:
        >>> controller = MyRobotController("robot1")
        >>> controller.move(1.0, 0.0)
    """

    def __init__(self, name: str) -> None:
        """
        Initialize controller.

        Args:
            name: Robot name
        """
        self.name = name
        logger.info(f"Controller created for {name}")

    def move(self, linear: float, angular: float) -> None:
        """
        Move robot.

        Args:
            linear: Linear velocity in m/s
            angular: Angular velocity in rad/s
        """
        logger.debug(f"Moving: linear={linear}, angular={angular}")
        # Implementation...


if __name__ == "__main__":
    # Example usage
    controller = MyRobotController("test_robot")
    controller.move(1.0, 0.5)
```

**Code Standards**:
- ✅ Comprehensive docstrings (functions, classes, modules)
- ✅ Type hints for function parameters and returns
- ✅ Comments for complex logic
- ✅ Error handling for edge cases
- ✅ Logging for debugging
- ✅ PEP 8 compliant

#### 4. Create README

```markdown
# Example Name

Brief description of what this example does.

## Prerequisites

- Module 1 complete
- ROS 2 Humble
- Python 3.10+

## Running the Example

```bash
python3 my_example.py
```

## Expected Output

```
[Output here]
```

## What It Demonstrates

- Concept 1
- Concept 2
- Concept 3

## Key Points

- Point 1: Explanation
- Point 2: Explanation

## Further Reading

- [Link to relevant chapter]
- [Link to external resource]
```

#### 5. Test Across Platforms

Test your code on:
- [ ] Ubuntu 22.04
- [ ] Windows 10/11 (WSL2)
- [ ] macOS 12+

Document any platform-specific behavior.

#### 6. Submit Pull Request

```bash
git add module-X/chapter-X-Y/examples/my_example.py
git add module-X/chapter-X-Y/examples/README.md
git commit -m "Add example: my_example for Chapter X.Y"
git push origin feature/add-example-name
```

Create PR with:
- **Title**: "Add example: [name]"
- **Description**: What the example demonstrates
- **Fixes/Relates**: Link to related issues
- **Testing**: Platforms tested on

### Adding New Exercises

Follow the same process as examples, but:

1. **Exercises are templates**: Start with incomplete code (`# TODO: implement...`)
2. **Include solution**: Create corresponding solution in `solutions/`
3. **Document thoroughly**: Exercise should be self-explanatory
4. **Test difficulty**: Ensure it takes ~30-60 minutes

**Exercise Template**:
```python
#!/usr/bin/env python3
"""
Exercise: [Title]
Chapter: X.Y - [Chapter Name]

TODO: Complete this exercise by:
1. Implementing the move_forward() function
2. Implementing the turn_left() function
3. Running the code successfully
"""

class SimpleRobot:
    def __init__(self, name):
        self.name = name
        self.x = 0.0
        self.y = 0.0
        self.angle = 0.0

    def move_forward(self, distance):
        """
        TODO: Implement forward movement

        Hint: Update self.x and self.y based on self.angle
        """
        pass

    def turn_left(self, angle_rad):
        """
        TODO: Implement left turn

        Hint: Update self.angle
        """
        pass


if __name__ == "__main__":
    robot = SimpleRobot("MyRobot")

    # TODO: Test your implementation
    robot.move_forward(1.0)
    print(f"Position: ({robot.x}, {robot.y})")
```

### Improving Documentation

Found a typo or unclear explanation? Help us improve!

1. Fork and branch
2. Make improvements
3. Submit PR with clear description of changes

### Setting Up Development Environment

```bash
# Clone and setup
git clone https://github.com/physical-ai-lab/ai-humanoid-robotics-code.git
cd ai-humanoid-robotics-code

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install development tools
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest tests/

# Check code style
black --check module-*/
flake8 module-*/
```

## Naming Conventions

### File Names
- Use lowercase with underscores: `my_example.py`
- Descriptive names: `robot_controller.py` not `rc.py`

### Module Names
- Directory structure: `module-1/chapter-1-1/examples/`
- Chapter files: `chapter-1-1.md`

### Variable Names
```python
# Good
linear_velocity = 1.0
robot_position = (0.0, 0.0)

# Avoid
lv = 1.0
rp = (0.0, 0.0)
```

### Function Names
```python
# Good
def move_forward(distance):
def get_robot_state():

# Avoid
def moveForward(distance):
def getRobotState():
```

## Commit Message Guidelines

Format: `type: description`

**Types**:
- `feat`: New feature/example
- `fix`: Bug fix
- `docs`: Documentation change
- `refactor`: Code improvement
- `test`: Add/modify tests
- `chore`: Build, setup, etc.

**Examples**:
```
feat: Add example for Chapter 1.3 - Publisher/Subscriber

fix: Correct parameter validation in robot_controller.py

docs: Update setup instructions for macOS

refactor: Simplify motion control logic

test: Add unit tests for ConfigLoader
```

## Pull Request Process

1. **Update your branch**: `git pull origin main`
2. **Create feature branch**: `git checkout -b feature/description`
3. **Make changes**: Commit regularly with clear messages
4. **Test thoroughly**: Run on multiple platforms if possible
5. **Push to fork**: `git push origin feature/description`
6. **Create PR**: Include description, link issues, document testing
7. **Respond to review**: Address feedback promptly
8. **Merge**: Maintainers will merge when approved

## Review Expectations

Pull requests will be reviewed for:

- ✅ Code quality and correctness
- ✅ Documentation completeness
- ✅ Testing on multiple platforms
- ✅ Adherence to style guidelines
- ✅ Alignment with textbook content
- ✅ No breaking changes

## Large Contributions

For significant additions (new chapter examples, major refactoring):

1. **Open an issue first**: Discuss the proposal
2. **Get feedback**: Wait for maintainer input
3. **Plan together**: Agree on approach
4. **Implement incrementally**: Smaller PRs are easier to review
5. **Stay coordinated**: Update team on progress

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

- Check [README.md](README.md) first
- Open a discussion on GitHub
- Review existing examples and solutions
- See the main textbook for detailed guidance

---

## Contributor Recognition

We recognize and thank all contributors! Contributors are listed in:
- [CONTRIBUTORS.md](CONTRIBUTORS.md) - Hall of fame
- GitHub contributor stats
- Releases notes for significant contributions

---

**Thank you for contributing to making robotics education better! 🤖**

Last Updated: 2025-12-16
