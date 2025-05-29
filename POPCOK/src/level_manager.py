import pygame
from .constants import TILE_SIZE, TILE_MAP
from .entities.player import Player
from .entities.enemy import Enemy
from .entities.traps import MovingPiringTrap, MovingPiringDownTrap, MovingPiringUpTrap
from .platforms import Platform, FakePlatform, TimedPlatform, InvisiblePlatform, HiddenPlatform
from .entities.box import Box
from .entities.finish import Finish, FakeFinishKill, FakeFinishTeleport, FakeFinishHide

class LevelManager:
    def __init__(self, assets):
        self.assets = assets
        self.platforms = pygame.sprite.Group()
        self.moving_piring_traps = pygame.sprite.Group()
        self.moving_piring_down_traps = pygame.sprite.Group()
        self.moving_piring_up_traps = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.boxes = pygame.sprite.Group()
        self.finish_group = pygame.sprite.Group()
        self.fake_finish_group = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.hidden_platforms = []
        self.fake_platforms = pygame.sprite.Group()
        self.timed_platforms = pygame.sprite.Group()
        self.invisible_platforms = pygame.sprite.Group()
        self.initial_enemies = []  # FIXED: Only store original enemies from level
        self.spawned_enemies = []  # NEW: Track enemies spawned from boxes separately
        
        self.player = None
        self.spawn_pos = (0, 0)
        self.level_width = 0
        self.real_finish_hidden = False
    
    def build_level(self):
        # Clear all groups
        self._clear_all_groups()
        
        self.player = None
        self.spawn_pos = (0, 0)
        self.level_width = 0
        self.real_finish_hidden = False
        
        # Build level from tile map
        for row_index, row in enumerate(TILE_MAP):
            for col_index, cell in enumerate(row):
                x = col_index * 32
                y = row_index * TILE_SIZE
                
                self._create_tile_object(cell, x, y)
                self.level_width = max(self.level_width, x)
        
        # Create player
        self.player = Player(*self.spawn_pos, self.assets)
        self.all_sprites.add(self.player)
        self.level_width += TILE_SIZE
    
    def _clear_all_groups(self):
        self.platforms.empty()
        self.moving_piring_traps.empty()
        self.moving_piring_down_traps.empty()
        self.moving_piring_up_traps.empty()
        self.enemies.empty()
        self.boxes.empty()
        self.finish_group.empty()
        self.fake_finish_group.empty()
        self.all_sprites.empty()
        self.fake_platforms.empty()
        self.timed_platforms.empty()
        self.invisible_platforms.empty()
        self.hidden_platforms = []
        self.initial_enemies = []
        self.spawned_enemies = []  # NEW: Clear spawned enemies list
    
    def _create_tile_object(self, cell, x, y):
        if cell == 'P':
            plat = Platform(x, y, self.assets)
            self.platforms.add(plat)
            self.all_sprites.add(plat)
        elif cell == 'Q':
            moving_piring = MovingPiringTrap(x, y, self.assets)
            self.moving_piring_traps.add(moving_piring)
            self.all_sprites.add(moving_piring)
        elif cell == 'A':
            moving_piring_down = MovingPiringDownTrap(x, y, self.assets)
            self.moving_piring_down_traps.add(moving_piring_down)
            self.all_sprites.add(moving_piring_down)
        elif cell == 'B':
            moving_piring_up = MovingPiringUpTrap(x, y, self.assets)
            self.moving_piring_up_traps.add(moving_piring_up)
            self.all_sprites.add(moving_piring_up)
        elif cell == 'C':  # Box (moved from B to C)
            box = Box(x, y, self.assets)
            self.platforms.add(box)
            self.boxes.add(box)
            self.all_sprites.add(box)
        elif cell == 'E':
            enemy = Enemy(x, y, self.assets)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
            self.initial_enemies.append((x, y))  # FIXED: Only add original enemies
        elif cell == 'F':
            finish = Finish(x, y - 64, self.assets)
            self.finish_group.add(finish)
            self.all_sprites.add(finish)
        elif cell == 'V':
            fake_finish = FakeFinishKill(x, y - 64, self.assets)
            self.fake_finish_group.add(fake_finish)
            self.all_sprites.add(fake_finish)
        elif cell == 'U':
            fake_finish = FakeFinishTeleport(x, y - 64, self.assets)
            self.fake_finish_group.add(fake_finish)
            self.all_sprites.add(fake_finish)
        elif cell == 'Y':
            fake_finish = FakeFinishHide(x, y - 64, self.assets)
            self.fake_finish_group.add(fake_finish)
            self.all_sprites.add(fake_finish)
        elif cell == 'S':
            self.spawn_pos = (x, y)
        elif cell == 'I':
            self.hidden_platforms.append((x, y))
        elif cell == 'J':
            fake_plat = FakePlatform(x, y, self.assets)
            self.fake_platforms.add(fake_plat)
            self.all_sprites.add(fake_plat)
        elif cell == 'O':
            timed_plat = TimedPlatform(x, y, self.assets)
            self.platforms.add(timed_plat)
            self.timed_platforms.add(timed_plat)
            self.all_sprites.add(timed_plat)
        elif cell == 'X':
            invisible_plat = InvisiblePlatform(x, y, self.assets)
            self.platforms.add(invisible_plat)
            self.invisible_platforms.add(invisible_plat)
            self.all_sprites.add(invisible_plat)
    
    def spawn_enemy_from_box(self, box_x, box_y):
        """NEW: Method to spawn enemy from box and track it separately"""
        enemy = Enemy(box_x, box_y - TILE_SIZE, self.assets)
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)
        self.spawned_enemies.append((box_x, box_y - TILE_SIZE))  # Track spawned enemies separately
        return enemy
    
    def check_hidden_platforms(self):
        for i, (hx, hy) in enumerate(self.hidden_platforms[:]):
            if abs(self.player.rect.centerx - (hx + TILE_SIZE/2)) < TILE_SIZE*2 and abs(self.player.rect.centery - (hy + TILE_SIZE/2)) < TILE_SIZE*2:
                plat = HiddenPlatform(hx, hy, self.assets)
                self.platforms.add(plat)
                self.all_sprites.add(plat)
                self.hidden_platforms.remove((hx, hy))
    
    def reset_all_objects(self):
        # Reset all objects but keep enemies properly managed
        for fake_plat in self.fake_platforms:
            fake_plat.reset()
        for timed_plat in self.timed_platforms:
            timed_plat.reset()
        for invisible_plat in self.invisible_platforms:
            invisible_plat.reset()
        for moving_piring in self.moving_piring_traps:
            moving_piring.reset()
        for moving_piring_down in self.moving_piring_down_traps:
            moving_piring_down.reset()
        for moving_piring_up in self.moving_piring_up_traps:
            moving_piring_up.reset()
        for box in self.boxes:
            box.reset()
        
        # FIXED: Properly reset enemies
        # Remove all current enemies from groups
        for enemy in self.enemies.copy():
            enemy.kill()
        self.enemies.empty()
        
        # Clear spawned enemies list
        self.spawned_enemies = []
        
        # Respawn only original enemies from level (not from boxes)
        for initial_pos in self.initial_enemies:
            enemy = Enemy(initial_pos[0], initial_pos[1], self.assets)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
        
        # Remove hidden platforms that appeared
        for platform in self.platforms.copy():
            if hasattr(platform, 'is_hidden_platform') and platform.is_hidden_platform:
                platform.kill()
        
        # Reset finish visibility
        for finish in self.finish_group:
            finish.reset()
        for fake_finish in self.fake_finish_group:
            if hasattr(fake_finish, 'reset'):
                fake_finish.reset()
        self.real_finish_hidden = False
        
        # Reset hidden platforms list
        self.hidden_platforms = []
        for row_index, row in enumerate(TILE_MAP):
            for col_index, cell in enumerate(row):
                if cell == 'I':
                    x = col_index * 32
                    y = row_index * TILE_SIZE
                    self.hidden_platforms.append((x, y))