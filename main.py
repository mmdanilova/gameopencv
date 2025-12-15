from program3 import *  # from program1 import *
from pics import *  # import pygame
from rotation import *

pygame.init()
WIDTH, HEIGHT = 1100, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
a = [[3, 1, 1, 1, 1, 1, 1, 1, 1, 3], [1, 3, 1, 1, 1, 1, 1, 1, 3, 1], [1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
     [1, 3, 1, 1, 1, 1, 1, 1, 3, 1], [3, 1, 1, 1, 1, 1, 1, 1, 1, 3]]
running = 1
objects = []  # функция для создания объектов

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    results = get_hands()
    drawing(screen, a)

    object_index = None
    if results.multi_handedness:
        object_index, x, y = get_object(results, objects)
        if x and y:
            screen.blit(key.image, (x, y))

        for i in range(len(results.multi_handedness)):
            if "Right" in str(results.multi_handedness[i]):
                x1 = int(results.multi_hand_landmarks[i].landmark[8].x * WIDTH)
                y1 = int(results.multi_hand_landmarks[i].landmark[8].y * HEIGHT)
                x2 = int(results.multi_hand_landmarks[i].landmark[0].x * WIDTH)
                y2 = int(results.multi_hand_landmarks[i].landmark[0].y * HEIGHT)
                x, y = x1 - x2, y1 - y2
                angle = math.atan2(y, x)
                if object_index is not None:
                    objects[object_index].angle = -(math.degrees(angle) + 45) // 90 * 90

    pygame.display.flip()
    clock.tick(120)

handsDetector.close()
pygame.quit()
