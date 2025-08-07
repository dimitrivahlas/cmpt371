#create a TCP/IP socket for a client
import queue
import socket
import threading


def run_client():
    #define server address and port to connect to
    host = 'localhost'
    port = 50558

    #create tcp socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #connect to sever
    s.connect((host, port))

    #message we send to server
    msg = "hello from client"

    while True:
        #send message to sever encoded as bytes
        s.sendall(msg.encode('ascii'))

        #recieve a response from server up to 1024 bytes
        data = s.recv(1024)

        #decode and print server
        print('Received from server:', data.decode('ascii'))

        ans = input('Do you want to continue (y/n): ')
        if ans.lower() != 'y':
            break

    #close socket connection
    s.close()

def run_client2(ip, portno):
    """
    Run client whose connection will not be localhost
    """

    #define server address and port to connect to
    host = 'localhost'
    if ip is not None:
        host = ip
    port = portno

    #create tcp socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #connect to sever
    s.connect((host, port))

    # #create queue for handling messages
    # msg_queue = queue.Queue()
    #
    # def recv_loop():
    #     try:
    #         while True:
    #             data = s.recv(1024)
    #             if not data:
    #                 break
    #             msg_queue.put(data.decode('ascii'))
    #     finally:
    #         s.close()
    #         msg_queue.put(None)
    #
    # threading.Thread(target=recv_loop, daemon=True).start()
    #
    # #
    # s.setblocking(True)

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
    run_client()
