import sys
import pygame
from settings_eje import Settings2
from ship_eje import Ship2
from bullet_eje import Bullet
from alien_eje import Alien2

class AlienInvasion2:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings2()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_widht = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion 2")
        self.ship2 = Ship2(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        while True:
            self._check_events()
            self.ship2.update()
            self._update_bullets()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship2.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship2.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship2.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship2.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship2.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship2.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship2.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship2.moving_down = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullet group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        self.bullets.update()
        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.settings.screen_width:
                bullet.kill()  # alternativa a self.bullets.remove(bullet)

    def _create_fleet(self):
        """Create the fleet of aliens"""
        alien = Alien2(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = (self.settings.screen_width - 2 * alien_width), alien_height

        while current_y < (self.settings.screen_height - 2 * alien_height):
            while current_x > (8 * alien_width):
                self._create_alien(current_x, current_y)
                current_x -= 2 * alien_width

            #Finished a row, reset x value, and increment y value
            current_x = (self.settings.screen_width - 2 * alien_height)
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row"""
        new_alien = Alien2(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship2.blitme2()
        self.aliens.draw(self.screen)
        pygame.display.flip()

if __name__=='__main__':
    ai2 = AlienInvasion2()
    ai2.run_game()