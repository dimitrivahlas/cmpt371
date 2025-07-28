#create a TCP/IP socket for a client

import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect the socket to port where the server is listening
server_address = ('localhost', 8000)

print('connecting to port' , server_address)
client_socket.connect(server_address)

try:
    # send data 
    message = 'This is new message. Please repeat. '
    print('Sending: "%s"' % message)
    client_socket.sendall(bytes(message, 'utf-8')) #encoding in bytes using utf-8 protocl

    # listen for a response back to establish connection
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = client_socket.recv(1024)
        amount_received += len(data)

        print('recieved "%s"' %data)
finally:
    print('closing client')
    client_socket.close()
