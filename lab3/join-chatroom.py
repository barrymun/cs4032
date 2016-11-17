
import socket
import sys
import os


msgType = int(sys.argv[1])
room_ref = str(sys.argv[2])
address = str(sys.argv[3])
port = int(sys.argv[4])
client_name = str(sys.argv[5])


if msgType == 1:
	msg = ("JOIN_CHATROOM: %s\n" +
		"CLIENT_IP: %s\n" +
		"PORT: %d\n" +
		"CLIENT_NAME: %s" %(room_ref,address,port,client_name))

elif msgType == 2:
	msg = ("LEAVE_CHATROOM: %s\n" +
		"JOIN_ID: %d\n" +
		"CLIENT_NAME: %s" %(room_ref,join_id,client_name))

else:
	print >>sys.stderr, 'Invalid arguements, please edit msg contents'
	os._exit(1)

def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	print >>sys.stderr, 'starting up'
	# connection port set to 8000 for the purposes of testing here
	# altered to "port"
	sock.connect(("", port))
	connected = True
	
	try:
		sock.sendall(msg)
		data = sock.recv(4096)

		while True:
			print >>sys.stderr, 'received: "%s"' % data
   			data = sock.recv(4096)
   			if data == "":
   				break   			

   	finally:
   		print >>sys.stderr, 'closing socket, terminating connection\n'
   		sock.close()


if __name__ == '__main__':
	main()


