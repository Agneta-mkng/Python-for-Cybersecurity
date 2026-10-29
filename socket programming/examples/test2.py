import socket
import time

s = socket.create_connection(("127.0.0.1", 8080))
s.settimeout(15)

start = time.monotonic()
s.sendall(b"A" * 1500)

try:
    data = s.recv(1024)
    elapsed = time.monotonic() - start
    print(f"Server replied after {elapsed:.1f}s:", data.decode("UTF-8", errors="replace"))
except socket.timeout:
    print("No reply within 15 seconds.")

s.close()