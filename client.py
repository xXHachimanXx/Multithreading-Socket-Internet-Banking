import sys
import json
import socket
import threading
from threading import Thread

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 3333

class Client:
    def __init__(self, operation):
        self.operation = operation
        self.send_operation(operation)

    def send_operation(self, operation):
        with socket.create_connection((SERVER_HOST, SERVER_PORT)) as sock:
            msg = json.dumps(operation)
            sock.send(msg.encode('utf-8'))

            print(f'Thread #{threading.get_ident()} - sending', msg)
            
            data = sock.recv(1024)

            print("-------------RESPONSE-------------")
            print(data.decode('utf-8'))

# def send_operation(self, operation):
#     with socket.create_connection((SERVER_HOST, SERVER_PORT)) as sock:
#         msg = json.dumps(operation)
#         sock.sendall(msg.encode('utf-8'))
#         print(f'Thread #{threading.get_ident()} - sending', msg)
#         alldata = bytes()
#         while True:
#             data = sock.recv(1024)
#             if not data:
#                 break
#             alldata += data
#         print(f'Thread #{threading.get_ident()} - received', repr(alldata))

account_number = int(sys.argv[1]) or 0
op_type = sys.argv[2] or 'deposit'
value = float(sys.argv[3]) or 100
operation = {
    'account_number': account_number,
    'type': op_type,
    'value': value
}
Client(operation)

# Thread(target=send_operation, args=((operation,))).start()

# operation = { 'account_number': 0, 'type': 'withdrawal', 'value': 100 }
# Thread(target=send_operation, args=((operation,))).start()

# operation = { 'account_number': 1, 'type': 'deposit', 'value': 200 }
# Thread(target=send_operation, args=((operation,))).start()

# operation = { 'account_number': 0, 'type': 'deposit', 'value': 300 }
# Thread(target=send_operation, args=((operation,))).start()

# operation = { 'account_number': 1, 'type': 'withdrawal', 'value': 100 }
# Thread(target=send_operation, args=((operation,))).start()
