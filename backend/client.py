
import queue
import socket
import threading
import subprocess, os, time


def run_client():
    """
    localhost client for echoing
    """
    # define server address and port to connect to
    host = 'localhost'
    port = 50558

    # create tcp socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to sever
    s.connect((host, port))

    # message we send to server
    msg = "hello from client"

    while True:
        # send message to sever encoded as bytes
        s.sendall(msg.encode('ascii'))

        # recieve a response from server up to 1024 bytes
        data = s.recv(1024)

        # decode and print server
        print('Received from server:', data.decode('ascii'))

        ans = input('Do you want to continue (y/n): ')
        if ans.lower() != 'y':
            break

    # close socket connection
    s.close()

def run_client2(ip, portno):
    """
    Run client whose connection will not be localhost
    """

    # define server address and port to connect to
    host = 'localhost'
    if ip is not None:
        host = ip
    port = portno

    # create tcp socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to sever
    s.connect((host, port))

    # message we send to server
    msg = "hello from client"

    while True:
        # send message to sever encoded as bytes
        s.send(msg.encode('ascii'))

        # receive a response from server up to 1024 bytes
        data = s.recv(1024).decode("ascii")
        parts = data.split("|")

        if parts[0] == "server_start":
            try:
                host = parts[1]
                port = parts[2]
                print("Server is starting at " +  host + " " + port)

                game_path = os.path.join("..", "frontend", "gui", "interface.py")

                #Open game
                subprocess.Popen(["python", game_path, host, port])
                time.sleep(5)
                break
            except Exception as e:
                print("Failed to start game:", e)

    # close socket connection
    s.close()


if __name__ == '__main__':
    run_client()