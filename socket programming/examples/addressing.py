import socket

host=input("Enter the host name")
port=input("Enter the port number")

def get_address_info():
    address=socket.getaddrinfo(host,port)
    # getaddrinfo() provides more general address information,
    # including IPv4/IPv6 and connection-related details.

    print(f"Complete address list returned by getaddrinfo() : {address}")
    print()
    print(f"Type of the complete getaddrinfo() : {type(address)}")
    print(f"Type of the first entry in the result : {type(address[0])}") 
    print(f"The first tuple returned by getaddrinfo() : {address[0]}") 
    print(f"The IP address from the first tuple : {address [0] [4] [0]} ")
    return (address [0] [4] [0])

def forward_dns_lookup():
    print(f"Getting ip address using the host name {host} gives: {socket.gethostbyname(host)}")
    resolved=socket.gethostbyname_ex(host)
    # gethostbyname() returns a single IPv4 address as a string, while gethostbyname_ex() returns a tuple containing the hostname, aliases, and a list of IPv4 addresses.
    print(resolved)
    print(f"Address one: {resolved [2] [0]}")
    print(f"Address two: {resolved [2][1]}")
    
def reverse_dns_lookup(ip):
    #Hardcoded reverse lookup
    print(socket.gethostbyaddr("8.8.8.8"))
    print("Successful reverse dns lookup")

    #Interactive reverse dns lookup
    user_ip=input("Enter a IP address")
    print(socket.gethostbyaddr(user_ip))

    print(f"IP being looked up: {ip}")
    print(socket.gethostbyaddr(ip)) #This reverse dns lookup is unsuccessful

    # Error handling:
# socket.gethostbyaddr() can raise socket.herror when a reverse DNS record cannot be found.

# Later, handle this with:
# try:
#     socket.gethostbyaddr(ip)
# except socket.herror:
#     print("Reverse DNS lookup failed.")

# I am intentionally leaving error handling out for now so 
#I can first understand how the DNS functions behave when they succeed
#and when they fail.


def get_fqdn():
    print(socket.getfqdn(host))
    #When no argument is provided, getfqdn() uses the local machine's hostname as the starting point for determining the FQDN.


ip_address=get_address_info()  
forward_dns_lookup() 
reverse_dns_lookup(ip_address)
get_fqdn()






    
    
    


