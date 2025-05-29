import pygame
import time
from .constants import *
from .assets import AssetManager
from .level_manager import LevelManager
from .ui.renderer import Renderer
from .ui.menu import MenuManager

class GameManager:
    def __init__(self, win):
        self.win = win
        self.assets = AssetManager()
        self.level_manager = LevelManager(self.assets)
        self.renderer = Renderer(win, self.assets)
        self.menu_manager = MenuManager(win, self.assets)
        
        self.game_state = START
        self.clock = pygame.time.Clock()
        
        # Timer variables
        self.game_start_time = 0
        self.game_time_elapsed = 0
        self.is_timer_running = False
        
        # FIXED: Game over variables with longer display time
        self.explosion_display_time = 120  # 2 seconds at 60 FPS
        self.current_explosion_count = 0
        self.explosion_display_counter = 0
        self.death_screen_delay = 60  # 1 second delay before showing death screen
        self.death_delay_counter = 0
        
        # Global explosion count
        self.global_explosion_count = 0
    
    def run(self):
        self.level_manager.build_level()
        self.start_background_music()
        
        running = True
        while running:
            running = self._handle_events()
            self._update_game()
            self._render_game()
            self.clock.tick(60)
    
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == START:
                    button_clicked = self.menu_manager.handle_start_screen_click(event.pos)
                    if button_clicked == "start":
                        self._start_new_game()
                    elif button_clicked == "credits":
                        self.game_state = CREDITS
                    elif button_clicked == "exit":
                        return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == CREDITS:
                        self.game_state = START
                    elif self.game_state in [PLAYING, GAME_OVER]:
                        self.game_state = START
                        self.stop_background_music()
                
                if self.game_state == GAME_OVER:
                    if event.key == pygame.K_r:
                        self._reset_game()
                
                if event.key == pygame.K_RETURN:
                    if self.game_state == SHOW_SURAT_1:
                        self.assets.surat_sound.play()
                        self.game_state = SHOW_SURAT_2
                    elif self.game_state == SHOW_SURAT_2:
                        self._full_reset_game()
                        self.game_state = START
        
        return True
    
    def _update_game(self):
        if self.game_state == PLAYING:
            self._update_playing()
        elif self.game_state == GAME_OVER:
            self._update_game_over()
    
    def _update_playing(self):
        self.update_timer()
        
        # Update platforms
        for timed_plat in self.level_manager.timed_platforms:
            timed_plat.update(self.game_time_elapsed)
        for invisible_plat in self.level_manager.invisible_platforms:
            invisible_plat.update()
        for fake_plat in self.level_manager.fake_platforms:
            fake_plat.update()
        
        # Update moving traps
        for moving_piring in self.level_manager.moving_piring_traps:
            moving_piring.check_player_proximity(self.level_manager.player.rect.centerx)
            moving_piring.update()
        
        for moving_piring_down in self.level_manager.moving_piring_down_traps:
            moving_piring_down.check_player_proximity(
                self.level_manager.player.rect.centerx, 
                self.level_manager.player.rect.centery
            )
            moving_piring_down.update()
        
        for moving_piring_up in self.level_manager.moving_piring_up_traps:
            moving_piring_up.check_player_proximity(
                self.level_manager.player.rect.centerx, 
                self.level_manager.player.rect.centery
            )
            moving_piring_up.update()
        
        # Update entities
        self.level_manager.player.update(
            self.level_manager.platforms, 
            self.level_manager.fake_platforms, 
            self.level_manager.invisible_platforms,
            self.level_manager
        )
        
        for enemy in self.level_manager.enemies:
            enemy.update(self.level_manager.platforms)
        
        for finish in self.level_manager.finish_group:
            finish.update()
        for fake_finish in self.level_manager.fake_finish_group:
            if hasattr(fake_finish, 'update'):
                fake_finish.update()
        
        # Check hidden platforms
        self.level_manager.check_hidden_platforms()
        
        # Update camera
        self.renderer.update_camera(self.level_manager.player, self.level_manager.level_width)
        
        # FIXED: Check if explosion animation finished, then trigger game over
        if self.level_manager.player.explosion_finished:
            self._trigger_game_over()
            self.level_manager.player.explosion_finished = False
        
        # Check collisions only if player is not dead
        if not self.level_manager.player.is_dead:
            self._check_collisions()
    
    def _update_game_over(self):
        # FIXED: Add delay before showing death screen, then show for 2 seconds
        self.death_delay_counter += 1
        if self.death_delay_counter > self.death_screen_delay:
            self.explosion_display_counter += 1
            if self.explosion_display_counter > self.explosion_display_time:
                self._reset_game()
    
    def _check_collisions(self):
        player = self.level_manager.player
        
        # FIXED: Only check collisions if player is not exploding or dead
        if player.exploding or player.is_dead:
            return
        
        # Enemy collisions
        hit_enemies = pygame.sprite.spritecollide(player, self.level_manager.enemies, False)
        for enemy in hit_enemies:
            if player.dy > 0 and player.rect.bottom <= enemy.rect.top + 10:
                enemy.kill()
                player.dy = -10
            else:
                player.explode()
                return  # Exit immediately after explosion
        
        # Moving trap collisions
        for moving_piring in self.level_manager.moving_piring_traps:
            if player.collision_rect.colliderect(moving_piring.collision_rect):
                player.explode()
                return  # Exit immediately after explosion
        
        for moving_piring_down in self.level_manager.moving_piring_down_traps:
            if player.collision_rect.colliderect(moving_piring_down.collision_rect):
                player.explode()
                return  # Exit immediately after explosion
        
        for moving_piring_up in self.level_manager.moving_piring_up_traps:
            if player.collision_rect.colliderect(moving_piring_up.collision_rect):
                player.explode()
                return  # Exit immediately after explosion
        
        # Fake finish collisions
        hit_fake_finishes = pygame.sprite.spritecollide(player, self.level_manager.fake_finish_group, False)
        for fake_finish in hit_fake_finishes:
            if fake_finish.fake_type == "kill":
                player.explode()
                return  # Exit immediately after explosion
            elif fake_finish.fake_type == "teleport":
                player.teleport_to_start(self.level_manager.spawn_pos)
            elif fake_finish.fake_type == "hide":
                if not self.level_manager.real_finish_hidden:
                    for finish in self.level_manager.finish_group:
                        finish.hide()
                    fake_finish.hide()
                    self.level_manager.real_finish_hidden = True
        
        # Real finish collision
        if not self.level_manager.real_finish_hidden:
            hit_finishes = pygame.sprite.spritecollide(player, self.level_manager.finish_group, False)
            for finish in hit_finishes:
                if finish.visible:
                    self.stop_timer()
                    self.stop_background_music()
                    self.assets.finish_sound.play()
                    self.game_state = SHOW_SURAT_1
    
    def _render_game(self):
        if self.game_state == START:
            self.menu_manager.draw_start_screen()
        elif self.game_state == CREDITS:
            self.menu_manager.draw_credits_screen()
        elif self.game_state == PLAYING:
            self.renderer.draw_game(self.level_manager, self.game_time_elapsed)
        elif self.game_state == GAME_OVER:
            # FIXED: Show game during delay, then death screen for 2 seconds
            if self.death_delay_counter <= self.death_screen_delay:
                self.renderer.draw_game(self.level_manager, self.game_time_elapsed)
            else:
                self.renderer.draw_game_over(self.current_explosion_count, self.game_time_elapsed)
        elif self.game_state == SHOW_SURAT_1:
            self.renderer.draw_surat_1(self.game_time_elapsed)
        elif self.game_state == SHOW_SURAT_2:
            self.renderer.draw_surat_2(self.game_time_elapsed)
        
        pygame.display.flip()
    
    def _start_new_game(self):
        self._full_reset_game()
        self.start_timer()
        if not self.is_background_music_playing():
            self.start_background_music()
        self.game_state = PLAYING
    
    def _trigger_game_over(self):
        if self.game_state != GAME_OVER:
            self.current_explosion_count = self.level_manager.player.explode_count
            self.stop_timer()
            self.game_state = GAME_OVER
            self.explosion_display_counter = 0
            self.death_delay_counter = 0  # Reset delay counter
    
    def _reset_game(self):
        if self.level_manager.player:
            self.global_explosion_count = self.level_manager.player.explode_count
        
        self.level_manager.reset_all_objects()
        
        if self.level_manager.player:
            self.level_manager.player.respawn(self.level_manager.spawn_pos)
            self.level_manager.player.explode_count = self.global_explosion_count
        
        self.renderer.camera_x = 0
        self.renderer.camera_y = 0
        self.game_time_elapsed = 0
        self.start_timer()
        self.game_state = PLAYING
        self.explosion_display_counter = 0
        self.death_delay_counter = 0  # Reset delay counter
    
    def _full_reset_game(self):
        self.global_explosion_count = 0
        self.level_manager.build_level()
        self.renderer.camera_x = 0
        self.renderer.camera_y = 0
        self.game_time_elapsed = 0
    
    # Timer methods
    def start_timer(self):
        self.game_start_time = time.time()
        self.is_timer_running = True
    
    def stop_timer(self):
        if self.is_timer_running:
            self.game_time_elapsed = time.time() - self.game_start_time
            self.is_timer_running = False
    
    def update_timer(self):
        if self.is_timer_running:
            self.game_time_elapsed = time.time() - self.game_start_time
    
    def format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    # Music methods
    def start_background_music(self):
        if self.assets.background_music:
            try:
                pygame.mixer.music.load(self.assets.background_music)
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
            except pygame.error:
                print("Could not load background music")
    
    def stop_background_music(self):
        pygame.mixer.music.stop()
    
    def is_background_music_playing(self):
        return pygame.mixer.music.get_busy()