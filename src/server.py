import socket
import pickle
import threading
import select

# Задача основных значений
PORT = 9090  # Порт соединения с сервером
IP = socket.gethostname()  # Получение локального IP
DATA_LENGTH = 10  # Задаёт максиальное кол-во байт для передачи


# Создание класса клиента
class Client:

    # Конструктор класса
    def __init__(self, socket_, address):
        # Инициализация параметров
        self.socket = socket_  # Сокет клиента
        self.address = address  # Адрес клиента
        self.name = False  # Имя не задаём

    # Задаёт имя пользователю
    def set_name(self):
        self.name = self.get_data()

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
        # Если данные не были получены, то вернем False
        try:
            len_message = int(self.socket.recv(DATA_LENGTH).decode("utf-8"))  # Получаем длину данных
            data = self.socket.recv(len_message)  # Получаем данные заданной длинны
            data = pickle.loads(data)  # Преобразуем данные из байт обратно в объект
            return data
        except:
            return False


# Получение данных
def output_thread():
    while True:
        sockets, _, _ = select.select(socket_list, [], [])  # Прослушиваем все подключения
        for i_socket in sockets:  # Пробегаемся по ним
            if i_socket == server_socket:  # Если такого подключения еще нет
                # Принимаем подключение
                client_socket, client_address = server_socket.accept()  # Принимаем подключение
                client = Client(client_socket, client_address)  # Создаем нового пользователя

                clients.update({client.socket: client})  # Добавляем в список пользоваетелей
                socket_list.append(client.socket)  # Добавляем сокет пользователя
                print(f"Новый пользователь присоединился {client.address[1]}")

                if not client.name:  # Если его имя не задано

                    client.send_data("Введите своё имя")
                    client.set_name()  # Устанавливаем ему имя

                    # Оповещаем о подключении
                    print(f"Пользователь {client.address[1]} выбрал имя {client.name}")
                    client.send_to_all(f"Пользователь {client.name} присоеденился", clients)
                    continue

            else:  # Если такое подключение уже существует
                client = clients[i_socket]  # Получаем пользователя

                # Получаем и отправляем сообщения
                data = client.get_data()
                if not data:
                    socket_list.remove(client.socket)
                    clients.pop(client.socket)
                    print(f"Пользователь {client.name} вышел")
                else:
                    client.send_to_all(f"{client.name} {client.address[1]} >>> {data}", clients)


# Ввод
def input_thread():
    while True:
        data = input()
        if data:
            for client in clients.values():
                client.send_data(f"server >>> {data}")


# Настройка сервера
server_socket = socket.socket()  # Получаем сокет сервера
server_socket.bind((IP, PORT))  # Настраиваем подключение через IP, PORT
server_socket.listen(5)  # Задаём максимальное число подключений

# Для работы с клиентами
clients = dict()
socket_list = [server_socket]

# Чтобы сервер не закрывался
threading.Thread(target=output_thread).start()  # Получение данных
threading.Thread(target=input_thread).start()  # Ввод
