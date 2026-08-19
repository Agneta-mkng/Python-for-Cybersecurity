# Python Socket DNS Cheat Sheet

| Function | Purpose | Returns |
|---|---|---|
| gethostname() | Get local computer's hostname | string |
| getfqdn() | Get fully qualified domain name | string |
| gethostbyname() | Hostname → IPv4 address | string |
| gethostbyname_ex() | Hostname → hostname, aliases, addresses | tuple |
| gethostbyaddr() | IP address → hostname information | tuple |
| getaddrinfo() | Get detailed address/connection information | list of tuples |

Forward lookup:
hostname → IP address

Reverse lookup:
IP address → hostname

### gethostbyaddr()

Performs a reverse DNS lookup:

IP address → hostname

Note:
A successful forward lookup does not guarantee that a
reverse lookup will succeed because an IP address may not have
a usable reverse-DNS record.
