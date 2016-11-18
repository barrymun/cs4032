
import socket
import threading
import os
import sys

#can be set to any arbitrary value, 5 chosen for the purposes of testing only
maxThreadCount = 5
#total number of threads in use
totalThreads = 0
#check if connection is active
activeConnection = True
#array used to keep track of the threads
threadPool = []

#host = 'localhost'
host = '134.226.32.10'
port = 8220
address = (host, port)
student_id = "13327106"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(address)
server_socket.listen(5)


def handleClientConnections(conn,address):
	checkConnection = True
	chat_id = "room1"
	room_ref = 0
	join_id = 0
	err_code = 1337
	client_name = "client"
	
	err_desc = "error"
	msg = "hello"

	while checkConnection:
		data = conn.recv(2048);

		if "HELO BASE_TEST" in data:
			#confirm that the message has been received
			print "message recieved, number of threads: %d" % (totalThreads)
			conn.send("%sIP:%s\nPort:%d\nStudentID:%s" %(data,host,port,student_id))

		elif "JOIN_CHATROOM" in data:
			print data
			conn.send("JOINED_CHATROOM: %s\nSERVER_IP: %s\nPORT: %d\nROOM_REF: %d\nJOIN_ID: %d\r\n\r\n" %(chat_id,host,port,room_ref,join_id))

		elif "LEAVE_CHATROOM" in data:
			print data
			conn.send("LEFT_CHATROOM: %s\nJOIN_ID: %d\r\n\r\n" %(chat_id,join_id))
			#checkConnection = False

		elif "CHAT" in data:
			print data
			conn.send("CHAT: %s\nCLIENT_NAME: %s\nMESSAGE: %s\r\n\r\n" %(chat_id,client_name,msg))

		elif "DISCONNECT" in data:
			conn.close()

		elif "KILL_SERVICE" in data:
			print "terminating now ..."
			server_socket.close()
			print "Socket closed, connection terminated"
			sys.exit(0)

		else:
			print "Invalid message"
			break

	activeConnection = False
	conn.close()


while activeConnection:
  if totalThreads < maxThreadCount:
    conn,address = server_socket.accept()
    threadPool.append(threading.Thread(target = handleClientConnections, args =(conn,address)))
    threadPool[totalThreads].start()
    global totalThreads
    totalThreads = totalThreads + 1
  else:
    print "no available threads at this moment"