import pygame

class Ship:
    """A class to manage the ship"""
    def __init__(self, ai_game): # ai = self = ai_game
        """Initialize the ship and set its starting position"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        # En pygame, get_rect devuelve un objeto con las dimensiones y posición de un elemento, aquí se usa para conocer los bordes de la pantalla

        #Load the ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        #Obtiene el rectángulo de la imagen de la nave. Este rectángulo es lo que pygame usa para saber donde dibujar la nave

        #Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        # El centro inferior de la nave es igual al centro inferior de la pantalla

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)
        #blit es el término de pygame para dibujar una imagen sobre una superficie