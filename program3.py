import config
from program1 import *
import cv2
import numpy as np
import math
from pics import *  # import pygame
from rotation import *
import mediapipe as mp

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
a = [[0, 3, 1, 2, 4], [0, 2, 0, 0, 1], [0, 1, 0, 0, 1], [0, 6, 2, 2, 5]]
a2 = [[0, 3, 1, 2, 4], [0, 2, 0, 0, 1], [0, 1, 0, 0, 1], [0, 6, 2, 2, 5]]
a1 = solution(len(a), len(a[0]), a2)


def get_points(landmark, shape):
    points = []
    for mark in landmark:
        points.append([mark.x * shape[1], mark.y * shape[0]])
    return np.array(points, dtype=np.int32)


def get_point(landmark, shape, i):
    return landmark[i].x * shape[1], landmark[i].y * shape[0]


def size(landmark, shape, i, j):
    x1, y1 = landmark[i].x * shape[1], landmark[i].y * shape[0]
    x2, y2 = landmark[j].x * shape[1], landmark[j].y * shape[0]
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def check_circle(xp, yp, xc, yc, r, flippedRGB):
    new_r = math.hypot(abs(xp - xc), abs(yp - yc))
    cv2.circle(flippedRGB, (int(xc), int(yc)), int(r), (0, 0, 255), 2)
    if new_r > r * 1.3:
        return 2  # вне окружности
    elif r * 1.3 >= new_r >= 0.7 * r:
        return 1  # на окружности
    else:
        return 0  # в окружности


def check_paper(i, results, flippedRGB):
    points = get_points(results.multi_hand_landmarks[i].landmark, flippedRGB.shape)
    (x, y), r = cv2.minEnclosingCircle(points)
    a = [4, 8, 12, 16, 20]
    for j in a:
        x1, y1 = get_point(results.multi_hand_landmarks[i].landmark, flippedRGB.shape, j)
        ws = size(results.multi_hand_landmarks[i].landmark, flippedRGB.shape, 0, 5)
        if check_circle(x1, y1, x, y, r, flippedRGB) != 1 or r * 2 / ws < 1.8:
            return 0
    return 1


def get_object(res, objs):
    on_index = None
    xk, yk = None, None
    for i in range(len(res.multi_handedness)):
        if "Left" in str(res.multi_handedness[i]):
            xk = int(res.multi_hand_landmarks[i].landmark[8].x * config.WIDTH)
            yk = int(res.multi_hand_landmarks[i].landmark[8].y * config.HEIGHT)
            for x in range(len(objs)):
                for y in range(len(objs[x])):
                    elem = objs[x][y]
                    if elem != 0:
                        if elem.x <= xk < elem.x + elem.width and elem.y <= yk < elem.y + elem.height:
                            on_index = [x, y]
    return on_index, xk, yk


def draw_cur(now: list[list]):
    clock = pygame.time.Clock()
    running = 1
    while running:
        screen.fill((102, 100, 105))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0
        for i in range(len(now)):
            for j in range(len(now[i])):
                if now[i][j] != 0:
                    screen.blit(pic[now[i][j]], (j * 100 + 50, i * 100 + 50))

        pygame.display.flip()
        clock.tick(5)


def you_win(screen):
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.Font('M_PLUS_Rounded_1c/MPLUSRounded1c-ExtraBold.ttf', 45)
    txt = ["   Well done! you managed to pass this", "level. Show a like to start the next one."]
    txt_surfaces = []
    for i in txt:
        txt_surfaces.append(font.render(i, True, '#060E26'))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill('#A1A6B5')
        for i in range(len(txt_surfaces)):
            screen.blit(txt_surfaces[i], (100, i * 60 + 50))
        pygame.display.flip()
        clock.tick(120)
    pygame.quit()


def left_and_right(hands):
    rl, ri, li = False, None, None
    for i in range(len(hands)):
        if "Right" in str(hands[i]):
            ri = i
        else:
            li = i
    if ri is not None and li is not None:
        rl = True
    return rl, ri, li


def give_up(results, flippedRGB):
    if results.multi_hand_landmarks is not None and len(results.multi_hand_landmarks) >= 2:
        r_and_l, r_index, l_index = left_and_right(results.multi_handedness)
        if r_and_l:
            if check_paper(r_index, results, flippedRGB) == 1 and check_paper(l_index, results, flippedRGB) == 1:
                return True
    return False


