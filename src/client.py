import socket
import pickle
import select
import sys

# Задача основных значений
PORT = 9090  # Порт соединения с сервером
IP = socket.gethostname()  # Получение локального IP
DATA_LENGTH = 10  # Задаёт максиальное кол-во байт для передачи


# Отправка данных серверу
def send_data(data):
    data = pickle.dumps(data)  # Первод данных в байты
    data = bytes(f"{len(data):<{DATA_LENGTH}}", "utf-8") + data  # Добавление длинны данных
    client_socket.send(data)  # Отпрвака данных серверу


# Получение данных от сервера
def get_data():
    # Если данные не были получены, то вернем False
    try:
        len_message = int(client_socket.recv(DATA_LENGTH).decode("utf-8"))  # Получаем длину данных
        data = client_socket.recv(len_message)  # Получаем данные заданной длинны
        data = pickle.loads(data)  # Преобразуем данные из байт обратно в объект
        return data
    except:
        return False


# Подключение к серверу
client_socket = socket.socket()  # Получаем сокет клиента
client_socket.connect((IP, PORT))  # Подключаемся к серверу с IP, PORT
client_socket.setblocking(False)  # Не тормозим

while True:

    # Либо отпраляем, либо получаем
    reads, _, _ = select.select([client_socket, sys.stdin], [], [])
    for i in reads:
        if i == client_socket:
            data = get_data()
            if data:
                print(data)
        else:
            data = input()
            if data:
                send_data(data)
