import random


server_ip = '127.0.0.1'
server_port = None
with open('port') as f:
    server_port = f.read()
server_port = int(server_port)
