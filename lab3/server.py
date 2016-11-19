
import socket
import threading
import os
import sys
from chatroom import ChatRoom

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
	chat_room = ChatRoom(chat_id,host,port)
	
	join_id = 0
	err_code = 1337	
	err_desc = "error"

	while checkConnection:
		data = conn.recv(2048);

		if "HELO BASE_TEST" in data:
			#confirm that the message has been received
			print "message recieved, number of threads: %d" % (totalThreads)
			conn.send("%sIP:%s\nPort:%d\nStudentID:%s" %(data,host,port,student_id))

		elif "JOIN_CHATROOM" in data:
			print data
			split_data = data.split('\n')
			client_name = split_data[3].split(':')[1]
			chat_room.join_chatroom(client_name,conn)

		elif "LEAVE_CHATROOM" in data:
			print data
			split_data = data.split('\n')
			client_name = split_data[2].split(':')[1]
			chat_room.leave_chatroom(client_name,conn)

		elif "CHAT" in data:
			print data
			split_data = data.split('\n')
			rm_ref = int(split_data[0].split(':')[1])
			client_name = split_data[2].split(':')[1]
			msg = split_data[3].split(':')[1]
			chat_room.send_message(rm_ref,client_name,msg,conn)

		elif "DISCONNECT" in data:
			checkConnection = False

		elif "KILL_SERVICE" in data:
			server_socket.close()
			print "Socket closed, connection terminated"
			os.exit(1)

		else:
			print "ERROR"
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