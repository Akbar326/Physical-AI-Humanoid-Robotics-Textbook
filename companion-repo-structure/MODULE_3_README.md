# Module 3: Isaac Sim & AI Integration - Code Examples & Exercises

**Time**: 19-25 hours | **Chapters**: 5 | **Difficulty**: Advanced

This directory contains all code examples, exercises, and solutions for **Module 3: Isaac Sim & AI Integration** of the Physical AI & Humanoid Robotics textbook.

---

## Quick Links

| Chapter | Topic | Time | Files |
|---------|-------|------|-------|
| [3.1](chapter-3-1/) | Introduction to Isaac Sim | 3-4h | Examples |
| [3.2](chapter-3-2/) | Robot Simulation in Isaac Sim | 3-4h | Robot models |
| [3.3](chapter-3-3/) | Synthetic Data Generation | 3-4h | Dataset scripts |
| [3.4](chapter-3-4/) | Computer Vision Fundamentals | 3-4h | Vision examples |
| [3.5](chapter-3-5/) | AI and Machine Learning Integration | 3-5h | ML training |

---

## Learning Objectives

After completing this module, you will be able to:

- ✅ Setup and configure NVIDIA Isaac Sim
- ✅ Create photorealistic simulations
- ✅ Generate synthetic training datasets
- ✅ Implement computer vision algorithms
- ✅ Train machine learning models on simulation data
- ✅ Evaluate sim-to-real transfer effectiveness

---

## Prerequisites

### Required
- Complete **Modules 1 & 2**
- **NVIDIA GPU** (RTX 1060 minimum, RTX 3090 recommended)
- CUDA Toolkit 11.8+
- Isaac Sim 2023.1 installed

### Recommended
- 24GB+ VRAM
- Deep learning framework experience (PyTorch/TensorFlow)
- Linux (Ubuntu 22.04) for best support

---

## GPU Setup

### Verify GPU

```bash
# Check NVIDIA drivers
nvidia-smi

# Output should show GPU with CUDA capability
# GPU Memory: ~12GB+
```

### Install CUDA

```bash
# Ubuntu 22.04
sudo apt-get install nvidia-cuda-toolkit

# Verify CUDA
nvcc --version
```

### Install PyTorch with GPU

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

## Getting Started

### 1. Launch Isaac Sim

```bash
# Start Isaac Sim
isaacsim

# Or launch specific scenario
isaacsim --scenario ./scenarios/robot_manipulation.usd
```

### 2. Run First Example

```bash
cd module-3/chapter-3-1/examples
python3 isaac_hello_world.py
```

### 3. Follow Chapters

Each chapter builds on previous knowledge:

1. **Ch 3.1**: Isaac Sim introduction
2. **Ch 3.2**: Robot simulation with physics
3. **Ch 3.3**: Data generation pipeline
4. **Ch 3.4**: Vision processing
5. **Ch 3.5**: ML model training

---

## Chapter Breakdown

### Chapter 3.1: Introduction to Isaac Sim

**Topics**: Isaac Sim setup, workflows, Python scripting

**Files**:
- `examples/hello_isaac.py` - Basic Isaac Sim script
- `examples/scene_setup.py` - Scene configuration
- `scenarios/` - Pre-built scenarios

**Quick Start**:
```bash
cd chapter-3-1/examples
isaacsim-python hello_isaac.py
```

### Chapter 3.2: Robot Simulation in Isaac Sim

**Topics**: Robot models, articulation, control, sensors

**Files**:
- `robots/` - Robot URDF/USD files
- `examples/robot_control.py` - Control demonstration
- `examples/sensor_simulation.py` - Sensor simulation

**Quick Start**:
```bash
cd chapter-3-2/examples
isaacsim-python robot_control.py
```

### Chapter 3.3: Synthetic Data Generation

**Topics**: Domain randomization, dataset creation, labeling

**Files**:
- `data_generation/` - Dataset generation scripts
- `examples/generate_dataset.py` - Data pipeline
- `datasets/` - Generated data (large, git-lfs)

**Quick Start** (Warning: generates large datasets):
```bash
cd chapter-3-3/
python3 data_generation/generate_dataset.py --num-samples 1000
```

### Chapter 3.4: Computer Vision Fundamentals

**Topics**: Image processing, feature detection, pose estimation

**Files**:
- `examples/image_processing.py` - OpenCV operations
- `examples/feature_detection.py` - Feature extraction
- `examples/pose_estimation.py` - 6D pose estimation

