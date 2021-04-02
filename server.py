import queue
from threading import Thread
from database.AccountDatabase import AccountDatabase
from services.AccountService import AccountService

database = AccountDatabase()

queues = [queue.Queue(), queue.Queue()]
AccountService(queues[0], database).start()
AccountService(queues[1], database).start()

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

def run(func, operation_type, value, account_number):
    index = account_number % len(queues)
    t = Thread(target=func, args=((value, account_number, operation_type, queues[index])))
    t.start()

run(do_operation, 'deposit', 100, 0)
run(do_operation, 'withdrawal', 100, 0)
run(do_operation, 'deposit', 200, 1)
run(do_operation, 'deposit', 300, 0)
run(do_operation, 'withdrawal', 100, 1)
