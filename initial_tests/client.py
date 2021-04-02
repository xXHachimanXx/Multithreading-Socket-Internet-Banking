import socket
import threading
from threading import Thread
import multiprocessing

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65432

def send_data():
    with socket.create_connection((SERVER_HOST, SERVER_PORT)) as sock:
        msg = f'Hello, world {threading.get_ident()}'
        sock.sendall(msg.encode('utf-8'))
        print(msg)
        alldata = bytes()
        while True:
            data = sock.recv(1024)
            if not data:
                break
            alldata += data
        print('Received', repr(alldata))

for i in range(multiprocessing.cpu_count()):
    Thread(target=send_data).start()
