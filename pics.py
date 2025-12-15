import pygame

# 1 - прямая труба вправо
# 2 - прямая труба влево
# 3 - труба верх лево
# 4 - труба верх право
# 5 - труба вниз вправо
# 6 - труба вниз влево

pipe_t2 = pygame.image.load('pipes1_v10.png')
pipe_t2 = pygame.transform.scale(pipe_t2, (100, 100))
pipe_t1 = pygame.transform.rotate(pipe_t2, 90)
pipe_t6 = pygame.image.load('pipes2_v5.png')
pipe_t6 = pygame.transform.scale(pipe_t6, (100, 100))
pipe_t5 = pygame.transform.rotate(pipe_t6, 90)
pipe_t4 = pygame.transform.rotate(pipe_t6, 180)
pipe_t3 = pygame.transform.rotate(pipe_t6, 270)

# список картинок труб
pic = [1e9, pipe_t1, pipe_t2, pipe_t3, pipe_t4, pipe_t5, pipe_t6]
