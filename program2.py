import pygame
import cv2
import numpy as np
import sys

# Инициализация PyGame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("OpenCV + PyGame Camera")

# Открываем камеру через OpenCV
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Не удалось открыть камеру!")
    sys.exit()

# Параметры квадрата
square_size = 100
square_x = WIDTH // 2 - square_size // 2
square_y = HEIGHT // 2 - square_size // 2
square_color = (0, 0, 255)  # Синий
square_thickness = 3

# Шрифт
font = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False

    # Читаем кадр из OpenCV
    ret, frame = cap.read()
    if ret:
        # Конвертируем BGR (OpenCV) в RGB (PyGame)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Масштабируем под размер окна
        frame_resized = cv2.resize(frame_rgb, (WIDTH, HEIGHT))

        # Поворачиваем на 90 градусов ТОЛЬКО если камера установлена вертикально
        # Если у вас нормальная горизонтальная камера - уберите эту строку!
        # frame_resized = np.rot90(frame_resized)

        # Транспонируем массив для корректного отображения в PyGame
        # (swaps width and height dimensions for pygame.surfarray)
        frame_transposed = np.transpose(frame_resized, (1, 0, 2))

        # Конвертируем в поверхность PyGame
        frame_surface = pygame.surfarray.make_surface(frame_transposed)
        screen.blit(frame_surface, (0, 0))
    else:
        screen.fill((0, 0, 0))

    # Рисуем квадрат
    pygame.draw.rect(screen, square_color,
                     (square_x, square_y, square_size, square_size),
                     square_thickness)

    # Текст
    text = font.render("OpenCV + PyGame", True, (255, 255, 0))
    screen.blit(text, (10, 10))

    # Обновляем экран
    pygame.display.flip()
    clock.tick(60)

# Очистка
cap.release()
pygame.quit()
sys.exit()
