class SpiritIsland:
    """Handles interaction between components when a game is run"""
    def __init__(self, board, game, player):
        self.board = board
        self.game = game
        self.player = player

    def run(self):
        # Initial setup
        self.board = self.game.initial_setup(self.board)

        # While game is not won or loss
        while True:
            if self.game.is_won(self.board):
                # Handle win
                break
            if self.game.is_lost(self.board):
                # Handle loss
                break
            
            # Spirit phase
            self.player = self.player.growth(self.board, self.game)
            self.player = self.player.gain_energy(self.board, self.game)
            fast, slow = self.player.choose_powers(self.board, self.game)
            
            # Fast powers
            for power in fast:
                self.board = self.board.apply(power)
                self.game = self.game.apply(power)
                self.player = self.player.apply(power)
            
            # Invader phase
            if self.game.is_blighted():
                self.game.blighted_island(self.board, self.player)


            # Slow powers

            # Time passes
        pass