
class ChatRoom:

	def __init__(self, name, reference):
		users = []
		self.name = name
		self.reference = reference

	def add_user(username, socket):
		if not socket in username:
			users[socket] = username
		socket.send("%s has joined this chatroom." %(username))

	def remove_user(username, socket):
		socket.send("%s has left this chatroom." %(username))
		users.delete(socket)
		for i in users:
			if i == socket:
				users.pop(i)

	def disconnect_user(socket):
		if socket in users:
			remove_user(users[socket], socket)

	def send_message(message, from_socket):
		username = users[from_socket]
		for user in users:
			msg = ("CHAT: %s\nCLIENT_NAME: %s\nMESSAGE: %s\n\n" %(reference,username,message))
			user.write(msg)