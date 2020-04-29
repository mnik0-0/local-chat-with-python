import socket
import select
import sys

import src.User as User

# Main variables
PORT = 9090
IP = socket.gethostname()


class Client(User.User):

    def __init__(self):
        self._socket = socket.socket()
        self._socket.connect((IP, PORT))
        self._socket.setblocking(False)

    @property
    def socket(self):
        return self._socket


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
