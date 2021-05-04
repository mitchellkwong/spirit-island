class Movement:
    def __init__(self, quantity, resource, source, target):
        self.quantity = quantity
        self.resource = resource
        self.source = source
        self.target = target 

class Move(Movement):
    def __call__(self, board):
        board.nodes.loc[self.source, self.resource] -= self.quantity
        board.nodes.loc[self.source, self.resource] -= self.quantity

class Gather(Movement):
    def __call__(self, board):
        pass

class Push(Movement):
    def __call__(self, board):
        pass