import pygame

class Finish(pygame.sprite.Sprite):
    def __init__(self, x, y, assets):
        super().__init__()
        self.assets = assets
        self.original_image = assets.finish_image.copy()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.visible = True
        self.hiding = False
        self.hide_timer = 0
    
    def hide(self):
        if not self.hiding:
            self.hiding = True
            self.hide_timer = 0
    
    def update(self):
        if self.hiding:
            self.hide_timer += 1
            if self.hide_timer > 1 and self.hide_timer < 2:
                self.image.set_alpha(150)
            elif self.hide_timer > 2 and self.hide_timer < 3:
                self.image.set_alpha(100)
            elif self.hide_timer > 3:
                self.visible = False
                self.image.set_alpha(0)
    
    def show(self):
        self.visible = True
        self.hiding = False
        self.hide_timer = 0
        self.image = self.original_image.copy()
        self.image.set_alpha(255)
    
    def reset(self):
        self.show()

class FakeFinishKill(pygame.sprite.Sprite):
    def __init__(self, x, y, assets):
        super().__init__()
        self.assets = assets
        self.image = assets.finish_image.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.fake_type = "kill"

class FakeFinishTeleport(pygame.sprite.Sprite):
    def __init__(self, x, y, assets):
        super().__init__()
        self.assets = assets
        self.image = assets.finish_image.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.fake_type = "teleport"

class FakeFinishHide(pygame.sprite.Sprite):
    def __init__(self, x, y, assets):
        super().__init__()
        self.assets = assets
        self.image = assets.finish_image.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.fake_type = "hide"
        self.hiding = False
        self.hide_timer = 0
    
    def update(self):
        if self.hiding:
            self.hide_timer += 1
            if self.hide_timer > 1 and self.hide_timer < 2:
                self.image.set_alpha(150)
            elif self.hide_timer > 2 and self.hide_timer < 3:
                self.image.set_alpha(100)
            elif self.hide_timer > 3:
                self.image.set_alpha(0)
    
    def hide(self):
        if not self.hiding:
            self.hiding = True
            self.hide_timer = 0
    
    def reset(self):
        self.hiding = False
        self.hide_timer = 0
        self.image = self.assets.finish_image.copy()
        self.image.set_alpha(255)