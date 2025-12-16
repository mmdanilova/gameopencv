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
txt1 = pygame.image.load('congratulations_txt-Photoroom.png')
txt1 = pygame.transform.scale(txt1, (int(1.5 * 600), int(1.5 * 435)))
hand1 = pygame.image.load('ladon.png')
hand1 = pygame.transform.scale(hand1, (int(0.5 * hand1.get_rect()[2]), int(0.5 * hand1.get_rect()[3])))
hand2 = pygame.image.load('hand2.webp')
hand2 = pygame.transform.scale(hand2, (int(0.2 * hand2.get_rect()[2]), int(0.2 * hand2.get_rect()[3])))
hand3 = pygame.image.load('image-Photoroom.png')
hand3 = pygame.transform.scale(hand3, (int(0.7 * hand3.get_rect()[2]), int(0.7 * hand3.get_rect()[3])))
hand3 = pygame.transform.rotate(hand3, 330)


key = pygame.image.load("key.png")
key = pygame.transform.scale(key, (50, 50))
key1 = picture(key, 1100//2, 600//2, 50, 50, 0)

# список картинок труб
pic = [1e9, pipe_t1, pipe_t2, pipe_t3, pipe_t4, pipe_t5, pipe_t6]
