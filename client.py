import socket
import threading

HOST = "127.0.0.1"
PORT = 55555

def send_message():
    while True:
        input_message = input()
        if input_message == 'exit':
            chat_socket.close()
            exit(0)
        chat_socket.send(input_message.encode())

def receive_message():
    while True:
        received_message = chat_socket.recv(1024)
        print(received_message.decode())
        print('> ', end='')

chat_socket = socket.socket()
chat_socket.connect((HOST, PORT))

name = input("Введите Ваш никнейм: ")
chat_socket.send(name.encode())

send_thread = threading.Thread(target=send_message)
send_thread.start()

receive_thread = threading.Thread(target=receive_message)
receive_thread.start()
