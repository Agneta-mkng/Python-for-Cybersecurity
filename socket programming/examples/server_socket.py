import socket

def server():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    address = ("127.0.0.1",8080)
    s.set_sockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR)
    s.bind(address)
        
    s.listen(5)
#when a sixth connection comes in,the queue is already full as server listens up to 5 connections. 
#The client may receive an error of ECONNREFUSE or if the protocol used allows for retransmission the request may
#be ignored so that a latter reattempt to connect is successful.

    conn,address = s.accept()
    print(f"Connection is received from {address}")
    while True:
        received_data = conn.recv(1024)
        if not received_data:
            break
        




    
    

