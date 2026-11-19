import socket
import getpass
import ssl


def secure_client():
    context = ssl.create_default_context(cafile="certs/server.crt")
    buffer = b""

    try:
        with socket.create_connection(("127.0.0.1", 8080)) as raw_socket:
            with context.wrap_socket(raw_socket, server_hostname="localhost") as tls_socket:
                print("Connected using", tls_socket.version())
                while True:
                    prompt = tls_socket.recv(1024).decode("UTF-8").strip()
                    if not prompt or prompt.startswith("Error : Too many"):
                        print(prompt)
                        return

                    username = input(prompt+ "\n")
                    tls_socket.sendall((username + "\n").encode("UTF-8"))

                    prompt = tls_socket.recv(1024).decode("UTF-8").strip()
                    password = getpass.getpass(prompt + "\n")
                    tls_socket.sendall((password + "\n").encode("UTF-8"))
            
                    #Receive authentication response
                    response = tls_socket.recv(1024).decode("UTF-8")
                    print(response)
                    break

                userInput = input("->")
                while userInput.strip().lower() != "bye":
                    try:
                        tls_socket.sendall((userInput + "\n").encode("UTF-8"))
                    except UnicodeEncodeError:
                        print("Unable to decode the message")
                        userInput = input("->")
                        continue

                    serverResponse = tls_socket.recv(1024)

                    if not serverResponse:
                        print("Server closed the connection")
                        break

                    try: #decoding the server's response
                        decoded = serverResponse.decode("UTF-8")
                        print(f"Echoed this from the server: {decoded}")

                    except UnicodeDecodeError:
                        print("unable to decode the message")
                    userInput = input("->")

    except ssl.SSLEOFError:
        print("The server may be full")
            
if __name__ == "__main__":
    secure_client()






