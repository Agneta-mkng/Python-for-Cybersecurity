# Secure chat server: login capture (plaintext)

## Goal
To see what the authentication step looks like on the network before TLS is added.

## Setup
- **Tool:** Wireshark on Ubuntu
- **Interface:** `lo` (loopback)
- **Display filter:** `tcp.port == 8080`
- **Client:** `nc 127.0.0.1 8080`
- **Login used:** demo credentials (`Bob` / `pass123`)
- **Capture file:** `secure chat login-plaintext.pcapng`

## How to explore the capture
1. Open the file in Wireshark and apply the filter `tcp.port == 8080`.
2. Right-click a packet and choose **Follow → TCP Stream**.

## What I observed
*Follow → TCP Stream* showed everything I typed and everything the server sent as readable text: the prompts, the username, the password, the login result, and my chat messages with their echoes. 

## Why it matters
Authentication checks who the client is, but it does not protect the credentials in transit. Anyone who captures this traffic can read the password.   
This is the reason for adding TLS.

## Next
Repeat the same login after adding TLS and compare the two captures.