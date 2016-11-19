
class ChatRoom:

	def __init__(self,name,reference,host,port):
		self.name = name
		self.reference = reference
		self.host = host
		self.port = port
		self.users_in_room = []

	def join_chatroom(self,user,conn):
		join_id = len(self.users_in_room)
		if not user in self.users_in_room:
			self.users_in_room.append(user)
		print "%s has joined chatroom: %s." %(user,self.name)
		conn.send("JOINED_CHATROOM: %sSERVER_IP: %sPORT: %dROOM_REF: %dJOIN_ID: %d\r\n\r\n"
			%(self.name,self.host,self.port,self.reference,join_id))

	def leave_chatroom(self,user,conn):
		join_id = len(self.users_in_room)
		if user in self.users_in_room:
			self.users_in_room.remove(user)
		print "%s has left chatroom: %s." %(user,self.name)
		conn.send("LEFT_CHATROOM: %s\nJOIN_ID: %d\r\n\r\n" %(self.name,join_id))

	def disconnect_user(self,user,conn):
		print "%s has disconnected due to transmission error." %(user)
		leave_chatroom(user,conn)

	def send_message(self,user,message,conn):
		if user in self.users_in_room:
			conn.send("CHAT: %s\nCLIENT_NAME: %s\nMESSAGE: %s\n\n" %(self.reference,user,message))
		print "%s: %s" %(user,message)