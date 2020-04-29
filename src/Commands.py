class Commands:

    def __init__(self):
        self._commands = {"!left": self.left}

    @property
    def commands(self):
        return self._commands

    def command(self, client, room, com):
        self._commands[com](self, client, room)

    @staticmethod
    def left(self, client, room):
        room.remove_connection(client)
        client.clear_room_name()
