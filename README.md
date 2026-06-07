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
```
**2. Run the Autonomous Tracker (Windows)** 

**Open your Windows terminal** (PowerShell or VS Code), activate your Python virtual environment, and install the required dependencies:
 ```powershell
 pip install mavsdk ultralytics opencv-python
 ```

**Find the internal IP address of your WSL instance:**
```PowerShell
wsl -d Ubuntu-22.04 hostname -I
```

Update line 8 in autonomous_tracker.py with this IP address:
```Python
await drone.connect(system_address="udpout://<YOUR_WSL_IP>:14580")
```

**Run the tracker:**
```
PowerShell
python autonomous_tracker.py
```
## Demonstration Video
[**🎥 Click Here to Watch the Demo Video**](https://drive.google.com/file/d/11ein57lz1enEkYAUhtu6pH6mifdShMoF/view?usp=sharing)
The video demonstrates the drone taking off autonomously, tracking a moving person, maintaining distance, and executing a search sweep when the target is lost.
