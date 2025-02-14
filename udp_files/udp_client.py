import socket
import argparse

def main():
    # Set up command-line arguments to choose network address and port.
    parser = argparse.ArgumentParser(description="UDP Client for transmitting equipment codes and game control codes.")
    parser.add_argument('--network', type=str, default="127.0.0.1", help="Network address to send UDP messages to (default: 127.0.0.1)")
    parser.add_argument('--port', type=int, default=7500, help="UDP port to send messages to (default: 7500)")
    args = parser.parse_args()

    serverAddressPort = (args.network, args.port)
    bufferSize = 1024

    # Create a UDP socket for the client.
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    print("UDP Client started. Sending messages to {}:{}".format(args.network, args.port))
    print("Enter an integer equipment code or game control code (for example, 202 for game start, 221 for game end).")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("Enter code: ")
        if user_input.lower() == 'exit':
            print("Exiting UDP Client.")
            break
        try:
            # Validate input as an integer.
            code = int(user_input)
            message = str(code).encode()
            UDPClientSocket.sendto(message, serverAddressPort)
            print("Sent code {} to {}:{}".format(code, args.network, args.port))
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

if __name__ == '__main__':
    main()