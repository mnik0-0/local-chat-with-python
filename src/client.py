import socket
import pickle
import select

# Задача основных значений
PORT = 9090  # Порт соединения с сервером
IP = socket.gethostname()  # Получение локального IP

# Подключение к серверу
client_socket = socket.socket()  # Получаем сокет клиента
client_socket.connect((IP, PORT))  # Подключаемся к серверу с IP, PORT
client_socket.setblocking(False)  # Non-blocking

# Чтобы клиент не закрывался
while True:
    pass