def instruction(screen):
    clock = pygame.time.Clock()
    font = pygame.font.Font('M_PLUS_Rounded_1c/MPLUSRounded1c-ExtraBold.ttf', 45)
    step1 = 1
    txt = [" Your main task in the game will", "be to assemble the water supply", "  system so that it can be used"]
    txt_surfaces = []
    for i in txt:
        txt_surfaces.append(font.render(i, True, '#060E26'))
    while step1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                step1 = 0
        screen.fill('#A1A6B5')
        for i in range(len(txt_surfaces)):
            screen.blit(txt_surfaces[i], (200, i * 60 + 50))
        pygame.draw.rect(screen, '#D4FAB9', ((275, 275), (250, 250)))
        pygame.draw.rect(screen, '#FCCCCC', ((575, 275), (250, 250)))
        pygame.draw.rect(screen, '#060E26', ((275, 275), (250, 250)), 3)
        pygame.draw.rect(screen, '#060E26', ((575, 275), (250, 250)), 3)

        screen.blit(pic[5], (300, 300))
        screen.blit(pic[6], (400, 300))
        screen.blit(pic[4], (300, 400))
        screen.blit(pic[3], (400, 400))

        screen.blit(pic[3], (600, 300))
        screen.blit(pic[5], (700, 300))
        screen.blit(pic[4], (600, 400))
        screen.blit(pic[6], (700, 400))

        # if рука показывает лайк, то step1 = 0

        pygame.display.flip()
        clock.tick(120)

    step2 = 1
    handsDetector = mp.solutions.hands.Hands()
    cap = cv2.VideoCapture(0)
    txt = ["    Place your left index finger on", "   the pipe to control its position.",
           "The wrench will follow your finger."]
    txt_surfaces = []
    objects = [[picture(pic[1], 300, 300, WIDTH, HEIGHT)]]
    for i in txt:
        txt_surfaces.append(font.render(i, True, '#060E26'))
    while step2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                step2 = 0
        screen.fill('#A1A6B5')
        for i in range(len(txt_surfaces)):
            screen.blit(txt_surfaces[i], (150, i * 60 + 50))

        results, fRGB = get_hands(cap, handsDetector)
        if results.multi_handedness:
            object_index, x, y = get_object(results, objects)
            if x and y:
                screen.blit(big_key, (x, y))

        # if рука показывает лайк, то step2 = 0
        pygame.display.flip()
        clock.tick(120)

    step3 = 1
    txt = ["    You can use the finger of your other", "  hand to control the position of the pipe.",
           "Just rotate the pipe with your index finger."]
    txt1_surface = font.render("try here", True, '#060E26')
    txt_surfaces = []
    for i in txt:
        txt_surfaces.append(font.render(i, True, '#060E26'))
    objects = [[picture(pipe_t3, 300, 300, 100, 100, 3)]]

    while step3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                step3 = 0
        screen.fill('#A1A6B5')
        pygame.draw.rect(screen, '#D4FAB9', (275, 275, 150, 150))
        pygame.draw.rect(screen, '#060E26', (275, 275, 150, 150), 3)

        drawing(screen, objects, "test")

        results, fRGB = get_hands(cap, handsDetector)
        if results.multi_handedness:
            object_index, x, y = get_object(results, objects)
            if x and y:
                screen.blit(key1.image, (x, y))

            for i in range(len(results.multi_handedness)):
                if "Right" in str(results.multi_handedness[i]):
                    x1 = int(results.multi_hand_landmarks[i].landmark[8].x * WIDTH)
                    y1 = int(results.multi_hand_landmarks[i].landmark[8].y * HEIGHT)
                    x2 = int(results.multi_hand_landmarks[i].landmark[0].x * WIDTH)
                    y2 = int(results.multi_hand_landmarks[i].landmark[0].y * HEIGHT)
                    x, y = x1 - x2, y1 - y2
                    angle = math.atan2(y, x)
                    if abs(x1 - x2) + abs(y1 - y2) > 150:
                        if object_index is not None:
                            r_angle = (math.degrees(angle) + 45) // 90 * 90
                            if r_angle < 0:
                                r_angle += 360
                            change_rotation(r_angle, objects, object_index)

        for i in range(len(txt_surfaces)):
            screen.blit(txt_surfaces[i], (50, i * 60 + 50))
        screen.blit(txt1_surface, (250, 450))

        # if рука показывает лайк, то step3 = 0

        pygame.display.flip()
        clock.tick(120)

    step4 = 1
    txt = ["     If you realize that you cannot complete", "a level, then after 10 seconds show 2 palms",
           "  and you will be shown the correct solution.",
           "If you're ready to start playing, give us a like!"]
    txt_surfaces = []
    for i in txt:
        txt_surfaces.append(font.render(i, True, '#060E26'))
    objects = [[picture(pipe_t3, 300, 300, 100, 100, 3)]]
    while step4:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                step4 = 0
        screen.fill('#A1A6B5')
        for i in range(len(txt_surfaces)):
            screen.blit(txt_surfaces[i], (50, i * 60 + 50))

        # if рука показывает лайк, то step4 = 0

        pygame.display.flip()
        clock.tick(120)


def show_ans(now: list[list], ans: list[list],
             now_time):  # ресует процесс получения из данного состояния правильные трубы
    i, j = 0, 0
    clock = pygame.time.Clock()
    running = 1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0

        screen.fill((102, 100, 105))
        while i < len(now) and j < len(now[0]) and ans[i][j] == 0:
            j += 1
            if j >= len(now[0]):
                j = 0
                i += 1
        if i < len(now) and j < len(now[0]):
            if now[i][j].pipe_type == ans[i][j]:
                pygame.draw.rect(screen, (182, 250, 175), (now[i][j].x, now[i][j].y, now[i][j].width, now[i][j].height))
                j += 1
                if j >= len(now[0]):
                    j = 0
                    i += 1
            elif now[i][j] != 0 and now[i][j].pipe_type != ans[i][j]:
                if now[i][j].pipe_type == 1 or now[i][j].pipe_type == 2:
                    now[i][j].pipe_type = now[i][j].pipe_type % 2 + 1
                else:
                    now[i][j].pipe_type += 1
                    if now[i][j].pipe_type > 6:
                        now[i][j].pipe_type = 3
                now[i][j].image = pic[now[i][j].pipe_type]
        drawing(screen, now, now_time)
        pygame.display.flip()
        clock.tick(2)
