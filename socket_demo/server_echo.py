import socket,sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_name = sys.argv[1]
server_addr = (server_name,8000)
print  >>sys.stderr, 'starting up on %s port %s' %server_addr
sock.bind(server_addr)
sock.listen(1)

while True:
	print >>sys.stderr,'waiting for a connection'
	connection, client_addr = sock.accept()
	try:
		print >>sys.stderr,'connection from',client_addr
		while True:
			data = connection.recv(1024)
			print >>sys.stderr,'reveived "%s"' %data
			if data:
				print >>sys.stderr,'sending data back to the client'
				connection.sendall(data)
			else:
				print >>sys.stderr,'no data from', client_addr
				break
	finally:
		connection.close()