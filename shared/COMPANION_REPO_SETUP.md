# Companion Repository Setup Guide

## Overview

The Physical AI & Humanoid Robotics textbook project uses a companion repository to store code examples, datasets, and additional learning resources. This guide explains how to create and configure the companion repository.

## Repository Structure

```
ai-humanoid-robotics-code/  (Companion Repository)
├── README.md
├── LICENSE
├── .gitignore
├── CONTRIBUTING.md
├── docs/
│   └── SETUP.md            # Links to main textbook setup
├── module-1/
│   ├── chapter-1.1/
│   │   ├── examples/
│   │   ├── exercises/
│   │   ├── solutions/
│   │   └── README.md
│   ├── chapter-1.2/
│   └── ...
├── module-2/
│   ├── chapter-2.1/
│   └── ...
├── module-3/
│   ├── chapter-3.1/
│   └── ...
├── module-4/
│   ├── chapter-4.1/
│   └── ...
├── datasets/
│   ├── README.md
│   └── [Large files with git-lfs]
├── shared/
│   ├── utils/
│   │   ├── ros2_helpers.py
│   │   ├── gazebo_utils.py
│   │   └── visualization.py
│   └── config/
│       ├── gazebo_models.yaml
│       └── robot_configs.yaml
└── tools/
    ├── scripts/
    ├── docker/
    └── ci_tools/
```

## Step 1: Create the Repository

### Option A: Using GitHub Web Interface

1. Go to https://github.com/new
2. Repository name: `ai-humanoid-robotics-code`
3. Description: "Code examples, exercises, and datasets for the Physical AI & Humanoid Robotics textbook"
4. Visibility: **Public** (recommended for educational content)
5. Initialize with:
   - ✅ Add a README file
   - ✅ Add .gitignore (select "Python")
   - ✅ Add a license (select "MIT License")
6. Create repository

### Option B: Using GitHub CLI

```bash
# Login to GitHub
gh auth login

# Create repository
gh repo create ai-humanoid-robotics-code \
  --public \
  --description "Code examples, exercises, and datasets for Physical AI & Humanoid Robotics textbook" \
  --add-readme \
  --license MIT
```

### Option C: Manual Git Setup

```bash
# Create local directory
mkdir ai-humanoid-robotics-code
cd ai-humanoid-robotics-code

# Initialize git
git init
git branch -M main

# Create initial files
echo "# AI & Humanoid Robotics - Code Examples" > README.md
git add README.md
git commit -m "Initial commit: Add README"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/ai-humanoid-robotics-code.git
git push -u origin main
```

## Step 2: Configure Repository Structure

### Clone the repository (if not already done)

```bash
git clone https://github.com/YOUR_USERNAME/ai-humanoid-robotics-code.git
cd ai-humanoid-robotics-code
```

### Create directory structure

```bash
# Module directories
mkdir -p module-{1..4}/{chapter-{1..6},examples,exercises,solutions}

# Shared utilities
mkdir -p shared/{utils,config}

# Datasets
mkdir -p datasets

# Tools
mkdir -p tools/{scripts,docker,ci_tools}
```

### Create module README files

For each module, create `module-1/README.md`:

```markdown
# Module 1: ROS 2 Fundamentals

This module contains code examples and exercises for Module 1 of the Physical AI & Humanoid Robotics textbook.

## Chapters

- **Chapter 1.1**: ROS 2 Overview and Installation
- **Chapter 1.2**: Creating and Working with ROS 2 Packages
- **Chapter 1.3**: Publishers and Subscribers
- **Chapter 1.4**: Services and Actions
- **Chapter 1.5**: Parameters and Launch Files
- **Chapter 1.6**: Debugging and Profiling

## Getting Started

1. Complete the setup from the main textbook: `docs/preface/setup-guide.md`
2. Navigate to the specific chapter: `cd chapter-1.1/`
3. Follow the exercise instructions in each chapter's README

## File Organization

- `examples/` - Complete, working code examples from the textbook
- `exercises/` - Starting code templates for hands-on exercises
- `solutions/` - Reference solutions for all exercises

## Dependencies

See the main textbook for complete setup instructions. This module requires:
- ROS 2 Humble
- Python 3.10+
- Ubuntu 22.04 (or macOS/Windows with WSL2)

## Resources

- [ROS 2 Humble Documentation](https://docs.ros.org/en/humble/)
- [Main Textbook](https://github.com/physical-ai-lab/ai-humanoid-robotics)
```

## Step 3: Add Essential Files

### .gitignore

