class CSignal:
    def __init__(self):
        self.connections = []

    def emit(self, *args, **kwargs):
        #print(f"CSignal emit: {args}, {kwargs}")
        for connection in self.connections:
            connection()

    def connect(self, func: callable):
        self.connections.append(func)
