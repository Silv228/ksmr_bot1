class State:    
    def __init__(self) -> None:
        self._in_orders = False
        self._in_order = False
        self._in_payment = False
        self._payment = ''
        self._in_profile = False
        self._order = ''
        self._orders = {
            'ordersList': [],
            'cursor': 0,
            'lentgh': 0
        }
    def resetState(self): 
        self._in_orders = False
        self._in_order = False
        self._in_payment = False
        self._in_profile = False
        self._payment = ''
        self._order = ''
    def setInOrders(self, newState):
        self._in_orders = newState
    def setInOrder(self, newState):
        self._in_order = newState
    def setInPayment(self, newState):
        self._in_payment = newState
    def setPayment(self, newPayment):
        self._payment = newPayment
    def setInProfile(self, newState):
        self._in_profile = newState
    def setOrder(self, newOrder):
        self._order = newOrder
    def setOrders(self, orders, cursor):
        self._orders = {
            'ordersList': orders,
            'cursor': cursor,
            'lentgh': len(orders)
        }
    def getState(self): 
        return {'in_order': self._in_order,
                'in_orders': self._in_orders, 
                'in_payment': self._in_payment,
                'payment': self._payment, 
                'in_profile': self._in_profile,
                'order': self._order,
                'orders': self._orders
                }