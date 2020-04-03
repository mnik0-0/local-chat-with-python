import socket
import pickle
import select
import sys

DATA_LENGTH = 10


class User:

    def send_data(self, data):
        data = pickle.dumps(data)
        data = bytes(f"{len(data):<{DATA_LENGTH}}", "utf-8") + data
        self.socket.send(data)

    def get_data(self):

        try:
            len_message = int(self.socket.recv(DATA_LENGTH).decode("utf-8"))
            data = self.socket.recv(len_message)
            data = pickle.loads(data)
            return data
        except:
            return False
