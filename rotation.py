import cv2, mediapipe as mp, numpy as np, pygame, math, time

class picture:
    def __init__(self, img, x, y, angle, width, height):
        self.image = img
        self.x = x
        self.y = y
        self.angle = angle
        self.width = width
        self.height = height

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
handsDetector = mp.solutions.hands.Hands()
cap = cv2.VideoCapture(0)
clock = pygame.time.Clock()
running = True
image = pygame.image.load('pipe.png')
x, y = image.get_size()
image = pygame.transform.scale(image, (x//2, y//2))
imag = picture(image, 100, 100, 0, x, y)
rotates = []
objects = [imag]
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    ret, frame = cap.read()
    flipped = np.fliplr(frame)
    if ret:
        frame_rgb = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (WIDTH, HEIGHT))
        frame_transposed = np.transpose(frame_resized, (1, 0, 2))
        frame_surface = pygame.surfarray.make_surface(frame_transposed)

    rotates = []
    for obj in objects:
        imag = pygame.transform.rotate(obj.image, obj.angle)
        screen.blit(imag, (obj.x, obj.y))

    flippedRGB = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
    results = handsDetector.process(flippedRGB)
    if results.multi_handedness:
        on_index = None
        for i in range(len(results.multi_handedness)):
            if "Left" in str(results.multi_handedness[i]):
                xk = int(results.multi_hand_landmarks[i].landmark[8].x * WIDTH)
                yk = int(results.multi_hand_landmarks[i].landmark[8].y * HEIGHT)
                pygame.draw.circle(screen, (255, 0, 0), (xk, yk), 10)
                for j in range(len(objects)):
                    elem = objects[j]
                    if elem.x <= xk < elem.x + elem.width and elem.y <= yk < elem.y + elem.height:
                        on_index = j

        if on_index is not None:
            for i in range(len(results.multi_handedness)):
                if "Right" in str(results.multi_handedness[i]):
                    x1 = int(results.multi_hand_landmarks[i].landmark[8].x * WIDTH)
                    y1 = int(results.multi_hand_landmarks[i].landmark[8].y * HEIGHT)
                    x2 = int(results.multi_hand_landmarks[i].landmark[0].x * WIDTH)
                    y2 = int(results.multi_hand_landmarks[i].landmark[0].y * HEIGHT)
                    pygame.draw.circle(screen, (255, 0, 0), (x1, y1), 5)
                    pygame.draw.circle(screen, (255, 0, 0), (x2, y2), 5)
                    x, y = x1-x2, y1-y2
                    angle = math.atan2(y, x)
                    objects[on_index].angle = math.degrees(angle)

    pygame.display.flip()
    clock.tick(5)

handsDetector.close()
pygame.quit()