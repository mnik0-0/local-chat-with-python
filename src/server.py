import socket
import pickle
import select

# Задача основных значений
PORT = 9090  # Порт соединения с сервером
IP = socket.gethostname()  # Получение локального IP


# Создание класса клиента
class Client:

    # Конструктор класса
    def __init__(self, socket_, address):
        # Инициализация параметров
        self.socket = socket_  # Сокет клиента
        self.address = address  # Адрес клиента


# Настройка сервера
server_socket = socket.socket()  # Получаем сокет сервера
server_socket.bind((IP, PORT))  # Настраиваем подключение через IP, PORT
server_socket.listen(5)  # Задаём максимальное число подключений

# Принимаем подключение
client_socket, client_address = server_socket.accept()  # Принимаем подключение
client = Client(client_socket, client_address)  # Создаем нового пользователя

print("Клиент подключён")

# Чтобы сервер не закрывался
while True:
    pass
