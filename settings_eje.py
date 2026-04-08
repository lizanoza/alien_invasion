
class Settings2:
    def __init__(self):
        """Initialize game settings"""
        self.screen_width = 1520
        self.screen_height = 760
        self.bg_color = (0, 0, 250) # En hexadecimal #0000FA
        #Ship settings
        self.ship_speed = 1.5
        #Bullet settings
        self.bullet_speed = 2
        self.bullet_height = 3
        self.bullet_width = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5
        #Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_left_speed = 10
        self.fleet_direction = 1

