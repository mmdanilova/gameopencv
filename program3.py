from program1 import *
from pics import *  # import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
a = [[0, 3, 1, 2, 4], [0, 2, 0, 0, 1], [0, 1, 0, 0, 1], [0, 6, 2, 2, 5]]
a2 = [[0, 3, 1, 2, 4], [0, 2, 0, 0, 1], [0, 1, 0, 0, 1], [0, 6, 2, 2, 5]]
a1 = solution(len(a), len(a[0]), a2)

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
