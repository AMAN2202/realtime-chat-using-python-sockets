import socket
import select


class ChatServer:
	def __init__( self, port ):
		self.port = port;
		self.srvsock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		self.srvsock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
		self.srvsock.bind( ("", port) )
		self.srvsock.listen( 5 )
		self.descriptors = [self.srvsock]
		print('ChatServer started on port ', port)

	def run( self ):
		while 1:
			(sread, swrite, sexc) = select.select( self.descriptors, [], [] )
			for sock in sread:
				if sock == self.srvsock:
					self.accept_new_connection()
				else:
					st = (sock.recv(100)).decode('ASCII')
					if st == '' :
						host,port = sock.getpeername()
						st = 'Client left %s:%s\r\n' % (host, port)
						self.broadcast_sting( st, sock )
						sock.close
						self.descriptors.remove(sock)
					else:
						host,port = sock.getpeername()
						newst = '[%s:%s] %s' % (host, port, st)
						self.broadcast_sting( newst, sock )
	def accept_new_connection( self ):
		newsock, (remhost, remport) = self.srvsock.accept()
		self.descriptors.append( newsock )
		newsock.send(b"WELCOME TO CHAT SERVICE\nENTER YOUR NAME")
		nam = (newsock.recv(100)).decode('ASCII')
		st = 'Client joined %s:%s\r\n' % (remhost, remport)
		self.broadcast_sting( st, newsock )

	def broadcast_sting( self, st, omit_sock ):
		for sock in self.descriptors:
			if sock != self.srvsock and sock != omit_sock:
				sock.send(bytes(st,'utf-8'))
		print(st)

myServer = ChatServer( 8080 )
myServer.run()
