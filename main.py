from program3 import *  # from program1 import, import pics *, import numpy as np
from rotation import *
import mediapipe as mp
import cv2
import math


pygame.init()
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
a = [[3, 1, 1, 1, 3], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [3, 1, 1, 1, 3]]
a_copy = [[3, 1, 1, 1, 3], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [3, 1, 1, 1, 3]]
a_ans = solution(len(a_copy), len(a_copy[0]), a_copy)
handsDetector = mp.solutions.hands.Hands()
cap = cv2.VideoCapture(0)
clock = pygame.time.Clock()
running = True
objects = f(a)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    results = get_hands(cap, handsDetector)
    drawing(screen, objects)
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
                ex = int(results.multi_hand_landmarks[i].landmark[12].x * WIDTH)
                ey = int(results.multi_hand_landmarks[i].landmark[12].y * HEIGHT)
                x, y = x1 - x2, y1 - y2
                angle = math.atan2(y, x)
                if abs(ex - x2) + abs(ey - y2) > 150:
                    if object_index is not None:
                        r_angle = (math.degrees(angle) + 45) // 90 * 90
                        if r_angle < 0:
                            r_angle += 360
                        change_rotation(r_angle, objects, object_index)
    if check_solution(a, a_ans):
        running = 1
    pygame.display.flip()
    clock.tick(120)

handsDetector.close()
pygame.quit()
