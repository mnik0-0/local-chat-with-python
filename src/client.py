import socket
import pickle
import threading

# Задача основных значений
PORT = 9090  # Порт соединения с сервером
IP = socket.gethostname()  # Получение локального IP
DATA_LENGTH = 10  # Задаёт максиальное кол-во байт для передачи
LOGGED_IN = False  # Ввёл пользователь имя или нет
INPUT = True  # Можно ли пользователю отправлять сообщения или нет


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


# Получение данных
def output_thread():
    global LOGGED_IN
    global INPUT
    while True:
        data = get_data()
        if not LOGGED_IN and not data:  # Елси до пользователя еще не дошла очередь
            print("Подождите пока придет ваша очередь")
            INPUT = False  # Запрещаем ему отправлять сообщения
            while not data:  # До тех пор пока до нас не дойтёт очередь
                data = get_data()
        if data:
            LOGGED_IN = True  # Пользователь вошёл
            INPUT = True  # Разрешаем отправлять
            print(data)


# Ввод
def input_thread():
    global INPUT
    while True:
        data = input()
        if data and INPUT:
            send_data(data)


# Подключение к серверу
client_socket = socket.socket()  # Получаем сокет клиента
client_socket.connect((IP, PORT))  # Подключаемся к серверу с IP, PORT
client_socket.setblocking(False)  # Non-blocking

# Поток для обработки ввода и получения сообщений
threading.Thread(target=input_thread).start()  # Ввод
threading.Thread(target=output_thread).start()  # Получение данных
