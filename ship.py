import pygame

class Ship:
    """A class to manage the ship"""
    def __init__(self, ai_game): # ai = self = ai_game
        """Initialize the ship and set its starting position"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        # En pygame, get_rect devuelve un objeto con las dimensiones y posición de un elemento, aquí se usa para conocer los bordes de la pantalla

        #Load the ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        #Obtiene el rectángulo de la imagen de la nave. Este rectángulo es lo que pygame usa para saber donde dibujar la nave

        #Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        #Store a float for the ships exact horizontal position
        #El atributo x solo acepta enteros, para que la velocidad sea 1.5 pixeles convertimos rect.x a un flotante y lo metemos dentro de una variable
        self.x = float(self.rect.x) #Guarda la posición real con decimales

        # Movement flag; start with a ship that is not moving
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship position based on the movement flag"""
        # Update the ships x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right: # < 1200
            self.x += self.settings.ship_speed # self.x += 1.5
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Pygame necesita enteros para dibujar píxeles por eso necesario convertir el flotante de vuelta a entero.
        # Luego sincroniza el rect con esa nueva posición para que se dibuje la nave
        self.rect.x = self.x # Le dice a pygame donde dibujar la nave y convierte de float a int

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)
        #blit es el término de pygame para dibujar una imagen sobre una superficie