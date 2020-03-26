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

    # Отправка данных серверу
    def send_data(self, data):
        data = pickle.dumps(data)  # Первод данных в байты
        data = bytes(f"{len(data):<{DATA_LENGTH}}", "utf-8") + data  # Добавление длинны данных
        self.socket.send(data)  # Отпрвака данных серверу

    # Получение данных от сервера
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
        data = client.get_data()
        if data:
            print(data)


# Ввод
def input_thread():
    while True:
        data = input()
        client.send_data(data)


# Настройка сервера
server_socket = socket.socket()  # Получаем сокет сервера
server_socket.bind((IP, PORT))  # Настраиваем подключение через IP, PORT
server_socket.listen(5)  # Задаём максимальное число подключений

# Принимаем подключение
client_socket, client_address = server_socket.accept()  # Принимаем подключение
client = Client(client_socket, client_address)  # Создаем нового пользователя

print("Клиент подключён")

# Чтобы сервер не закрывался

threading.Thread(target=output_thread).start()  # Получение данных
threading.Thread(target=input_thread).start()  # Ввод
