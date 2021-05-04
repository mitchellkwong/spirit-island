from utils import resource_table

class GainResource:
    def __init__(self, quantity, resource, how):
        self.resources = resource_table() # Maintain a resource table to help optimization software
        self.resources.loc[resource, how] = quantity

    @classmethod
    def from_growth(cls, quantity, resource):
        return cls(quantity, resource, 'amount')
    
    @classmethod
    def from_track(cls, quantity, resource):
        return cls(quantity, resource, 'change')

    def __call__(self, player):
        player.resources = player.resources.value + self.resources.value
        return player

class AddPresence(GainResource):
    def __init__(self, range, restriction):
        super().__init__(1, 'presence', 'change')
        self.range = range
        self.restriction = restriction

class GainPowerCard:
    def __call__(self, player):
        return player

class ReclaimCards:
    def __init__(self, quantity=None):
        self.quantity = quantity

    def __call__(self, player):
        return player

