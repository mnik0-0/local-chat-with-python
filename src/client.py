import socket
import select
import sys

from src.add.user import User

# Main variables
PORT = 9090
IP = socket.gethostname()


class Client(User):

    def __init__(self):
        self.socket = socket.socket()
        self.socket.connect((IP, PORT))
        self.socket.setblocking(False)


client = Client()

while True:

    reads, _, _ = select.select([client.socket, sys.stdin], [], [])
    for to_do in reads:
        if to_do == client.socket:
            data = client.get_data()
            if data:
                print(data)
        else:
            data = input()
            if data:
                client.send_data(data)
