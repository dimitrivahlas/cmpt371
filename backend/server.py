import socket
import threading
from _thread import start_new_thread


lock = threading.Lock()

#add each thread/player to this map 
players = {}

#handle clietn connectiong function
def handle_client(c):
    while True:
        data = c.recv(1024)
        if not data:
            print('bye')
            lock.release()
            break
        c.send(data[::-1])
    c.close()

def main():

    #creating a TCP socket server
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    host = 'localhost'
    port = 8000
    
    #binding socket to server port
    print("Server running on port", port)
    s.bind((host,port))
    
    #listening for inbound connections
    s.listen(5)


    while True:
        c, addr = s.accept()
        lock.acquire()
        print('connected to:', addr[0], ":", addr[1])
        start_new_thread(handle_client,(c,))

if __name__ == '__main__':
    main()