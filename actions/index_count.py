class IndexCount():


    def __init__(self):
        self.index = 0

    def increment(self,i):
        self.index=i
    
    def clear(self):
        self.index=0

    def get__index(self):
        return self.index