import pygame
from pygame.locals import *
import numpy as np
import socket, threading, sys, queue

#Initialize pygame
pygame.init()

#Define diff player colours (server assigns one of these)
player_colours = {
    1: (255,0,0),
    2: (0,255,0),
    3: (0,0,255),
    4: (255,255,0),
}

current_player = 1  # overwritten by ASSIGN
current_colour = (255,0,0)  # overwritten by ASSIGN

#set up game window
tile_size = 100
screen_width = 800
grid_height = 800
leaderboard_height = 100
screen_height = grid_height + leaderboard_height

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Deny and Conquer")

#Colour
black = (0,0,0)

#fill game window with white
screen.fill((255,255,255))

# scribble surface (grid area only)
scribble_surf = pygame.Surface((screen_width, grid_height), SRCALPHA)

drawing = False
locked_tiles = {}  # key: (row,col), value: player_id
current_tile = None

# locked while someone is scribbling
busy_tiles = {}  # key: (row, col), value: player_id


pygame.font.init()
font = pygame.font.SysFont(None, 36)

total_tiles = (screen_width // tile_size) * (grid_height // tile_size)

# Queue to store incoming messages
incoming = queue.Queue()
sock = None



def net_send(line: str):
    """
    Send text command / changes in game state from the client to the server
    """
    try:
        if sock:
            sock.sendall((line.strip() + "\n").encode("ascii"))
    except Exception as e:
        print("net_send error:", e)


def net_recv_loop():
    """
    continuously listen for messages from the server for game loop use
    """
    buf = b""
    while True:
        try:
            data = sock.recv(4096)
            if not data: break
            buf += data
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                incoming.put(line.decode("ascii").strip())
        except Exception as e:
            print("net_recv error:", e)
            break

def connect_to_server():
    """
    TCP Protocol to establish connection from peers to server
    """
    global sock
    host = "127.0.0.1"
    port = 50558
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        port = int(sys.argv[2])
    print(f"Connecting to {host}:{port} ...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print("Connected.")
    sock = s
    threading.Thread(target=net_recv_loop, daemon=True).start()

connect_to_server()

def draw_leaderboard():
    """
    Draw leaderboard on bottom of screen via pygame
    """
    pygame.draw.rect(screen, (255, 255, 255), (0, grid_height, screen_width, leaderboard_height))
    pygame.draw.line(screen, (0, 0, 0), (0, grid_height), (screen_width, grid_height), 2)

    # Count score per player
    scores = {pid: 0 for pid in player_colours}
    for owner in locked_tiles.values():
        scores[owner] += 1

    # Display Scores
    x_offset = 10
    for pid in sorted(scores.keys()):
        colour = player_colours[pid]
        text = font.render(f"P{pid}: {scores[pid]}", True, colour)
        screen.blit(text, (x_offset, grid_height + 30))
        x_offset += 180

def draw_grid(tile_size):
    """
    Draw game grid of 8x8 with tile_size pixels per tile
    """
    screen.fill((255,255,255), rect=(0,0,screen_width,grid_height))
    screen.blit(scribble_surf, (0,0))
    for x in range(tile_size, screen_width, tile_size):
        pygame.draw.line(screen, black, (x, 0), (x, grid_height))
    for y in range(tile_size, grid_height, tile_size):
        pygame.draw.line(screen, black, (0, y), (screen_width, y))



def is_tile_blocked(tile, for_player):
    """
    Helper to check if certain tile is unavailable
    :param tile: row, col Tuple[int, int]
    :param for_player: particular player trying to draw on tile
    :return: bool indicating availability of tile
    """
    # Block if permanently locked, or temporarily locked by another player
    return (tile in locked_tiles) or (tile in busy_tiles and busy_tiles[tile] != for_player)


def apply_remote(msg: str):
    """
    Update local gamestate with server gamestate
    """
    global current_player, current_colour
    try:
        parts = msg.split(";")
        typ = parts[0]
        if typ == "ASSIGN":
            # msg structure: ASSIGN;id;R;G;B
            pid = int(parts[1])
            r,g,b = int(parts[2]), int(parts[3]), int(parts[4])
            current_player = pid
            current_colour = (r,g,b)
            print(f"Assigned player {pid} colour {current_colour}")

        elif typ == "PEN":
            # msg structure: PEN;row;col;x;y;R;G;B
            row = int(parts[1]); col = int(parts[2])
            x = int(parts[3]); y = int(parts[4])
            r = int(parts[5]); g = int(parts[6]); b = int(parts[7])
            if y >= grid_height:  # ignore HUD area
                return
            tile_rect = pygame.Rect(col*tile_size, row*tile_size, tile_size, tile_size)
            scribble_surf.set_clip(tile_rect)
            pygame.draw.circle(scribble_surf, (r,g,b), (x,y), 3)
            scribble_surf.set_clip(None)

        elif typ == "LOCK":
            # msg structure: LOCK;row;col;player_id
            row = int(parts[1])
            col = int(parts[2])
            pid = int(parts[3])
            busy_tiles[(row, col)] = pid

        elif typ == "UNLOCK":
            # msg structure: UNLOCK;row;col
            row = int(parts[1])
            col = int(parts[2])
            busy_tiles.pop((row, col), None)

        elif typ == "CLAIM":
            # msg structure: CLAIM;row;col;R;G;B
            row = int(parts[1]); col = int(parts[2])
            r = int(parts[3]); g = int(parts[4]); b = int(parts[5])
            tile_rect = pygame.Rect(col*tile_size, row*tile_size, tile_size, tile_size)
            pygame.draw.rect(scribble_surf, (r,g,b), tile_rect)

            # Attempt to identify the claiming player by the given colour
            owner_id = None
            for pid, clr in player_colours.items():
                if clr == (r,g,b):
                    owner_id = pid
                    break

            # If player is identified, register ownership of this tile (using their id)
            if owner_id is not None:
                locked_tiles[(row,col)] = owner_id
            busy_tiles.pop((row, col), None)

        elif typ == "CLEAR":
            # msg structure: CLEAR;row;col
            row = int(parts[1]); col = int(parts[2])
            tile_rect = pygame.Rect(col*tile_size, row*tile_size, tile_size, tile_size)

            # erase scribbles from that tile only (alpha clear)
            pygame.draw.rect(scribble_surf, (0,0,0,0), tile_rect)
            if (row,col) in locked_tiles:
                del locked_tiles[(row,col)]
            busy_tiles.pop((row, col), None)

    except Exception as e:
        print("apply_remote error:", e, "for msg:", msg)


########################################################
#
# GAME LOOP
#
########################################################

running = True
while running:

    # apply all incoming network events first
    while not incoming.empty():
        apply_remote(incoming.get())

    draw_grid(tile_size)
    draw_leaderboard()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEMOTION:
            if drawing and current_tile and not is_tile_blocked(current_tile, current_player):
                mx, my = event.pos
                if my >= grid_height:
                    continue
                col = mx // tile_size
                row = my // tile_size
                if (row, col) == current_tile:
                    tile_rect = pygame.Rect(col*tile_size, row*tile_size, tile_size, tile_size)
                    scribble_surf.set_clip(tile_rect)
                    pygame.draw.circle(scribble_surf, current_colour, (mx,my), 3)
                    scribble_surf.set_clip(None)
                    # broadcast live pen
                    net_send(f"PEN;{row};{col};{mx};{my};{current_colour[0]};{current_colour[1]};{current_colour[2]}")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if my >= grid_height:
                continue
            col = mx // tile_size
            row = my // tile_size
            tile = (row, col)
            if not drawing and not is_tile_blocked(tile, current_player):
                current_tile = tile
                drawing = True
                busy_tiles[tile] = current_player
                net_send(f"LOCK;{row};{col};{current_player}")

        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing and current_tile and current_tile not in locked_tiles:
                drawing = False
                row, col = current_tile
                x = col * tile_size
                y = row * tile_size
                tile_rect = pygame.Rect(x, y, tile_size, tile_size)
                tile_surface = scribble_surf.subsurface(tile_rect).copy().convert_alpha()
                mask = pygame.mask.from_surface(tile_surface)
                filled_pixels = mask.count()
                total_pixels = tile_size * tile_size
                percent_filled = filled_pixels / total_pixels
                if percent_filled >= 0.5:
                    pygame.draw.rect(scribble_surf, current_colour, tile_rect)
                    # logic for updating host score based on colour
                    owner_id = current_player
                    if owner_id not in player_colours:
                        # try to map by colour to an existing palette slot
                        mapped = next((pid for pid, clr in player_colours.items() if clr == current_colour), None)
                        if mapped is not None:
                            owner_id = mapped

                    if owner_id in player_colours:
                        locked_tiles[(row, col)] = owner_id
                        net_send(f"CLAIM;{row};{col};{current_colour[0]};{current_colour[1]};{current_colour[2]}")
                else:
                    pygame.draw.rect(scribble_surf, (0,0,0,0), tile_rect)
                    net_send(f"CLEAR;{row};{col}")

                # remove temporary lock locally
                if current_tile in busy_tiles:
                    del busy_tiles[current_tile]

                # If we didn’t claim, tell others the tile is free again
                if percent_filled < 0.5:
                    net_send(f"UNLOCK;{row};{col}")

            drawing = False
            current_tile = None

    pygame.display.update()

pygame.quit()