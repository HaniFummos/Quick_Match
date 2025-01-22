class State:
    def __init__(self, state):
        self.state = state
        self.ip = '0:0'
        self.port = '0'
    def getState(self):
        print(self.ip)
        print(self.port)
        return self.state
    def setState(self, newState):
        self.state = newState
