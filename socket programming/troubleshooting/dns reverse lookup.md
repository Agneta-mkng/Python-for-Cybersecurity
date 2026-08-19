# Issue: gethostbyaddr() returned "Unknown host"

### What I was trying to do
The host name was example.com and the port number 8080. 

I wanted to perform a reverse DNS lookup using the IP address
extracted from the result of `getaddrinfo()` using: `address[0][4][0]`

### What happened

The forward lookup successfully returned: 172.66.147.243 

However, calling:  

socket.gethostbyaddr(ip)  
where ip was the parameter passed to reverse_dns_lookup() function

resulted in:

socket.herror: [Errno 1] Unknown host

### How I investigated it

I tested `gethostbyaddr()` with Google's public DNS server:

socket.gethostbyaddr("8.8.8.8")

This returned:

('dns.google', [], ['8.8.8.8'])

### What I learned

`gethostbyaddr()` itself was working correctly.

The problem was that a successful forward DNS lookup does not explicitly guarantee that a reverse DNS record exists for the resulting IP address.

