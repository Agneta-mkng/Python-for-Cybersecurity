# Python TCP Socket
## TCP Socket Basics

A TCP socket can be created using:

socket.socket(socket.AF_INET, socket.SOCK_STREAM)


AF_INET → use IPv4 addressing.

SOCK_STREAM → create a stream socket, which uses TCP.

## TCP Server

A basic TCP server follows this general flow:

socket()
    ↓
bind()
    ↓
listen()
    ↓
accept()
    ↓
recv() / sendall()
    ↓
close()

1.bind()

Associates the server socket with an IP address and port.

`s.bind(("127.0.0.1", 8080))`
127.0.0.1 refers to the local machine.

2.listen()
Places the server socket into passive listening mode.

`s.listen(5)`
The 5 is the backlog value. It relates to pending connection requests waiting in the OS while the application is not calling accept().

> Important: The 5 does not mean that the server can only handle five clients.

3.accept()
Accepts an incoming connection:

`conn, address = s.accept()`

accept() returns:
***conn*** → a new connected socket used to communicate with the client.
***address*** → the client's address.

The original socket remains the listening socket.

## TCP Client

A basic TCP client follows this flow:

socket()
    ↓
connect()
    ↓
sendall() / recv()
    ↓
close()

The client connects to the server using:

`c.connect(("127.0.0.1", 8080))`

### Sending and Receiving Data

Network data is handled as bytes.
A Python string must be encoded before being sent:

`encoded_data = message.encode("UTF-8")`
`c.sendall(encoded_data)`

Received bytes can be decoded back into a Python string:

`received_data = c.recv(1024)`
`decoded_data = received_data.decode("UTF-8")`

**Basic Data Flow**
str
 ↓
encode()
 ↓
bytes
 ↓
sendall()
 ↓
TCP connection
 ↓
recv()
 ↓
bytes
 ↓
decode()
 ↓
str

recv()

Example:

`data = c.recv(1024)`

***recv(1024)*** attempts to receive up to 1024 bytes from the connected socket.
If recv() returns an empty bytes object:

`if not data:`
    `break`

It generally indicates that the other side has closed its connection.

### Encoding and Decoding Errors 

**UnicodeEncodeError**
Encoding a string can potentially raise a UnicodeEncodeError:

`try:`
    `encoded_data = message.encode("UTF-8")`
`except UnicodeEncodeError:`
    `print("Unable to encode the message as UTF-8")`

**UnicodeDecodeError**
Decoding received bytes can raise a UnicodeDecodeError if the bytes are not valid UTF-8:

`try:`
    `decoded_data = data.decode("UTF-8")`
`except UnicodeDecodeError:`
    `print("Received non-UTF-8 data")`

### SO_REUSEADDR
The following socket option can be used:

`s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)`
This allows the socket to reuse the address under conditions where the address might otherwise still be considered in use after the server closes.

This can help avoid:
Address already in use errors when restarting a server.

### Current Learning Observation

The current client sends data and then calls:

`server_response = c.recv(1024)`

The client will wait for a response because the current server only receives and prints the client's message; it does not send a response back.

Therefore, the client is waiting for data that the server never sends.

This will be addressed when implementing two-way client-server communication.




