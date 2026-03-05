# Modular LeKiwi Robot - Dual Robot Docking and Collaborative Manipulation System

This project extends the **old version of lekiwi-lerobot** with advanced capabilities for autonomous dual-robot coordination, real-time tracking, and collaborative object manipulation.

## Project Overview

This work presents a complete system for controlling two LeKiwi mobile robots to perform autonomous docking and collaborative object carrying tasks. The system integrates multiple sensing modalities and demonstrates stable cooperative manipulation through experimental validation.

### Key Innovations

1. **Autonomous Dual-Robot Docking**
   - Uses AprilTag visual markers and camera feedback for precise docking alignment
   - Implements a mechanical threading lock mechanism on wheel hubs for secure coupling
   - Enables two independent robots to autonomously dock and form a unified system

2. **Real-Time Spatial Tracking**
   - Utilizes HTC Vive Tracker system for continuous position and orientation tracking
   - Monitors both robots throughout the entire experimental process
   - Provides ground-truth data for performance evaluation

3. **Stability Monitoring During Collaborative Manipulation**
   - Integrates IMU (Inertial Measurement Unit) sensors on the carried object
   - Transmits sensor data via ESP32-S3 microcontroller
   - Measures object stability and acceleration during cooperative carrying tasks

## Installation & Setup

### Prerequisites
- Ubuntu 20.04 or later
- Python 3.10+
- ROS 2 (recommended)

### Clone and Install

```bash
# Clone the repository
git clone https://github.com/khacnambn/Modular-lekiwi-robot.git
cd Modular-lekiwi-robot

# Navigate to source folder
cd src

# Follow the original LeRobot README for installation
# Install dependencies as specified in lerobot/README.md
pip install -e lerobot

# Install additional robot-specific packages
cd lekiwi_controller
pip install -e .
cd ../lekiwi_servo_control
# Follow CMake build instructions in package
```

### Hardware Requirements

- 2x LeKiwi Mobile Robot Platforms
- 2x RGB Cameras (for AprilTag detection)
- 2x HTC Vive Trackers
- IMU Sensor (with ESP32-S3 interface)
- AprilTag markers (tag36_11 family included in `apriltag-imgs/`)

## Project Structure

```
Modular-lekiwi-robot/
├── src/
│   ├── apriltag-imgs/           # AprilTag visual markers and utilities
│   ├── apriltags/               # AprilTag detection library
│   ├── lekiwi_controller/       # Main robot control package (ROS 2)
│   ├── lekiwi_description/      # URDF models and robot description
│   ├── lekiwi_servo_control/    # C++ servo control interface
│   ├── lerobot/                 # LeRobot framework (modified for dual robots)
│   ├── imu_data/                # IMU data collection and analysis scripts
│   ├── experiment2/             # Experimental results and analysis tools
│   ├── Vive_Tracker/            # Vive Tracker integration code
│   ├── omni_teleop/             # Teleoperation utilities
│   └── scripts/                 # Utility scripts
├── README.md                    # This file
└── [other configuration files]
```

## System Components

### 1. AprilTag-Based Docking System
- **Location**: `src/apriltag-imgs/` and `src/apriltags/`
- Detects AprilTag markers for precise pose estimation
- Enables camera-based visual servoing for robot alignment
- Automatically controls wheel threading mechanism for secure coupling

### 2. LeKiwi Robot Controller
- **Location**: `src/lekiwi_controller/`
- ROS 2-based control interface
- Manages dual-robot coordination
- Implements docking and undocking procedures

### 3. Servo Control Interface
- **Location**: `src/lekiwi_servo_control/`
- Low-level motor control
- Implements threading mechanism for wheel coupling
- C++ implementation for real-time performance

### 4. IMU Data Acquisition
- **Location**: `src/imu_data/`
- Collects accelerometer and gyroscope data during experiments
- Transmits data via ESP32-S3 wireless interface
- Provides stability metrics for object manipulation assessment

### 5. Vive Tracker Integration
- **Location**: `src/Vive_Tracker/`
- Interfaces with HTC Vive tracking system
- Logs position and orientation of both robots in real-time
- Enables ground-truth validation of autonomous docking

