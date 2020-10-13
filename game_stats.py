
class GameStats:
    #Track stats for alien invasion

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()

        #start alien invasion in an active state
        self.game_active = False

        #set high scrore
        self.high_score = 0

    def reset_stats(self):
        #initialize stats that can change during a game
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 0
