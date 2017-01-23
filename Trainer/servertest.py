import socket

address = (socket.gethostname(), 22222)
sock = socket.create_connection(address)

for i in range(10):
    print("sending")
    sock.send(b'%d\n' % i)
    print("receiving")
    print(sock.recv(2048))
