import pygame
from ..constants import WIDTH, HEIGHT, WHITE, BLACK, RED, TILE_MAP, TILE_SIZE

class Renderer:
    def __init__(self, win, assets):
        self.win = win
        self.assets = assets
        self.camera_x = 0
        self.camera_y = 0
    
    def draw_game(self, level_manager, game_time_elapsed):
        self.win.blit(self.assets.background_img, (0, 0))
        
        # Draw all sprites with camera offset
        for sprite in level_manager.all_sprites:
            self.win.blit(sprite.image, (sprite.rect.x - self.camera_x, sprite.rect.y - self.camera_y))
        
        # Draw UI
        self._draw_ui(level_manager.player, game_time_elapsed)
    
    def _draw_ui(self, player, game_time_elapsed):
        # Explosion count
        count_text = self.assets.font.render(f"Deaths: {player.explode_count}", True, WHITE)
        self.win.blit(count_text, (10, 10))
        
        # Timer
        timer_text = self.assets.timer_font.render(f"Time: {self._format_time(game_time_elapsed)}", True, WHITE)
        timer_rect = timer_text.get_rect(center=(WIDTH // 2, 25))
        
        # Semi-transparent background for timer
        timer_bg = pygame.Surface((timer_rect.width + 20, timer_rect.height + 10), pygame.SRCALPHA)
        timer_bg.fill((0, 0, 0, 128))
        self.win.blit(timer_bg, (timer_rect.x - 10, timer_rect.y - 5))
        self.win.blit(timer_text, timer_rect)
        
        # Controls
        controls_text = self.assets.timer_font.render("Controls: WASD or Arrow Keys + Space/W to jump", True, WHITE)
        self.win.blit(controls_text, (10, HEIGHT - 30))
    
    def draw_game_over(self, explosion_count, game_time_elapsed):
        self.win.fill(BLACK)
        
        # Game over text
        game_over_text = self.assets.font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        self.win.blit(game_over_text, game_over_rect)
        
        # Explosion count
        explosion_text = self.assets.font.render(f"x {explosion_count} meledak", True, WHITE)
        explosion_rect = explosion_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 140))
        self.win.blit(explosion_text, explosion_rect)
        
        # Time
        time_text = self.assets.timer_font.render(f"Time: {self._format_time(game_time_elapsed)}", True, WHITE)
        time_rect = time_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        self.win.blit(time_text, time_rect)
        
        # Instructions
        restart_text = self.assets.timer_font.render("Press R to restart or ESC for menu", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        self.win.blit(restart_text, restart_rect)
    
    def draw_surat_1(self, game_time_elapsed):
        self.win.fill(BLACK)
        surat_rect = self.assets.surat_1_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.win.blit(self.assets.surat_1_image, surat_rect)
        
        instruction = self.assets.font.render("Press ENTER to continue", True, WHITE)
        instruction_rect = instruction.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.win.blit(instruction, instruction_rect)
        
        time_text = self.assets.timer_font.render(f"Your time: {self._format_time(game_time_elapsed)}", True, WHITE)
        time_rect = time_text.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        self.win.blit(time_text, time_rect)
    
    def draw_surat_2(self, game_time_elapsed):
        self.win.fill(BLACK)
        surat_rect = self.assets.surat_2_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.win.blit(self.assets.surat_2_image, surat_rect)
        
        instruction = self.assets.font.render("Press ENTER to return to menu", True, WHITE)
        instruction_rect = instruction.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.win.blit(instruction, instruction_rect)
        
        time_text = self.assets.timer_font.render(f"Your time: {self._format_time(game_time_elapsed)}", True, WHITE)
        time_rect = time_text.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        self.win.blit(time_text, time_rect)
    
    def update_camera(self, player, level_width):
        # Horizontal camera
        self.camera_x = player.rect.centerx - WIDTH // 2
        self.camera_x = max(0, min(self.camera_x, level_width - WIDTH))
        
        # Vertical camera
        target_camera_y = player.rect.centery - HEIGHT // 2
        self.camera_y += (target_camera_y - self.camera_y) * 0.1
        
        max_camera_y = (len(TILE_MAP) * TILE_SIZE) - HEIGHT
        self.camera_y = max(0, min(self.camera_y, max_camera_y))
    
    def _format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"