import pygame
from pygame.sprite import Sprite

class Alien2(Sprite):
    """A class to represent a single alien in the fleet"""
    def __init__(self, ai2_game):
        """Initialize the alien and set its starting position"""
        super().__init__()
        self.screen = ai2_game.screen
        self.settings = ai2_game.settings
        #Load the alien image and set its rect
        self.image = pygame.image.load("images/alien_eje.bmp")
        self.rect = self.image.get_rect()

        #Start each new alien near the middle top of the screen
        self.rect.x = 10 * self.rect.width
        self.rect.y = self.rect.height

        #Store the alien exact horizontal position
        self.y = float(self.rect.y)

    def check_edges(self):
        """Return True if alien is at the edge of the screen"""
        screen_rect = self.screen.get_rect()
        return (self.rect.bottom >= screen_rect.bottom) or (self.rect.top <= 0)

    def update(self):
        """Move the aliens down or up"""
        self.y += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.y = self.y

