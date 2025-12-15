from program3 import *  # from program1 import *
import pics, mediapipe as mp, cv2, math, numpy as np

def get_object(res, objs):
    on_index = None
    xk, yk = None, None
    for i in range(len(res.multi_handedness)):
        if "Left" in str(res.multi_handedness[i]):
            xk = int(res.multi_hand_landmarks[i].landmark[8].x * WIDTH)
            yk = int(res.multi_hand_landmarks[i].landmark[8].y * HEIGHT)
            for j in range(len(objs)):
                elem = objs[j]
                if elem.x - 25 <= xk < elem.x + elem.width + 25 and elem.y - 25 <= yk < elem.y + elem.height + 25:
                    on_index = j
    return on_index, xk, yk

def get_hands():
    ret, frame = cap.read()
    flipped = np.fliplr(frame)
    flippedRGB = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
    results = handsDetector.process(flippedRGB)
    return results

class picture:
    def __init__(self, img, x, y, angle, width, height):
        self.image = img
        self.x = x
        self.y = y
        self.angle = angle
        self.width = width
        self.height = height

pygame.init()
WIDTH, HEIGHT = 1100, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
a = [[3, 1, 1, 1, 1, 1, 1, 1, 1, 3], [1, 3, 1, 1, 1, 1, 1, 1, 3, 1], [1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
     [1, 3, 1, 1, 1, 1, 1, 1, 3, 1], [3, 1, 1, 1, 1, 1, 1, 1, 1, 3]]

handsDetector = mp.solutions.hands.Hands()
cap = cv2.VideoCapture(0)

clock = pygame.time.Clock()
running = True

key = pygame.image.load("key.png")
key = pygame.transform.scale(key, (50, 50))
key = picture(key, 400, 200, 0, 50, 50)

objects = []
for i in range(len(a)):
    for j in range(len(a[i])):
        if a[i][j] == 1:
            image = pics.pipe_t1
            w, h = image.get_size()
            imag = picture(image, 100 * j + 35, 100 * i + 35, 0, w, h)
            objects.append(imag)
        else:
            image = pics.pipe_t3
            w, h = image.get_size()
            imag = picture(image, 100 * j + 35, 100 * i + 35, 0, w, h)
            objects.append(imag)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    results = get_hands()
    screen.fill((0, 0, 0))
    for obj in objects:
        imag = pygame.transform.rotate(obj.image, obj.angle)
        screen.blit(imag, (obj.x, obj.y))

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
