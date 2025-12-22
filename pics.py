import pygame

# 1 - прямая труба влево
# 2 - прямая труба вверх
# 3 - труба верх лево
# 4 - труба верх право
# 5 - труба вниз вправо
# 6 - труба вниз влево

class picture:
    def __init__(self, img, x, y, width, height, pipe_type=0):
        self.image = img
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pipe_type = pipe_type  # 0 - не труба

pipe_t2 = pygame.image.load('pipes1_v10.png')
pipe_t2 = pygame.transform.scale(pipe_t2, (100, 100))
pipe_t1 = pygame.transform.rotate(pipe_t2, 90)
pipe_t6 = pygame.image.load('pipes2_v5.png')
pipe_t6 = pygame.transform.scale(pipe_t6, (100, 100))
pipe_t5 = pygame.transform.rotate(pipe_t6, 90)
pipe_t4 = pygame.transform.rotate(pipe_t6, 180)
pipe_t3 = pygame.transform.rotate(pipe_t6, 270)
big_pipe_t3 = pygame.image.load('pipes2_v5.png')
big_pipe_t3 = pygame.transform.scale(big_pipe_t3, (300, 300))
big_pipe_t3 = pygame.transform.rotate(big_pipe_t3, 270)


key = pygame.image.load("key.png")
big_key = pygame.transform.scale(key, (150, 150))
key = pygame.transform.scale(key, (50, 50))
key1 = picture(key, 1100//2, 600//2, 50, 50, 0)

# список картинок труб
pic = [1e9, pipe_t1, pipe_t2, pipe_t3, pipe_t4, pipe_t5, pipe_t6]
