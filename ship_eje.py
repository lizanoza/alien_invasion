import pygame

class Ship2:
    def __init__(self, ai2_game):
        self.screen = ai2_game.screen
        self.settings = ai2_game.settings
        self.screen_rect = ai2_game.screen.get_rect()
        self.image = pygame.image.load("images/PurpleSpaceShip_0.bmp")
        self.ship_rect = self.image.get_rect()
        self.ship_rect.midleft = self.screen_rect.midleft
        self.x = float(self.ship_rect.x) # Guarda la posición real con decimales
        self.y = float(self.ship_rect.y)

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_right and self.ship_rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.ship_rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.ship_rect.top > self.screen_rect.top:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.ship_rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        self.ship_rect.x = self.x # Le dice a pygame donde dibujar la nave y convierte rect de float a int
        self.ship_rect.y = self.y

    def blitme2(self):
        self.screen.blit(self.image, self.ship_rect)