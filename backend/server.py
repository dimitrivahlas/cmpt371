import socket
import threading
from _thread import start_new_thread

lock = threading.Lock()

# add each thread/player to this map
players = {}

# placeholder for map that keeps track of game state
game_grid = {}

# handle client connection function


'''

'''


def broadcast():
    return 0


def handle_client(c):
    while True:
        data = c.recv(1024)
        print("Received from client:", data.decode('ascii'))
        if not data:
            print('bye')
            lock.release()
            break
        c.send(data[::-1])
    c.close()


def run(ip, portno):
    # creating a TCP socket server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = 'localhost'
    if ip is not None:
        host = ip

    port = portno

    # binding socket to server port
    print("Server running on port", port)
    s.bind((host, port))

    # listening for inbound connections
    s.listen(5)

    while True:
        c, addr = s.accept()
        lock.acquire()
        print('connected to:', addr[0], ":", addr[1])
        thread = threading.Thread(target=handle_client, args=(c,), daemon=True).start()


def run2():
    # creating a TCP socket server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = 'localhost'
    port = 8000

    # binding socket to server port
    print("Server running on port", port)
    s.bind((host, port))

    # listening for inbound connections
    s.listen(5)

    while True:
        c, addr = s.accept()
        lock.acquire()
        print('connected to:', addr[0], ":", addr[1])
        thread = threading.Thread(target=handle_client, args=(c,), daemon=True).start()


if __name__ == '__main__':
    run2()