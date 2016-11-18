
import socket
import time
import sys
import os

address = "localhost"
port = 8220

chat_id = "dank"
client_name = str(raw_input("Provide your nickname: "))
join_id = 0
room_ref = 0
the_msg = "insert the message here"

join_msg = ("JOIN_CHATROOM: %s\nCLIENT_IP: %s\nPORT: %d\nCLIENT_NAME: %s\n\n" %(chat_id,address,port,client_name))
exit_msg = ("LEAVE_CHATROOM: %s\nJOIN_ID: %d\nCLIENT_NAME: %s\n\n" %(chat_id,join_id,client_name))
disconnect_msg = ("DISCONNECT: %s\nPORT: %d\nCLIENT_NAME: %s\n\n" %(address,port,client_name))
#chat_msg = ("CHAT: %d\nJOIN_ID: %d\nCLIENT_NAME: %s\nMESSAGE: %s\n\n" %(room_ref,join_id,client_name,the_msg))


def main():
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect((address, port))

	user_msg = ""

	client_socket.send(join_msg)
	while not "JOINED_CHATROOM" in client_socket.recv(2048):
		print "Waiting for connection . . ."
	print "Successfully joined chatroom: %s" %(chat_id)

	while user_msg != "/leave":
	  user_msg = raw_input("type your message: ")
	  chat_msg = ("CHAT: %d\nJOIN_ID: %d\nCLIENT_NAME: %s\nMESSAGE: %s\n\n" %(room_ref,join_id,client_name,user_msg))
	  if user_msg != "/leave":
	  	client_socket.send(chat_msg)
	  	while "CHAT" in client_socket.recv(2048):
		  	print "%s: %s" %(client_name,user_msg)
		  	break;

	client_socket.send(exit_msg)
	while not "LEFT_CHATROOM" in client_socket.recv(2048):
		print "Disconnecting . . ."
	print "Successfully left chatroom: %s" %(chat_id)

	print "Goodbye"
	client_socket.close()

if __name__ == '__main__':
	main()