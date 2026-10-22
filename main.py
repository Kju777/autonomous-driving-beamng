import socket
import struct

# Listen on all interfaces (including Tailscale) on port 4444
UDP_IP = "0.0.0.0"
UDP_PORT = 4444

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print(f"Listening for BeamNG telemetry on {UDP_IP}:{UDP_PORT}...")
    print("Drive the car on your PC to see live data! (Press Ctrl+C to stop)")

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            if len(data) >= 92:
                unpacked = struct.unpack('I4sHBBfffffffIIfff16s16si', data[:96])
                
                gear = unpacked[3]       # 0=R, 1=N, 2=1st, etc.
                speed_kmh = unpacked[5] * 3.6
                rpm = unpacked[6]
                throttle = unpacked[14] * 100
                brake = unpacked[15] * 100

                print(f"Speed: {speed_kmh:5.1f} km/h | RPM: {rpm:5.0f} | Gear: {gear-1} | Throttle: {throttle:3.0f}% | Brake: {brake:3.0f}%")

    except KeyboardInterrupt:
        print("\nTelemetry stream stopped.")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
