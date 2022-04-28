from typing import List

import os

class Account:
    account_id : str
    balance : int

    def __init__(self, account_id : str, balance : int = 0):
        self.account_id = account_id
        self.balance = balance
        
class IncompleteTransaction:
    account_id : str
    residue : int
    completed : bool

    def __init__(self, account_id : str, residue : int, completed : bool = False):
        self.account_id = account_id
        self.residue = residue
        self.completed = completed

class Session:
    card_id : str
    list_accounts : List[Account]
    action : str
    session_token : str

class ATMModel:
    user_session : Session
    machine_master_session_token : str
    list_incomplete_transactions : List[IncompleteTransaction]

    def __init__(self):
        self.clear()
        self.machine_master_session_token = os.environ['MACHINE_MASTER_SESSION_TOKEN']
        self.list_incomplete_transactions=[]
        
    def clear(self):
        self.user_session = Session()

    def append_incomplete_transaction(self, account_id: str, residue : int):
        self.list_incomplete_transactions.append(
            IncompleteTransaction(
                account_id=account_id,
                residue=residue,
                completed=False
            )
        )

    def clear_completed_transactions(self):
        new_list_incomplete_transactions=[]
        for transaction in self.list_incomplete_transactions:
            if not transaction.completed:
                new_list_incomplete_transactions.append(transaction)

        self.list_incomplete_transactions = new_list_incomplete_transactions

    def get_account(self, account_id):
        for account in self.user_session.list_accounts:
            if account.account_id == account_id:
                return account

        return None
        
            

