#create a TCP/IP socket for a client

import socket

def main():
    #define server address and port to connect to
    host = 'localhost'
    port = 8000

    #create tcp socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #connect to sever
    s.connect((host, port))

    #message we send to server
    msg = "hello from client"

    while True:
        #send message to sever encoded as bytes
        s.send(msg.encode('ascii'))

        #recieve a response from server up to 1024 bytes
        data = s.recv(1024)

        #decode and print server
        print('Received from server:', data.decode('ascii'))

        ans = input('Do you want to continue (y/n): ')
        if ans.lower() != 'y':
            break

    #close socket connection
    s.close()
    
if __name__ == '__main__':
    main()
