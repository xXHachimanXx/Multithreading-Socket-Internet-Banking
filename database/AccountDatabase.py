import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from typing import Dict
from models.Account import Account

class AccountDatabase:
    def __init__(self):
        self.data: Dict[int, Account] = {
            0: Account(0),
            1: Account(1)
        }

    def get_by_number(self, number: int) -> Account:
        return self.data[number]

    def update_by_number(self, number: int, account: Account) -> Account:
        self.data[number] = account
        return account
