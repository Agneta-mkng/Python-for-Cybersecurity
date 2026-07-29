# Socket Programming

Socket is an endpoint used to send and receive data across a network hence allows for Inter process Communication(IPC).

Socket programming enables processes running on different machines or same machines to communicate over a network using sockets as the communication endpoint.

### Python Socket Module

The python socket module provides an interactive low level network interface to the Berkeley sockets API.

 The primary methods in this module are;

- socket()
- .bind() - Binds a socket to a local address and port.
- .listen() - Prepares a server to receive incoming connection requests.
- .accept() - Enables the server to connect to a client connection request.
- .connect() - Enables client to connect to a server.
- .connect_ex() - Similar to connect() but it returns an error instead of raising an exception when it fails.
- .send() -Sends data to a connected socket.
- .recv() - Receives data from a connected socket.
- .close() - Closes a socket and releases all resources associated with it.

Note

*Listen()*

Listen() only prepares the server to receive connection requests.this keeps the server in a passive state where it waits for clients.

It does not establish a connection with clients. It only prepares the socket to accept connections.

*Accept()*

The accept() method accepts an incoming connection request.
It returns:
- A new socket object used for communication with the client
- The client's address
The original server socket continues listening for additional connections.

### Socket families

Sockets have two properties controlling how they send data.

- Address family(AF) - Defines the addressing scheme and the network protocol.
- Socket type - Defines the communication method and transport protocol.

Python supports three address families;

1. AF_INET - Used for IPv4 addresses.
The address is represented as:
(host, port)

Example:
("192.168.1.10", 8080)

b.  AF_INET6 - Used for IPv6 addresses. 
A four tuple is used (host,port,flowinfo,scope_id).

c.   AF_UNIX - Used for Unix Domain Sockets (UDS).

UDS allows the OS to pass data directly from process to process, without going through the network stack.This is more efficient than using AF_INET, the only limitation is that it is restricted to processes on the same operating system because the filesystem is used as the namespace for addressing.