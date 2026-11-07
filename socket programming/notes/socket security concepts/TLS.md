# TLS (Transport Layer Security)
This is a cryptographic protocol which enables a client to be able to communicate to a server over an untrusted network.
## The problem
My capture of the secure chat server showed the login as readable text: the username, the password, and every chat message.   
Authentication checks **who** the client is, but it does not protect the data on the way. Anyone who can capture the traffic can read it. TLS fixes this.

## What TLS provides

| Property | Meaning |
|---|---|
| **Confidentiality** | Data is encrypted, so a capture shows unreadable bytes. |
| **Integrity** | Tampering with data in transit is detected. |
| **Server authentication** | The client can check that it is talking to the real server, using a certificate. |

TLS sits between TCP and my application. My newline-framed messages stay the same. They are encrypted before they are sent and decrypted when they arrive.

**Related terms:**   
TLS replaced SSL, which is obsolete, though Python's module is still called `ssl`. HTTPS is HTTP carried over TLS.

## How a connection starts (the handshake)
1. The client says hello and lists the TLS versions and cipher suites it supports.
2. The server picks one and sends its **certificate**.
3. The client checks the certificate.
4. Both sides agree on session keys. After that, all data is encrypted with them.

The handshake happens after the TCP handshake and before any application data, so my login prompts will travel inside the encrypted connection.

## Certificates and trust
A certificate links a server's identity (a name) to its **public key**.   
The server keeps the matching **private key** secret.

- Normally a **certificate authority (CA)** signs the certificate, and clients already trust the CA.
- For this project I will use a **self-signed certificate**, which no CA has vouched for. A client will only accept it if I tell the client to trust that specific file. That is fine for learning on my own machine, and wrong for a real service.
- Verification also checks that the certificate's name matches the host being connected to.
