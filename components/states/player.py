from docplex.mp.model import Model
import pandas as pd
from components.actions.growth import GainResource, AddPresence, ReclaimCards, GainPowerCard
from utils import resource_table

class Player:
    def __init__(self, resources=None, permanent=None):
        # All possible resources that can be held by a player
        if resources is None:
            self.resources = resources
        else:
            self.resources = resource_table()

        # Whether resources are persisted across turns
        if permanent is not None:
            self.permanent = permanent
        else:
            self.permanent = resource_table()
            
            # Amounts are always reset but not changes from uncovered growth
            self.permanent.loc[:, 'amount'] = False
            self.permanent.loc[:, 'change'] = True
            
            # Exceptions for energy and presence gain
            self.permanent.loc['energy', 'amount'] = True
            self.permanent.loc['presence', 'change'] = False

    def copy(self):
        resources = self.resources.copy()
        permanent = self.permanent.copy()
        cls = type(self)
        return cls(resources=resources, permanent=permanent)
    
    def spirit_phase(self, board, game):
        """Consists of Growth, Gain Energy and Choose actions"""
        with Model() as model:
            # Stub: Formulate the problem and implement here
            pass

    def time_passes(self, board=None, game=None):
        player = self.copy()
        player.resources = player.resources.value * player.permanent.value
        return player

# Starting with this cuz it has the widest range of growth options and powers
class RampantGreen(Player):    
    def __init__(self, resources=None, permanent=None):
        super().__init__(resources=resources, permanent=permanent)
        
        self.growth = [
            [
                AddPresence(range=2, restriction=lambda x: x['land'].isin(['J', 'W'])),
                ReclaimCards(),
                GainPowerCard(),
            ],
            [
                AddPresence(range=2, restriction=lambda x: x['land'].isin(['J', 'W'])),
                AddPresence(range=1),
                GainResource.from_growth(1, 'card_plays'),
            ],
            [
                AddPresence(range=2, restriction=lambda x: x['land'].isin(['J', 'W'])),
                GainPowerCard(),
                GainResource.from_growth(1, 'energy'),
            ]
        ]
        
        # Note: Values are adjusted to reflect improvement in that resource
        self.tracks = [
            [
                GainResource.from_track(0-0, 'energy'),
                GainResource.from_track(1-0, 'energy'),
                GainResource.from_track(1-0, 'plant'),
                GainResource.from_track(2-1, 'energy'),
                GainResource.from_track(2-2, 'energy'),
                GainResource.from_track(2-1, 'plant'),
                GainResource.from_track(3-2, 'energy'),
            ],
            [
                GainResource.from_track(1-0, 'card_plays'),
                GainResource.from_track(1-1, 'card_plays'),
                GainResource.from_track(2-1, 'card_plays'),
                GainResource.from_track(2-2, 'card_plays'),
                GainResource.from_track(3-2, 'card_plays'),
                GainResource.from_track(4-3, 'card_plays'),
            ],
        ]

        self.resources = resource_table()
        
        self.powers = [
            # How to implement powers?
        ]
