# Wireshark: Multi-Client Chat Server Capture

## Goal
To see what my threaded TCP chat server looks like on the network, using Wireshark to observe connections and messages between the server and two clients.

## Setup
- **Tool:** Wireshark 4.2.2 on Ubuntu.
- **Interface:** `lo` (loopback), since the server and clients run on the same machine.
- **Server port:** 8080
- **Display filter:** `tcp.port == 8080`
- **Clients:** 2 clients connected to the server.
- **Capture file:** `wireshark-captures/chat-server-2-clients.pcapng`

## What I observed

### TCP handshake
When a client connected, the first three packets were the TCP three-way handshake:
1. `[SYN]`: the client asks to connect.
2. `[SYN, ACK]`: the server accepts.
3. `[ACK]`: the client confirms, and the connection is established.

### Messages
Each message I typed appeared as a `[PSH, ACK]` packet with a data length greater than zero. Clicking the packet showed my message in plaintext in the packet bytes pane (bottom right).

### Plaintext traffic
Anyone able to capture this traffic could read the messages, because my chat server does not encrypt anything.

Each client's messages appeared in the capture, and each connection used a different client port while the server stayed on 8080. Port number 52684 for client A and port number 55672 for client B as shown in Statistics→ Conversations. 


## Next steps
- Add broadcasting to the server, then capture again to see the server forward messages between clients
- Capture a client disconnecting and compare it with a client being killed abruptly
- Add TLS later and compare the capture with this plaintext one