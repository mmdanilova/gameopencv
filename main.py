import time
from events import *
from check import *
from pics import *


pygame.init()
pygame.display.set_caption("plumbing")
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

instruction(screen)
level(screen, 0)
#Здесь можно по порядку вызывать уровни
pygame.quit()
