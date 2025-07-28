import socket

#create a TCP socket server
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#binding the socket to the server port  
server_port = ('localhost', 8000)
print('starting socketServer %s on port %s ' % server_port)
socket.bind(server_port)

#listenign for inbound connections
socket.listen(1)

while True:
    #wait for conncetion
    print('Server waiting for connection')

    connection, client_address = socket.accept()

    try:
        #print connceting and client address
        print('Connected by', client_address)
        
        #recieving the data in chucnks of bytes

        while True:
            data = connection.recv(1024) #CHANGE once we know how much data to receive
            print("recieved" % data)
            if data: 
                #send back to client if data exists (echo)
                print("sending data back to client")
                msg = str(data)
                msg = msg + 'plus extra from the sever'
                msg = bytes(msg, 'utf-8')

                connection.sendall(data)

            else:
                print("no more data from", client_address)
    finally:
        #clean up connection
        connection.close()