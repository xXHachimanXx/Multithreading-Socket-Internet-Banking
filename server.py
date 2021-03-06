import queue
from _thread import *
import threading
from threading import Thread
from database.AccountDatabase import AccountDatabase
from services.AccountService import AccountService
import multiprocessing
import queue
import json
import socket

class DataReceiver(Thread):
   def __init__(self, conn, addr, queues):
      self.conn = conn
      self.addr = addr
      self.queues = queues
      super().__init__()

   def run(self) -> None:
      # lock acquired by client
      print('Connected by', self.addr)
      
      data = self.conn.recv(1024)

      print('Received #', threading.get_ident(), data.decode('utf-8'))
      
      # client data to string
      operation = json.loads(data.decode('utf-8'))
      self.send_to_queue(operation)
      # conn.sendall(alldata)

   def send_to_queue(self, operation: object):
      account_number = operation["account_number"]
      operation_type = operation["type"]
      value = operation["value"]

      def response(value: object):
         msg = json.dumps(value)

         print('result', value)
         print('-----------------------')
         
         self.conn.sendall(msg.encode('utf-8'))
         self.conn.close()
         # send_to_client

      index = account_number % len(self.queues)
      self.queues[index].put((operation, response)) 


class Server(Thread):
   def __init__(self, host, port):
      self.HOST = host #'127.0.0.1'
      self.PORT = port #3333
      self.database = AccountDatabase()
      self.queues = []
      super().__init__()

   def init_queues_and_account_services(self):
      # create queues, AccoutServices and database
      for i in range(multiprocessing.cpu_count()):
         self.queues.append(queue.Queue())
         AccountService(self.queues[i], self.database).start()

   def open_socket_to_listen_requests(self):
       with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
         s.bind((self.HOST, self.PORT))
         s.listen()
         print(f'Listening on {self.HOST}:{self.PORT}')

         while True:
            # establish connection with client
            conn, addr = s.accept()
            self.send_to_some_data_receiver(conn, addr)

   def run(self) -> None:
      self.init_queues_and_account_services()
      self.open_socket_to_listen_requests()

   def stop(self):
        self.__tcpListener.shutdown(socket.SHUT_RDWR)
        time.sleep(1)
        print("Thread: User searching will quit NOW!")

   def send_to_some_data_receiver(self, conn, addr):
      t = DataReceiver(conn, addr, self.queues)
      t.start()


def Main():
   HOST = '127.0.0.1'
   PORT = 3333  
   Server(HOST, PORT).start()


Main()
