import socket
import sys
import urllib

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening

server_address = ('localhost', 8000)
print >>sys.stderr, 'connecting to %s on port %s' % server_address
sock.connect(server_address)

BUFFER_SIZE = 1024

try:
    
    # Send data
    message_query = "upper case here"
    message = "GET /server-echo.php?message=%s HTTP/1.0\r\n\r\n" % urllib.quote(message_query)
    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)
    
    while amount_received < amount_expected:
        data = sock.recv(BUFFER_SIZE)
        amount_received += len(data)
        print >>sys.stderr, 'received "%s"' % data

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
