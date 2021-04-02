import json
import socket
import threading
from threading import Thread

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65432

def send_operation(operation):
    with socket.create_connection((SERVER_HOST, SERVER_PORT)) as sock:
        msg = json.dumps(operation)
        sock.sendall(msg.encode('utf-8'))
        print(f'Thread #{threading.get_ident()} - sending', msg)
        alldata = bytes()
        while True:
            data = sock.recv(1024)
            if not data:
                break
            alldata += data
        print(f'Thread #{threading.get_ident()} - received', repr(alldata))

operation = { 'account_number': 0, 'type': 'deposit', 'value': 100 }
Thread(target=send_operation, args=((operation,))).start()

operation = { 'account_number': 0, 'type': 'withdrawal', 'value': 100 }
Thread(target=send_operation, args=((operation,))).start()

operation = { 'account_number': 1, 'type': 'deposit', 'value': 200 }
Thread(target=send_operation, args=((operation,))).start()

operation = { 'account_number': 0, 'type': 'deposit', 'value': 300 }
Thread(target=send_operation, args=((operation,))).start()

operation = { 'account_number': 1, 'type': 'withdrawal', 'value': 100 }
Thread(target=send_operation, args=((operation,))).start()
