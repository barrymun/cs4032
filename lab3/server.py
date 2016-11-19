
import socket
import threading
import os
import collections
from chatroom import ChatRoom

maxThreadCount = 1000
totalThreads = 0
activeConnection = True
threadPool = []

host = 'localhost'
#host = '134.226.32.10'
port = 8220
address = (host, port)
student_id = "13327106"
BUFF = 2048
chat_rooms = collections.OrderedDict()


def handleClientConnections(conn,address):
	checkConnection = True
	global users_in_room
	global chat_rooms
	chat_room = ChatRoom(host,port)
	
	# err_code = 1337
	# err_desc = "error"

	while checkConnection:
		data = conn.recv(BUFF);

		if "HELO BASE_TEST" in data:
			print "message recieved, number of threads: %d" % (totalThreads)
			conn.send("%sIP:%s\nPort:%d\nStudentID:%s" %(data,host,port,student_id))

		elif "KILL_SERVICE" in data:
			server_socket.close()
			print "Socket closed, connection terminated"
			os.exit(1)

		elif "JOIN_CHATROOM" in data:
			split_data = data.split('\n')
			room_name = split_data[0].split(':')[1]
			client_name = split_data[3].split(':')[1]
			chat_room.join_chatroom(room_name,client_name,chat_rooms,conn)

		elif "LEAVE_CHATROOM" in data:
			split_data = data.split('\n')
			room_ref = split_data[0].split(':')[1]
			join_id = split_data[1].split(':')[1]
			client_name = split_data[2].split(':')[1]
			chat_room.leave_chatroom(client_name,chat_rooms,room_ref,join_id,conn)

		elif "CHAT" in data:
			split_data = data.split('\n')
			room_ref = split_data[0].split(':')[1]
			join_id = split_data[0].split(':')[1]
			client_name = split_data[2].split(':')[1]
			message = split_data[3].split(':')[1]
			chat_room.send_message(room_ref,join_id,client_name,message,chat_rooms,conn)

		elif "DISCONNECT" in data:
			split_data = data.split('\n')
			client_name = split_data[2].split(':')[1]
			disconnect_user(client_name,chat_rooms,conn)
			checkConnection = False


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(address)
server_socket.listen(5)

while activeConnection:
  if totalThreads < maxThreadCount:
    conn,address = server_socket.accept()
    threadPool.append(threading.Thread(target = handleClientConnections, args =(conn,address)))
    threadPool[totalThreads].start()
    global totalThreads
    totalThreads = totalThreads + 1
  else:
    print "no available threads at this moment"