class State:    
    def __init__(self) -> None:
        self._in_orders = False
        self._in_order = False
        self._order = ''
        self._orders = {
            'ordersList': [],
            'cursor': 0,
            'lentgh': 0
        }
    def resetState(self): 
        self._in_orders = False
        self._in_order = False
        self._order = ''
    def setInOrders(self, newState):
        self._in_orders = newState
    def setInOrder(self, newState):
        self._in_order = newState
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
                'order': self._order,
                'orders': self._orders,
                }