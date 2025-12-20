#!/bin/bash

################################################################################
# Physical AI & Humanoid Robotics - Ubuntu Installation Script
#
# This script automates the complete setup for Ubuntu 22.04 with:
# - ROS 2 Humble Hawksbill
# - Gazebo Fortress
# - Python 3.10 and dependencies
# - Development tools and build essentials
#
# Usage: bash ubuntu-setup.sh
# Requires: sudo access
################################################################################

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
ROS_DISTRO="humble"
PYTHON_VERSION="3.10"

################################################################################
# Helper Functions
################################################################################

print_header() {
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

check_command() {
    if command -v $1 &> /dev/null; then
        print_success "$1 is installed"
        return 0
    else
        print_warning "$1 is not installed"
        return 1
    fi
}

################################################################################
# System Check
################################################################################

check_system() {
    print_header "System Verification"

    # Check if running Ubuntu 22.04
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        print_info "Detected OS: $ID $VERSION_ID"

        if [[ "$ID" != "ubuntu" || "$VERSION_ID" != "22.04" ]]; then
            print_warning "This script is optimized for Ubuntu 22.04"
            print_warning "You are running $ID $VERSION_ID"
            read -p "Continue anyway? (y/n) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                print_error "Installation aborted"
                exit 1
            fi
        fi
    fi

    # Check for sudo
    if [ "$EUID" -ne 0 ] && ! sudo -n true 2>/dev/null; then
        print_error "This script requires sudo access"
        exit 1
    fi

    print_success "System checks passed"
}

################################################################################
# Update System
################################################################################

update_system() {
    print_header "Updating System Packages"

    sudo apt-get update
    sudo apt-get upgrade -y

    print_success "System packages updated"
}

################################################################################
# Install Python 3.10
################################################################################

install_python() {
    print_header "Installing Python $PYTHON_VERSION"

    if check_command python3; then
        INSTALLED_VERSION=$(python3 --version | awk '{print $2}')
        print_info "Python version: $INSTALLED_VERSION"
    fi

    sudo apt-get install -y \
        python3.10 \
        python3.10-dev \
        python3.10-venv \
        python3-pip \
        python3-setuptools \
        python3-wheel

    # Verify installation
    python3 --version
    print_success "Python $PYTHON_VERSION installed"
}

################################################################################
# Install Build Tools
################################################################################

install_build_tools() {
    print_header "Installing Build Tools and Dependencies"

    sudo apt-get install -y \
        build-essential \
        cmake \
        git \
        curl \
        wget \
        gnupg \
        lsb-release \
        software-properties-common \
        apt-utils \
        ca-certificates \
        sudo

    print_success "Build tools installed"
}

################################################################################
# Setup ROS 2 Repository
################################################################################

setup_ros2_repo() {
    print_header "Setting up ROS 2 Repository"

    # Add ROS 2 GPG key
    sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

    # Add ROS 2 repository
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | \
        sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

    sudo apt-get update

    print_success "ROS 2 repository configured"
}

################################################################################
# Install ROS 2 Humble
################################################################################

install_ros2() {
    print_header "Installing ROS 2 $ROS_DISTRO"

    sudo apt-get install -y ros-$ROS_DISTRO-desktop

    # Install additional tools
    sudo apt-get install -y \
        ros-$ROS_DISTRO-ros2-control \
        ros-$ROS_DISTRO-ros2-controllers \
        ros-$ROS_DISTRO-gazebo-ros2-control \
        ros-$ROS_DISTRO-geometry2 \
        ros-$ROS_DISTRO-tf-transformations

    print_success "ROS 2 $ROS_DISTRO installed"
}

################################################################################
# Install Gazebo Fortress
################################################################################

install_gazebo() {
    print_header "Installing Gazebo Fortress"

    # Add Gazebo repository
    sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
    wget https://packages.osrfoundation.org/gazebo.gpg -O - | sudo apt-key add -

    sudo apt-get update
    sudo apt-get install -y \
        gazebo \
        libgazebo-dev

    print_success "Gazebo Fortress installed"
}

################################################################################
# Install Python Dependencies
################################################################################

install_python_deps() {
    print_header "Installing Python Dependencies"

    python3 -m pip install --upgrade pip
    python3 -m pip install \
        numpy \
        scipy \
        matplotlib \
        PyYAML \
        pillow \
        opencv-python \
        pyyaml \
        colcon-common-extensions \
        flake8 \
        pytest

    print_success "Python dependencies installed"
}

################################################################################
# Setup ROS 2 Environment
################################################################################

setup_ros2_env() {
    print_header "Setting up ROS 2 Environment"

    # Add sourcing to bashrc if not already present
    if ! grep -q "source /opt/ros/$ROS_DISTRO/setup.bash" ~/.bashrc; then
        echo "source /opt/ros/$ROS_DISTRO/setup.bash" >> ~/.bashrc
        print_success "Added ROS 2 setup to ~/.bashrc"
    else
        print_info "ROS 2 setup already in ~/.bashrc"
    fi

    # Source for current session
    source /opt/ros/$ROS_DISTRO/setup.bash

    print_success "ROS 2 environment configured"
}

################################################################################
# Create ROS 2 Workspace
################################################################################

create_ros_workspace() {
    print_header "Creating ROS 2 Workspace"

    WORKSPACE_DIR="${HOME}/ros2_ws"

    if [ ! -d "$WORKSPACE_DIR" ]; then
        mkdir -p "$WORKSPACE_DIR/src"
        print_success "Workspace created at $WORKSPACE_DIR"
    else
        print_info "Workspace already exists at $WORKSPACE_DIR"
    fi

    # Build workspace
    cd "$WORKSPACE_DIR"
    colcon build --symlink-install 2>/dev/null || print_warning "Colcon build had warnings (workspace may be empty, which is ok)"

    # Add sourcing to bashrc if not already present
    if ! grep -q "source $WORKSPACE_DIR/install/setup.bash" ~/.bashrc; then
        echo "source $WORKSPACE_DIR/install/setup.bash" >> ~/.bashrc
        print_success "Added workspace setup to ~/.bashrc"
    fi

    source "$WORKSPACE_DIR/install/setup.bash" 2>/dev/null || true

    print_success "ROS 2 workspace configured"
}

################################################################################
# Verification
################################################################################

verify_installation() {
    print_header "Verifying Installation"

    echo "Checking installed versions:"

    # Reload bashrc to get ROS setup
    source ~/.bashrc 2>/dev/null || true

    echo ""
    print_info "Python:"
    python3 --version

    echo ""
    print_info "ROS 2:"
    if command -v ros2 &> /dev/null; then
        source /opt/ros/$ROS_DISTRO/setup.bash
        ros2 --version
        print_success "ROS 2 command available"
    else
        print_warning "ROS 2 command not yet available (reload shell to activate)"
    fi

    echo ""
    print_info "Gazebo:"
    if command -v gazebo &> /dev/null; then
        gazebo --version
        print_success "Gazebo available"
    else
        print_warning "Gazebo command not yet available (reload shell to activate)"
    fi

    echo ""
    print_success "Installation verification complete"
}

################################################################################
# Main Installation Flow
################################################################################

main() {
    print_header "Physical AI & Humanoid Robotics - Ubuntu Setup"
    echo "Target: Ubuntu 22.04 with ROS 2 Humble, Gazebo, Python 3.10"
    echo ""

    check_system
    update_system
    install_python
    install_build_tools
    setup_ros2_repo
    install_ros2
    install_gazebo
    install_python_deps
    setup_ros2_env
    create_ros_workspace
    verify_installation

    print_header "Installation Complete!"
    echo ""
    echo "To activate the ROS 2 environment in your current shell:"
    echo "  source ~/.bashrc"
    echo ""
    echo "Next steps:"
    echo "  1. Start the textbook: cd ~/ai-humanoid-robotics"
    echo "  2. Follow the setup guide: docs/preface/setup-guide.md"
    echo "  3. Begin with Module 1: Chapter 1.1"
    echo ""
    print_success "Ready to begin learning Physical AI & Humanoid Robotics!"
}

# Run main function
main
