class State:    
    def __init__(self) -> None:
        self._in_profile = False
    def resetState(self): 
        self._in_profile = False
    def setInProfile(self, newState):
        self._in_profile = newState
    def getState(self): 
        return { 
                'in_profile': self._in_profile,
                }