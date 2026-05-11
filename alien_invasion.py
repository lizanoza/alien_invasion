import sys
import pygame
from time import sleep
from pathlib import Path

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button


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
        pygame.display.set_caption("Alien Invasion") # Establece el título de la ventana que aparece en la barra superior
        self.stats = GameStats(self) #Instancia que guarda las estadísticas
        self.sb = Scoreboard(self) #Instancia para llevar el marcador

        self.ship = Ship(self) # self = ai = ai_game
        self.bullets = pygame.sprite.Group() #Crea un grupo de bullets vacío.
        #Un Group es como una lista inteligente de pygame que permite manejar multiples sprites(balas) a la vez.
        self.aliens = pygame.sprite.Group()
        self._create_fleet() #Crea la flota de aliens, se ejecuta una sola vez con el init
        # Make the play button
        self.play_button = Button(self, "Play")
        # Make difficulty level buttons
        self._make_difficulty_buttons()
        # Start alien invasion in an inactive state
        self.game_active = False

    def _make_difficulty_buttons(self):
        """Make buttons that allow player to select difficulty level."""
        self.easy_button = Button(self, "Easy")
        self.medium_button = Button(self, "Medium")
        self.difficult_button = Button(self, "Difficult")

        # Position buttons so they don't all overlap.
        self.easy_button.rect.top = (self.play_button.rect.top + 1.5 * self.play_button.rect.height)
        self.easy_button._update_msg_position()

        self.medium_button.rect.top = (self.easy_button.rect.top + 1.5 * self.easy_button.rect.height)
        self.medium_button._update_msg_position()

        self.difficult_button.rect.top = (self.medium_button.rect.top + 1.5 * self.medium_button.rect.height)
        self.difficult_button._update_msg_position()

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            """Start the main loop for the game"""
            self._check_events() # Method para revisar eventos

            if self.game_active:
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
                path = Path("alien_invasion_highscore.txt")
                path.write_text(str(self.stats.high_score))
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos() #Retorna una tupla con las coordenadas del mouse al hacer clic
                self._check_play_buttom(mouse_pos)
                self._check_difficulty_buttons(mouse_pos)

    def _check_play_buttom(self, mouse_pos):
        """Start a new game when the player clicks play"""
        # Verifica si mouse_pos está dentro del rect del botón y lo guarda dentro de la variable button_click
        button_click = self.play_button.rect.collidepoint(mouse_pos)
        # El juego se reiniciará solo si se hace clic en play y el juego no está activo en ese momento
        if button_click and not self.game_active:
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self._start_game()

    def _check_difficulty_buttons(self, mouse_pos):
        """Set the appropriate difficulty level."""
        easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        medium_button_clicked = self.medium_button.rect.collidepoint(
            mouse_pos)
        diff_button_clicked = self.difficult_button.rect.collidepoint(
            mouse_pos)
        if easy_button_clicked:
            self.settings.difficulty_level = 'easy'
            self.easy_button.set_highlighted_color()
            self.medium_button.set_base_color()
            self.difficult_button.set_base_color()
        elif medium_button_clicked:
            self.settings.difficulty_level = 'medium'
            self.easy_button.set_base_color()
            self.medium_button.set_highlighted_color()
            self.difficult_button.set_base_color()
        elif diff_button_clicked:
            self.settings.difficulty_level = 'difficult'
            self.easy_button.set_base_color()
            self.medium_button.set_base_color()
            self.difficult_button.set_highlighted_color()

    def _start_game(self):
        """Start a new game."""
        # Reset the game settings.
        self.settings.initialize_dynamic_settings()
        # Reset the game statistics.
        self.stats.reset_stats()
        self.game_active = True
        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()
        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            """Move the ship to the right"""
            self.ship.moving_right = True  # Permite movimiento continuo
        elif event.key == pygame.K_LEFT:
            """Move the ship to the left"""
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            path = Path("alien_invasion_highscore.txt")
            path.write_text(str(self.stats.high_score))
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

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create a new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

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

        #Look for alien-ship collisions.
        #spritecollideany detecta la primera colisión con un alien
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

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

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            #Decrement ships_left and update the scoreboard
            self.stats.ships_left -= 1 #Resta una vida al contador
            self.sb.prep_ships() #Regenera los iconos de vidas con el nuevo número

            #Get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #Pause
            sleep(0.5)
        else:
            self.game_active = False
            # Make the mouse cursor visible when game is inactive
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _update_screen(self):
        """Update images on the screen and flip to new screen"""
        self.screen.fill(self.settings.background_color)  # Establece el color de fondo de la pantalla.
        # Hace visible la última pantalla dibujada, siempre debe ir al final del bucle.
        for bullet in self.bullets.sprites():
        # El metodo .sprites() convierte el grupo en una lista iterable de todos los sprites que contiene, y en cada vuelta del ciclo bullet representa una bala individual.
            bullet.draw_bullet() #Dibuja cada bala en su posición actual de la pantalla
        self.ship.blitme()  # Dibuja la nave en el centro inferior de la pantalla.
        self.aliens.draw(self.screen) #Al llamar al metodo draw() en un grupo, Pygame dibuja cada elemento del grupo en la posición definida por su atributo rect
        self.sb.show_score() #Dibuja la información del marcador

        #Draw the play button if the game is inactive
        if not self.game_active:
            self.play_button.draw_button()
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.difficult_button.draw_button()

        pygame.display.flip()  # Actualiza la pantalla una vez en cada iteración del bucle

if __name__=="__main__":
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
