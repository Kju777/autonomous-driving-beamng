import time
from beamngpy import BeamNGpy, Scenario, Vehicle

# 1. Network configuration
# If running BeamNG on a separate PC on your local network, enter its IP address (e.g. "192.168.1.xxx")
# If running locally on the same machine, leave as "127.0.0.1"
BEAMNG_HOST = "127.0.0.1"
BEAMNG_PORT = 25252

def main():
    print(f"Connecting to BeamNG instance at {BEAMNG_HOST}:{BEAMNG_PORT}...")
    bng = BeamNGpy(BEAMNG_HOST, BEAMNG_PORT)
    
    # Connect to the already running BeamNG process
    bng.open()
    print("Connected successfully!")

    # Reference the active ego vehicle (default vehicle ID usually 'ego')
    vehicle = Vehicle('ego_vehicle', model='etk800')
    bng.vehicles.connect(vehicle)

    try:
        while True:
            # Poll vehicle state
            vehicle.sensors.poll()
            state = vehicle.state
            
            pos = state['pos']
            vel = state['vel']
            speed_kmh = (vel[0]**2 + vel[1]**2 + vel[2]**2)**0.5 * 3.6

            print(f"Position: X={pos[0]:.2f}, Y={pos[1]:.2f}, Z={pos[2]:.2f} | Speed: {speed_kmh:.1f} km/h")
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nStopping telemetry stream.")
    finally:
        bng.disconnect()

if __name__ == "__main__":
    main()
