import pickle

DATA_LENGTH = 10


class User:
    _socket = None

    def send_data(self, data):
        data = pickle.dumps(data)
        data = bytes(f"{len(data):<{DATA_LENGTH}}", "utf-8") + data
        self._socket.send(data)

    def get_data(self):

        try:
            len_message = int(self._socket.recv(DATA_LENGTH).decode("utf-8"))
            data = self._socket.recv(len_message)
            data = pickle.loads(data)
            return data
        except:
            return None
