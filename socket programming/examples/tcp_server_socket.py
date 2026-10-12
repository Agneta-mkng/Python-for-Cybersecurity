import socket

def server():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    address = ("127.0.0.1",8080)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# Allow the socket to reuse the address after the server closes.
# This can help avoid "Address already in use" errors when restarting.

    s.bind(address)
        
# Start listening for incoming TCP connections.
# 5 is the backlog size: it limits the number of
# connection requests that can wait in the OS queue
# while the application is not calling accept().
#
# If the pending queue becomes full, additional connection
# attempts may be refused, dropped, or handled differently
# depending on the OS and networking conditions.
#
# Note: this does NOT limit the server to 5 total clients.
# This particular server accepts only one client because
# accept() is currently called once.
    s.listen(5)

    conn,address = s.accept()
    #accept() returns two values, a new socket object representing the estbalished connection and the client address.
    print(f"Connection is received from {address}")
    while True:
        received_data = conn.recv(1024)
    # recv() returns the received data as bytes.
    # Decode the bytes into a string so we can interpret it as text.

        if not received_data:
            break
        try:
            decoded_data = received_data.decode('UTF-8')
        except UnicodeDecodeError:
            print("Non UTF-8 data received.")
            continue
        print(f"The decoded data received is: {decoded_data}")

    conn.close()
    s.close()
    # s is the listening socket in this code while conn is the connected socket used to communicate with client
if __name__ == "__main__":
    server()
        




    
    

