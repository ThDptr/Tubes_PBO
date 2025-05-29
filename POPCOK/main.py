import pygame
import sys
from src.game_manager import GameManager
from src.constants import WIDTH, HEIGHT

def main():
    pygame.init()
    pygame.mixer.init()
    
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("POPCOK")
    
    game_manager = GameManager(WIN)
    game_manager.run()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()