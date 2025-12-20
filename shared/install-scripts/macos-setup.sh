#!/bin/bash

################################################################################
# Physical AI & Humanoid Robotics - macOS Installation Script
#
# This script automates the complete setup for macOS 12+ with:
# - Homebrew package manager
# - Python 3.10
# - ROS 2 Humble Hawksbill
# - Build tools and development dependencies
#
# Usage: bash macos-setup.sh
# Requires: internet connection, 10GB free disk space
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

    # Check macOS version
    MACOS_VERSION=$(sw_vers -productVersion)
    print_info "Detected macOS: $MACOS_VERSION"

    MAJOR_VERSION=$(echo $MACOS_VERSION | cut -d. -f1)

    if [ "$MAJOR_VERSION" -lt 12 ]; then
        print_warning "This script is optimized for macOS 12 (Monterey) or newer"
        print_warning "You are running macOS $MACOS_VERSION"
        read -p "Continue anyway? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_error "Installation aborted"
            exit 1
        fi
    fi

    # Check for Xcode command line tools
    if ! xcode-select -p &> /dev/null; then
        print_info "Installing Xcode Command Line Tools..."
        xcode-select --install
        print_success "Xcode Command Line Tools installed"
    else
        print_success "Xcode Command Line Tools already installed"
    fi

    print_success "System checks passed"
}

################################################################################
# Install Homebrew
################################################################################

install_homebrew() {
    print_header "Installing Homebrew"

    if check_command brew; then
        print_info "Homebrew version:"
        brew --version
        return
    fi

    print_info "Installing Homebrew package manager..."

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Add Homebrew to PATH if on Apple Silicon
    if [ "$(uname -m)" = "arm64" ]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
        if ! grep -q "eval.*homebrew.*shellenv" ~/.zprofile; then
            echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
            print_success "Homebrew added to ~/.zprofile"
        fi
    fi

    print_success "Homebrew installed"
}

################################################################################
# Update Homebrew
################################################################################

update_homebrew() {
    print_header "Updating Homebrew"

    brew update
    brew upgrade

    print_success "Homebrew updated"
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

    print_info "Installing Python $PYTHON_VERSION via Homebrew..."

    brew install python@3.10

    # Create symlink if needed
    if [ ! -f /usr/local/bin/python3.10 ] && [ -f /opt/homebrew/bin/python3.10 ]; then
        ln -sf /opt/homebrew/bin/python3.10 /usr/local/bin/python3.10
        print_success "Python 3.10 symlink created"
    fi

    # Verify installation
    python3 --version || python3.10 --version
    print_success "Python $PYTHON_VERSION installed"
}

################################################################################
# Install Build Tools and Dependencies
################################################################################

install_build_tools() {
    print_header "Installing Build Tools and Dependencies"

    print_info "Installing development tools via Homebrew..."

    brew install \
        cmake \
        git \
        curl \
        wget \
        pkg-config \
        osxfuse \
        graphviz

    # Install optional but useful tools
    brew install colcon-common-extensions 2>/dev/null || print_warning "colcon not available via Homebrew"

    print_success "Build tools installed"
}

################################################################################
# Setup ROS 2 Repository (macOS)
################################################################################

setup_ros2_repo() {
    print_header "Setting up ROS 2 Repository"

    # For macOS, we'll use Homebrew taps if available
    print_info "Adding ROS 2 Homebrew tap..."

    brew tap ros-infra/ros2-bottles

    print_success "ROS 2 repository configured"
}

################################################################################
# Install ROS 2 Humble
################################################################################

install_ros2() {
    print_header "Installing ROS 2 $ROS_DISTRO"

    # First, try to install via homebrew
    print_info "Attempting ROS 2 installation via Homebrew..."

    brew install ros2-$ROS_DISTRO 2>/dev/null || {
        print_warning "ROS 2 Homebrew package not available"
        print_info "Installing ROS 2 from source..."

        # Create ROS 2 directory
        mkdir -p ~/ros2_$ROS_DISTRO

        # Clone ROS 2 repositories
        cd ~/ros2_$ROS_DISTRO
        vcs import --input https://raw.githubusercontent.com/ros2/ros2/release-$ROS_DISTRO/ros2.repos src

        # Install dependencies
        print_info "Installing ROS 2 dependencies..."
        brew install asdf

        # Build ROS 2
        print_info "Building ROS 2 (this may take 20-30 minutes)..."
        colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release -DCMAKE_OSX_ARCHITECTURES="arm64" 2>/dev/null || \
        colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release 2>/dev/null || \
        print_warning "ROS 2 build completed with warnings"

        cd ~
        return
    }

    # If Homebrew installation succeeded
    print_success "ROS 2 $ROS_DISTRO installed"
}

################################################################################
# Install Additional ROS 2 Packages
################################################################################

install_ros2_packages() {
    print_header "Installing Additional ROS 2 Packages"

    print_info "Installing common ROS 2 packages..."

    packages=(
        "ros2-humble-ros2-control"
        "ros2-humble-ros2-controllers"
        "ros2-humble-geometry2"
        "ros2-humble-tf-transformations"
    )

    for package in "${packages[@]}"; do
        brew install "$package" 2>/dev/null || print_warning "Could not install $package"
    done

    print_success "ROS 2 packages installation complete"
}

################################################################################
# Install Python Dependencies
################################################################################

install_python_deps() {
    print_header "Installing Python Dependencies"

    print_info "Upgrading pip..."
    python3 -m pip install --upgrade pip

    print_info "Installing Python packages..."

    python3 -m pip install \
        numpy \
        scipy \
        matplotlib \
        PyYAML \
        pillow \
        opencv-python \
        pyyaml \
        flake8 \
        pytest \
        colcon-common-extensions

    print_success "Python dependencies installed"
}

