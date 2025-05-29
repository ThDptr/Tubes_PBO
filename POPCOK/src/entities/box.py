import pygame

class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, assets):
        super().__init__()
        self.assets = assets
        self.original_image = assets.box_image.copy()
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.used = False
    
    def hit(self):
        if not self.used:
            self.used = True
            self.image = self.original_image.copy()
            self.image.fill((120, 60, 20), special_flags=pygame.BLEND_MULT)
            self.assets.box_hit_sound.play()
            return True
        return False
    
    def reset(self):
        self.used = False
        self.image = self.original_image.copy()