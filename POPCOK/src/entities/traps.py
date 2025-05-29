import pygame
from ..constants import TILE_SIZE


class MovingPiringDownTrap(pygame.sprite.Sprite):
    def __init__(self, x, y, assets):
        super().__init__()
        self.assets = assets
        self.images = assets.piring_images
        self.index = 0
        self.image = self.images[self.index]
        self.original_x = x
        self.original_y = y
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animation_counter = 0
        self.triggered = False
        self.moving = False
        self.move_speed = 5  # Faster than Q traps
        self.move_distance = 0
        self.max_move_distance = TILE_SIZE * 8
        
        mask_size = int(min(self.rect.width, self.rect.height) * 0.7)
        self.collision_rect = pygame.Rect(
            x + (self.rect.width - mask_size) // 2,
            y + (self.rect.height - mask_size) // 2,
            mask_size, mask_size
        )
    
    def check_player_proximity(self, player_x, player_y):
        horizontal_distance = abs(player_x - self.rect.centerx)
        horizontal_trigger = 3 * TILE_SIZE
        
        # Only trigger if player is below the trap
        if player_y > self.rect.bottom and horizontal_distance <= horizontal_trigger and not self.triggered:
            self.triggered = True
            self.moving = True
    
    def update(self):
        # Animation
        self.animation_counter += 1
        if self.animation_counter >= 8:
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
            self.animation_counter = 0
        
        # Movement - only move down
        if self.moving:
            self.rect.y += self.move_speed
            self.move_distance += self.move_speed
            
            if self.move_distance >= self.max_move_distance:
                self.moving = False
        
        # Update collision rect
        self.collision_rect.x = self.rect.x + (self.rect.width - self.collision_rect.width) // 2
        self.collision_rect.y = self.rect.y + (self.rect.height - self.collision_rect.height) // 2
    
    def reset(self):
        self.index = 0
        self.image = self.images[self.index]
        self.animation_counter = 0
        self.triggered = False
        self.moving = False
        self.move_distance = 0
        self.rect.x = self.original_x
        self.rect.y = self.original_y

# NEW: Moving Piring Trap Up (B) - moves up with same speed as A
class MovingPiringUpTrap(pygame.sprite.Sprite):
    def __init__(self, x, y, assets):
        super().__init__()
        self.assets = assets
        self.images = assets.piring_images
        self.index = 0
        self.image = self.images[self.index]
        self.original_x = x
        self.original_y = y
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animation_counter = 0
        self.triggered = False
        self.moving = False
        self.move_speed = 5  # Same speed as A traps
        self.move_distance = 0
        self.max_move_distance = TILE_SIZE * 8
        
        mask_size = int(min(self.rect.width, self.rect.height) * 0.7)
        self.collision_rect = pygame.Rect(
            x + (self.rect.width - mask_size) // 2,
            y + (self.rect.height - mask_size) // 2,
            mask_size, mask_size
        )
    
    def check_player_proximity(self, player_x, player_y):
        horizontal_distance = abs(player_x - self.rect.centerx)
        horizontal_trigger = 3 * TILE_SIZE
        
        # Only trigger if player is above the trap
        if player_y < self.rect.top and horizontal_distance <= horizontal_trigger and not self.triggered:
            self.triggered = True
            self.moving = True
    
    def update(self):
        # Animation
        self.animation_counter += 1
        if self.animation_counter >= 8:
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
            self.animation_counter = 0
        
        # Movement - only move up
        if self.moving:
            self.rect.y -= self.move_speed
            self.move_distance += self.move_speed
            
            if self.move_distance >= self.max_move_distance:
                self.moving = False
        
        # Update collision rect
        self.collision_rect.x = self.rect.x + (self.rect.width - self.collision_rect.width) // 2
        self.collision_rect.y = self.rect.y + (self.rect.height - self.collision_rect.height) // 2
    
    def reset(self):
        self.index = 0
        self.image = self.images[self.index]
        self.animation_counter = 0
        self.triggered = False
        self.moving = False
        self.move_distance = 0
        self.rect.x = self.original_x
        self.rect.y = self.original_y

# Existing Moving Piring Trap (Q) - horizontal movement
class MovingPiringTrap(pygame.sprite.Sprite):
    def __init__(self, x, y, assets):
        super().__init__()
        self.assets = assets
        self.images = assets.piring_images
        self.index = 0
        self.image = self.images[self.index]
        self.original_x = x
        self.original_y = y
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animation_counter = 0
        self.triggered = False
        self.moving = False
        self.move_speed = 3
        self.move_direction = 0
        self.move_distance = 0
        self.max_move_distance = TILE_SIZE * 6
        
        mask_size = int(min(self.rect.width, self.rect.height) * 0.7)
        self.collision_rect = pygame.Rect(
            x + (self.rect.width - mask_size) // 2,
            y + (self.rect.height - mask_size) // 2,
            mask_size, mask_size
        )
    
    def check_player_proximity(self, player_x):
        distance = abs(player_x - self.rect.centerx)
        trigger_distance = 4 * TILE_SIZE
        
        if distance <= trigger_distance and not self.triggered:
            self.triggered = True
            self.moving = True
            if player_x < self.rect.centerx:
                self.move_direction = -1
            else:
                self.move_direction = 1
    
    def update(self):
        # Animation
        self.animation_counter += 1
        if self.animation_counter >= 8:
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
            self.animation_counter = 0
        
        # Movement
        if self.moving:
            move_amount = self.move_speed * self.move_direction
            self.rect.x += move_amount
            self.move_distance += abs(move_amount)
            
            if self.move_distance >= self.max_move_distance:
                self.moving = False
        
        # Update collision rect
        self.collision_rect.x = self.rect.x + (self.rect.width - self.collision_rect.width) // 2
        self.collision_rect.y = self.rect.y + (self.rect.height - self.collision_rect.height) // 2
    
    def reset(self):
        self.index = 0
        self.image = self.images[self.index]
        self.animation_counter = 0
        self.triggered = False
        self.moving = False
        self.move_direction = 0
        self.move_distance = 0
        self.rect.x = self.original_x
        self.rect.y = self.original_y