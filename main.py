from program3 import *  # from program1 import *
from pics import *  # import pygame

pygame.init()
WIDTH, HEIGHT = 1100, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
a = [[3, 1, 1, 1, 1, 1, 1, 1, 1, 3], [1, 3, 1, 1, 1, 1, 1, 1, 3, 1], [1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
     [1, 3, 1, 1, 1, 1, 1, 1, 3, 1], [3, 1, 1, 1, 1, 1, 1, 1, 1, 3]]
a_c = [[3, 1, 1, 1, 1, 1, 1, 1, 1, 3], [1, 3, 1, 1, 1, 1, 1, 1, 3, 1], [1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
       [1, 3, 1, 1, 1, 1, 1, 1, 3, 1], [3, 1, 1, 1, 1, 1, 1, 1, 1, 3]]
a1 = solution(len(a), len(a[0]), a_c)
show_ans(a, a1)
