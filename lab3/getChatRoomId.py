class getChatroomId():

	def __init__(self):
		self.room_id = 0

	# set the chat room id's
	def setRoomId(roomIdPool, count):
		if count in roomIdPool:
			count += 1
		roomIdPool.append(count)
	
	def getRoomId(count):
		return count

	def romoveIdFromPool(x):
		index = 0
		while index != len(roomIdPool)
			if x in roomIdPool:			
				roomIdPool.pop(index)
				break;
			index += 1