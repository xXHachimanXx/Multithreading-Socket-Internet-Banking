import socket
import threading
from time import sleep
from threading import Thread
from threading import Lock
import multiprocessing
import queue

HOST = '127.0.0.1'
PORT = 65432

class DataReceiver(Thread):
    def __init__(self, socket):
        self.socket = socket
        super().__init__()

    def run(self) -> None:
        while True:
            conn, addr = self.socket.accept()
            with conn:
                print('Connected by', addr)
                alldata = bytes()
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    alldata += data
                print('Received #', threading.get_ident(), repr(alldata))
                conn.sendall(alldata)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f'Listening on {HOST}:{PORT}')
    for i in range(multiprocessing.cpu_count()):
        DataReceiver(s).start()

class AccountDatabase:
    def __init__(self):
        pass

    def get_get_id(self):
        pass

    def update_by_id(self):
        pass

class AccountService:
    def __init__(self, queue: queue.Queue, database):
        self.queue = queue
        # network layer
        op = { 'account': 123, 'type': 'deposit', 'value': 200 }
        def response(value: any):
            value.to_bytes()
            sock.sendall(value)
        self.queue.put((op, response))
        # service layer
        obj, response = self.queue.get()
        if obj.type == 'deposit':
            response({
                account: 1,
                saldo: 500
            })
            self.queue.task_done()
