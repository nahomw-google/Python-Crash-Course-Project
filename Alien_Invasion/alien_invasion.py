import sys
from time import sleep

import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion():

    def __init__(self):
        #initialize the game, and create the game resources
        pygame.init()
        self.settings = Settings()

        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((1200, 800))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        #create an instance to store the game stats
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        #Instance of ship, group of bullets, and group of aliens
        self.ship = Ship(self)
        self.bullets = Group()
        self.aliens = Group()

        self._create_fleet()
        
        self.play_button = Button(self, "Click Play")

        self.bg_color = (230, 230, 230)

    def run_game(self):
        #start the main loop for the game
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_alien()

            self._update_screen()
    
    def _check_events(self):
        #respond to keypress and mouse events
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
    
    def _check_play_button(self, mouse_pos):
        #start the new game when player clicks play
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            #remove aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #create new fleet and ship
            self._create_fleet()
            self.ship.center_ship()

            #hide mouse when game is active
            pygame.mouse.set_visible(False)
    
    def _check_keydown_events(self, event):
        #Respond to keypress
        if event.key == pygame.K_RIGHT:
            #Move the ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit(0)
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _fire_bullet(self):
        #create a new bullet and add it to the bullets
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            #move the ship to the left
            self.ship.moving_left = False

    def _update_bullets(self):
        #get rid of bullets that have disappeared and update the position
        #update bullet position
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        #check fleet and bullet collision 
        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        #respond to bullet collision
        #check for any bullets that hit an alien
        #if so, get rid of the bullet and alien
        collision = pygame.sprite.groupcollide(self.bullets, self.aliens, False, True)

        if collision:
            for aliens in collision.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            #destroy the exist bullets and create a new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _update_alien(self):
        #update the position of all aliens in the fleet
        #check if a fleet at an edge then update the fleet.
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        #look for alien hittim the bottom of the screen
        self._check_aliens_bottom()
        
    def _ship_hit(self):
        #Respond to the ship being hit by alien
        if self.stats.ships_left > 0:
            #decrease the amount of ship left
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #get rid of any remaining bullets and aliens
            self.aliens.empty()
            self.bullets.empty()

            #create a new fleet
            self._create_fleet()
            self.ship.center_ship()

            #pause
            sleep(1)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        #check if any aliens have reached the bottome of the screen
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #treat as the same way as ship hit
                self._ship_hit()
                break
    
    def _create_fleet(self):
        #create a fleet
        #make an alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #create a full fleet alien
        for row_number in range(number_rows):
        #create the first row of aliens
            for alien_number in range(number_aliens_x):
                #create an alien and place it in the row
                self._create_alien(alien_number,row_number)

    def _create_alien(self, alien_number, row_number):
        #create an alien and plact it in the row
        alien = Alien(self)
        alien_width = alien.rect.width
        self.x = alien_width + (2 * alien_width * alien_number)
        alien.rect.x = self.x
        alien.rect.y = alien.rect.height + (2 * alien.rect.height * row_number)
        self.aliens.add(alien)
    
    def _check_fleet_edges(self):
        #respond appropriately if any aliens have reached an edge
        for aliens in self.aliens.sprites():
            if aliens.check_edges():
                self._change_fleet_direction()
                break
        
    def _change_fleet_direction(self):
        #drop the entire fleet and change fleet direction
        for aliens in self.aliens.sprites():
            aliens.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        #update the images on screen and flip to the new screen
        #Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        #draw the alien on the screen
        self.aliens.draw(self.screen)

        #draw the scrore board info
        self.sb.show_score()

        #draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.daw_button()

        #make the most recently drawn screen visible
        pygame.display.flip()


if __name__=='__main__':
    #make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
