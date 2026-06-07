import asyncio
import cv2
from ultralytics import YOLO
from mavsdk import System
from mavsdk.offboard import VelocityBodyYawspeed

# Proportional gain for rotation speed
Kp_yaw = 0.01 

async def run():
    # 1. Connect to Drone
    drone = System()
    print("Initializing MAVSDK Server...")
    
    # Use the specific IP that successfully connected for you
    await drone.connect(system_address="udpout://172.22.252.223:14580")
    
    print("Waiting for drone connection...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone connected!")
            break

    # Wait for the drone to establish a GPS lock AND pass pre-flight checks
    print("Waiting for drone to run pre-flight checks...")
    async for health in drone.telemetry.health():
        # Notice we added 'health.is_armable' to the requirements!
        if health.is_global_position_ok and health.is_home_position_ok and health.is_armable:
            print("Pre-flight checks passed! Drone is armable.")
            break

    # Arm and Takeoff
    print("Arming and taking off...")
    await drone.action.arm()
    await drone.action.takeoff()
    
    # Give the simulator 15 seconds to actually climb into the air
    print("Climbing to hover altitude...")
    await asyncio.sleep(15) 

    # Start Offboard mode
    print("Starting Offboard control...")
    await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
    await drone.offboard.start()

    # 2. Setup ML Pipeline
    model = YOLO('yolov8n.pt')
    cap = cv2.VideoCapture(0)

    print("Tracking Started. Stand in front of the camera!")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        
        frame_height, frame_width = frame.shape[:2]
        frame_center_x = int(frame_width / 2)
        frame_center_y = int(frame_height / 2)

        results = model(frame, classes=0, verbose=False)
        
        # 2.1. THE SAFETY BRAKES
        forward_speed = 0.0
        down_speed = 0.0
        yaw_speed = 0.0 
        
        target_found = False 

        for result in results:
            boxes = result.boxes
            if len(boxes) > 0:
                target_found = True 
                
                x1, y1, x2, y2 = boxes[0].xyxy[0].int().tolist()
                target_center_x = int((x1 + x2) / 2)
                target_center_y = int((y1 + y2) / 2)
                current_area = (x2 - x1) * (y2 - y1)

                # YAW CONTROL
                error_x = target_center_x - frame_center_x
                if abs(error_x) > 30:
                    yaw_speed = error_x * 0.25

                # ALTITUDE CONTROL 
                error_y = target_center_y - frame_center_y
                if abs(error_y) > 30:
                    down_speed = error_y * 0.01
                    down_speed = max(-1.0, min(0.5, down_speed))

                # DISTANCE CONTROL
                TARGET_AREA = 80000 
                error_area = TARGET_AREA - current_area
                if abs(error_area) > 15000:
                    forward_speed = error_area * 0.00002
                    forward_speed = max(-1.0, min(1.0, forward_speed))

                print(f"Yaw: {yaw_speed:.2f} | Alt: {down_speed:.2f} | Fwd: {forward_speed:.2f}")

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(frame, (target_center_x, target_center_y), 5, (0, 0, 255), -1)

        # 2. SEARCH MODE LOGIC
        # If the loop finishes and we saw nobody, execute the search sweep
        if not target_found:
            print("Target lost! Initiating search sweep...")
            yaw_speed = 15.0 # Rotate right at 15 deg/s to scan the room
            
        # 3. Send the movement command (Hover-Lock active: down_speed is forced to 0.0)
        await drone.offboard.set_velocity_body(
            VelocityBodyYawspeed(forward_speed, 0.0, 0.0, yaw_speed) # changed down_speed to 0.0 for hover-lock
        )
        
        cv2.imshow("Drone View", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
        await asyncio.sleep(0.01)

        cv2.imshow("Drone View", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
        await asyncio.sleep(0.01)

    # Cleanup and Land
    print("Stopping script. Landing drone...")
    await drone.offboard.stop()
    await drone.action.land()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(run())