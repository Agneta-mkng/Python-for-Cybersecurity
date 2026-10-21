# Introduction
In the previous topic,the Python socket module has been used to establish communication between the client and the server.  
A basic sequential server is meant to handle one client at a time which becomes a limitation because other clients have to wait while the server communicates with the first client.  
The existing TCP server will be modified so that it can communicate with several clients at a time.
The main issues handled are: blocking operations,concurrency,threading and client management.  

# Blocking operations
A blocking operation is one that causes the calling thread to wait until the operation completes or required event occurs.  
In Python socket programming some socket operations are blocking by default.They include `accept()` and `recv()`.    
A single threaded server that handles one client at a time inside a blocking receive loop cannot be able to actively accept and handle another client until it returns to accepting connections.  
The pending connection might be waiting in the operating system's connection queue but the server application has not accepted it yet.  

# Concurrency
Concurrency is handling multiple tasks at the same time by overlapping their execution periods instead of finishing one task before starting the next one.   
Depending on the implementation and available resources,the tasks can be executed in parallel or even take turns in being executed.   
In concurrency,multiple tasks make progress during overlapping periods while in parallelism,multiple tasks execute simultaneously, typically on different CPU cores 


## Sequential handling vs concurrency handling  

|Sequential handling| Concurrency handling|  
|---|---|
|Tasks are handled one after the other | Multiple tasks can be handled during overlapping periods |  
|One task may delay the handling of the other| A waiting task does not prevent other tasks from making progress.|  
|A basic single-client server exhibits this behaviour| A threaded server exhibits this behaviour|  
  
  
Concurrency can be handled in many ways including threading and asynchronous programming.

## Threading  
A new thread is created for each accepted connection using Python's threading module. Each thread can communicate with its assigned client independently.  
Each accepted connection,a worker thread is created and started. The thread can be configured as a daemon thread so that it does not prevent the interpreter from exiting when only daemon threads remain.  
The server operates using two main components:
1. Main thread - This is responsible for accepting incoming connections.
2. Worker threads - These handle communication with individual assigned clients.  

Each worker thread works independently,hence a blocking operation in one worker thread does not prevent other worker threads from executing.  
A thread is created using `threading.Thread()` which accepts the following arguments:

|Parameter |Type |Default | Description|
|--|--|--|--|
|**group**| None | None | Reserved for future extension.|
|**target**| Callable | None | Invoked by `run()` method |
|**name** | String | None |  This is the thread name. By default, a unique name is constructed of the form “Thread-N” where N is a small decimal number. |
|**args** | Tuple | () | A tuple of positional arguments to pass to the target function. |
|**kwargs** | Dictionary | {} | A dictionary of keyword arguments to pass to the target function. |
|**daemon** | Boolean | Inherited from the creating thread. | Determines whether the thread is a daemon thread |

#### Advantages of threading
- ***Improved responsiveness***: A client waiting for data does not necessarily prevent other clients from being served.
- ***Concurrent communication***: Multiple clients can send and receive data during overlapping periods.
- ***Simpler implementation***: Each worker thread can use a straightforward blocking communication loop.
- ***Isolation of client handling***: Each client can have its own socket and worker function, reducing interference between individual communication loops.  

#### Disadvantages of threading
- High resource consumption especially when a large number of threads is created.  
- Shared data accessed by multiple threads may require synchronization to prevent race conditions.  
- Thread creation and management overhead.


### Daemon threads  
This is a background thread that does not prevent the  Python interpreter from exiting when only daemon threads remain.  
In a multi-client server,a worker thread can be created as a daemon thread by setting `daemon = True` .  
Daemon threads are useful when background tasks should not keep the application running indefinitely. They may however be terminated abruptly when the interpreter shuts down.  
For this reason, applications that require reliable cleanup of client connections may use non-daemon threads and implement a controlled shutdown procedure.  

## Client management
This involves controlling the lifecycle of client connections. The multi-client server must manage each connection correctly to ensure that resources are released when no longer needed.  
1. In a multi-client server, the main thread accepts the connection and passes the resulting client socket to a worker thread.  
2. Each accepted connection can be assigned to a separate handler function.The handler function manages communication with its assigned client by receiving incoming data, processing requests, and sending responses.  
3. The server handles normal and unexpected disconnetions.
4. The server should close the client socket once communication is accomplished using `socket.close()` to release resources associated with that connection.  
5. Each client connection has its own socket and handler thread.







