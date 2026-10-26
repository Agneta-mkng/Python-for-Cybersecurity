import socket

s = socket.create_connection(("127.0.0.1", 8080))
s.settimeout(3)
s.sendall(b"A" * 3000)

try:
    while True:
        reply = s.recv(1024)
        if not reply:
            break
        print(f"Reply chunk: {len(reply)} bytes")
except socket.timeout:
    pass

s.close()