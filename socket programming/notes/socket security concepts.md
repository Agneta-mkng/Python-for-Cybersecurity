# Socket Security Concepts
In this sub-topic,we are exploring security concepts that can be impelemented during socket programming.  

## Exposed services and Listening interfaces
**Listening interfaces**
An interface is a way that a computer connects to a network.    
A listening interface is any process actively waiting for incoming connection requests on a specific local IP address and port.  

 **Exposed service**
An exposed service is a network application or port accessible from outside its local machine or private network.
 
|Bind Address | Who can connect | Typical use |
|--|--|--|
| 127.0.0.1 | Only programs on the same machine | Development, local-only services, databases |
| A specific IP, e.g. 192.168.1.10	| Only devices that can reach that one interface | A server that should be reachable on one network only |
| 0.0.0.0 | Any device that can reach any of your interfaces	| Public-facing servers that are meant to accept outside connections|

```
server.bind("127.0.0.1",8080) #local connection only  
server.bind("0.0.0.0",8080)  #All interfaces  
```  
## Why it matters
A service reachable from anywhere can be probed by anyone who can reach it.  
If the service has a bug, no authentication, or weak input handling, that exposure can become a real vulnerability.  
- Example: a development server bound to `0.0.0.0` on public Wi-Fi can be reached by strangers on the same network.
- Firewalls and routers can reduce exposure, but binding correctly is the first line of defence.

## Principle: least exposure
Bind to the narrowest address that does the job. Use `127.0.0.1` for local-only services. Use `0.0.0.0` only when outside access is needed, and then add input validation, resource limits, authentication, and TLS.  

## My experiment

```bash
ss -tlnp
```    

**Bind address in my chat server:** ("127.0.0.1",8080)

***Output of `ss -tlnp` for port 8080:***
```
State   Recv-Q  Send-Q  Local Address:Port  Peer Address:Port  Process
LISTEN  0       5       127.0.0.1:8080      0.0.0.0:*          users:(("python3",pid=13931,fd=3))
```

**After changing the bind address to ("0.0.0.0",8080):**
```
LISTEN  0  5  0.0.0.0:8080  0.0.0.0:*  users:(("python3",pid=15606,fd=3))
```

**What I observed:** 

## What I learned



