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
    return ((x1 - x2)**2 + (y1 - y2) **2) ** 0.5

def check_circle(xp, yp, xc, yc, r, flippedRGB):
    new_r = math.hypot(abs(xp-xc), abs(yp - yc))
    cv2.circle(flippedRGB, (int(xc), int(yc)), int(r), (0, 0, 255), 2)
    if new_r > r*1.3:
        return 2  # вне окружности
    elif r*1.3 >= new_r >= 0.7*r:
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
        if check_circle(x1, y1, x, y, r, flippedRGB) != 1 or r*2/ws < 1.8:
            return 0
    return 1

def get_object(res, objs):
    on_index = None
    xk, yk = None, None
    for i in range(len(res.multi_handedness)):
        if "Left" in str(res.multi_handedness[i]):
            xk = int(res.multi_hand_landmarks[i].landmark[8].x * config.WIDTH)
            yk = int(res.multi_hand_landmarks[i].landmark[8].y * config.HEIGHT)
            for j in range(len(objs)):
                elem = objs[j]
                if elem.x <= xk < elem.x + elem.width and elem.y <= yk < elem.y + elem.height:
                    on_index = j
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
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((102, 100, 105))
        screen.blit(txt1, (100, -50))
        pygame.display.flip()
        clock.tick(120)
    pygame.quit()

def instruction(screen):
    clock = pygame.time.Clock()
    handsDetector = mp.solutions.hands.Hands()
    cap = cv2.VideoCapture(0)
    running = True
    font = pygame.font.SysFont(None, 48)
    font1 = pygame.font.SysFont(None, 40)

    txt_surface1 = font.render("Your main task is to assemble the plumbing correctly.", True, (0, 0, 0))
    txt_surface2 = font.render("This is small instruction:", True, (0, 0, 0))
    txt_surface3 = font1.render("1. if you want to start the game", True, (0, 0, 0))
    txt_surface4 = font1.render("2. if you want to see the correct answer", True, (0, 0, 0))
    txt_surface5 = font1.render("3. To turn the pipe over, point", True, (0, 0, 0))
    txt_surface6 = font1.render("one finger with the key at the pipe", True, (0, 0, 0))
    txt_surface7 = font1.render("rotate the wrist of your other hand,", True, (0, 0, 0))
    txt_surface8 = font1.render("maintaining the gesture as in photo", True, (0, 0, 0))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        results, flippedRGB = get_hands(cap, handsDetector)
        screen.fill((102, 100, 105))
        screen.blit(txt_surface1, (100, 100))
        screen.blit(txt_surface2, (100, 150))
        screen.blit(txt_surface3, (50, 320))
        screen.blit(txt_surface4, (50, 350))
        screen.blit(txt_surface5, (600, 260))
        screen.blit(txt_surface6, (600, 290))
        screen.blit(txt_surface7, (600, 320))
        screen.blit(txt_surface8, (600, 350))
        screen.blit(hand1, (100, 375))
        screen.blit(hand2, (600, 400))
        screen.blit(key, (730, 400))
        screen.blit(hand3, (620, 300))

        if results.multi_hand_landmarks is not None:
            for i in range(len(results.multi_hand_landmarks)):
                if check_paper(0, results, flippedRGB) == 1:
                    return

        pygame.display.flip()
        clock.tick(120)
    pygame.quit()

def show_ans(now: list[list], ans: list[list]):  # ресует процесс получения из данного состояния правильные трубы
    ind = (0, 0)
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
        while ind[0] < len(now) and ind[1] < len(now[0]) and (now[ind[0]][ind[1]] == 0
                                                              or now[ind[0]][ind[1]] == ans[ind[0]][ind[1]]):
            if ind[0] < len(now) and ind[1] < len(now[0]):
                if now[ind[0]][ind[1]] == ans[ind[0]][ind[1]]:
                    if ind[1] + 1 < len(now[0]):
                        ind = (ind[0], ind[1] + 1)
                    else:
                        ind = (ind[0] + 1, 0)
            else:
                break
        if ind[0] < len(now) and ind[1] < len(now[0]):
            if now[ind[0]][ind[1]] == ans[ind[0]][ind[1]]:
                if ind[1] + 1 < len(now[0]):
                    ind = (ind[0], ind[1] + 1)
                else:
                    ind = (ind[0] + 1, 0)
            else:
                if now[ind[0]][ind[1]] == 1 or now[ind[0]][ind[1]] == 2:
                    now[ind[0]][ind[1]] = now[ind[0]][ind[1]] + 1
                    if now[ind[0]][ind[1]] > 2:
                        now[ind[0]][ind[1]] = 1
                elif now[ind[0]][ind[1]] > 2:
                    now[ind[0]][ind[1]] = now[ind[0]][ind[1]] + 1
                    if now[ind[0]][ind[1]] > 6:
                        now[ind[0]][ind[1]] = 3

        pygame.display.flip()
        clock.tick(5)
