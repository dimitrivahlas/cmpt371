import socket
import threading
from dataclasses import dataclass
from typing import Tuple, Dict, List, Optional

# Colours assigned in join order
COLOURS = [
    (255, 0, 0),   # Red
    (0, 255, 0),   # Green
    (0, 0, 255),   # Blue
    (255, 255, 0), # Yellow
]

class Game:
    def __init__(self):
        self.clients: Dict[Tuple[str, int], ClientInfo] = {}
        self.client_list: List[ClientInfo] = []
        self.next_player_id: int = 1
        self.lock = threading.Lock()

    def add_client(self, conn: socket.socket, addr: Tuple[str, int]):
        with self.lock:
            colour = COLOURS[(self.next_player_id - 1) % len(COLOURS)]
            info = ClientInfo(conn, addr, self.next_player_id, colour)
            self.clients[addr] = info
            self.client_list.append(info)
            self.next_player_id += 1
        # Send information of assigned client
        try:
            conn.sendall(f"ASSIGN;{info.player_id};{colour[0]};{colour[1]};{colour[2]}\n".encode("ascii"))
        except Exception as e:
            print("Error sending ASSIGN:", e)

    def remove_client(self, addr):
        with self.lock:
            info = self.clients.pop(addr, None)
            if info:
                self.client_list = [c for c in self.client_list if c.addr != addr]
                try:
                    info.sock.close()
                except:
                    pass

    def broadcast_all(self, data: bytes, sender_addr=None):
        # Relay changes in the game to everyone except the sender
        with self.lock:
            for addr, info in list(self.clients.items()):
                if sender_addr is not None and addr == sender_addr:
                    continue
                try:
                    info.sock.sendall(data)
                except Exception as e:
                    print("Broadcast error to", addr, ":", e)

    def broadcast_start(self, data: bytes, sender_addr=None):
        # Relay to all clients to start the game
        with self.lock:
            for addr, info in list(self.clients.items()):
                if sender_addr is not None and addr != sender_addr:
                    continue
                try:
                    info.sock.sendall(data.encode("ascii"))
                except Exception as e:
                    print("Broadcast error to", addr, ":", e)

# store information about each client
@dataclass
class ClientInfo:
    sock: socket.socket
    addr: Tuple[str, int]
    player_id: int
    colour: Tuple[int, int, int]

game = Game()

server_running = False
server_socket = None

def broadcast(msg, sender=None):
    game.broadcast_start(msg,sender)

def stop_server():
    global server_running, server_socket
    server_running = False

def handle_client(c, addr):
    """
    Simple line-oriented relay:
    - Clients send lines like: PEN;row;col;x;y;R;G;B\n, CLAIM;... or CLEAR;...
    - We broadcast those lines to all other clients
    """
    try:
        buf = b""
        while True:
            chunk = c.recv(4096)
            if not chunk:
                print("client disconnected:", addr)
                break
            buf += chunk
            # Split on newline and broadcast each complete line
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                line = line.strip()
                if not line:
                    continue
                # Relay to everyone else
                game.broadcast_all(line + b"\n", sender_addr=addr)
    except Exception as e:
        print("handle_client error from", addr, ":", e)
    finally:
        game.remove_client(addr)

def run(ip, portno):
    global server_running, server_socket
    server_running = True
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = 'localhost'
    if ip is not None:
        host = ip
    port = portno

    # Reuse address to avoid TIME_WAIT bind issues
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # binding socket to server port
    print("Server running on port", port)
    server_socket.bind((host, port))

    # listening for inbound connections
    server_socket.listen(5)

    # Set a timeout of 1 second
    server_socket.settimeout(1.0)

    try:
        while server_running:
            try:
                c, addr = server_socket.accept()
                print("connected to:", addr[0], ":", addr[1])
                # Assign connected client a colour and id
                game.add_client(c, addr)
                # Start client thread
                threading.Thread(target=handle_client, args=(c, addr), daemon=True).start()
            except socket.timeout:
                continue
    finally:
        server_socket.close()
        server_running = False

if __name__ == '__main__':
    run("0.0.0.0", 50558)