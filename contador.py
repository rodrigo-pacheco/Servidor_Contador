#!/usr/bin/python3
"""
Contador Server: serves inverse counter: 5,4,3,2,1,0,5

Rodrigo Pacheco Martinez-Atienza
r.pachecom @ gsyc.es
SAT subject (Universidad Rey Juan Carlos)
"""

import socket

# Create a TCP objet socket and bind it to a port
# Port should be 80, but since it needs root privileges,
# let's use one above 1024

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Let the port be reused if no process is actually using it
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind to the address corresponding to the main name of the host
mySocket.bind(('localhost', 1234))

# Queue a maximum of 5 TCP connection requests
mySocket.listen(5)

# Accept connections, read incoming data, and answer back an HTML page
#  (in an almost-infinite loop; the loop can be stopped with Ctrl+C)

# Parse petition
def parse(received):
    method = received.split()[0]
    resource = received.split()[1]
    return(method, resource)

# Process petition
def process(request):
    if request[0] == 'GET' and request[1] == '/contador':
        return('Petición correcta')
    else:
        return('Petición INCORRECTA')

try:
    while True:
        print('Waiting for connections')
        (recvSocket, address) = mySocket.accept()
        print('Request received:')
        print('Answering back...')

        received = str(recvSocket.recv(2048), 'utf-8')
        request = parse(received)
        answer = process(request)

        recvSocket.send(bytes(
                        "HTTP/1.1 200 OK\r\n\r\n" +
                        "<html><body><h1>Welcome to online reverse counter</h1>" +
                        answer +
                        "</body></html>" +
                        "\r\n", "utf-8"))
        recvSocket.close()

except KeyboardInterrupt:
    print("Closing binded socket")
    mySocket.close()
