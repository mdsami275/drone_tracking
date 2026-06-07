import asyncio
from mavsdk import System

async def run():
    # 1. Initialize the drone object
    drone = System()
    
    # 2. Connect to the simulator (default UDP port for PX4 SITL is 14540)
    print("Connecting to the simulator...")
    await drone.connect(system_address="udp://:14540")

    # Wait until the connection is established
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("-- Successfully connected to the drone!")
            break

    # 3. Check if the drone has a GPS lock (required for takeoff)
    print("Waiting for GPS lock...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- GPS lock acquired!")
            break

    # 4. Execute Flight Commands
    print("Arming the motors...")
    await drone.action.arm()

    print("Taking off...")
    await drone.action.takeoff()

    # Let it hover in the air for 10 seconds
    print("Hovering...")
    await asyncio.sleep(10)

    print("Landing...")
    await drone.action.land()

if __name__ == "__main__":
    # Start the asynchronous event loop
    asyncio.run(run())