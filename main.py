import time
from events import *
from check import *
from pics import *


pygame.init()
pygame.display.set_caption("plumbing")
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

if not starting_message(screen):
    pygame.quit()
    exit(0)
if not instruction(screen):
    pygame.quit()
    exit(0)
level(screen, 0)
pygame.quit()
