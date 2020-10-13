
class Settings:
    # A class to store to store all settings for alian invasion

    def __init__(self):
        #initialize the games settings

        #screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color   = (230, 230, 230)

        #ships settings
        self.ship_limit = 3

        #aliens speed
        self.fleet_drop_speed = 10
        

        #bullets
        self.bullet_width = 500
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5

        #How quick the game speeds up
        self.speedup_scale = 1.1

        #how quick the score scales
        self.score_scale = 1.5
        #original settings
        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        #initialize settings that change throught the game
        self.ship_speed = 10
        self.bullet_speed = 10.0
        self.alien_speed = 5.0
        
        #alien points for shooting down the aliens
        self.alien_points = 50

        #fleet direction of 1 represent right and -1 represents left
        self.fleet_direction = 1


    def increase_speed(self):
        #increase speed settings
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)



