import pygame
from pygame.sprite import Sprite
#Un sprite es la clase base de pygame para representar objetos visuales en el juego (personajes, balas, enemigos)

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""
    def __init__(self,ai_game):
        """Create a bullet object at ships current position"""
        super().__init__() #Llama al constructor de la clase padre Sprite
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #Create a bullet rect at (0,0) and then set the correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        #Mueve el rectángulo de la bala para que su punto midtop coincida con el midtop de la nave

        #Store the bullet position as a float
        self.y = float(self.rect.y)
        # Esto permite hacer movimientos suaves y precisos, ya que rect.y solo acepta enteros, pero los calculos de movimientos necesitan decimales.
    def update(self):
        """Move the bullet up the screen"""
        #Update the exact position of the bullet
        self.y -= self.settings.bullet_speed #Calcula nueva posición(float)
        #Update the rect position
        self.rect.y = self.y #Mueve el rectángulo al nuevo lugar

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
