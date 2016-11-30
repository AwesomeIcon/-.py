import socket,sys

# create a TCP/IP socket
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# connect the socket to the port where the server is listening
server_name = sys.argv[1]
server_addr = (server_name,8000)
print >>sys.stderr,'connecting to %s port %s' %server_addr
sock.connect(server_addr)

try:
	message = 'this is a message. it will be repeated.'
	print >> sys.stderr,'sending "%s"' %message
	sock.sendall(message)

	amount_received = 0
	amount_expected = len(message)

	while amount_received < amount_expected:
		data = sock.recv(1024)
		amount_received += len(data)
		print >>sys.stderr,'received "%s"' %data
finally:
	print >>sys.stderr,'closing socket'
	sock.close()
