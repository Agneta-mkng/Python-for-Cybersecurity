# TLS handshake: openssl s_server and s_client
This uses the `openssl` test server and client on my machine,not the previously built chat server.  
No key log or decryption secrets were used, so the capture shows what a bystander sees.

## Goal
To watch a real TLS handshake on my own machine and see what a bystander can and cannot read.

## Setup
- **Tool:**   
Wireshark on Ubuntu, interface `lo`, filter `tcp.port == 8443`
- **Server:**  
 `openssl s_server -accept 8443 -cert certs/server.crt -key certs/server.key`
- **Client:**  
 `openssl s_client -connect 127.0.0.1:8443 -CAfile certs/server.crt`
- **Certificate:**  
 Self-signed, created with `openssl req`, valid for `localhost` and `127.0.0.1`
- **TLS version:**  
 1.3
- **Capture file:**  
`tls-handshake-openssl.pcapng` 

## What I observed
- The Client Hello and Server Hello were readable.   
-  The client offered [31] cipher suites, and the server chose TLS_AES_256_GCM_SHA384 and the `x25519` key exchange.
- Each side sent a 32-byte public key_share.
- After the Server Hello, the capture showed only unreadable data, labelled Application Data.
- The terminals on both ends showed the whole handshake, including the certificate, and `Verification: OK`.  
## Reading the cipher suite
`TLS_AES_256_GCM_SHA384`:
- `AES_256`: the encryption method, with a 256-bit key
- `GCM`: the mode, which also detects tampering
- `SHA384`: the hash used to derive the keys

The key itself is never sent. Each side sends a public key_share, then combines the other's with its own temporary secret and reaches the same key.   
`x25519` is an elliptic-curve version of the same idea as my Alice and Bob demo.


## Why the capture shows less than the terminal
The terminals are the two endpoints, which hold the encryption keys.  
Wireshark is a bystander on the wire without the keys. In TLS 1.3 the certificate is sent after the Server Hello, so it is encrypted and Wireshark cannot show it.

## TLS 1.2 comparison

I ran the same server and certificate again, with the client forced to TLS 1.2, and captured it in Wireshark.   
I did not keep this capture in the repo, but the result is easy to reproduce:

```bash
openssl s_client -connect 127.0.0.1:8443 -CAfile certs/server.crt -tls1_2
```

**What I observed:**   
In the TLS 1.2 capture I could see the details of the certificate. In the TLS 1.3 capture I could not.

**Why:**   
TLS 1.3 completes the key exchange first and encrypts the rest of the handshake, including the certificate. TLS 1.2 sends the certificate before any keys exist, so it travels in the clear. The server and the certificate were the same in both runs, so the TLS version is the only difference.

The messages I sent were still unreadable in TLS 1.2. Only the certificate was exposed.
## What surprised me
I could see the full certificate in the terminals but not in the Wireshark capture.   
The terminals are the two endpoints, so they hold the keys and can read everything. Wireshark is a bystander without the keys, and TLS 1.3 encrypts the certificate after the Server Hello.  
The certificate itself is public, any client that connects receives it. What stays private is the server’s private key, which never appeared in either terminal’s output, because it is used to sign the handshake and is never sent.