
from hashlib import md5

def broadcast(room_ref,join_id,user,chat_rooms,message,conn):
	for join_id, conn in chat_rooms[room_ref].iteritems():
		conn.send("CHAT:%s\nCLIENT_NAME:%s\nMESSAGE:%s\n\n" %(str(room_ref),user,message))

class ChatRoom:

	def __init__(self,host,port):
		self.host = host
		self.port = port

	def join_chatroom(self,name,user,chat_rooms,conn):
		room_ref = int(md5(name).hexdigest(), 16)
		if room_ref not in chat_rooms:
			chat_rooms[room_ref] = {}

		join_id = int(md5(user).hexdigest(), 16)
		if join_id not in chat_rooms[room_ref]:
			chat_rooms[room_ref][join_id] = conn
			message = ("%s has joined the chatroom." %(user))
			conn.send("JOINED_CHATROOM:%s\nSERVER_IP:%s\nPORT:%s\nROOM_REF:%s\nJOIN_ID:%s\n\n"
				%(name,self.host,str(self.port),str(room_ref),str(join_id)))
			message = ("%s has joined the chatroom." %(user))
			broadcast(room_ref,join_id,user,chat_rooms,message,conn)

	def leave_chatroom(self,user,chat_rooms,room_ref,join_id,conn):
		print "%s has left the chatroom." %(user)
		conn.send("LEFT_CHATROOM:%s\nJOIN_ID:%s\n\n" %(room_ref,str(join_id)))
		message = ("%s has left the chatroom." %(user))
		broadcast(room_ref,join_id,user,chat_rooms,message,conn)
		del chat_rooms[room_ref][join_id]

	def disconnect_user(self,user,chat_rooms,conn):
		join_id = int(md5(user).hexdigest(), 16)
		print "%s has disconnected due to transmission error." %(user)
		for room_ref in chat_rooms.keys():
			if join_id in chat_rooms[room_ref]:
				message = ("%s has left the chatroom." %(user))
				broadcast(room_ref, message)
				if join_id in chat_rooms[room_id]:
					del chat_rooms[room_ref][join_id]

	def send_message(self,room_ref,join_id,user,message,chat_rooms,conn):
		message = ("%s: %s" %(user,message))
		conn.send("CHAT:%s\nCLIENT_NAME:%s\nMESSAGE:%s\n\n" %(str(room_ref),user,message))
		broadcast(room_ref,join_id,user,chat_rooms,message,conn)