# Autonomous Visual Target Tracking Drone 

**Hackathon Submission: Track A (Visual Target Tracking)**

A computer-vision-powered autonomous drone system that tracks and follows a human target in a 3D simulated environment without manual intervention. This project bridges perception and control by utilizing a lightweight object detection model running in real-time alongside a drone flight controller.

##  Features
* **Real-Time Object Detection:** Uses YOLOv8n to identify and lock onto human targets.
* **Dynamic Distance Control:** Automatically pitches forward or backward to maintain a safe tracking distance based on bounding box depth estimation.
* **Altitude Hover-Lock:** Maintains a stable 2.5m altitude to prevent ground collisions while tracking in 2D space.
* **Autonomous Search Sweep:** Automatically engages safety brakes and initiates a 360-degree rotational search sweep if the target is lost.

##  Tech Stack
* **Language:** Python 3.10+
* **AI & Computer Vision:** Ultralytics YOLOv8, OpenCV
* **Drone Control API:** MAVSDK-Python
* **Simulation Environment:** PX4 SITL, Gazebo Harmonic

##  Setup & Installation

**1. Start the Drone Simulator (Linux/WSL2)**
Open your Ubuntu terminal and bridge the network:
```bash
export PX4_SIM_HOST_ADDR=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}')
make px4_sitl gz_x500
