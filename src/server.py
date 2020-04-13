import socket
import pickle
import select
import sys

from extra.user import User

# Main variables
PORT = 9090
IP = socket.gethostname()


class Room:

    # Create new room
    def __init__(self, name):

        self.name = name
        self.clients = {}

        # Alerts
        print(f"Room {self.name} has been created")

    # New client in room
    def new_connection(self, client):

        self.clients[client.socket] = client

        # Alerts
        client.send_to_all(f"{client.name} join the room", self.clients)
        print(f"{client.name} join the {self.name}")

    # Remove client from room and global
    def remove_connection(self, client):

        # Alerts
        print(f"{client.name} leave the room")

        # Remove from room
        self.clients.pop(client.socket)

        # Remove global
        socket_list.remove(client.socket)
        clients.pop(client.socket)

    def room_activity(self, client):

        # Receive and get messages
        data = client.get_data()

        if not data:
            self.remove_connection(client)
        else:
            client.send_to_all(f"{client.name} {client.address[1]} >>> {data}", self.clients)


class Client(User):

    # Create new client
    def __init__(self):

        self.socket, self.address = server_socket.accept()
        self.name = False
        self.room = False
        self.is_send = False
        self.socket.setblocking(False)

    def set_name(self):

        try:
            if not self.is_send:  # Send once
                self.send_data("Enter your name")
                self.is_send = True

            self.name = self.get_data()

            if not self.name:  # If no input from client
                return

            self.is_send = False

            # Alerts
            print(f"User {self.address[1]} chose the name {self.name}")
        except:
            return False

    def set_room(self):

        try:
            if not self.is_send:  # Send once
                self.send_data("Select a room to join")
                self.is_send = True

            self.room = self.get_data()

            if not self.room:  # If no input from client
                return

            if self.room not in rooms:  # Create new room
                room = Room(self.room)
                rooms.update({self.room: room})
                room.new_connection(self)
            else:  # Connect to existing one
                room = rooms[self.room]
                room.new_connection(self)
                self.room = self.room
            self.is_send = False
        except:
            return False

    # Send data to all users except our
    def send_to_all(self, data, to_clients):

        for client_socket, client in to_clients.items():
            if client_socket != self.socket:  # Except our
                client.send_data(data)


# Server setup
server_socket = socket.socket()
server_socket.bind((IP, PORT))
server_socket.listen(5)

# Main variables
clients = dict()
socket_list = [server_socket, sys.stdin]
rooms = dict()

# Logic
while True:

    server_socket.setblocking(False)  # Don't stop
    sockets, _, _ = select.select(socket_list, [], [], 0)

    for i_socket in sockets:

        if i_socket == server_socket:
            client = Client()

            clients.update({client.socket: client})
            socket_list.append(client.socket)

            # Alerts
            print(f"New user has successfully connected to the server. [{client.address[1]}]")
            client.send_data("You are in!!")

        elif i_socket == sys.stdin:
            data = input()

            if data:
                for client in clients.values():
                    client.send_data(f"server >>> {data}")

        else:
            client = clients[i_socket]

            if client.name and client.room:
                room = rooms[client.room]
                room.room_activity(client)

    # Set name and room to all connections
    for client in clients.values():

        if not client.name:
            client.set_name()
            continue

        if not client.room:
            client.set_room()
            continue
