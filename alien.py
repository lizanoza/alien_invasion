import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""
    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen

        #Load the alien image and set its rect attribute.
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        #Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        #Coloca el alien horizontalmente a una distancia desde el borde izquierdo igual a su propio ancho. Por ejemplo, si el alien mide 50px de ancho, su posición X será 50px.
        self.rect.y = self.rect.height
        #Coloca el alien verticalmente a una distancia desde el borde superior igual a su propia altura. Si mide 50px de alto, su posición Y será 50px.

        #Store the alien exact horizontal position.
        self.x = float(self.rect.x)
