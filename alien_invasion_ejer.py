import sys
import pygame
from settings_eje import Settings2
from ship_eje import Ship2
from bullet_eje import Bullet

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

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship2.blitme2()
        pygame.display.flip()

if __name__=='__main__':
    ai2 = AlienInvasion2()
    ai2.run_game()