**Quick Start**:
```bash
cd chapter-3-4/examples
python3 image_processing.py
```

### Chapter 3.5: AI and Machine Learning Integration

**Topics**: Model training, inference, optimization

**Files**:
- `training/` - Training scripts
- `models/` - Pre-trained models (git-lfs)
- `examples/train_detector.py` - Training pipeline
- `notebooks/` - Jupyter notebooks

**Quick Start**:
```bash
cd chapter-3-5/training
python3 train_detector.py --dataset ../datasets --epochs 10
```

---

## Project: Object Detection Pipeline

Build complete detection system:

**Scope**:
- Generate synthetic object detection dataset
- Train YOLOv8 model
- Deploy in Isaac Sim
- Evaluate performance

**Files**: `projects/object_detection/`
**Time**: 5-6 hours
**Skills**: All Module 3 concepts

---

## Working with Datasets

### Dataset Organization

```
datasets/
├── train/
│   ├── images/
│   └── labels/
├── val/
│   ├── images/
│   └── labels/
└── test/
    ├── images/
    └── labels/
```

### Download Datasets (Git-LFS)

```bash
# Install git-lfs
sudo apt-get install git-lfs

# Clone with LFS
git clone https://github.com/physical-ai-lab/ai-humanoid-robotics-code
git lfs pull
```

### Generate Custom Dataset

```python
from data_generation import DatasetGenerator

generator = DatasetGenerator()
generator.generate(
    num_samples=5000,
    output_dir="datasets/custom",
    randomize_lighting=True,
    randomize_texture=True,
)
```

---

## Training Models

### PyTorch Training

```bash
# Train detection model
cd chapter-3-5/training
python3 train_detector.py \
    --dataset ../datasets/object_detection \
    --model yolov8 \
    --epochs 50 \
    --batch-size 32 \
    --output ./checkpoints
```

### Monitor Training

```bash
# TensorBoard
tensorboard --logdir ./logs

# Training metrics
python3 -c "import torch; print(torch.cuda.utilization_percent())"
```

### Evaluate Model

```python
from models import ObjectDetector
import torch

model = ObjectDetector("checkpoints/best.pt")
results = model.evaluate("datasets/test")
print(f"mAP: {results['mAP']:.3f}")
```

---

## Optimization Tips

### GPU Memory

```python
# Reduce batch size if OOM
batch_size = 8  # Try smaller values

# Use mixed precision training
from torch.cuda.amp import autocast
with autocast():
    # Training code
    pass
```

### Training Speed

- **Use GPU**: Verify CUDA is active
- **Reduce image size**: Faster training, less memory
- **Data parallelism**: Use multiple GPUs if available
- **Quantization**: For faster inference

### Deployment

```python
# Convert to ONNX for deployment
import torch
model = torch.load("model.pt")
torch.onnx.export(model, dummy_input, "model.onnx")

# Deploy on edge
import onnxruntime
session = onnxruntime.InferenceSession("model.onnx")
```

---

## Resources

### Official Documentation
- [Isaac Sim Docs](https://docs.omniverse.nvidia.com/app_isaacsim/)
- [PyTorch Docs](https://pytorch.org/docs/)
- [OpenCV Docs](https://docs.opencv.org/)

### Pre-trained Models
- [YOLOv8](https://github.com/ultralytics/yolov8)
- [Detectron2](https://detectron2.readthedocs.io/)
- [Hugging Face Models](https://huggingface.co/models)

---

## Troubleshooting

### "CUDA not detected"
```bash
# Verify CUDA
nvidia-smi
nvcc --version

# Check PyTorch
python3 -c "import torch; print(torch.cuda.is_available())"
```

### "Isaac Sim not found"
```bash
# Install Isaac Sim 2023.1
# Download from NVIDIA Omniverse
# Follow installation guide
```

### "GPU out of memory"
- Reduce batch size
- Use gradient accumulation
- Try 16-bit precision
- Use smaller models

### Training very slow
- Verify GPU is being used: `nvidia-smi` (watch mode)
- Check training loop bottleneck
- Consider smaller dataset for testing

---

## Next Steps

After completing Module 3:

1. ✅ Complete all vision examples
2. ✅ Train custom detection model
3. ✅ Evaluate sim-to-real transfer
4. → Proceed to [Module 4: Vision-Language-Action Models](../module-4/)

---

**Advanced AI-powered robotics ahead! 🤖🧠**

**Last Updated**: 2025-12-16
