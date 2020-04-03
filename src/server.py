import socket
import pickle
import select
import sys

# Задача основных значений
PORT = 9090  # Порт соединения с сервером
IP = socket.gethostname()  # Получение локального IP
DATA_LENGTH = 10  # Задаёт максиальное кол-во байт для передачи


class Room:

    # Конструктор класса
    def __init__(self, name):

        self.name = name  # Задаём имя
        self.clients = dict()  # Создём словарь клиентов внутри комнаты

        # Оповещения
        print(f"Создана комната {self.name}")

    # Добавление нового клиента в комнату
    def new_connection(self, client):
        self.clients.update({client.socket: client})  # Добавляем клиента в словарь

        # Оповещения
        client.send_to_all(f"Пользователь {client.name} присоединился к комнате", self.clients)
        print(f"Пользователь {client.name} подключился к {self.name}")

    # Удаление клиента из комнаты и глобально
    def remove_connection(self, client):

        # Оповещения
        print(f"Пользователь {client.name} вышел")

        # Удаление из комнаты
        self.clients.pop(client.socket)

        # Удаление глобально
        socket_list.remove(client.socket)
        clients.pop(client.socket)

    # Активность внутри комнаты
    def room_activity(self, client):

        # Получаем и отправляем сообщения
        data = client.get_data()

        if not data:
            self.remove_connection(client)  # Если пользователь отключился, удаляем подключение
        else:
            client.send_to_all(f"{client.name} {client.address[1]} >>> {data}", self.clients)


class Client:

    # Конструктор класса
    def __init__(self):

        # Инициализация параметров
        self.socket, self.address = server_socket.accept()  # Принимаем подключение
        self.name = False  # Имя не задаём
        self.room = False  # Комнату не задаём
        self.is_send = False  # Отправлено ли сообщение
        self.socket.setblocking(False)  # Не ждём данных

    # Задаёт имя клиенту
    def set_name(self):

        try:
            if not self.is_send:  # Если сообщение еще не отправлено, то отправить
                self.send_data("Введите своё имя")
                self.is_send = True

            self.name = self.get_data()

            if not self.name:  # Если пользователь не ввел имя тогда прекращаем выполнение
                return

            self.is_send = False  # Ставим значание по умолчанию

            # Оповещения
            print(f"Пользователь {self.address[1]} выбрал имя {self.name}")
        except:
            return False

    # Задаёт комнату клиенту
    def set_room(self):

        try:
            if not self.is_send:  # Если сообщение еще не отправлено, то отправить
                self.send_data("Выберите комнату к которой хотите присоедениться")
                self.is_send = True

            self.room = self.get_data()

            if not self.room:  # Если пользователь не ввел имя комнаты тогда прекращаем выполнение
                return

            if self.room not in rooms:  # Если комнаты с таким именем еще не существует, то создаём ее
                room = Room(self.room)
                rooms.update({self.room: room})  # Новая комната
                room.new_connection(self)  # Новый клиент
            else:  # Если же она уже существует
                room = rooms[self.room]
                room.new_connection(self)  # Новый клиент
                self.room = self.room
            self.is_send = False  # Ставим значание по умолчанию
        except:
            return False

    # Отправка данных клиенту
    def send_data(self, data):

        data = pickle.dumps(data)  # Первод данных в байты
        data = bytes(f"{len(data):<{DATA_LENGTH}}", "utf-8") + data  # Добавление длинны данных
        self.socket.send(data)  # Отпрвака данных серверу

    # Отправляет сообщение всем пользователям, кроме отправителя
    def send_to_all(self, data, to_clients):

        for client_socket, client in to_clients.items():  # Перебор всех пользоваетелей
            if client_socket != self.socket:  # Кроме нашего
                client.send_data(data)

    # Получение данных от клиента
    def get_data(self):

        try:
            len_message = int(self.socket.recv(DATA_LENGTH).decode("utf-8"))  # Получаем длину данных
            data = self.socket.recv(len_message)  # Получаем данные заданной длинны
            data = pickle.loads(data)  # Преобразуем данные из байт обратно в объект
            return data
        except:
            return False


# Настройка сервера
server_socket = socket.socket()  # Получаем сокет сервера
server_socket.bind((IP, PORT))  # Настраиваем подключение через IP, PORT
server_socket.listen(5)  # Задаём максимальное число подключений

# Для работы с клиентами и комнатами
clients = dict()
socket_list = [server_socket, sys.stdin]
rooms = dict()

# Логика
while True:

    server_socket.setblocking(False)  # Не тормозим
    sockets, _, _ = select.select(socket_list, [], [], 0)  # Прослушиваем все подключения

    for i_socket in sockets:  # Пробегаемся по ним

        if i_socket == server_socket:  # Если такого подключения еще нет
            client = Client()  # Создаем нового клиента

            clients.update({client.socket: client})  # Добавляем в список клиентов
            socket_list.append(client.socket)  # Добавляем сокет клинта

            # Оповещения
            print(f"Новый пользователь присоединился {client.address[1]}")
            client.send_data("Вы успешно подключились к серверу")

        elif i_socket == sys.stdin:  # Если сервер хочет отправить сообщение
            data = input()

            if data:
                for client in clients.values():
                    client.send_data(f"server >>> {data}")

        else:  # Если такое подключение уже существует
            client = clients[i_socket]  # Получаем клинта

            if client.name and client.room:  # Прооверка на имя и комнату
                room = rooms[client.room]
                room.room_activity(client)

    # У всех ли клиентов есть имя и комната
    for client in clients.values():

        if not client.name:  # Если его имя не задано
            client.set_name()
            continue

        if not client.room:  # Если его комната не задана
            client.set_room()
            continue
