# Secure chat server: login capture (TLS)

## Goal
To see what the same login looks like on the network after TLS is added, and compare it with the plaintext capture.

## Setup
- **Tool:** Wireshark 4.2.2 on Ubuntu
- **Interface:** `lo` (loopback)
- **Display filter:** `tcp.port == 8080`
- **Client:** `secure_client.py` (Python, verifies the server certificate and hostname)
- **Server:** `Secure chat application.py`, self-signed certificate, run from `projects/`
- **Login used:** demo credentials (`Bob` / `pass123`)
- **TLS version negotiated:** Connected using TLSv1.3
- **Capture file:** `tls_client_login.pcapng` 

## Prediction
The previously visible information during the last capture will look scrambled as it is encrypted across th channel hence wireshark(a bystander) cannot know what was sent.

## How to explore the capture
1. Open the file in Wireshark and apply the filter `tcp.port == 8080`.
2. Right-click a packet and choose **Follow → TCP Stream** (keep "Show data as" on ASCII, same as the plaintext capture).
3. To find the ClientHello, look at packet 26, then open the hex dump in the bottom pane.

## What I observed
- *Follow → TCP Stream* showed unreadable data. The username, password, login result and chat messages could not be read.
- The stream was 2,809 bytes (6 client packets, 8 server packets). The plaintext capture of the same kind of login was 111 bytes (3 client packets, 5 server packets).
- The Protocol column showed **TCP**, not TLS, for these packets. I have not fixed the Decode As step yet. 
- Packet 26 (`52150 → 8080`, `Len=517`) is the first data the client sent. Its bytes start with `16 03 01`, which marks a TLS handshake record, and it is the ClientHello.
- The word `localhost` is readable inside that packet, in the server_name field.

## Why `localhost` is readable
My client was created with `server_hostname="localhost"`, and that name is sent in the ClientHello. The ClientHello is the first message of the handshake, so the two sides have not agreed on a key yet and there is nothing to encrypt it with. Everything after the handshake (the login and the chat) is encrypted.

## Why it matters
TLS protects what is said, not the fact that a connection happened. Someone capturing this traffic can see which machines are talking, when, roughly how much data moved, and the server name in the ClientHello. They cannot read the password or the messages.

## Compared with the plaintext capture
| | Plaintext | TLS |
|---|---|---|
| Follow TCP Stream | Readable, including `pass123` | Unreadable |
| Stream size | 111 bytes | 2,809 bytes |
| Packets | 3 client, 5 server | 6 client, 8 server |

The TLS stream is much larger for the same short conversation. I think most of that is handshake data, but I have not verified that. 

## What I learned
- After adding TLS, Follow → TCP Stream no longer showed the username, password, login result or chat messages. The same kind of login that was fully readable in the plaintext capture was unreadable here.
- Not everything is hidden. The server name `localhost` was readable in the ClientHello (packet 26). It is sent at the start of the handshake, before the two sides have agreed on a key, so nothing can encrypt it yet.
- Wireshark labelled the packets as TCP and not TLS, because I have not fixed the Decode As step. The raw bytes still showed the handshake record (`16 03 01`).
- My prediction was right that the login would be unreadable. TLS hid the content of the conversation, not the fact that it happened.

## Next
Fix the Decode As step so Wireshark labels the packets as TLS, then check the rest of the handshake