import pygame
from ..constants import EXPLOSION_DELAY, HEIGHT, TILE_SIZE

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, assets):
        super().__init__()
        # Aset dan sprite
        self.assets = assets
        self.idle_image = assets.player_idle_image
        self.run_images = assets.player_run_images
        self.jump_image = assets.player_jump_image
        self.explosion_images = assets.explosion_images
        self.image = self.idle_image
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Collision box
        self.collision_rect = pygame.Rect(
            x + self.rect.width * 0.1,
            y + self.rect.height * 0.1,
            self.rect.width * 0.8,
            self.rect.height * 0.8
        )
        
        # Movement & state
        self.dx = 0
        self.dy = 0
        self.on_ground = False
        
        # PRIVATE SEJATI: invincibility flag
        # Tidak dapat diakses langsung dari luar class (name-mangled)
        self.__invincible = False  
        
        # Animasi
        self.anim_index = 0
        self.anim_counter = 0
        self.facing_right = True
        
        # Explosion & death
        self.exploding = False
        self.explode_frame = 0
        self.explode_timer = 0
        self.explode_count = 0
        self.death_y = HEIGHT + 100
        self.standing_on = None
        self.death_by_falling = False
        self.explosion_finished = False
        self.is_dead = False

    def update(self, platforms, fake_platforms, invisible_platforms, level_manager):
        # Jika sudah mati dan tidak sedang meledak, hentikan update
        if self.is_dead and not self.exploding:
            return
        
        # Tangani animasi ledakan
        if self.exploding:
            self.explode_timer += 1
            if self.explode_timer % EXPLOSION_DELAY == 0:
                if self.explode_frame < len(self.explosion_images):
                    self.image = self.explosion_images[self.explode_frame]
                    if not self.facing_right:
                        self.image = pygame.transform.flip(self.image, True, False)
                    self.explode_frame += 1
                else:
                    # Animasi ledakan selesai
                    self.explosion_finished = True
                    self.exploding = False
                    self.explode_frame = 0
                    self.explode_timer = 0
                    self.is_dead = True
            return
        
        # Input dan gerakan horizontal
        keys = pygame.key.get_pressed()
        self.dx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.dx = -5
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.dx = 5
            self.facing_right = True
        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.on_ground:
            self.dy = -12
            self.on_ground = False
            self.assets.jump_sound.play()
        
        # Pergerakan horizontal & deteksi tabrakan
        self.rect.x += self.dx
        self.collision_rect.x = self.rect.x + self.rect.width * 0.1
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for plat in hits:
            if self.dx > 0:
                self.rect.right = plat.rect.left
                self.collision_rect.right = plat.rect.left
            elif self.dx < 0:
                self.rect.left = plat.rect.right
                self.collision_rect.left = plat.rect.right
        
        self.standing_on = None
        self.on_ground = False
        
        # Gravitasi & gerakan vertikal
        self.dy += 0.5
        self.rect.y += self.dy
        self.collision_rect.y = self.rect.y + self.rect.height * 0.1
        
        # Jika jatuh di bawah layar, mulai ledakan
        if self.rect.y > self.death_y:
            self.death_by_falling = True
            self.explode()
            return
        
        # Tabrakan dengan berbagai jenis platform
        self._handle_platform_collisions(platforms, fake_platforms, invisible_platforms, level_manager)
        
        # Update animasi berjalan/jumping/idling
        self._update_animation()

    def _handle_platform_collisions(self, platforms, fake_platforms, invisible_platforms, level_manager):
        # Fake platforms
        fake_hits = pygame.sprite.spritecollide(self, fake_platforms, False)
        for plat in fake_hits:
            if self.dy > 0 and self.rect.bottom <= plat.rect.top + 1 and plat.active:
                self.rect.bottom = plat.rect.top
                self.collision_rect.bottom = plat.rect.top
                self.dy = 0
                self.on_ground = True
                self.standing_on = plat
                plat.stepped_on = True
        
        # Invisible platforms
        invisible_hits = pygame.sprite.spritecollide(self, invisible_platforms, False)
        for plat in invisible_hits:
            if self.dy > 0 and self.rect.bottom <= plat.rect.top + 1:
                self.rect.bottom = plat.rect.top
                self.collision_rect.bottom = plat.rect.top
                self.dy = 0
                self.on_ground = True
                self.standing_on = plat
        
        # Regular platforms
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for plat in hits:
            if self.dy > 0:
                if hasattr(plat, 'active') and not plat.active:
                    continue
                self.rect.bottom = plat.rect.top
                self.collision_rect.bottom = plat.rect.top
                self.dy = 0
                self.on_ground = True
                self.standing_on = plat
            elif self.dy < 0:
                if hasattr(plat, 'hit') and not plat.used:
                    if plat.hit():
                        level_manager.spawn_enemy_from_box(plat.rect.x, plat.rect.y)
                self.rect.top = plat.rect.bottom
                self.collision_rect.top = plat.rect.bottom
                self.dy = 0
        
        # Jika platform tempat berdiri tidak aktif lagi
        if self.standing_on:
            if hasattr(self.standing_on, 'active') and not self.standing_on.active:
                self.on_ground = False
                self.dy = 0.1

    def _update_animation(self):
        if not self.on_ground:
            self.image = self.jump_image
        elif self.dx == 0:
            self.image = self.idle_image
        else:
            self.anim_counter += 1
            if self.anim_counter > 5:
                self.anim_index = (self.anim_index + 1) % len(self.run_images)
                self.anim_counter = 0
            self.image = self.run_images[self.anim_index]
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def explode(self):
        if not self.exploding and not self.is_dead:
            self.exploding = True
            self.explode_frame = 0
            self.explode_timer = 0
            self.explode_count += 1
            self.explosion_finished = False
            self.assets.explosion_sound.play()

    def respawn(self, spawn_pos):
        # Reset posisi dan state dasar
        self.rect.topleft = spawn_pos
        self.collision_rect.topleft = (
            spawn_pos[0] + self.rect.width * 0.1,
            spawn_pos[1] + self.rect.height * 0.1
        )
        self.dx = 0
        self.dy = 0
        self.on_ground = False
        self.standing_on = None
        self.death_by_falling = False
        self.explosion_finished = False
        self.exploding = False
        self.explode_frame = 0
        self.explode_timer = 0
        self.is_dead = False
        
        # Panggil PRIVATE SEJATI method untuk reset animasi
        self.__reset_animation()

    def teleport_to_start(self, spawn_pos):
        # Gunakan respawn untuk memindahkan & reset
        self.respawn(spawn_pos)

    # ===== PRIVATE SEJATI =====
    def __reset_animation(self):
        """
        Private method sejati (name-mangled) untuk mereset
        anim_index dan anim_counter.
        """
        self.anim_index = 0
        self.anim_counter = 0
