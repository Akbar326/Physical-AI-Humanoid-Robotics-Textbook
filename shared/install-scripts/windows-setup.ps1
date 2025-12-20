# ============================================================================
# Physical AI & Humanoid Robotics - Windows Installation Script
#
# This script automates the complete setup for Windows 10/11 with:
# - Python 3.10
# - ROS 2 Humble Hawksbill (binary installation)
# - Visual Studio Build Tools
# - Git and development tools
#
# Usage: powershell.exe -ExecutionPolicy Bypass -File windows-setup.ps1
# Requires: Administrator access, internet connection
# ============================================================================

#Requires -RunAsAdministrator

param(
    [switch]$SkipPython = $false,
    [switch]$SkipROS2 = $false,
    [switch]$SkipBuildTools = $false
)

# Configuration
$ROS_DISTRO = "humble"
$PYTHON_VERSION = "3.10"
$PYTHON_DOWNLOAD_URL = "https://www.python.org/ftp/python/3.10.13/python-3.10.13-amd64.exe"
$ANACONDA_DOWNLOAD_URL = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe"

# Color codes
$Colors = @{
    Red    = "Red"
    Green  = "Green"
    Yellow = "Yellow"
    Cyan   = "Cyan"
}

# ============================================================================
# Helper Functions
# ============================================================================

function Write-Header {
    param([string]$Message)
    Write-Host "================================================" -ForegroundColor $Colors.Cyan
    Write-Host $Message -ForegroundColor $Colors.Cyan
    Write-Host "================================================" -ForegroundColor $Colors.Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor $Colors.Green
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor $Colors.Red
}

function Write-Warning-Custom {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor $Colors.Yellow
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ️  $Message" -ForegroundColor $Colors.Cyan
}

