class PaymentStore:
    def __init__(self) -> None:
        self._in_payment = False
        self._payment = ''
        self._in_payout = False

    def resetState(self):
        self._in_payment = False
        self._payment = ''
        self._in_payout = False

    def setInPayment(self, newState):
        self._in_payment = newState

    def setInPayout(self, newState):
        self._in_payout = newState

    def setPayment(self, newPayment):
        self._payment = newPayment

    def getState(self):
        return {'in_payment': self._in_payment,
                'in_payout': self._in_payout,
                'payment': self._payment, }
