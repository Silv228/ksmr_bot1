class BalanceErr(Exception):
    def __init__(self, message='Недостаточно средств на балансе') -> None:
        self.message = message
        super().__init__(self.message)