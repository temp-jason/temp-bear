from .const import *

def read_card_id_from_card_reader(timeout : int =DEFAULT_TIMEOUT):
    """
    Reads and returns the id of the inserted card
    TODO: returns -1 in case of a hardware error
    """
    PHONY_CARD_ID=7777

    return PHONY_CARD_ID

def eject_card(timeout : int = DEFAULT_TIMEOUT):
    """
    Ejects the card if inserted (i.e. does nothing if no card is inserted)
    TODO: raise CardEjectionError() in case of a hardware error (or # attempts exceeds the threshold)
    """    
    return True

def open_cash_bin(amount : int = 0, timeout : int = CASH_BIN_TIMEOUT):
    """
    Opens the cash bin with the `amount` of money
    For deposit mode, `amount` must be set as 0 (the default)
    TODO: raise CashBinError() in case of a hardware error (or # attempts exceeds the threshold)
    """

    return True

def close_cash_bin():
    """
    Called by a view
    TODO: raise CashBinError() in case of a hardware error (or # attempts exceeds the threshold)
    """
    pass