import queue
# import thread module
from _thread import *
import threading
from threading import Thread
from database.AccountDatabase import AccountDatabase
from services.AccountService import AccountService
import multiprocessing
import queue
import json
import socket

HOST = '127.0.0.1'
PORT = 3333
database = AccountDatabase()
queues = []

class DataReceiver(Thread):
   def __init__(self, conn, addr):
      self.conn = conn
      self.addr = addr
      super().__init__()

   def run(self) -> None:
         with conn:
               # lock acquired by client
               print('Connected by', addr)
               alldata = bytes()
               while True:
                  data = conn.recv(1024)
                  if not data:
                     break
                  alldata += data
               
               print('Received #', threading.get_ident(), repr(alldata))
               
               # client data to string
               operation = json.loads(alldata.decode('utf-8'))
               sendToQueue(operation)
               # conn.sendall(alldata)

   def sendToQueue(operation: object):
      account_number = operation["account_number"]
      operation_type = operation["type"]
      value = operation["value"]

      index = account_number % len(queues)
      t = AccountService(target=func, args=((value, account_number, operation_type, queues[index])))
      t.start()

   
   def do_operation(value: int, account_number: int, operation_type: str, q: queue.Queue):
      operation = {
         'account_number': account_number,
         'type': operation_type,
         'value': value
      }

   def response(value: object):
      print(operation)
      print('result', value)
      print('-----------------------')
      q.put((operation, response)) 

# def run(func, operation_type, value, account_number):
#     index = account_number % len(queues)
#     t = AccountService(target=func, args=((value, account_number, operation_type, queues[index])))
#     t.start()


def Main():

   # create queues, AccoutServices and database
   for i in range(multiprocessing.cpu_count()):
      queues.append(queue.Queue()) 
      AccountService(queues[i], database).start()

   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.bind((HOST, PORT))
      s.listen()
      print(f'Listening on {HOST}:{PORT}')

      while True:
         # establish connection with client
         conn, addr = s.accept()

      for i in range(multiprocessing.cpu_count()):
         DataReceiver(conn, addr).start()

Main()


# run(do_operation, 'deposit', 100, 0)
# run(do_operation, 'withdrawal', 100, 0)
# run(do_operation, 'deposit', 200, 1)
# run(do_operation, 'deposit', 300, 0)
# run(do_operation, 'withdrawal', 100, 1)
