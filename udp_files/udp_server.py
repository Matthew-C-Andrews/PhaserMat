import socket

def main():
    local_ip = "0.0.0.0"  # Listen on all available interfaces
    local_port = 7501
    buffer_size = 1024
    
    # Create and bind the UDP server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((local_ip, local_port))
    
    print(f"UDP server listening on {local_ip}:{local_port}")
    
    while True:
        data, addr = server_socket.recvfrom(buffer_size)
        message = data.decode("utf-8")
        print(f"Received message '{message}' from {addr}")
        
        # Optionally, send an acknowledgment or process the message further.
        # For now, we simply print the message.

if __name__ == "__main__":
    main()
