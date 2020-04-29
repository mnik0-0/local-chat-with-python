import sys


class Variables:

    def __init__(self, server_socket):
        self._clients = {}
        self._socket_list = [server_socket, sys.stdin]
        self._rooms = {}

    @property
    def clients(self):
        return self._clients

    def add_client(self, client):
        self._clients[client.socket] = client

    def get_client(self, socket):
        return self._clients[socket]

    def remove_client(self, client):
        self._clients.pop(client.socket)

    @property
    def socket_list(self):
        return self._socket_list

    def add_socket(self, client):
        self._socket_list.append(client.socket)

    def remove_socket(self, client):
        self._socket_list.remove(client.socket)

    @property
    def rooms(self):
        return self._rooms

    def add_room(self, room):
        self._rooms[room.name] = room

    def get_room(self, client):
        return self._rooms[client.room]

    def remove_room(self, room):
        self._rooms.pop(room.name)

    def check_room(self, room):
        if room.is_empty():
            self.remove_room(room)
