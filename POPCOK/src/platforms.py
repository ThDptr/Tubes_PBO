import pygame
from .constants import TILE_SIZE

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, assets):
        super().__init__()
        self.assets = assets
        self.image = assets.platform_image
        self.rect = self.image.get_rect(topleft=(x, y))

class HiddenPlatform(Platform):
    def __init__(self, x, y, assets):
        super().__init__(x, y, assets)
        self.is_hidden_platform = True

class InvisiblePlatform(Platform):
    def __init__(self, x, y, assets):
        super().__init__(x, y, assets)
        self.image = assets.platform_image.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.cycle_timer = 0
        self.visible = False
        self.image.set_alpha(0)
    
    def update(self):
        self.cycle_timer += 1/60
        cycle_time = self.cycle_timer % 6.5
        
        if cycle_time < 5.0:
            if self.visible:
                self.visible = False
                self.image.set_alpha(0)
        else:
            if not self.visible:
                self.visible = True
                self.image.set_alpha(255)
    
    def reset(self):
        self.cycle_timer = 0
        self.visible = False
        self.image = self.assets.platform_image.copy()
        self.image.set_alpha(0)

class FakePlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, assets):
        super().__init__()
        self.assets = assets
        self.image = assets.platform_image.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.stepped_on = False
        self.disappear_timer = 0
        self.active = True
    
    def update(self):
        if self.stepped_on:
            self.disappear_timer += 1
            if self.disappear_timer > 1 and self.disappear_timer < 2:
                self.image.set_alpha(150)
            elif self.disappear_timer > 2 and self.disappear_timer < 3:
                self.image.set_alpha(100)
            elif self.disappear_timer > 3:
                self.active = False
                self.image.set_alpha(0)
    
    def reset(self):
        self.stepped_on = False
        self.disappear_timer = 0
        self.active = True
        self.image = self.assets.platform_image.copy()
        self.image.set_alpha(255)

class TimedPlatform(Platform):
    def __init__(self, x, y, assets):
        super().__init__(x, y, assets)
        self.image = assets.platform_image.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.disappear_times = [3, 7, 11, 35, 40]
        self.visible = True
        self.blink_start = 0.5
        self.active = True
    
    def update(self, current_time):
        for disappear_time in self.disappear_times:
            if abs(current_time - disappear_time) < self.blink_start and current_time < disappear_time:
                blink_speed = max(1, int((disappear_time - current_time) * 40))
                if int(current_time * 40) % blink_speed < blink_speed // 2:
                    self.image.set_alpha(255)
                else:
                    self.image.set_alpha(100)
                break
            elif current_time >= disappear_time and current_time < disappear_time + 0.5:
                self.visible = False
                self.active = False
                self.image.set_alpha(0)
                break
            elif current_time >= disappear_time + 0.5:
                self.visible = True
                self.active = True
                self.image.set_alpha(255)
        
        if self.visible and all(abs(current_time - t) >= self.blink_start or current_time > t + 0.5 for t in self.disappear_times):
            self.image.set_alpha(255)
    
    def reset(self):
        self.visible = True
        self.active = True
        self.image = self.assets.platform_image.copy()
        self.image.set_alpha(255)