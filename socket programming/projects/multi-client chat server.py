'''
In this implementation we are using the threading module 
to handle multiple clients connections concurrently.

The existing TCP client program will be reused to test the server.

To execute this program:
1. Open terminal and run the multi-chat server. 
2. Open other instances in terminal and run the client code.
'''

import socket
import threading

def handle_client(client_socket,address):
    print(f"Client connected on{address} ")

    try:
        while True:          
            data = client_socket.recv(1024)
            
            if not data:
                break

            message = data.decode('UTF-8')
            print(f"Received the following from the client {message}")
            response = f" {message}"

            client_socket.sendall(response.encode('UTF-8'))

    except UnicodeDecodeError:
        print("Non-UTF 8 data received.")
        try:
            client_socket.sendall(b"Error:invalid message encoding")
        except OSError as e:
            pass 
        
    except OSError as e:
        print(f"Connection error with {address}:{e}")

    finally:
        client_socket.close()
        print("The socket is closed.")

def server():
    m = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    m.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    addr = ("127.0.0.1",8080)

    m.bind(addr)
    m.listen(5)
    print(f"Server is listening on {addr}")

    try:
        while True:
            client_socket,address = m.accept()
            thread = threading.Thread(
                target = handle_client,
                args = (client_socket,address),
                daemon = True
            )
            #Start the worker thread so that handle_client can execute.
            thread.start()

    except KeyboardInterrupt:
        print("The server is shutting down.")

    finally:
        #The listening socket m is kept open for the lifetime of the server and only closes when the server shuts down.
        m.close()

if __name__== "__main__":
    server()





