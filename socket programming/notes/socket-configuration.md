# Socket Configuration

A socket has various settings that control its behavior.

 The `sock.setsockopt()` method is used to configure the options and modify the behavior of an active network socket, while `sock.getsockopt()` is used to inspect the current value of an option.  

 ```python
 value = sock.getsockopt( 
    socket.SOL_SOCKET,  
    socket.SO_REUSEADDR
)
print(value)
```


`sock.setsockopt()` accepts three parameters; level,option and value.
`sock.setsockopt(level,option,value)`

- Level - Identifies the socket or protocol subsystem that owns the option.
- Option - Identifies the specific behavior being configured in the sub-sytem.
- Value - specifies the value to assign to the option.  
Using the analogy of a company we can illustrate these three parameters as;  
***Level*** = department
***Option*** = the specific setting/behavior in that department
***Value*** = Specifies the value of that setting to be.  

## Level

The **`level`** parameter identifies the socket or protocol subsystem that owns an option.

- `socket.SOL_SOCKET`:

*What it is*

SOL stands for Socket Option Level.This controls the generic behaviors of the socket interface itself, completely independent of the underlying network protocol (it works the same whether you use TCP, UDP, or Unix sockets).

*What it does*

It controls general socket behavior including things such as socket buffers, address reuse, and certain timeout-related settings.

*Common tasks it handles*

1. Port Management

Allowing multiple sockets to bind to the same port (`SO_REUSEADDR`).

2. Memory Allocations

Changing the size of the OS memory buffers allocated for incoming and outgoing data queues (`SO_RCVBUF`, `SO_SNDBUF`).

3. Timeouts 

Setting structural boundaries on how long a socket should block while waiting to send or receive data .

---

- `socket.IPPROTO_IP` or `socket.IPPROTO_IPV6`:

*What it is*

These levels are used for IP-layer options.

`IPPROTO_IP` is associated with IPv4, while `IPPROTO_IPV6` is associated with IPv6.

These options control aspects of how IP traffic is handled by the operating system.

*What it does*

They can configure characteristics of IP communication, including packet lifetime, multicast behavior, and other IP-level features.

*Common tasks it handles:*

1. Time-to-Live (TTL)

Sets the maximum number of router hops a packet can take before it is discarded (`IP_TTL`).

2. Multi-casting

Joining or leaving a specific multicast group so a server can multicast data to multiple machines simultaneously in that specific group.(`IP_ADD_MEMBERSHIP`, `IP_DROP_MEMBERSHIP`).

3. Type of Service (ToS)

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

1. Data Bundling

Disabling Nagle’s algorithm - which combines small outgoing data packets to reduce the number of small TCP segments - to allow for small writes to be sentwithout waiting for Nagle's algorithim to combine them (`TCP_NODELAY`).

2. Maximum Segment Size (MSS)

The MSS represents the maximum amount of TCP payload data that can be carried in a TCP segment, excluding the TCP and IP headers.(`TCP_MAXSEG`).

3. Connection Probing

TCP keepalive allows the operating system to periodically probe an otherwise idle TCP connection to determine whether the remote endpoint is still responsive. This can help detect connections where the peer has become unreachable without performing a normal TCP connection shutdown.

1. **`TCP_KEEPIDLE`**: The amount of time (in seconds) the connection must stay completely idle before the OS sends the first "probe" ping.
2. **`TCP_KEEPINTVL`**: The interval (in seconds) between subsequent probe pings if the first one gets no response.
3. **`TCP_KEEPCNT`**: The maximum number of failed probes allowed before the OS gives up, kills the connection, and throws an error.
  

## Option
This parameter identifies the specific socket behaviour we want to configure.
There are so many options based on different levels.

1. General socket options (`sock.SOL_SOCKET`)

They include;

socket.SO_REUSEADDR  
This specifies whether a socket can reuse an address based on conditions set by the underlying operating system such as restarting a server. 
For example,in the code below address reuse is enabled by setting the value to 1.
```python 
        sock.setsockopt( 
           socket.SOL_SOCKET,  
           socket.SO_REUSEADDR,  
           1 
        )
 ```       

socket.SO_RCVBUF  
This is used to set the socket's receive buffer size.
**NOTE:** We are still using the general socket level in the example below and 65536 is the requested receive buffer size in bytes.
```python
        sock.setsockopt( 
           socket.SOL_SOCKET,  
           socket.SO_RCVBUF,  
           65536  
        )
```

socket.SO_SNDBUF  
This is used to set the send buffer size.
```python
        sock.setsockopt( 
           socket.SOL_SOCKET,  
           socket.SO_SNDBUF,  
           65536  
        )
```

2. IP options (`socket.IPPROTO_IP`)
socket.IP_TTL  
socket.IP_ADD_MEMBERSHIP  
socket.IP_DROP_MEMBERSHIP  

3. TCP options (`socket.IPPROTO_TCP`)  
socket.TCP_NODELAY  
This is used to disable Nagle's algorithim hence small data packets can be delivered without any delay. 
```python 
        socket.setsockopt(
           socket.IPPROTO_TCP,  
           socket.TCP_NODELAY,
           1
        )
``` 

socket.TCP_KEEPIDLE  
From the example below,the keepidle time is set to 60 seconds before the first probe is made.  
```python
       sock.setsockopt(  
           socket.IPPROTO_TCP,  
           socket.TCP_KEEPIDLE,  
           60  
        ) 
```

socket.TCP_KEEPINTVL  
the time interval between keepalive probes is 10 seconds.  
```python
        sock.setsockopt( 
           socket.IPPROTO_TCP,  
           socket.TCP_KEEPINTVL,  
           10 
        )
``` 

socket.TCP_KEEPCNT  
The count is set to 5,so after five failed probes the connection is considered dead. 
```python 
        sock.setsockopt( 
           socket.IPPROTO_TCP,  
           socket.TCP_KEEPCNT,  
           5  
        )
```

## Value
This parameter specifies the setting we want to assign to the selected option.  
The different value types that cabe used include:  

1. Boolean values  
These values are used for socket options that have an on/off switch states.   
0 is used to disable and 1 to enable some of these socket options such as SO_REUSEADDR.  

2. Numeric values
These values represent a quantity for example the buffer size we specifies previously for the receive and send buffer.  

3. Time related values  
These are used for options that require a time period for example TCP_keepalive.


















