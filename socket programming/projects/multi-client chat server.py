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
import time

max_message_length = 1024
idle_timeout = 10
max_clients = 4
active_clients = 0
client_lock = threading.Lock()
max_messages = 5
rate_window = 1

def send_error(client_socket,text):
    try:
        client_socket.sendall((text + "\n").encode("UTF-8"))
    except OSError:
        pass

def handle_client(client_socket,address):
    global active_clients
    client_socket.settimeout(idle_timeout)
    print(f"Client connected on {address} ")
    message_buffer = b""
    message_count = 0
    window_start = time.monotonic()

    
    try:
        while True:          
            data = client_socket.recv(1024)
            
            if not data:
                break

            message_buffer += data
            # message_buffer holds the leftover data plus the latest chunk.
            # Data longer than one recv() call arrives in several chunks.

            while b"\n" in message_buffer:
                line,message_buffer = message_buffer.split(b"\n",1)
                #Split cuts at the first new line and returns two variables,the complete message and everything left after it

                #check 1 : A complete message that is too long
                if len(line) > max_message_length:
                    send_error(client_socket,"Error : message too long")
                    return 
                
                message = line.decode('UTF-8')
                
                now = time.monotonic()

                if now - window_start >= rate_window:
                # Rate limiting: allow at most max_messages per rate_window seconds.
                # If the current window has run out, start a new one and reset the count.
                    window_start = now
                    message_count = 0
    
                message_count += 1               

                if message_count > max_messages:
                    send_error(client_socket, "Error : Rate limit exceeded")
                    return
                
                if not message.strip():
                    send_error(client_socket,"Error : Message is empty")
                    continue

                if not message.isprintable():
                    send_error(client_socket,"Error : Message contains invalid characters")
                    continue

                print(f"Received the following from the client: {message}")
                response = f" {message}\n"
                client_socket.sendall(response.encode('UTF-8'))

            # check 2 : the remaining incomplete message is too long
            if len(message_buffer) > max_message_length:
                send_error(client_socket,"Error : Message too long")
                return

    except UnicodeDecodeError:
        print(f"Non-UTF 8 data received from {address}.")
        send_error(client_socket, "Error : Invalid message encoding")

    except socket.timeout:
        send_error(client_socket,"Error : Connection timed out")
        
    except OSError as e:
        print(f"Connection error with {address}:{e}")

    finally:
        client_socket.close()
        with client_lock:
            active_clients -=1

        print("The socket is closed.")

def server():
    global active_clients
    m = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    m.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    addr = ("127.0.0.1",8080)

    m.bind(addr)
    m.listen(5)
    print(f"Server is listening on {addr}")

    try:
        while True:
            client_socket,address = m.accept()
            with client_lock:
                if active_clients >= max_clients:
                    accepted = False
                else: 
                    active_clients +=1
                    accepted = True

            if not accepted:
                print(f"Rejected {address}: server full")
                send_error(client_socket, "Error : server is full")
                client_socket.close()
                continue

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