### 6. Experimental Analysis
- **Location**: `src/experiment2/`
- Data processing and visualization tools
- Benchmark analysis scripts
- Result compilation and reporting utilities

## Usage

### Basic Robot Control
```bash
cd src/lekiwi_controller
# Launch robot control node
ros2 launch lekiwi_controller robot_launch.py

# In another terminal, control the robot
python scripts/control_robot.py
```

### Autonomous Docking Experiment
```bash
# Start the docking procedure
python src/experiment2/experiment2.py

# Monitor robot positions with Vive Tracker
python src/Vive_Tracker/track_robots.py

# Analyze IMU data during manipulation
python src/imu_data/data_analysis.py
```

### Visualize Experimental Results
```bash
# Generate analysis plots
python src/experiment2/analyze_log.py

# Create benchmark reports
python src/experiment2/benchmark_log.py

# Visualize reference paths
python src/experiment2/visualize_reference_path.py
```

## Experimental Results

This work demonstrates:
- **Docking Success Rate**: Autonomous alignment and coupling of two robots
- **Stability Metrics**: Object acceleration during collaborative carrying measured via IMU
- **Tracking Accuracy**: Continuous position monitoring using Vive Tracker system
- **Task Completion**: Synchronized cooperative manipulation of shared payloads

### Results Publication

Complete experimental results and detailed analysis are published in an accompanying research paper. Key findings include:
- Accuracy of AprilTag-based visual servoing for docking
- Stability characteristics of the threaded coupling mechanism
- Object manipulation stability under dual-robot control
- System robustness and repeatability metrics

## Key Files and Scripts

| File | Purpose |
|------|---------|
| `src/experiment2/experiment2.py` | Main docking and manipulation experiment |
| `src/imu_data/data_collect.py` | IMU sensor data collection |
| `src/imu_data/data_analysis.py` | IMU data processing and visualization |
| `src/experiment2/visualize_reference_path.py` | Plot robot trajectories |
| `src/experiment2/analyze_log.py` | Comprehensive experiment analysis |
| `src/lekiwi_controller/scripts/control_robot.py` | Robot teleoperation interface |

## Configuration

Robot parameters and experiment settings can be modified in:
- `src/lekiwi_controller/config/robot_config.yaml`
- `src/experiment2/config/experiment_config.yaml`
- `src/imu_data/config/imu_config.yaml`

## Dependencies

Core dependencies include:
- **LeRobot**: State-of-the-art robotics framework
- **ROS 2**: Robot Operating System
- **OpenCV**: Computer vision for AprilTag detection
- **PyTorch**: Machine learning framework
- **NumPy/Pandas**: Data processing and analysis

For complete dependency list, see `src/lerobot/setup.py`

## Contributing

This project builds upon the LeRobot framework from Hugging Face. To contribute improvements:

1. Follow the LeRobot contribution guidelines
2. Ensure all new code includes appropriate tests
3. Update documentation for new features
4. Submit pull requests with clear descriptions

## Citation

If you use this work in your research, please cite:

```bibtex
@thesis{khacnambn2024modular,
    title={Modular LeKiwi Robot: Autonomous Dual-Robot Docking and Collaborative Manipulation},
    author={Khac Nam B.N.},
    year={2024}
}
```

Also cite the original LeRobot framework:
```bibtex
@misc{cadene2024lerobot,
    author = {Cadene, Remi and Alibert, Simon and Soare, Alexander and Gallouedec, Quentin and Zouitine, Adil and Wolf, Thomas},
    title = {LeRobot: State-of-the-art Machine Learning for Real-World Robotics in Pytorch},
    howpublished = "\url{https://github.com/huggingface/lerobot}",
    year = {2024}
}
```

## License

This project extends LeRobot which is licensed under Apache License 2.0. See LICENSE files in respective directories.

## Acknowledgments

- Original LeRobot framework by Hugging Face
- LeKiwi robot platform development
- HTC Vive tracking system integration
- ESP32-S3 microcontroller support

## Contact & Support

For questions or issues related to this project:
- Create an issue on the GitHub repository
- Refer to the accompanying research paper for detailed methodology
- Check the LeRobot documentation for framework-specific questions

---

**Last Updated**: March 2026
**Status**: Research Project - Experimental
