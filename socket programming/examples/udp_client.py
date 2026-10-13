import socket

def udp_client():
    address = ("127.0.0.1",8080)

    u = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    u.settimeout(10)
    try:
        while True:
            message = input("Message to send to server(Type 'exit' to quit)")
            if message.lower() == "exit":
                break
        
            send = message.encode('UTF-8')
            u.sendto(send,address)

            try:
                received,server_address = u.recvfrom(1024)
                decoded = received.decode('UTF-8')

                print(f"Reply from the server: {decoded}")
                print(f"The server address is {server_address}")
            except socket.timeout:
                #Incase no reply arrives before the timeout
                print("No reply from the server")
    
    finally:
        u.close()
        print("\nClient socket is closed")

if __name__ == "__main__" :
    udp_client()      

 