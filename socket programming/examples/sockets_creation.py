"""
This program demonstrates two techniques for managing socket resources in Python:

1. Using the `with` statement (context manager), which automatically closes the socket (preferred).
2. Using `try...finally`, where the programmer explicitly closes the socket.

Both approaches ensure that socket resources are released properly.
"""

import socket


def ipv4_tcp_socket():
 # Using 'WITH' automatically closes the socket when the block exits,even if an exception occurs.
 #No explicit call to s.close()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #IPv4 expects two tuple format for the address,host and port
      address = ("127.0.0.1",8080)
      s.bind(address)

    print(f"The IPv4 tcp socket is bound to {address}")


def ipv4_udp_socket():
   # Using try...finally guarantees that the socket is closed even if an exception occurs.
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   try:
     address = ("127.0.0.1",9090)
     s.bind(address)
     print(f"The IPv4 udp socket created is bound to {address}")
   finally:
     s.close()


def ipv6_create_tcp():
    with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as st:
    #IPv6 uses four tuple format for address;host,port,flow_info and scope_id
      address = ("::1",8080,0,0)
      st.bind(address)
      print(f"The IPv6 tcp socket is bound to {address [0]} and port {address [1]}")


def ipv6_create_udp():
    st = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    try:
      address = ("::1",9090,0,0)
      st.bind(address)
      print(f"The IPv6 udp socket is bound to {address [0]} and port{address [1]}")
    finally:
      st.close()


#Example function call
ipv4_tcp_socket()