function Test-AdminPrivileges {
    $principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Test-CommandExists {
    param([string]$Command)
    try {
        if (Get-Command $Command -ErrorAction Stop) {
            Write-Success "$Command is installed"
            return $true
        }
    }
    catch {
        Write-Warning-Custom "$Command is not installed"
        return $false
    }
}

# ============================================================================
# System Check
# ============================================================================

function Check-System {
    Write-Header "System Verification"

    # Check Windows version
    $OSVersion = [System.Environment]::OSVersion.Version
    Write-Info "Detected Windows: $($OSVersion.Major).$($OSVersion.Minor) (Build $($OSVersion.Build))"

    if ($OSVersion.Major -lt 10) {
        Write-Error-Custom "This script requires Windows 10 or newer"
        exit 1
    }

    # Check admin privileges
    if (-not (Test-AdminPrivileges)) {
        Write-Error-Custom "This script requires Administrator privileges"
        exit 1
    }

    Write-Success "System checks passed"
}

# ============================================================================
# Install Python 3.10
# ============================================================================

function Install-Python {
    if ($SkipPython) {
        Write-Info "Skipping Python installation (--SkipPython flag set)"
        return
    }

    Write-Header "Installing Python $PYTHON_VERSION"

    if (Test-CommandExists python) {
        $PythonVersion = python --version 2>&1
        Write-Info "Python is already installed: $PythonVersion"
        return
    }

    Write-Info "Downloading Python $PYTHON_VERSION installer..."

    $DownloadPath = "$env:TEMP\python-installer.exe"

    try {
        (New-Object Net.WebClient).DownloadFile($PYTHON_DOWNLOAD_URL, $DownloadPath)
        Write-Info "Download complete: $DownloadPath"
    }
    catch {
        Write-Error-Custom "Failed to download Python: $_"
        Write-Info "Please install Python 3.10 manually from https://www.python.org"
        return
    }

    Write-Info "Running Python installer..."
    $ArgumentList = @(
        $DownloadPath,
        '/passive',
        'PrependPath=1',
        'InstallAllUsers=0'
    )

    Start-Process -FilePath "msiexec.exe" -ArgumentList "/i $DownloadPath /quiet /qn ALLUSERS=1 ADDLOCAL=ALL" -Wait -NoNewWindow

    # Verify installation
    if (Test-CommandExists python) {
        Write-Success "Python $PYTHON_VERSION installed"
        python --version
    }
    else {
        Write-Error-Custom "Python installation verification failed"
    }

    # Cleanup
    Remove-Item -Force $DownloadPath -ErrorAction SilentlyContinue
}

# ============================================================================
# Install Git
# ============================================================================

function Install-Git {
    Write-Header "Checking Git Installation"

    if (Test-CommandExists git) {
        git --version
        return
    }

    Write-Info "Git not found. Installing via winget..."

    try {
        winget install -e --id Git.Git -h 2>$null
        Write-Success "Git installed"
    }
    catch {
        Write-Warning-Custom "Could not install Git via winget"
        Write-Info "Please install Git manually from https://git-scm.com/download/win"
    }
}

# ============================================================================
# Install Visual Studio Build Tools
# ============================================================================

function Install-BuildTools {
    if ($SkipBuildTools) {
        Write-Info "Skipping Build Tools installation (--SkipBuildTools flag set)"
        return
    }

    Write-Header "Installing Visual Studio Build Tools"

    # Check if MSVC is available
    $vcvars_paths = @(
        "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat",
        "C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvars64.bat",
        "C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Auxiliary\Build\vcvars64.bat",
        "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"
    )

    $found = $false
    foreach ($path in $vcvars_paths) {
        if (Test-Path $path) {
            Write-Success "Visual Studio Build Tools found"
            $found = $true
            break
        }
    }

    if (-not $found) {
        Write-Warning-Custom "Visual Studio Build Tools not found"
        Write-Info "Installing via winget..."

        try {
            winget install -e --id Microsoft.VisualStudio.BuildTools -h 2>$null
            Write-Success "Build Tools installed"
        }
        catch {
            Write-Warning-Custom "Could not auto-install Build Tools"
            Write-Info "Please manually install: https://visualstudio.microsoft.com/downloads/"
        }
    }
}

# ============================================================================
# Setup Python Environment
# ============================================================================

function Setup-PythonEnvironment {
    Write-Header "Setting up Python Environment"

    # Upgrade pip
    Write-Info "Upgrading pip..."
    python -m pip install --upgrade pip -q

    # Install required packages
    Write-Info "Installing Python dependencies..."
    $dependencies = @(
        "numpy",
        "scipy",
        "matplotlib",
        "PyYAML",
        "pillow",
        "opencv-python",
        "colcon-common-extensions",
        "flake8",
        "pytest",
        "lark"
    )

    foreach ($package in $dependencies) {
        Write-Info "Installing $package..."
        python -m pip install $package -q 2>$null
    }

    Write-Success "Python environment configured"
}

# ============================================================================
# Install ROS 2 Humble
# ============================================================================

function Install-ROS2 {
    if ($SkipROS2) {
        Write-Info "Skipping ROS 2 installation (--SkipROS2 flag set)"
        return
    }

    Write-Header "Installing ROS 2 $ROS_DISTRO"

    # Check if ROS 2 is already installed
    if (Test-Path "C:\opt\ros\$ROS_DISTRO") {
        Write-Success "ROS 2 $ROS_DISTRO is already installed"
        return
    }

    Write-Info "Downloading ROS 2 $ROS_DISTRO..."

    # Download ROS 2 installer
    $ROS2_URL = "https://github.com/ros2/ros2/releases/download/release-$ROS_DISTRO-20230712/ros2-$ROS_DISTRO-20230712-windows-Release-amd64.zip"
    $DownloadPath = "$env:TEMP\ros2-$ROS_DISTRO.zip"

    try {
        (New-Object Net.WebClient).DownloadFile($ROS2_URL, $DownloadPath)
        Write-Info "Download complete"
    }
    catch {
        Write-Error-Custom "Failed to download ROS 2: $_"
        Write-Info "Please download manually from https://docs.ros.org/en/$ROS_DISTRO/Installation/Windows-Install-Binary.html"
        return
    }

    # Extract
    Write-Info "Extracting ROS 2..."
    Expand-Archive -Path $DownloadPath -DestinationPath "C:\" -Force

    # Add to PATH
    Write-Info "Configuring system PATH..."
    $ROS2_Path = "C:\ros2_$ROS_DISTRO\bin"
    $CurrentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")

    if ($CurrentPath -notlike "*$ROS2_Path*") {
        $NewPath = "$CurrentPath;$ROS2_Path"
        [Environment]::SetEnvironmentVariable("Path", $NewPath, "Machine")
        Write-Success "ROS 2 added to system PATH"
    }

    Write-Success "ROS 2 $ROS_DISTRO installed"

    # Cleanup
    Remove-Item -Force $DownloadPath -ErrorAction SilentlyContinue
}

# ============================================================================
# Setup ROS 2 Environment Variables
# ============================================================================

function Setup-ROS2-Environment {
    Write-Header "Setting up ROS 2 Environment Variables"

    $ROS_DOMAIN_ID = 0
    [Environment]::SetEnvironmentVariable("ROS_DOMAIN_ID", $ROS_DOMAIN_ID, "User")
    Write-Success "ROS_DOMAIN_ID set to $ROS_DOMAIN_ID"

    # Add ROSDISTRO environment variable
    [Environment]::SetEnvironmentVariable("ROS_DISTRO", $ROS_DISTRO, "User")
    Write-Success "ROS_DISTRO set to $ROS_DISTRO"
}

# ============================================================================
# Create ROS 2 Workspace
# ============================================================================

function Create-ROS2-Workspace {
    Write-Header "Setting up ROS 2 Workspace"

    $WORKSPACE_DIR = "$env:USERPROFILE\ros2_ws"

    if (-not (Test-Path $WORKSPACE_DIR)) {
        New-Item -ItemType Directory -Path $WORKSPACE_DIR -Force > $null
        New-Item -ItemType Directory -Path "$WORKSPACE_DIR\src" -Force > $null
        Write-Success "Workspace created at $WORKSPACE_DIR"
    }
    else {
        Write-Info "Workspace already exists at $WORKSPACE_DIR"
    }
}

# ============================================================================
# Verification
# ============================================================================

function Verify-Installation {
    Write-Header "Verifying Installation"

    Write-Info "Checking installed versions:"
    Write-Host ""

    if (Test-CommandExists python) {
        Write-Info "Python:"
        python --version
    }
    else {
        Write-Warning-Custom "Python not found in PATH (restart PowerShell or computer)"
    }

    Write-Host ""

    if (Test-CommandExists git) {
        Write-Info "Git:"
        git --version
    }
    else {
        Write-Warning-Custom "Git not found in PATH"
    }

    Write-Host ""
    Write-Success "Verification complete"
}

# ============================================================================
# Main Installation Flow
# ============================================================================

function Main {
    Write-Header "Physical AI & Humanoid Robotics - Windows Setup"
    Write-Host "Target: Windows 10/11 with Python 3.10, ROS 2 Humble"
    Write-Host ""

    Check-System
    Install-Python
    Install-Git
    Install-BuildTools
    Setup-PythonEnvironment
    Install-ROS2
    Setup-ROS2-Environment
    Create-ROS2-Workspace
    Verify-Installation

    Write-Header "Installation Complete!"
    Write-Host ""
    Write-Host "To activate the environment:"
    Write-Host "  1. Restart PowerShell or your terminal"
    Write-Host "  2. Verify: python --version && git --version"
    Write-Host ""
    Write-Host "Next steps:"
    Write-Host "  1. Start the textbook: cd ~\ai-humanoid-robotics"
    Write-Host "  2. Follow the setup guide: docs\preface\setup-guide.md"
    Write-Host "  3. Begin with Module 1: Chapter 1.1"
    Write-Host ""
    Write-Success "Ready to begin learning Physical AI & Humanoid Robotics!"
}

# Run main function
Main
