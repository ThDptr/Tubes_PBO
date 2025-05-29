import pygame
from ..constants import WIDTH, HEIGHT, WHITE, BLACK

# Initialize mixer early (if not done in main)
pygame.mixer.init()

class MenuManager:
    def __init__(self, win, assets):
        self.win = win
        self.assets = assets
        self.music_started = False

        # Start background music immediately when menu is created
        self.start_background_music()
        
        # Calculate button positions with spacing
        button_spacing = 20
        start_y = HEIGHT // 2 - 50
        
        self.start_button_rect = self.assets.start_button_img.get_rect(center=(WIDTH // 2, start_y))
        self.credit_button_rect = self.assets.credit_button_img.get_rect(
            center=(WIDTH // 2, start_y + self.assets.start_button_img.get_height() + button_spacing)
        )
        self.exit_button_rect = self.assets.exit_button_img.get_rect(
            center=(WIDTH // 2, start_y + 2 * (self.assets.start_button_img.get_height() + button_spacing))
        )
        
        # Calculate title position (center top)
        self.title_rect = self.assets.popcok_text_img.get_rect(center=(WIDTH // 2, 100))
    
    def start_background_music(self):
        """Start background music if not already playing"""
        if not self.music_started and self.assets.background_music:
            try:
                # Use mixer.music to stream the music file
                pygame.mixer.music.load(self.assets.background_music)
                pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
                pygame.mixer.music.play(-1)  # Loop indefinitely
                self.music_started = True
            except pygame.error:
                print("Warning: Could not play background music")
    
    def stop_background_music(self):
        """Stop background music"""
        if self.music_started:
            pygame.mixer.music.stop()
            self.music_started = False
    
    def draw_start_screen(self):
        # Draw background
        self.win.blit(self.assets.background_img, (0, 0))
        # Draw title (popcok_text.png) at center top
        self.win.blit(self.assets.popcok_text_img, self.title_rect)
        # Draw buttons
        self.win.blit(self.assets.start_button_img, self.start_button_rect)
        self.win.blit(self.assets.credit_button_img, self.credit_button_rect)
        self.win.blit(self.assets.exit_button_img, self.exit_button_rect)
    
    def draw_credits_screen(self):
        # Stop menu music (optional) when showing credits
        self.stop_background_music()
        # Draw credits background
        self.win.blit(self.assets.credits_img, (0, 0))
    
    def handle_start_screen_click(self, pos):
        if self.start_button_rect.collidepoint(pos):
            return "start"
        elif self.credit_button_rect.collidepoint(pos):
            return "credits"
        elif self.exit_button_rect.collidepoint(pos):
            return "exit"
        return None
