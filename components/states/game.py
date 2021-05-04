from matplotlib import interactive


class BaseGame:
    def __init__(self, num_players, invader_deck, fear_deck, event_deck=None):
        self.invader_deck = invader_deck
        self.fear_deck = fear_deck
        self.event_deck = event_deck

        self.fear_pool = 4*num_players
        self.blight_pool = 1 + 2*num_players
