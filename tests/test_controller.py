from app.const import MAX_PIN_CODE_TRIAL
from app.controller import ATMController
from unittest import mock
import os
import pytest


@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    with mock.patch.dict(os.environ, {"MACHINE_MASTER_SESSION_TOKEN": "master_key"}):
        yield

def test():
    # This is by no means a full-coverage test
    ctrl = ATMController()
    ctrl.callback_card_inserted("test_card_id")
    assert ctrl.model.user_session.card_id == "test_card_id"

    ctrl.callback_pin_code_inputted(1234, MAX_PIN_CODE_TRIAL-1)
    assert ctrl.model.user_session.session_token
    assert ctrl.model.user_session.list_accounts

    ctrl.callback_account_and_action_selected("phony_account_id", "see_balance")
    ctrl.callback_account_and_action_selected("phony_account_id", "deposit", 3)
    ctrl.callback_account_and_action_selected("phony_account_id", "withdraw", 2)

    ctrl.callback_cash_bin_closed("phony_account_id", "deposit", 7)
    ctrl.callback_cash_bin_closed("phony_account_id", "withdraw", 0)
    ctrl.callback_cash_bin_closed("phony_account_id", "withdraw", 1)
    
    assert(ctrl.model.list_incomplete_transactions)

    ctrl.callback_process_incomplete_transactions()

    assert(not ctrl.model.list_incomplete_transactions)