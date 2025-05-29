import pygame
import os
from .constants import WIDTH, HEIGHT


class AssetManager:
    def __init__(self):
        # Define base paths for assets and sounds
        self.asset_path = os.path.join('assets')
        self.sound_path = os.path.join('sound')
        self.load_images()
        self.load_sounds()
        self.setup_fonts()

    # ENKAPSULASI: Method PUBLIC - dapat diakses dari luar class
    def load_images(self):
        try:
            # Background
            self.background_img_raw = pygame.image.load(os.path.join(self.asset_path, 'background.png')).convert()
            self.background_img = pygame.transform.scale(self.background_img_raw, (WIDTH, HEIGHT))
        except pygame.error:
            self.background_img = pygame.Surface((WIDTH, HEIGHT))
            self.background_img.fill((50, 150, 200))  # Sky blue
        
        try:
            # Buttons
            self.start_button_img_raw = pygame.image.load(os.path.join(self.asset_path, 'tombol_mulai.png')).convert_alpha()
            self.credit_button_img_raw = pygame.image.load(os.path.join(self.asset_path, 'tombol_kredit.png')).convert_alpha()
            self.exit_button_img_raw = pygame.image.load(os.path.join(self.asset_path, 'tombol_keluar.png')).convert_alpha()
            
            # Scale buttons
            button_width = int(WIDTH * 0.3)
            button_scale_factor = button_width / self.start_button_img_raw.get_width()
            button_height = int(self.start_button_img_raw.get_height() * button_scale_factor)
            
            self.start_button_img = pygame.transform.smoothscale(self.start_button_img_raw, (button_width, button_height))
            self.credit_button_img = pygame.transform.smoothscale(self.credit_button_img_raw, (button_width, button_height))
            self.exit_button_img = pygame.transform.smoothscale(self.exit_button_img_raw, (button_width, button_height))
        except pygame.error:
            # Create placeholder buttons
            button_width = int(WIDTH * 0.3)
            button_height = 60
            
            self.start_button_img = self._create_button_placeholder("START", button_width, button_height, (0, 200, 0))
            self.credit_button_img = self._create_button_placeholder("CREDITS", button_width, button_height, (0, 0, 200))
            self.exit_button_img = self._create_button_placeholder("EXIT", button_width, button_height, (200, 0, 0))
        
        try:
            # Credits image
            self.credits_img_raw = pygame.image.load(os.path.join(self.asset_path, 'credits_.png')).convert()
            self.credits_img = pygame.transform.scale(self.credits_img_raw, (WIDTH, HEIGHT))
        except pygame.error:
            # Create placeholder credits
            self.credits_img = pygame.Surface((WIDTH, HEIGHT))
            self.credits_img.fill((30, 30, 30))  # Dark background
            font = pygame.font.Font(None, 72)
            text = font.render("CREDITS", True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
            self.credits_img.blit(text, text_rect)
        
        try:
            # Load and scale the menu title image
            original_img = pygame.image.load(os.path.join(self.asset_path, 'popcok_text.png')).convert_alpha()
            self.popcok_text_img = pygame.transform.scale(original_img, (300, 300))  # Sesuaikan ukuran
        except pygame.error:
            # Create a larger placeholder title
            self.popcok_text_img = self._create_sprite_placeholder(600, 160, (255, 215, 0))  # Ukuran lebih besar
            font = pygame.font.Font(None, 72)  # Font lebih besar
            text = font.render("POPCOK GAME", True, (0, 0, 0))
            text_rect = text.get_rect(center=(300, 80))  # Sesuaikan posisi tengah
            self.popcok_text_img.blit(text, text_rect)
        
        try:
            # Player sprites
            self.player_idle_image = pygame.image.load(os.path.join(self.asset_path, 'diam.png')).convert_alpha()
            self.player_run_images = [pygame.image.load(os.path.join(self.asset_path, f'berlari{i}.png')).convert_alpha() for i in range(1, 3)]
            self.player_jump_image = pygame.image.load(os.path.join(self.asset_path, 'lompat.png')).convert_alpha()
            self.explosion_images = [
                pygame.image.load(os.path.join(self.asset_path, 'sebelum_meledak.png')).convert_alpha(),
                pygame.image.load(os.path.join(self.asset_path, 'pertengahan_meledak.png')).convert_alpha(),
                pygame.image.load(os.path.join(self.asset_path, 'setelah_meledak.png')).convert_alpha()
            ]
        except pygame.error:
            # Create placeholder player sprites
            self.player_idle_image = self._create_sprite_placeholder(32, 32, (0, 255, 0))
            self.player_run_images = [
                self._create_sprite_placeholder(32, 32, (0, 200, 0)),
                self._create_sprite_placeholder(32, 32, (0, 150, 0))
            ]
            self.player_jump_image = self._create_sprite_placeholder(32, 32, (0, 255, 100))
            self.explosion_images = [
                self._create_sprite_placeholder(32, 32, (255, 255, 0)),
                self._create_sprite_placeholder(32, 32, (255, 150, 0)),
                self._create_sprite_placeholder(32, 32, (255, 0, 0))
            ]
        
        try:
            # Enemy sprites
            self.enemy_idle_img = pygame.image.load(os.path.join(self.asset_path, 'musuh_diam.png')).convert_alpha()
            self.enemy_run_images = [pygame.image.load(os.path.join(self.asset_path, f'musuh_jalan_{i}.png')).convert_alpha() for i in range(1, 3)]
        except pygame.error:
            # Create placeholder enemy sprites
            self.enemy_idle_img = self._create_sprite_placeholder(32, 32, (255, 0, 0))
            self.enemy_run_images = [
                self._create_sprite_placeholder(32, 32, (200, 0, 0)),
                self._create_sprite_placeholder(32, 32, (150, 0, 0))
            ]
        
        try:
            # Trap sprites
            self.trap_images = [pygame.image.load(os.path.join(self.asset_path, f'jebakan{i}.png')).convert_alpha() for i in range(1, 4)]
            self.piring_images = [pygame.image.load(os.path.join(self.asset_path, f'piring{i}.png')).convert_alpha() for i in range(1, 4)]
        except pygame.error:
            # Create placeholder trap sprites
            self.trap_images = [
                self._create_sprite_placeholder(32, 32, (150, 0, 150)),
                self._create_sprite_placeholder(32, 32, (200, 0, 200)),
                self._create_sprite_placeholder(32, 32, (255, 0, 255))
            ]
            self.piring_images = [
                self._create_sprite_placeholder(32, 32, (255, 255, 0)),
                self._create_sprite_placeholder(32, 32, (255, 200, 0)),
                self._create_sprite_placeholder(32, 32, (255, 150, 0))
            ]
        
        try:
            # Other sprites
            self.box_image = pygame.image.load(os.path.join(self.asset_path, 'box_hadiah.png')).convert_alpha()
            self.platform_image = pygame.image.load(os.path.join(self.asset_path, 'platform.png')).convert_alpha()
            
            finish_img_raw = pygame.image.load(os.path.join(self.asset_path, 'finish.png')).convert_alpha()
            self.finish_image = pygame.transform.scale(finish_img_raw, (128, 128))
            
            self.surat_1_image = pygame.image.load(os.path.join(self.asset_path, 'surat_1.png')).convert_alpha()
            surat_2_raw = pygame.image.load(os.path.join(self.asset_path, 'surat_2.png')).convert_alpha()
            self.surat_2_image = pygame.transform.scale(
                surat_2_raw,
                (int(WIDTH * 0.8), int(HEIGHT * 0.8))
            )
        except pygame.error:
            # Create placeholder other sprites
            self.box_image = self._create_sprite_placeholder(32, 32, (139, 69, 19))
            self.platform_image = self._create_sprite_placeholder(32, 32, (100, 100, 100))
            self.finish_image = self._create_sprite_placeholder(128, 128, (255, 215, 0))
            self.surat_1_image = self._create_sprite_placeholder(400, 300, (255, 255, 255))
            self.surat_2_image = self._create_sprite_placeholder(400, 300, (255, 255, 255))
    
    def _create_sprite_placeholder(self, width, height, color):
        """Create a colored rectangle as placeholder sprite"""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface.fill(color)
        # Add border
        pygame.draw.rect(surface, (0, 0, 0), surface.get_rect(), 2)
        return surface
    
    def _create_button_placeholder(self, text, width, height, color):
        """Create a button placeholder with text"""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface.fill(color)
        pygame.draw.rect(surface, (0, 0, 0), surface.get_rect(), 3)
        
        # Add text
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(width//2, height//2))
        surface.blit(text_surface, text_rect)
        
        return surface
    # ENKAPSULASI: Method PUBLIC - dapat diakses dari luar class
    def load_sounds(self):
        try:
            self.explosion_sound = pygame.mixer.Sound(os.path.join(self.sound_path, 'meledak.mp3'))
            self.box_hit_sound = pygame.mixer.Sound(os.path.join(self.sound_path, 'hintBlock.mp3'))
            self.surat_sound = pygame.mixer.Sound(os.path.join(self.sound_path, 'surat.mp3'))
            self.finish_sound = pygame.mixer.Sound(os.path.join(self.sound_path, 'sound_finish.mp3'))
            self.jump_sound = pygame.mixer.Sound(os.path.join(self.sound_path, 'jump.mp3'))
            self.background_music = os.path.join(self.sound_path, 'background_sfx.mp3')
        except pygame.error:
            # Create placeholder sounds (silent)
            print("Warning: Sound files not found, using silent placeholders")
            self.explosion_sound = pygame.mixer.Sound(buffer=b'\x00\x00' * 1000)
            self.box_hit_sound = pygame.mixer.Sound(buffer=b'\x00\x00' * 1000)
            self.surat_sound = pygame.mixer.Sound(buffer=b'\x00\x00' * 1000)
            self.finish_sound = pygame.mixer.Sound(buffer=b'\x00\x00' * 1000)
            self.jump_sound = pygame.mixer.Sound(buffer=b'\x00\x00' * 1000)
            self.background_music = None
    
    def setup_fonts(self):
        self.font = pygame.font.Font(None, 48)
        self.timer_font = pygame.font.Font(None, 36)