```bash
# Already created by GitHub, but verify it includes:
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
.venv

# ROS
build/
devel/
install/
.catkin_workspace

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Large files (use git-lfs for these)
*.zip
*.tar.gz
*.7z
*.rar
*.bag

# Data files
datasets/*.zip
datasets/*.tar.gz
```

### CONTRIBUTING.md

```markdown
# Contributing to Physical AI & Humanoid Robotics Code

Thank you for your interest in contributing!

## How to Contribute

### Reporting Issues

- Check existing issues first
- Provide: OS, Python version, ROS 2 distro, complete error message
- Include: steps to reproduce, expected vs actual behavior

### Submitting Code

1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature`
3. Make changes
4. Add tests if applicable
5. Commit with clear messages: `git commit -m "Add feature: description"`
6. Push to your fork
7. Create a Pull Request

### Code Style

- Follow PEP 8 for Python
- Use meaningful variable names
- Add comments for complex logic
- Include docstrings for functions/classes

### Testing

```bash
# Run tests before submitting
python -m pytest tests/
```

## Guidelines

- Code examples must run on Ubuntu 22.04, Windows 10/11 (WSL2), and macOS 12+
- All exercises should have solutions
- Update READMEs when adding new chapters
- Link PRs to related issues

## Questions?

Open an issue or check the main textbook repository.
```

### README.md (update if needed)

```markdown
# Physical AI & Humanoid Robotics - Code Examples & Exercises

Complete code examples, hands-on exercises, and datasets for the Physical AI & Humanoid Robotics textbook.

## Quick Start

### Prerequisites

- Ubuntu 22.04, macOS 12+, or Windows 10/11 (WSL2)
- Python 3.10+
- ROS 2 Humble

### Installation

1. Complete the main textbook setup:
   ```bash
   cd ~/ai-humanoid-robotics
   bash shared/install-scripts/ubuntu-setup.sh  # or equivalent for your OS
   ```

2. Clone this repository:
   ```bash
   git clone https://github.com/physical-ai-lab/ai-humanoid-robotics-code
   cd ai-humanoid-robotics-code
   ```

3. Set up Python environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```

## Repository Structure

- **module-1/**: ROS 2 Fundamentals (6 chapters)
- **module-2/**: Gazebo Simulation (6 chapters)
- **module-3/**: Isaac Sim & AI (5 chapters)
- **module-4/**: Vision-Language-Action Models (6 chapters)
- **shared/**: Common utilities and configurations
- **datasets/**: Datasets for exercises and projects

## How to Use

Each chapter directory contains:
- `examples/` - Working code from the textbook
- `exercises/` - Starting templates
- `solutions/` - Reference implementations
- `README.md` - Chapter-specific instructions

### Running an Example

```bash
cd module-1/chapter-1.1/examples/
python3 my_first_node.py
```

### Completing an Exercise

```bash
cd module-1/chapter-1.1/exercises/
# Follow instructions in README.md
# Use solution/ as reference if needed
```

## Learning Paths

- **Sequential**: Complete all chapters in order (93-117 hours)
- **Fast Track**: Skip to specific modules (varies)
- **Deep Dive**: Combine textbook + code for specific topics (varies)

See main textbook for detailed learning strategies.

## Getting Help

1. Check chapter README for troubleshooting
2. Review solutions/ for reference
3. Open an issue on GitHub
4. Consult main textbook documentation

## Contributing

We welcome contributions! See CONTRIBUTING.md for guidelines.

## License

MIT License - See LICENSE file

## Resources

- [Main Textbook](https://github.com/physical-ai-lab/ai-humanoid-robotics)
- [ROS 2 Documentation](https://docs.ros.org/en/humble/)
- [Gazebo Documentation](https://gazebosim.org/)

---

**Last Updated**: 2025-12-16
**Maintainer**: Physical AI Lab
```

## Step 4: Configure GitHub Branch Protection

### Via GitHub Web Interface

1. Go to repository Settings → Branches
2. Under "Branch protection rules", click "Add rule"
3. Configure:
   - **Branch name pattern**: `main`
   - **Require a pull request before merging**: ✅
   - **Require status checks to pass before merging**: ✅
   - **Require branches to be up to date before merging**: ✅
   - **Include administrators**: ✅

### Via GitHub CLI

```bash
# Create branch protection rule
gh api repos/OWNER/REPO/branches/main/protection \
  -X PUT \
  -f required_pull_request_reviews='{"required_approving_review_count":1}' \
  -f required_status_checks='{"strict":true,"contexts":[]}' \
  -f enforce_admins=true
```

