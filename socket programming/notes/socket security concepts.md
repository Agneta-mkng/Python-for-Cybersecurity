# Socket Security Concepts
In this sub-topic,we are exploring security concepts that can be implemented during socket programming.  

## Exposed services and Listening interfaces
**Listening interfaces**
A listening interface is the network interface (identified by its IP address) on which a server waits for incoming connections.  
 The address passed to bind() decides which interfaces accept connections.  

**Exposed service**
An exposed service is a network application or port accessible from where it should not be accessible from.
|Bind Address | Who can connect | Typical use |
|--|--|--|
| 127.0.0.1 | Only programs on the same machine | Development, local-only services, databases |
| A specific IP, e.g. 192.168.1.10	| Only devices that can reach that one interface | A server that should be reachable on one network only |
| 0.0.0.0 | Any device that can reach any of your interfaces	| Public-facing servers that are meant to accept outside connections|

```python
server.bind(("127.0.0.1",8080)) #local connection only  
server.bind(("0.0.0.0",8080))  #All interfaces  
```  
### Why it matters
A service reachable from anywhere can be probed by anyone who can reach it.  
If the service has a bug, no authentication, or weak input handling, that exposure can become a real vulnerability.  
- Example: a development server bound to `0.0.0.0` on public Wi-Fi can be reached by strangers on the same network.
- Firewalls and routers can reduce exposure, but binding correctly is the first line of defence.

### Principle: least exposure
Bind to the narrowest address that does the job. Use `127.0.0.1` for local-only services. Use `0.0.0.0` only when outside access is needed, and then add input validation, resource limits, authentication, and TLS.  

### My experiment

```bash
ss -tlnp
```    
t = TCP, l = listening, n = numeric, p = process.”  

**Bind address in my chat server:** ("127.0.0.1",8080)  
The output becomes;  

```
State   Recv-Q  Send-Q  Local Address:Port  Peer Address:Port  Process
LISTEN  0       5       127.0.0.1:8080      0.0.0.0:*          users:(("python3",pid=13931,fd=3))
```

**After changing the bind address to ("0.0.0.0",8080):**
```
LISTEN  0  5  0.0.0.0:8080  0.0.0.0:*  users:(("python3",pid=15606,fd=3))
```

**What I observed:**   
With the server address set to 0.0.0.0 , 8080 and the client address set to 127.0.0.2,8080 the connection is successful.  
When the bind address for the server is changed back to 127.0.0.1,8080 and that of the client changed to 127.0.0.2,8080,a ConnectionRefusedError is raised.

### What I learned
When the server is bound to 0.0.0.0, it listens on all of the machine’s addresses and accepts connections to any of them. When it is bound to 127.0.0.1, it only accepts connections to that loopback address. A client connecting to any other address of the same machine gets ConnectionRefusedError.

## Input validation
This is the process of checking external data against a set of predefined rules before the server can process it.  
Unchecked input can crash a thread, confuse the server, or open the way to worse problems.  
**Checks for a chat server**
- Encoding: is the data valid UTF-8?
- Length: is the message too long?
- Content: is it empty or full of unexpected characters?
- Format: does it follow the format the server expects?

### Check 1: Encoding

**The problem**  
`recv()` returns bytes, and `decode('UTF-8')` turns them into text. If the bytes aren't valid UTF-8, `decode()` raises `UnicodeDecodeError`.

**Prediction vs. result**  
My original chat server did not handle this error. `UnicodeDecodeError` is a subclass of `ValueError`, not `OSError`, so `except OSError` doesn't catch it. The exception escaped `handle_client`, the `finally` block closed that client's socket, and only that client's thread ended. The server itself kept running.

**Text vs. bytes (a lesson from testing)**  
Typing `\xff\xfe\xfd` into my client sent the *text* of those characters, which is valid UTF-8. The client turns typed input into a string, so it can't send raw invalid bytes. To send real bytes, I used a separate script that calls `sendall()` with a bytes literal (`b"\xff\xfe\xfd"`).

**Test script**
```python
import socket

s = socket.create_connection(("127.0.0.1", 8080))
s.settimeout(3)
s.sendall(b"\xff\xfe\xfd")

try:
    reply = s.recv(1024)
    print("Server replied:", reply.decode("UTF-8", errors="replace"))
except socket.timeout:
    print("No reply received.")

s.close()
```

**Bugs I hit while testing**

- A missing backslash in the test bytes.    
I wrote `b"xff\xfe\xfd"` instead of `b"\xff\xfe\xfd"`. The error message gave it away:  

```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xfe in position 3: invalid start byte
```

I expected the error to name byte `0xff` at position 0, since that was meant to be the first invalid byte. Instead it named `0xfe` at position 3. Without the backslash, `xff` was sent as three plain characters (`x`, `f`, `f`) in positions 0 to 2, which are valid UTF-8. The first invalid byte was therefore `0xfe`, in position 3.

**Lesson:**   
The byte value and position in a `UnicodeDecodeError` show exactly where decoding failed, so they can be compared with what was meant to be sent.

- The server code had been edited but not restarted, so the old code was still running.
- The test script closed the connection without reading, so it never received the server's reply.  

| | Bytes sent | First invalid byte |
|---|---|---|
| Intended | `\xff \xfe \xfd` | `0xff` at position 0 |
| Actual (typo) | `x f f \xfe \xfd` | `0xfe` at position 3 |

**The fix on the server**
```python
except UnicodeDecodeError:
    print(f"Non-UTF-8 data received from {address}.")
    try:
        client_socket.sendall(b"Error: invalid message encoding.\n")
    except OSError:
        pass
```  

The inner `try/except` handles the case where the client has already disconnected.

**Design decision**  
When a client sends invalid data, the server replies with an error message and then disconnects the client (the `finally` block closes the socket).   
Alternatives were to ignore the message or to keep the connection open. Disconnecting rejects a misbehaving client. Rate limiting may be added later to handle repeated bad input.

**Result**  
Server replied: Error:invalid message encoding.  

### Check 2: Message length
