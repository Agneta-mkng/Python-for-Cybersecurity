# Socket Programming

A socket is a software endpoint that enables two processes to communicate by sending and receiving data over a network or, in the case of Unix domain sockets, on the same machine.
socket.socket() creates and returns a socket object that can be used for network communication.

Socket programming enables processes running on different machines or same machines to communicate over a network using sockets as the communication endpoint.

### Python Socket Module

The python socket module provides an interactive low level network interface to the Berkeley sockets API.
Berkeley Sockets API is the standard programming interface that is used by most operating system for network communication.
 The primary methods in this module are;

- socket()
- .bind() - Binds a socket to a local address and port.
- .listen() - Prepares a server to receive incoming connection requests.
- .accept() - Accepts a pending client connection request and returns a new socket for communicating with that client.
- .connect() - Enables client to connect to a server.
- .connect_ex() - Similar to connect() but it returns an error indicator code instead of raising an exception when it fails.
- .send() -Sends data to a connected socket.
- .recv() - Receives bytes from a connected socket. If no data is available, it blocks by default until data arrives or the connection closes.
- .close() - Closes a socket and releases all resources associated with it.

Note

*Listen()*

Listen() only prepares the server to receive connection requests.This keeps the server in a passive state where it waits for clients.

It does not establish a connection with clients. It only prepares the socket to accept connections.

*Accept()*

The accept() method accepts an incoming connection request.
It returns:
- A new socket object used for communication with the client
- The client's address
The original server socket continues listening for additional connections.

### Socket families

Every socket is configured with an address family and a socket type, which determine how it communicates.

- Address family(AF) - Defines the addressing scheme and the network protocol.
- Socket type - Defines the communication method and transport protocol.

Python supports three address families;

1. AF_INET - Used for IPv4 addresses.
The address is represented as:
(host, port)

Example:
("192.168.1.10", 8080)

2.  AF_INET6 - Used for IPv6 addresses. 
A four tuple is used (host,port,flowinfo,scope_id).

3.   AF_UNIX - Used for Unix Domain Sockets (UDS).

UDS allows the OS to pass data directly from process to process, without going through the network stack.This is more efficient than using AF_INET, the only limitation is that it is restricted to processes on the same operating system because the filesystem is used as the namespace for addressing.

### Creating sockets

The socket class constructor creates new sockets.

The constructor accepts up to four parameters, though most programs specify only the address family and socket type.For example;

`socket.socket(socket.AF_INET, socket.SOCK_STREAM)`

1. Address family _ This includes AF_INET, AF_INET6 or AF_UNIX. Default is AF_INET.
2.  Socket type - Entails either SOCK_STREAM for TCP, SOCK_DGRAM for UDP. Default is SOCK_STREAM.
3. Protocol number - Usually left as 0 (zero), allowing the operating system to automatically choose the correct protocol for the selected address family and socket type.
4. File descriptor - An integer handle managed by the operating system that identifies an open file, socket, or other I/O resource. This parameter is rarely supplied directly by user programs.
---
## TCP sockets

A socket object is created using socket.socket()

The socket type is specified as socket.SOCK_STREAM for Transmission Control Protocol and socket.SOCK_DGRAM for User Datagram Protocol.

> TCP is a connection-oriented protocol that provides reliable communication by:
> 
- Guaranteeing packet delivery
- Delivering packets in order
- Detecting transmission errors
- Re-transmitting lost packets

### TCP socket lifecycle.
The lifecycle is split into two;the server side lifecycle and the client side lifecycle.

*1. Server-Side Lifecycle (passive open)*
The server sits in a listening state waiting for incoming connections.
1. socket () - Creates an endpoint for communication.
2. bind() - Assigns an IP address and port number to the socket.
3. listen() - Puts the socket into passive mode, allowing it to queue incoming connection requests.
4.  accept() - Blocks and waits for a client. When a client connects, it completes the **3-way handshake** (SYN —>SYN-ACK —>ACK) and creates a new **dedicated** socket strictly for that client's session. The original listening socket continues accepting additional clients.
5. recv() /send() - Reads data from the client and sends responses back.
6. close() - Initiates  connection tear down via the **4-way handshake** (FIN—>ACK—>FIN—>ACK).

*2. Client-Side Lifecycle (Active Open)*
The client reaches out to initiate a connection.
1. socket() - Creates the client socket.
2. connect() - Initiates the connection to the server's IP and port. This automatically triggers the **TCP 3-Way Handshake** .
3. send() / recv() - Sends requests to the server and receives incoming responses.
4. close()  - Closes the connection once data exchange is complete.

#### Why the Three-Way Handshake Is Important

The TCP three-way handshake:

- Confirms that both endpoints are reachable.
- Synchronizes sequence numbers.
- Establishes a reliable connection before data transfer begins.
- Ensures both the client and server are ready to exchange data.

---

##### Blocking Behavior

By default, sockets operate in **blocking mode**.

This means methods such as: accept(), recv() and connect() pause the program until the requested operation completes.

For example:

- accept() waits until a client connects.
- recv()  waits until data is available.
- connect() waits until a connection is established or fails.

Sockets can also be configured to operate in **non-blocking mode** or with **timeouts**, allowing programs to continue executing while waiting for network events.