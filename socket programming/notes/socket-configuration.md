# Socket Configuration

A socket has various settings that control its behavior.

 The `socket.setsockopt()` method is used to configure the options and modify the behavior of an active network socket, while `socket.getsockopt()` is used to inspect the current value of an option.

`socket.setsockopt()` accepts three parameters; level,option and value.

- Level - Identifies the socket or protocol subsystem that owns the option.
- Option - Identifies the specific behavior being configured.
- Value - specifies the value to assign to the option.

## Level

The **`level`** parameter identifies the socket or protocol subsystem that owns an option.

- `socket.SOL_SOCKET`:

*What it is*

SOL stands for Socket Option Level.This controls the generic behaviors of the socket interface itself, completely independent of the underlying network protocol (it works the same whether you use TCP, UDP, or Unix sockets).

*What it does*

It controls general socket behavior including things such as socket buffers, address reuse, and certain timeout-related settings.

*Common tasks it handles*

Port Management

Allowing multiple sockets to bind to the same port (`SO_REUSEADDR`).

Memory Allocations

Changing the size of the OS memory buffers allocated for incoming and outgoing data queues (`SO_RCVBUF`, `SO_SNDBUF`).

Timeouts 

Setting structural boundaries on how long a socket should block while waiting to send or receive data (`SO_RCVTIMEO`, `SO_SNDTIMEO`).

---

- `socket.IPPROTO_IP` or `socket.IPPROTO_IPV6`:

*What it is*

These levels are used for IP-layer options.

`IPPROTO_IP` is associated with IPv4, while `IPPROTO_IPV6` is associated with IPv6.

These options control aspects of how IP traffic is handled by the operating system

*What it does*

 They can configure characteristics of IP communication, including packet lifetime, multicast behavior, and other IP-level features.

*Common tasks it handles:*

Time-to-Live (TTL)

Sets the maximum number of router hops a packet can take before it is discarded (`IP_TTL`).

Multi-casting

Joining or leaving a specific multicast group so a server can broadcast data to multiple machines simultaneously (`IP_ADD_MEMBERSHIP`, `IP_DROP_MEMBERSHIP`).

Type of Service (ToS)

This is an 8-bit field embedded inside every single IP packet header.

Routers and other network devices may use these values to apply different traffic-handling policies, such as different queuing or forwarding behavior.

- `socket.IPPROTO_TCP`:

*What it is*

`IPPROTO_TCP` is used for TCP-specific socket options.

TCP operates at the transport layer and provides a connection-oriented, reliable byte stream.

These options are intended for TCP sockets and generally do not apply to UDP sockets.

*What it does*

It allows applications to fine-tune certain aspects of TCP behavior, including packet transmission, segment size, and connection keepalive behavior.

*Common tasks it handles:*

Data Bundling

 Disabling Nagle’s algorithm - which bundles tiny data packets in order to save bandwidth - to stop the OS from buffering small packets, forcing immediate delivery (`TCP_NODELAY`).

Maximum Segment Size (MSS)

The MSS represents the maximum amount of TCP payload data that can be carried in a TCP segment, excluding the TCP and IP headers.(`TCP_MAXSEG`).

Connection Probing

 This is a mechanism TCP uses to detect dead or half open connections. In case of anything and a client losses internet connection the server does not send a formal disconnect signal hence the socket remains open leaking system resources and memory.

When TCP keepalive is enabled, the operating system can use several variables to determine whether the remote endpoint is still reachable.

1. **`TCP_KEEPIDLE`**: The amount of time (in seconds) the connection must stay completely idle before the OS sends the first "probe" ping.
2. **`TCP_KEEPINTVL`**: The interval (in seconds) between subsequent probe pings if the first one gets no response.
3. **`TCP_KEEPCNT`**: The maximum number of failed probes allowed before the OS gives up, kills the connection, and throws an error.