import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, assets):
        super().__init__()
        self.assets = assets
        self.idle_image = assets.enemy_idle_img
        self.run_images = assets.enemy_run_images
        self.anim_index = 0
        self.image = self.idle_image
        # Adjust position downward to prevent floating (adjust the 10 pixels as needed)
        self.rect = self.image.get_rect(topleft=(x, y + 40))
        self.dx = -2
        self.dy = 0
        self.animation_counter = 0
        self.animation_speed = 8  # Controls how fast animation changes
        self.facing_left = True  # Track direction for flipping
        self.idle_timer = 0  # Timer for idle state when hitting wall
        self.idle_duration = 10  # How long to stay idle (in frames, ~1 second at 60 FPS)
        self.is_idle = False  # Whether enemy is currently in idle state
        self.initial_x = x  # Store initial position for respawning
        self.initial_y = y + 40  # Store adjusted position
    
    def update(self, platforms):
        self.dy += 0.5  # gravity
        
        # Handle idle state when hitting wall
        if self.is_idle:
            self.idle_timer += 1
            self.image = self.get_flipped_image(self.idle_image)
            if self.idle_timer >= self.idle_duration:
                self.is_idle = False
                self.idle_timer = 0
        else:
            # Normal movement
            self.rect.x += self.dx
            
            # Update animation when moving
            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.animation_counter = 0
                self.anim_index = (self.anim_index + 1) % len(self.run_images)
            
            current_frame = self.run_images[self.anim_index]
            self.image = self.get_flipped_image(current_frame)
        
        # Horizontal collision
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for platform in hits:
            if not self.is_idle:  # Only process collision if not already idle
                if self.dx > 0:
                    self.rect.right = platform.rect.left
                    self.dx = -self.dx
                    self.facing_left = True
                    self.start_idle()
                elif self.dx < 0:
                    self.rect.left = platform.rect.right
                    self.dx = -self.dx
                    self.facing_left = False
                    self.start_idle()
        
        # Vertical movement
        self.rect.y += self.dy
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for platform in hits:
            if self.dy > 0:
                self.rect.bottom = platform.rect.top
                self.dy = 0
            elif self.dy < 0:
                self.rect.top = platform.rect.bottom
                self.dy = 0
    
    def get_flipped_image(self, image):
        """Return flipped image based on facing direction"""
        if self.facing_left:
            return pygame.transform.flip(image, True, False)
        else:
            return image
    
    def start_idle(self):
        """Start idle state when hitting wall"""
        self.is_idle = True
        self.idle_timer = 0
    
    def reset_position(self):
        """Reset enemy to initial position"""
        self.rect.x = self.initial_x
        self.rect.y = self.initial_y
        self.dx = -2
        self.dy = 0
        self.facing_left = True
        self.is_idle = False
        self.idle_timer = 0