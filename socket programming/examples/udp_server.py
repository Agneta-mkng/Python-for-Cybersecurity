import socket

def udp_server():
    address = ("127.0.0.1",8080)
    u = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    try:
        u.bind(address)
        print(f"The server is running on address {address}")

        while True:
            received, client_address = u.recvfrom(1024)
            #recvfrom() return a tuple with two values, the received data and client address.
        
            try:
                decoded = received.decode('UTF-8')
            except UnicodeDecodeError:
                print("Received non-UTF data")
                continue

            print(f"Received the following data from the client: {decoded}")
            message = "Hello from the server."
            u.sendto(message.encode('UTF-8'),client_address)
    except KeyboardInterrupt:
        print("\nServer shutting down.")

    finally:
        u.close()
        print("socket closed")

if __name__ == "__main__":
    udp_server()
