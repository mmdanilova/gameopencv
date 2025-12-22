import time
from events import *
from check import *
from pics import *


pygame.init()
pygame.display.set_caption("plumbing")
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
a = [[0, 0, 0, 3, 1, 1, 3, 0, 0, 0],
       [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
       [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
       [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
       [0, 0, 0, 3, 1, 1, 3, 0, 0, 0]]

a_copy = a.copy()

a_ans = solution(len(a_copy), len(a_copy[0]), a_copy)
handsDetector = mp.solutions.hands.Hands()
cap = cv2.VideoCapture(0)
clock = pygame.time.Clock()
running = 1
objects = f(a)
showing_ans = False
win = 0

#instruction(screen)

start = time.time()
finish = -1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill('#A1A6B5')
    now_time = str(round(time.time() - start, 2))
    results, fRGB = get_hands(cap, handsDetector)
    drawing(screen, objects, now_time)
    object_index = None
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
    if give_up(results) and time.time() - start > 10:
        running = False
        showing_ans = True

    if check_solution(objects, a_ans) and finish == -1:
        finish = time.time()
    elif not check_solution(objects, a_ans) and finish != -1:
        finish = -1
    elif check_solution(objects, a_ans) and time.time() - finish > 3:
        running = False
        win = True
    pygame.display.flip()
    clock.tick(120)

if win:
    you_win(screen)
if showing_ans:
    show_ans(screen, objects, a_ans, now_time)
handsDetector.close()
pygame.quit()