## Step 5: Setup GitHub Actions (Optional)

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest pep8 -r requirements.txt

    - name: Lint with PEP8
      run: |
        pep8 --max-line-length=100 . --exclude=venv,build || true

    - name: Run tests
      run: |
        python -m pytest tests/ -v
```

## Step 6: Setup Git LFS (for large files)

For datasets and binary files:

```bash
# Install git-lfs
# Ubuntu/Debian:
sudo apt-get install git-lfs

# macOS:
brew install git-lfs

# Initialize in repository
git lfs install

# Track large files
git lfs track "*.bag"
git lfs track "datasets/*.zip"
git add .gitattributes
git commit -m "Setup git-lfs for large files"
```

## Step 7: Link to Main Repository

In the main textbook repository, add to `README.md`:

```markdown
## Code Examples & Exercises

All code examples and exercises are available in the companion repository:

**[ai-humanoid-robotics-code](https://github.com/physical-ai-lab/ai-humanoid-robotics-code)**

Each textbook chapter links to corresponding code examples and exercises.
```

## Step 8: Create Initial Content

### Create chapter-specific files

```bash
# Example for Chapter 1.1
cd module-1/chapter-1.1/

# Create examples
cat > examples/README.md << 'EOF'
# Chapter 1.1 Examples

Examples from "ROS 2 Overview and Installation"

## Files

- `my_first_node.py` - Creating your first ROS 2 node
- `publisher_node.py` - Publishing messages
- `subscriber_node.py` - Subscribing to topics

## Running

```bash
# Terminal 1: Start ROS domain
source /opt/ros/humble/setup.bash

# Terminal 2: Run publisher
python3 examples/publisher_node.py

# Terminal 3: Run subscriber
python3 examples/subscriber_node.py
```
EOF

# Create exercises
cat > exercises/README.md << 'EOF'
# Chapter 1.1 Exercises

Hands-on exercises for Chapter 1.1

## Exercise 1: Create Your First Node

Follow instructions in textbook Chapter 1.1, section "Exercise 1"

- Start with: `starter_node.py`
- Solution: `../solutions/starter_node_solution.py`
EOF

# Create solutions (empty, for students to complete)
mkdir solutions
cat > solutions/README.md << 'EOF'
# Chapter 1.1 Solutions

Reference solutions for Chapter 1.1 exercises

Use only after attempting the exercises yourself!
EOF

git add .
git commit -m "Add Chapter 1.1 structure: examples, exercises, solutions"
```

## Step 9: Documentation and CI/CD

### Create requirements.txt

```bash
cat > requirements.txt << 'EOF'
numpy>=1.21.0
scipy>=1.7.0
matplotlib>=3.4.0
PyYAML>=5.4.1
pillow>=8.3.0
opencv-python>=4.5.3
pytest>=7.0.0
colcon-common-extensions>=0.1.0
EOF
```

### Create Makefile (optional, for easy commands)

```makefile
.PHONY: setup test clean help

help:
	@echo "Available commands:"
	@echo "  make setup - Setup virtual environment"
	@echo "  make test  - Run all tests"
	@echo "  make clean - Clean build artifacts"

setup:
	python3 -m venv venv
	source venv/bin/activate && pip install -r requirements.txt

test:
	python -m pytest tests/ -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ *.egg-info/
```

## Step 10: Initial Commit and Push

```bash
# Ensure all files are tracked
git add .

# Create initial commit
git commit -m "Initial repository setup with structure and documentation"

# Push to GitHub
git push -u origin main

# Verify
git log --oneline | head -5
```

## Verification Checklist

- [ ] Repository created on GitHub
- [ ] Directory structure matches specification
- [ ] README.md, CONTRIBUTING.md, .gitignore present
- [ ] Branch protection rules enabled
- [ ] requirements.txt created
- [ ] GitHub Actions workflows (if using CI/CD)
- [ ] Initial commit pushed to main
- [ ] Linked from main textbook repository

## Next Steps

1. **Add Module Content**
   - Create chapter structure for all 23 chapters
   - Add example code files
   - Create exercise templates

2. **Create GitHub Team** (optional)
   - Invite collaborators
   - Set permissions
   - Establish review process

3. **Setup Project Board** (optional)
   - Track chapter development
   - Manage issues and PRs
   - Monitor progress

4. **Publish to GitHub Pages** (optional)
   - Automatically generate documentation
   - Host code documentation
   - Create gallery of projects

---

**Related Documentation:**
- Main Textbook: `ai-humanoid-robotics` repository
- Setup Guide: `docs/preface/setup-guide.md`
- Installation Scripts: `shared/install-scripts/`

**Last Updated:** 2025-12-16
**Maintained By:** Physical AI Lab
