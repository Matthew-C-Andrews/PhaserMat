import sys
import socket

def main():
    # Default values: listen on all interfaces, port 7501
    local_ip = "0.0.0.0"
    local_port = 7501

    # Check command-line arguments:
    # Usage: python3 udp_server.py [listening_ip] [port]
    if len(sys.argv) > 1:
        local_ip = sys.argv[1]
    if len(sys.argv) > 2:
        try:
            local_port = int(sys.argv[2])
        except ValueError:
            print("Port must be an integer.")
            sys.exit(1)

    buffer_size = 1024
    # Create and bind the UDP server socket
    UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPServerSocket.bind((local_ip, local_port))
    print(f"UDP server listening on {local_ip}:{local_port}")

    while True:
        data, addr = UDPServerSocket.recvfrom(buffer_size)
        message = data.decode("utf-8")
        print(f"Received message '{message}' from {addr}")

if __name__ == "__main__":
    main()
