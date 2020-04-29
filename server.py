import socket
import select
import sys

import src.Variables as Variables
import src.User as User
import src.Commands as Commands

# Main variables
PORT = 9090
IP = socket.gethostname()


class Client(User.User):

    # Create new client
    def __init__(self):

        self._socket, self._address = server_socket.accept()
        self._name = False
        self._room = False
        self._is_send = False
        self._socket.setblocking(False)

    @property
    def name(self):
        return self._name

    @property
    def socket(self):
        return self._socket

    @property
    def address(self):
        return self._address

    @property
    def room(self):
        return self._room

    def clear_room_name(self):
        self._room = False

    def set_name(self):

        try:
            if not self._is_send:  # Send once
                self.send_data("Enter your name")
                self._is_send = True

            self._name = self.get_data()

            if not self._name:  # If no input from client
                return

            self._is_send = False

            # Alerts
            print(f"User {self._address[1]} chose the name {self._name}")
        except:
            return False

    def set_room(self):

        try:
            if not self._is_send:  # Send once
                self.send_data("Select a room to join")
                self._is_send = True

            self._room = self.get_data()

            if not self._room:  # If no input from client
                return

            if self._room not in variables.rooms:  # Create new room
                room = Room(self._room)
                variables.add_room(room)
                room.new_connection(self)
            else:  # Connect to existing one
                room = variables.get_room(self)
                room.new_connection(self)
            self._is_send = False
        except:
            return False

    # Send data to all users except our
    def send_to_all(self, data, to_clients):

        for client_socket, client in to_clients.items():
            if client_socket != self._socket:  # Except our
                client.send_data(data)


class Room:

    # Create new room
    def __init__(self, name):

        self._name = name
        self._clients = {}

        # Alerts
        print(f"Room {self._name} has been created")

    @property
    def name(self):
        return self._name

    # New client in room
    def new_connection(self, client: Client):

        self._clients[client.socket] = client

        # Alerts
        client.send_to_all(f"{client.name} join the room", self._clients)
        print(f"{client.name} join the {self._name}")

    # Remove client from room and global
    def remove_connection(self, client: Client):

        # Alerts
        print(f"{client.name} leave the room")

        # Remove from room
        self._clients.pop(client.socket)

        variables.check_room(self)

        """# Remove global
        variables.remove_client(client)
        variables.remove_socket(client)"""

    def room_activity(self, client: Client):

        # Receive and get messages
        data = client.get_data()

        if data is None:
            self.remove_connection(client)
            variables.remove_client(client)
            variables.remove_socket(client)
        else:
            if data not in commands.commands:
                client.send_to_all(f"{client.name} {client.address[1]} >>> {data}", self._clients)
            else:
                commands.command(client, self, data)

    def is_empty(self):
        if self._clients:
            return False
        return True


# Server setup
server_socket = socket.socket()
server_socket.bind((IP, PORT))
server_socket.listen(5)

# Main variables
variables = Variables.Variables(server_socket)
commands = Commands.Commands()

# Logic
while True:

    server_socket.setblocking(False)  # Don't stop
    sockets, _, _ = select.select(variables.socket_list, [], [], 0)

    for i_socket in sockets:

        if i_socket == server_socket:
            client = Client()

            variables.add_client(client)
            variables.add_socket(client)

            # Alerts
            print(f"New user has successfully connected to the server. [{client.address[1]}]")
            client.send_data("You are in!!")

        elif i_socket == sys.stdin:
            data = input()

            if data:

                for client in variables.clients.values():
                    client.send_data(f"server >>> {data}")

        else:
            client = variables.get_client(i_socket)

            if client.name and client.room:
                room = variables.get_room(client)
                room.room_activity(client)

    # Set name and room to all connections
    for client in variables.clients.values():

        if not client.name:
            client.set_name()
            continue

        if not client.room:
            client.set_room()
            continue
