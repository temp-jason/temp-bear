class HumanInterventionNeededError(Exception):
    # The ATM needs a human intervention for further operation
    pass

class CardEjectionError(HumanInterventionNeededError):
    pass

class CashBinError(HumanInterventionNeededError):
    pass

class ServerConnectionError(Exception):
    pass