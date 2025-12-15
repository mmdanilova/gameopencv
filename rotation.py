import cv2, mediapipe as mp, numpy as np, pygame, math, time

def get_object(res, objs):
    on_index = None
    xk, yk = None, None
    for i in range(len(res.multi_handedness)):
        if "Left" in str(res.multi_handedness[i]):
            xk = int(res.multi_hand_landmarks[i].landmark[8].x * WIDTH)
            yk = int(res.multi_hand_landmarks[i].landmark[8].y * HEIGHT)
            for j in range(len(objs)):
                elem = objs[j]
                if elem.x <= xk < elem.x + elem.width and elem.y <= yk < elem.y + elem.height:
                    on_index = j
    return on_index, xk, yk

def get_hands():
    ret, frame = cap.read()
    flipped = np.fliplr(frame)
    flippedRGB = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
    results = handsDetector.process(flippedRGB)
    return results

def drawing(screen, object):
    screen.fill((0, 0, 0))
    for obj in object:
        imag = pygame.transform.rotate(obj.image, obj.angle)
        screen.blit(imag, (obj.x, obj.y))



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

objects = [imag]

while running:
    results = get_hands()
    drawing(screen, objects)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    object_index = None
    if results.multi_handedness:
        object_index, x, y = get_object(results, objects)
        if x and y:
            pygame.draw.circle(screen, (255, 0, 0), (x, y), 10)

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
                if object_index is not None:
                    objects[object_index].angle = -(math.degrees(angle) + 45) // 90 * 90

    pygame.display.flip()
    clock.tick(120)

handsDetector.close()
pygame.quit()