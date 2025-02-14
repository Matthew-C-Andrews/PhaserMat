import socket
import argparse

def parse_message(message):
    """
    Attempt to decode the received message as either a single integer or
    a pair of integers in 'int:int' format.
    """
    try:
        decoded = message.decode().strip()
        if ':' in decoded:
            parts = decoded.split(':')
            if len(parts) == 2:
                return (int(parts[0]), int(parts[1]))
            else:
                return decoded
        else:
            return int(decoded)
    except Exception:
        return decoded

def main():
    parser = argparse.ArgumentParser(description="UDP Server for receiving equipment codes and game messages.")
    parser.add_argument('--ip', type=str, default="127.0.0.1", help="Local IP address to bind the UDP server (default: 127.0.0.1)")
    parser.add_argument('--port', type=int, default=7501, help="UDP port to bind the server (default: 7501)")
    args = parser.parse_args()

    localIP = args.ip
    localPort = args.port
    bufferSize = 1024

    # Create the UDP socket for the server.
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Bind the socket to the provided IP address and port.
    UDPServerSocket.bind((localIP, localPort))
    print("UDP Server up and listening on {}:{}".format(localIP, localPort))

    while True:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        parsed_message = parse_message(message)
        print("Received message from {}: {}".format(address, parsed_message))

if __name__ == '__main__':
    main()