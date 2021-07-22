import socket
from socket import socket

# print(dir(socket.__package__))
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 55555))
    s.listen()
except Exception as e:
    print(e)
