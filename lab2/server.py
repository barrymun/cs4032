
import socket
import threading
import os
import sys


#can be set to any arbitrary value, 5 chosen for the purposes of testing only
maxThreadCount = 5
#server machine address hard coded here (this is the IP used for the submission nad for tests)
address = "134.226.44.157"
#student id
student_id = "13327106"
#get the port number
port = int(sys.argv[1])
#socket used for the connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#total number of threads in use
totalThreads = 0
#check if connection is active
activeConnection = True
#array used to monitor the threads
monitorThreads = []



def handleClientConnections(conn,addr):
    checkConnection = True
    while checkConnection:
        data = conn.recv(1024)
        #check if the required text appears in the message
        if "HELO BASE_TEST" in data:
        		#confirm that the message has been received
            print "message recieved, number of threads: %d" % (totalThreads)
            conn.send("%sIP:%s\nPort:%d\nStudentID:%s" %(data,address,port,student_id))
        #check for alternative message type used to end the connection
        elif data == "KILL_SERVICE\n":
            print "terminating now ..."
            sock.close()
            print "Socket closed, connection terminated"
            os._exit(1)
        elif not data:
            checkConnection = False
        else:
            print data


sock.bind((address,port))
print "Socket generated at IP:%s and port:%d, listening for client connections" %(address,port)
sock.listen(5)

while activeConnection:
    if totalThreads < maxThreadCount:
        conn,addr = sock.accept()
        monitorThreads.append(threading.Thread(target = handleClientConnections, args =(conn,addr,)))
        monitorThreads[totalThreads].start()
        global totalThreads
        totalThreads = totalThreads + 1
    else:
        print "no available threads at this moment"


