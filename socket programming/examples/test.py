import socket

s = socket.create_connection(("127.0.0.1", 8080))
s.settimeout(3)
s.sendall(b"hi\n" * 20)

try:
    while True:
        data = s.recv(1024)
        if not data:
            break
        print(data.decode("UTF-8", errors="replace"), end="")
except socket.timeout:
    pass

s.close()