import socket

#create a TCP socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#binding the socket to the server port  
server_port = ('localhost', 8000)
print('starting socketServer %s on port %s ' % server_port)
server_socket.bind(server_port)

#listenign for inbound connections
server_socket.listen(1)

while True:
    #wait for conncetion
    print('Server waiting for connection')

    connection, client_address = server_socket.accept()

    try:
        #print connceting and client address
        print('Connected by', client_address)
        
        #recieving the data in chucnks of bytes

        while True:
            data = connection.recv(1024) #CHANGE once we know how much data to receive
            print("recieved" % data)
            if data: 
                #send back to client if data exists (echo)
                #add a bit of message so we know were on the right track
                print("sending data back to client")
                msg = str(data)
                msg = msg + 'plus extra from the sever'
                msg = bytes(msg, 'utf-8')

                connection.sendall(msg)

            else:
                print("no more data from", client_address)
                break
    finally:
        #clean up connection
        connection.close()