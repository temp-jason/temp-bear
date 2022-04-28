from typing import List

from .model import Account
from .const import DEFAULT_TIMEOUT

def show_init_prompt():
    pass

def show_input_pin_code_prompt(num_trial : int = 0):
    pass

def show_human_intervention_needed_prompt():
    pass

def show_accounts(accounts : List[Account]):
    pass

def show_account_info(account : Account):
    pass

def show_not_enough_money(timeout : int = DEFAULT_TIMEOUT):
    pass

def show_deposit_prompt():
    pass

def show_withdraw_prompt():
    pass

def show_bye_prompt():
    pass

def show_result_prompt():
    pass

def show_transaction_result(transaction_result, timeout : int = DEFAULT_TIMEOUT):
    pass
