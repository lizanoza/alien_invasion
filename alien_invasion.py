import sys
# Del módulo sys vamos a usar herramientas para salir del juego
import pygame
# Librería que proporciona todas las herramientas para crear el juego
from settings import Settings
from ship import Ship

class AlienInvasion:
    """Overall class to manage game assets and behavior"""
    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        # Crea una instancia de reloj que permite controlar y medir el tiempo en el juego
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        # Crea una ventana de 1200 x 800 píxeles donde se dibujaran los elementos gráficos del juego.
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # Establece el título de la ventana que aparece en la barra superior
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self) # self = ai = ai_game

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            """Start the main loop for the game"""
            self._check_events() # Method para revisar eventos
            self._update_screen() # Method para actualizar imágenes y la pantalla
            self.clock.tick(60) # Reloj que limita el juego a 60 FPS

    def _check_events(self):
        """Respond to key presses and mouse events"""
        """Un método auxiliar maneja una tarea especifica para que run game no tenga que hacerlo directamente.
        El _ al principio indica que el método es privado, o sea que es para uso interno de la clase y no para
         llamarse desde afuera"""
        for event in pygame.event.get():
            # pygame.event.get() devuelve una lista de los eventos ocurridos desde la última vez que se llamó.
            if event.type == pygame.QUIT:  # Si el evento es de tipo QUIT(presionar la x de la ventana).
                sys.exit()

    def _update_screen(self):
        """Update images on the screen and flip to new screen"""
        self.screen.fill(self.settings.background_color)  # Establece el color de fondo de la pantalla.
        # Hace visible la última pantalla dibujada, siempre debe ir al final del bucle.
        self.ship.blitme()  # Dibuja la nave en el centro inferior de la pantalla.
        pygame.display.flip()  # Actualiza la pantalla una vez por cada iteración del bucle

if __name__=="__main__":
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
