# Introduction
In the previous topic,the python socket module has been used to establish communication between the client and the server.  
A basic server is meant to handle one client at a time which becomes a limitation because other clients have to wait while the server communicates with the first client.  
The existing TCP server will be modified so that it can communicate with several clients at a time.
The of the issues handled are: blocking operations,concurrency,threading anf client management.  

# Blocking operations.  
A blocking operationis one that stops the program and forces it to wait for the operation to finish before continuing.  
In Python socket programming some socket operations are blocking by default.They include `accept()` and `recv()`.  
A single threaded server that handles one client at a time inside a blocing receive loop cannot be able to actively accept and handle another client until it returns to accepting connections.  
The pending connection might be waiting in the operating system's connection queue but the server application has not accepted it yet.  

# Concurrency
Concurrency is handling multiple tasks at the same time by overlapping their execution periods instead of finishing one task before starting the next one.  

## Sequential handling vs concurrency handling  

|Sequential handling| Concurrency handling|  
|---|---|
|Tasks are handled one after the other | Multiple tasks can be handled during overlapping periods |  
|One tadk may delay the handling of the other| A waiting task does not prevent other tasks from running|  
|A basic single client server exhibits this behaviour| A threaded server exhibits this behaviour|  

Concurrency can be handled using threading and asynchronous programming.


