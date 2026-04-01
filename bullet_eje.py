import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""
    def __init__(self, ai2_game):
        """Create a bullet object at the ship current position"""
        super().__init__()
        self.screen = ai2_game.screen
        self.settings = ai2_game.settings
        self.color = ai2_game.settings.bullet_color

        #Create a bullet rect at (0,0) and then set the correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midright = ai2_game.ship2.ship_rect.midright

        #Store the bullet position as a float
        self.x = float(self.rect.x)

    def update(self):
        """Move the bullet up the screen"""
        #update the exact position of the bullet
        self.x += self.settings.bullet_speed
        #update the rect position
        self.rect.x = self.x

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.settings.bullet_color, self.rect)


