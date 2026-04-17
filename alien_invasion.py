import sys
# Del módulo sys vamos a usar herramientas para salir del juego
import pygame
# Librería que proporciona todas las herramientas para crear el juego
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior"""
    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        # Crea una instancia de reloj que permite controlar y medir el tiempo en el juego
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        """
        # Crea una ventana de 1200 x 800 píxeles donde se dibujaran los elementos gráficos del juego.
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        """
        #Crea una ventana fullscreen donde se dibujaran los elementos gráficos del juego
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) # (0,0) le dice a pygame que use el tamaño del monitor y pygame.FULLSCREEN es una bandera que activa el modo pantalla completa.
        self.settings.screen_width = self.screen.get_rect().width #Guarda el ancho del monitor en settings
        self.settings.screen_height = self.screen.get_rect().height #Guarda el alto del monitor en settings
        # Establece el título de la ventana que aparece en la barra superior
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self) # self = ai = ai_game
        self.bullets = pygame.sprite.Group() #Crea un grupo de bullets vacío.
        #Un Group es como una lista inteligente de pygame que permite manejar multiples sprites(balas) a la vez.
        self.aliens = pygame.sprite.Group()
        self._create_fleet() #Crea la flota de aliens, se ejecuta una sola vez con el init

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            """Start the main loop for the game"""
            self._check_events() # Method para revisar eventos
            self.ship.update() # Actualiza la posición de la nave
            self._update_bullets() # Actualiza la posición de las balas y las remueve cuando salen de la pantalla
            self._update_aliens() # Actualiza la posición de los aliens
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
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            """Move the ship to the right"""
            self.ship.moving_right = True  # Permite movimiento continuo
        elif event.key == pygame.K_LEFT:
            """Move the ship to the left"""
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False  # Se deja de mover
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullet group"""
        if len(self.bullets) < self.settings.bullets_allowed: # limita la cantidad de balas
            new_bullet = Bullet(self) #Crea una nueva instancia de la clase bullet, pasando self(el juego completo) como argumento.
            # Bullet usa ese self para obtener self.screen, self.settings, self.ship.rect.midtop
            self.bullets.add(new_bullet) #Agrega la bala recién creada al grupo self.bullets. A partir de ese momento el grupo se encarga de ella automáticamente cada frame.

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        # Update bullets position
        self.bullets.update()
        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():  # Iteramos sobre una copia debido a que no se puede modificar una lista o grupo mientras se ejecuta un for
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)  # Elimina las balas de la lista original

        self._check_alien_bullet_collisions()

    def _check_alien_bullet_collisions(self):
        """Respond to bullet, alien collisions"""
        # Si un rect de bullets colisiona con un rect de aliens, la bala se borra, el alien se borra
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            # Destroy existing bullets and create a new fleet
            self.bullets.empty()
            self._create_fleet()

    def _create_fleet(self):
        """Create the fleet of aliens"""
        #Create an alien and keep adding aliens until there is no room left.
        #Spacing between aliens is one alien width and one alien height.
        alien = Alien(self) #Crea un alien temporal únicamente para medir su tamaño, no se agrega a la pantalla
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height #Define el punto de inicio en x, y para el primer alien
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width #Avanza la posición x para el siguiente alien saltando 2 anchos
            #Finished a row; reset x value, and increment y value
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet"""
        new_alien = Alien(self)
        new_alien.x = x_position # Guarda la posición x en el atributo propio del alien (valor flotante para movimiento preciso)
        new_alien.rect.x = x_position  # Valor entero que determina donde se dibuja visualmente
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions"""
        self._check_fleet_edges()
        self.aliens.update()

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reach an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleets direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen and flip to new screen"""
        self.screen.fill(self.settings.background_color)  # Establece el color de fondo de la pantalla.
        # Hace visible la última pantalla dibujada, siempre debe ir al final del bucle.
        for bullet in self.bullets.sprites():
        # El metodo .sprites() convierte el grupo en una lista iterable de todos los sprites que contiene, y en cada vuelta del ciclo bullet representa una bala individual.
            bullet.draw_bullet() #Dibuja cada bala en su posición actual de la pantalla
        self.ship.blitme()  # Dibuja la nave en el centro inferior de la pantalla.
        self.aliens.draw(self.screen) #Al llamar al metodo draw() en un grupo, Pygame dibuja cada elemento del grupo en la posición definida por su atributo rect
        pygame.display.flip()  # Actualiza la pantalla una vez en cada iteración del bucle

if __name__=="__main__":
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
