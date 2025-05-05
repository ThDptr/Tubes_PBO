import asyncio
import platform
import pygame
import sys
import random

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Popcok Adventure")
FPS = 60
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Load and scale assets
def load_image(img_path, scale_to=(32, 32)):
    image = pygame.image.load(img_path).convert_alpha()
    return pygame.transform.scale(image, scale_to)

assets = {
    "player_idle": load_image("diam.png", (48, 48)),  # Enlarged player
    "player_jump": load_image("lompat.png", (48, 48)),
    "player_run1": load_image("1berlari.png", (48, 48)),
    "player_run2": load_image("2berlari.png", (48, 48)),
    "player_explode": load_image("setelah_meledak.png", (48, 48)),
    "enemy1": load_image("musuh_jalan_1.png", (32, 32)),
    "enemy2": load_image("musuh_jalan_2.png", (32, 32)),
    "platform": load_image("platform.png", (64, 16)),
    "background": load_image("background.png", (WIDTH, HEIGHT)),
}

# Load start screen
start_screen = load_image("halaman_awal.png", (WIDTH, HEIGHT))

# Define button rectangles for "mulai" and "keluar" (adjust based on image)
mulai_rect = pygame.Rect(300, 400, 200, 50)  # Example coordinates
keluar_rect = pygame.Rect(300, 500, 200, 50)  # Example coordinates

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = {
            "idle": assets["player_idle"],
            "jump": assets["player_jump"],
            "run": [assets["player_run1"], assets["player_run2"]],
            "explode": assets["player_explode"]
        }
        self.image = self.images["idle"]
        self.rect = self.image.get_rect(bottomleft=(100, HEIGHT - 40))
        self.speed = 3.5  # Adjusted for better control
        self.jump_force = -9  # Adjusted for lower jump height
        self.gravity = 0.7  # Adjusted for natural fall
        self.direction = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.exploding = False
        self.animation_index = 0
        self.facing_right = True

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        if self.on_ground:
            self.direction.y = self.jump_force
            self.on_ground = False

    def move(self):
        keys = pygame.key.get_pressed()
        self.direction.x = 0
        if keys[pygame.K_LEFT]:  # Changed to arrow keys
            self.direction.x = -self.speed
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.direction.x = self.speed
            self.facing_right = True
        self.rect.x += self.direction.x

    def explode(self):
        if not self.exploding:
            self.exploding = True
            self.image = self.images["explode"]
            pygame.time.set_timer(pygame.USEREVENT, 1000)  # 1-second explosion before reset

    def update(self):
        if not self.exploding:
            self.move()
            self.apply_gravity()
            # Animation
            if not self.on_ground:
                self.image = self.images["jump"]
            elif self.direction.x != 0:
                self.animation_index += 0.2
                if self.animation_index >= len(self.images["run"]):
                    self.animation_index = 0
                self.image = self.images["run"][int(self.animation_index)]
            else:
                self.image = self.images["idle"]
            # Flip image based on direction
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = self.images["explode"]

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, patrol_range=100):
        super().__init__()
        self.images = [assets["enemy1"], assets["enemy2"]]
        self.image = self.images[0]
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.speed = 2
        self.direction = 1
        self.animation_index = 0
        self.start_x = x
        self.patrol_range = patrol_range
        self.facing_right = True

    def patrol(self):
        self.rect.x += self.speed * self.direction
        if self.rect.x < self.start_x or self.rect.x > self.start_x + self.patrol_range:
            self.direction *= -1
            self.facing_right = not self.facing_right
        self.animation_index += 0.1
        if self.animation_index >= len(self.images):
            self.animation_index = 0
        self.image = self.images[int(self.animation_index)]
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.patrol()

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w):
        super().__init__()
        self.image = pygame.transform.scale(assets["platform"], (w, 16))
        self.rect = self.image.get_rect(topleft=(x, y))

class Camera:
    def __init__(self, width, height, level_width):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.level_width = level_width

    def apply(self, entity):
        return entity.rect.move(-self.camera.x, -self.camera.y)

    def update(self, target):
        x = target.rect.centerx - self.width // 2
        self.camera.x = max(0, min(self.level_width - self.width, x))

async def main():
    # Sprite groups
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # Player
    player = Player()
    all_sprites.add(player)

    # Platforms
    platform_data = [
        (0, HEIGHT - 40, 2000),  # Continuous ground
        (200, HEIGHT - 150, 128),
        (400, HEIGHT - 200, 128),
        (600, HEIGHT - 250, 128),
        (900, HEIGHT - 200, 128),
        (1200, HEIGHT - 150, 128),
        (1500, HEIGHT - 250, 128),
    ]
    for x, y, w in platform_data:
        platform = Platform(x, y, w)
        platforms.add(platform)
        all_sprites.add(platform)

    # Enemies
    enemy_data = [
        (300, HEIGHT - 40, 100),
        (600, HEIGHT - 40, 100),
        (1000, HEIGHT - 40, 100),
    ]
    for x, y, range in enemy_data:
        enemy = Enemy(x, y, range)
        enemies.add(enemy)
        all_sprites.add(enemy)

    # Camera
    camera = Camera(WIDTH, HEIGHT, 2000)  # Level width is 2000

    game_state = "menu"
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_state == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mulai_rect.collidepoint(event.pos):
                        game_state = "playing"
                    elif keluar_rect.collidepoint(event.pos):
                        running = False
            elif game_state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.jump()
                if event.type == pygame.USEREVENT:
                    # Reset player position instead of restarting
                    player.rect.bottomleft = (100, HEIGHT - 40)
                    player.direction = pygame.math.Vector2(0, 0)
                    player.exploding = False
                    player.on_ground = False

        if game_state == "menu":
            screen.blit(start_screen, (0, 0))
        elif game_state == "playing":
            all_sprites.update()
            camera.update(player)

            # Collision with platforms
            platform_collisions = pygame.sprite.spritecollide(player, platforms, False)
            if platform_collisions:
                if player.direction.y > 0:
                    player.rect.bottom = platform_collisions[0].rect.top
                    player.direction.y = 0
                    player.on_ground = True
            else:
                player.on_ground = False

            # Check for falling or enemy collision
            if player.rect.y > HEIGHT:
                player.explode()
            if pygame.sprite.spritecollide(player, enemies, False):
                player.explode()

            # Draw
            screen.blit(assets["background"], (0, 0))
            for sprite in all_sprites:
                screen.blit(sprite.image, camera.apply(sprite))

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(1.0 / FPS)

    pygame.quit()
    sys.exit()

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())