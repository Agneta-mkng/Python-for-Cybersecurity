import socket

def client():
    address = ("127.0.0.1",8080)
    c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    c.connect(address)
    #connects to the listening server socket
    print(f"Successfully connected to the server on address: {address}")

    user_input = input("->")
    while user_input.strip().lower() != "bye":
        #convert the user input(string) into bytes before sending it over the network.
        try:
            encoded_data = user_input.encode('UTF-8')
        except UnicodeEncodeError:
            print("Unable to encode the message as UTF-8")
            user_input = input()
            continue
        c.sendall(encoded_data)

        # The client is expecting a response from the server. recv() returns response as bytes.
        # The current server only receives and prints the client's
        # message; it does not send a response yet.
        # This will be addressed when implementing two-way client-server communication.

        server_response = c.recv(1024)
        if not server_response:
            break

        #convert bytes received from the server back into string
        try:
            decoded_data = server_response.decode('UTF-8')
        except UnicodeDecodeError:
            print("Received non UTF-8 data from server")
            continue
        print(f"The data received from server is: {decoded_data}")

        user_input = input("->")
    c.close()
        



