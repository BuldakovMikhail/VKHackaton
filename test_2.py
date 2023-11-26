import socket

s = socket.socket()

s.connect(('localhost', 8080))
print('connected')

print(s.recv(1024))