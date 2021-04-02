import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import queue
from typing import Dict, Callable
from threading import Thread
from database.AccountDatabase import AccountDatabase

class AccountService(Thread):
    def __init__(self, queue: queue.Queue, database: AccountDatabase):
        super().__init__()
        self.queue = queue
        self.database = database
        self.operations = {
            'deposit': self.deposit,
            'withdrawal': self.withdrawal,
        }

    def run(self) -> None:
        while True:
            operation, response = self.queue.get()
            func = self.operations[operation['type']]
            if func == None:
                response({ 'error': 'Invalid operation' })
            else:
                func(operation, response)
            self.queue.task_done()

    def withdrawal(self, operation: object, response: Callable[[object], None]):
        account = self.database.get_by_number(operation['account_number'])
        if account == None:
            response({ 'error': 'Account not found' })
        elif account.balance - operation['value'] < 0:
            response({ 'error': 'Insufficient balance' })
        else:
            account.balance -= operation['value']
            self.database.update_by_number(operation['account_number'], account)
            response(vars(account))
    
    def deposit(self, operation: object, response: Callable[[object], None]):
        account = self.database.get_by_number(operation['account_number'])
        if account == None:
            response({ 'error': 'Account not found' })
        else:
            account.balance += operation['value']
            self.database.update_by_number(operation['account_number'], account)
            response(vars(account))
