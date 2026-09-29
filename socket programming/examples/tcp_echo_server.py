"""
TCP Echo Server

This server receives data from a TCP client and sends the same data back to the client.

How to run:
1. Open Terminal 1 and start the server:
   python3 tcp_echo_server.py

2. Open Terminal 2 and start the client:
   python3 tcp_client_socket.py

3. Type messages in the client to test the echo functionality.

4. Press Ctrl+C in the terminal running each program to stop it.
"""

import socket

def echo_server():
    e = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    address = ("127.0.0.1",8080)

    e.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    e.bind(address)
    e.listen(5)
    print(f"the echo server is listening for connections on address: {address}")

    conn,address=e.accept()
    print(f"Connection is received from {address}")
    while True:
        received = conn.recv(1024)

        if not received:
            break
        # We do not necessarily need to decode the data in order to echo it back to client
        # In the previous TCP server, the data was only received and printed.
        # This server implements echo functionality by sending the same data
        # back to the client after receiving it. "received" is already a bytes
        # object, so it can be sent directly through the connected socket without decoding it.

        conn.sendall(received)

    conn.close()
    e.close()

if __name__ == "__main__":
    echo_server()


