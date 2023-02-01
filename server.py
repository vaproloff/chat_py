import socket
import threading

HOST = "127.0.0.1"
PORT = 55555

def hold_connection(connection, address):
    with connection:
        print(f"{address} connected")
        username = connection.recv(1024).decode()
        mailing(f"{username} joined chat")
        while True:
            try:
                data = connection.recv(1024)
                if not data.decode() == b'':
                    mailing(f'{username} -> {data.decode()}')
            except socket.error:
                print(f"{address} disconnected")
                clients.pop(address)
                mailing(f"{username} has left.")
                return

def mailing(message):
    for conn in clients.values():
        conn.send(message.encode())
    print(f'> {message}')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as chat_socket_srv:
    chat_socket_srv.bind((HOST, PORT))
    chat_socket_srv.listen()
    print(f'Server listening on {HOST}:{PORT}...')
    clients = {}

    while True:
        connection, address = chat_socket_srv.accept()
        if not clients.get(address):
            clients[address] = connection
        connection_thread = threading.Thread(target=hold_connection, args=[connection, address])
        connection_thread.start()