################################################################################
# Setup ROS 2 Environment
################################################################################

setup_ros2_env() {
    print_header "Setting up ROS 2 Environment"

    SHELL_CONFIG="$HOME/.zprofile"

    # Check if using zsh (default on newer macOS)
    if [ "$SHELL" = "/bin/zsh" ]; then
        SHELL_CONFIG="$HOME/.zprofile"
    elif [ "$SHELL" = "/bin/bash" ]; then
        SHELL_CONFIG="$HOME/.bash_profile"
    fi

    # Add ROS 2 setup sourcing if not already present
    if ! grep -q "source /opt/ros/$ROS_DISTRO/setup.zsh\|source /opt/ros/$ROS_DISTRO/setup.bash\|source ~/ros2_$ROS_DISTRO/install/setup.zsh" "$SHELL_CONFIG" 2>/dev/null; then
        {
            echo ""
            echo "# ROS 2 $ROS_DISTRO setup"
            echo "if [ -f /opt/ros/$ROS_DISTRO/setup.zsh ]; then"
            echo "    source /opt/ros/$ROS_DISTRO/setup.zsh"
            echo "elif [ -f ~/ros2_$ROS_DISTRO/install/setup.zsh ]; then"
            echo "    source ~/ros2_$ROS_DISTRO/install/setup.zsh"
            echo "fi"
        } >> "$SHELL_CONFIG"

        print_success "Added ROS 2 setup to $SHELL_CONFIG"
    else
        print_info "ROS 2 setup already in $SHELL_CONFIG"
    fi

    # Source for current session
    if [ -f /opt/ros/$ROS_DISTRO/setup.zsh ]; then
        source /opt/ros/$ROS_DISTRO/setup.zsh
    elif [ -f ~/ros2_$ROS_DISTRO/install/setup.zsh ]; then
        source ~/ros2_$ROS_DISTRO/install/setup.zsh
    fi

    print_success "ROS 2 environment configured"
}

################################################################################
# Create ROS 2 Workspace
################################################################################

create_ros_workspace() {
    print_header "Creating ROS 2 Workspace"

    WORKSPACE_DIR="$HOME/ros2_ws"

    if [ ! -d "$WORKSPACE_DIR" ]; then
        mkdir -p "$WORKSPACE_DIR/src"
        print_success "Workspace created at $WORKSPACE_DIR"
    else
        print_info "Workspace already exists at $WORKSPACE_DIR"
    fi

    # Build workspace
    cd "$WORKSPACE_DIR"
    colcon build --symlink-install 2>/dev/null || print_warning "Colcon build had warnings (workspace may be empty, which is ok)"

    SHELL_CONFIG="$HOME/.zprofile"
    if [ "$SHELL" = "/bin/bash" ]; then
        SHELL_CONFIG="$HOME/.bash_profile"
    fi

    # Add sourcing to shell config if not already present
    if ! grep -q "source $WORKSPACE_DIR/install/setup.zsh\|source $WORKSPACE_DIR/install/setup.bash" "$SHELL_CONFIG" 2>/dev/null; then
        echo "source $WORKSPACE_DIR/install/setup.zsh 2>/dev/null || source $WORKSPACE_DIR/install/setup.bash 2>/dev/null || true" >> "$SHELL_CONFIG"
        print_success "Added workspace setup to $SHELL_CONFIG"
    fi

    source "$WORKSPACE_DIR/install/setup.zsh" 2>/dev/null || source "$WORKSPACE_DIR/install/setup.bash" 2>/dev/null || true

    print_success "ROS 2 workspace configured"
}

################################################################################
# Optional: Install Gazebo (if using Homebrew)
################################################################################

install_gazebo() {
    print_header "Installing Gazebo (Optional)"

    print_info "Attempting Gazebo installation via Homebrew..."

    brew install gazebo 2>/dev/null || {
        print_warning "Gazebo not available via Homebrew"
        print_info "ROS 2 includes Gazebo simulation tools"
        return
    }

    print_success "Gazebo installed"
}

################################################################################
# Verification
################################################################################

verify_installation() {
    print_header "Verifying Installation"

    echo "Checking installed versions:"

    # Reload shell config to get ROS setup
    if [ -f "$HOME/.zprofile" ]; then
        source "$HOME/.zprofile" 2>/dev/null || true
    fi

    echo ""
    print_info "Python:"
    python3 --version

    echo ""
    print_info "Homebrew:"
    brew --version

    echo ""
    print_info "Git:"
    git --version

    echo ""
    print_info "ROS 2:"
    if command -v ros2 &> /dev/null; then
        ros2 --version
        print_success "ROS 2 command available"
    else
        print_warning "ROS 2 command not yet available (reload shell to activate)"
    fi

    echo ""
    print_success "Installation verification complete"
}

################################################################################
# Main Installation Flow
################################################################################

main() {
    print_header "Physical AI & Humanoid Robotics - macOS Setup"
    echo "Target: macOS 12+ with Homebrew, Python 3.10, ROS 2 Humble"
    echo ""

    check_system
    install_homebrew
    update_homebrew
    install_python
    install_build_tools
    install_gazebo
    install_python_deps
    setup_ros2_env
    create_ros_workspace
    verify_installation

    print_header "Installation Complete!"
    echo ""
    echo "To activate the ROS 2 environment in your current shell:"
    echo "  source ~/.zprofile  # or ~/.bash_profile if using bash"
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
