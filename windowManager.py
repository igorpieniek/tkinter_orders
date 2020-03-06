

class windowManager():
    def __init__(self, status):
        self.options = ['START','NEW_ORDER', 'HISTORY' ]
        self.status = self.options[status]
    def getStatus(self):
        return self.status
    def setStatus(self, status):
        self.status = self.options[status]


