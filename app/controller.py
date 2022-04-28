
import logging
from .model import ATMModel, IncompleteTransaction

from .phony_hardware_apis import *
from .view import *
from .exceptions import *
from .utils import encode, decode


class ATMController:
    def __init__(self, log_file_path='controller.log'):
        logging.basicConfig(format='%(asctime)s %(message)s', filename=log_file_path, level=logging.INFO)
        self.model = ATMModel()
        
    def _fallback(self):
        # Update Model
        self.model.clear()
        try:
            eject_card()
            close_cash_bin()

        # Update View   
        except HumanInterventionNeededError:
            show_human_intervention_needed_prompt()

        show_init_prompt()
    

    def _call_server_api(self, method, url, data, **params):
        """
        TODO: implement (mock) api call to the server
        ex)

        data = encode(data)
        res = call_grpc()
        res = decode(res)
        return res
        """
        return {
            'return_code' : 404,
            'session_token' : 'phony_session_token'
        }
        


    def callback_card_inserted(self, card_id : str):
        if not card_id:
            self._fallback()
            return

        # Update Model
        self.model.user_session.card_id = card_id
        
        # Update View
        show_input_pin_code_prompt(num_trial=0)


        # TODO: logging
        # ex) logging.info(f"card_id : {card_id}, inserted and read")


    def callback_pin_code_inputted(self, pin_code, num_trial):
        res = self._call_server_api(
            method="POST",
            url="/login",
            data={
                "card_id": self.model.user_session.card_id,
                "pin_code": pin_code
            }
        )

        if res['session_token'] is None:
            if num_trial + 1 < MAX_PIN_CODE_TRIAL:
                # Update View
                show_input_pin_code_prompt(num_trial=num_trial+1)
            else:
                self._fallback()
        else:
            # Update Model
            self.model.user_session.session_token = res['session_token']

            res = self._call_server_api(
                method="GET",
                url="/accounts",
                data={
                    "card_id": self.model.user_session.card_id,
                }
            )
            if res["return_code"] != 404:
                self._fallback()
                
            # Update Model
            self.model.user_session.list_accounts = res.get('list_accounts', [Account(account_id='phony_account_id', balance=0),])
            
            # Update View
            show_accounts(self.model.user_session.list_accounts)


    def callback_account_and_action_selected(self, account_id : str, action : str, amount : int = 0):
        account = self.model.get_account(account_id)
        if not account:
            self._fallback()
            return

        if action=="see_balance":
            show_account_info(account.balance)
        elif action=="deposit":
            show_deposit_prompt()
            open_cash_bin()
            # see `callback_cash_bin_closed` for the next step

            return       
        elif action=="withdraw":
            if not amount or amount <=0:
                self._fallback()

            if account.balance < amount:
                show_not_enough_money(timeout=NOT_ENOUGH_MONEY_PROMPT_TIMEOUT)

                # Go back to the list of accounts
                show_account_info(account)
                return
            
            show_withdraw_prompt()

            res = self._call_server_api(
                method='POST',
                url='/withdraw',
                data={
                    'account_id': account_id,
                    'amount' : amount
                }
            )
            if res["return_code"] != 404:
                self._fallback()
            
            open_cash_bin(amount = amount)
            # see `callback_cash_bin_closed` for the next step
            return           
        else:
            raise NotImplementedError


    def callback_cash_bin_closed(self, account_id : str, action : str, amount : int):
        if action=="deposit":
            res = self._call_server_api(
                method='POST',
                url='/deposit',
                data={
                    'account_id' : account_id,
                    'amount' : amount
                }
            )
            show_transaction_result(res)

            if res["return_code"] != 404:
                open_cash_bin()
                return

            show_result_prompt()

        elif action=="withdraw":
            if amount==0:
                show_bye_prompt()
                return
            else:
                self.model.append_incomplete_transaction(
                    account_id=account_id,
                    residue=amount
                )
                self._fallback()
        else:
            raise NotImplementedError


    def callback_process_incomplete_transactions(self):
        # This function MUST NOT be called concurrently

        for incomplete_transaction in self.model.list_incomplete_transactions:
            res = self._call_server_api(
                method="POST",
                url="/process_incomplete_transactions",
                data={
                    'account_id': incomplete_transaction.account_id,
                    'amount' : incomplete_transaction.residue
                }
            )

            if res["return_code"] == 404:
                incomplete_transaction.completed=True
            else:
                # Okay to fail
                pass
        
        self.model.clear_completed_transactions()
        
        
