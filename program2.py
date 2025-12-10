import pygame
import cv2
import numpy as np
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
cap = cv2.VideoCapture(0)
square_size = 100
square_x = 100
square_y = 100
square_color = (0, 0, 255)
square_thickness = 3
font = pygame.font.SysFont("Arial", 36)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ret, frame = cap.read()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (WIDTH, HEIGHT))
        frame_transposed = np.transpose(frame_resized, (1, 0, 2))
        frame_surface = pygame.surfarray.make_surface(frame_transposed)
        screen.blit(frame_surface, (0, 0))
    else:
        screen.fill((0, 0, 0))

    pygame.draw.rect(screen, square_color,
                     (square_x, square_y, square_size, square_size),
                     square_thickness)

    pygame.display.flip()
    clock.tick(60)

cap.release()
pygame.quit()
sys.exit()
