from config import *
from detection import *
from pics import *
import mediapipe as mp
from rotation import *
import time
from check import *
import math

def level(screen, ind):
    a = read_level(ind)
    a_copy = a.copy()
    a_ans = solution(len(a_copy), len(a_copy[0]), a_copy)
    handsDetector = mp.solutions.hands.Hands()
    cap = cv2.VideoCapture(0)
    clock = pygame.time.Clock()
    running = 1
    objects = f(a)
    showing_ans = False
    win = 0
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
            showing_ans = True
            running = False

        if check_solution(objects, a_ans) and finish == -1:
            finish = time.time()
        elif not check_solution(objects, a_ans) and finish != -1:
            finish = -1
        elif check_solution(objects, a_ans) and time.time() - finish > 3:
            win = True
            running = False

        pygame.display.flip()
        clock.tick(120)
    if win:
        you_win(screen, ind)
        if time.time() - finish > 10 and finish != -1:
            return None
    elif showing_ans:
        show_ans(screen, objects, a_ans, now_time)
        end_of_showing = time.time()
        if time.time() - end_of_showing > 10:
            return None


def you_win(screen, ind):
    handsDetector = mp.solutions.hands.Hands()
    cap = cv2.VideoCapture(0)
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.Font('fonts/MPLUSRounded1c-ExtraBold.ttf', 45)
    txt = ["   Well done! you managed to pass this", "level. Show a like to start the next one."]
    txt_surfaces = []
    for i in txt:
        txt_surfaces.append(font.render(i, True, '#060E26'))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        results, _ = get_hands(cap, handsDetector)
        screen.fill('#A1A6B5')
        for i in range(len(txt_surfaces)):
            screen.blit(txt_surfaces[i], (100, i * 60 + 50))
        pygame.display.flip()
        clock.tick(120)
        if is_like(results):
            level(screen, ind + 1)
    return


def instruction(screen):
    handsDetector = mp.solutions.hands.Hands()
    cap = cv2.VideoCapture(0)
    clock = pygame.time.Clock()
    font = pygame.font.Font('fonts/MPLUSRounded1c-ExtraBold.ttf', 45)
    step1 = 1
    txt = [" Your main task in the game will", "be to assemble the water supply", "  system so that it can be used"]
    txt_surfaces = []
    for i in txt:
        txt_surfaces.append(font.render(i, True, '#060E26'))
    start = time.time()
    while step1:
        results, _ = get_hands(cap, handsDetector)
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

        if is_like(results) and time.time() - start > 3:
            step1 = 0

        pygame.display.flip()
        clock.tick(120)

    step2 = 1
    txt = ["    Place your left index finger on", "   the pipe to control its position.",
           "The wrench will follow your finger."]
    txt_surfaces = []
    objects = [[picture(pic[1], 300, 300, WIDTH, HEIGHT)]]
    for i in txt:
        txt_surfaces.append(font.render(i, True, '#060E26'))
    start = time.time()
    while step2:
        results, _ = get_hands(cap, handsDetector)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                step2 = 0
        screen.fill('#A1A6B5')
        for i in range(len(txt_surfaces)):
            screen.blit(txt_surfaces[i], (150, i * 60 + 50))

        if results.multi_handedness:
            object_index, x, y = get_object(results, objects)
            if x and y:
                screen.blit(big_key, (x, y))

        if is_like(results) and time.time() - start > 3:
            step2 = 0
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
    start = time.time()
    while step3:
        results, _ = get_hands(cap, handsDetector)
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

        if is_like(results) and time.time() - start > 3:
            step3 = 0

        pygame.display.flip()
        clock.tick(120)

    step4 = 1
    txt = ["     If you realize that you cannot complete", "a level, then after 10 seconds show like",
           "  and you will be shown the correct solution.",
           "If you're ready to start playing, give us a like!"]
    txt_surfaces = []
    for i in txt:
        txt_surfaces.append(font.render(i, True, '#060E26'))
    objects = [[picture(pipe_t3, 300, 300, 100, 100, 3)]]
    start = time.time()
    while step4:
        results, _ = get_hands(cap, handsDetector)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                step4 = 0
        screen.fill('#A1A6B5')
        for i in range(len(txt_surfaces)):
            screen.blit(txt_surfaces[i], (50, i * 60 + 50))

        if is_like(results) and time.time() - start > 3:
            step4 = 0

        pygame.display.flip()
        clock.tick(120)


def show_ans(screen, now: list[list], ans: list[list],
             now_time):  # ресует процесс получения из данного состояния правильные трубы
    i, j = 0, 0
    clock = pygame.time.Clock()
    running = 1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0

        screen.fill('#A1A6B5')
        while i < len(now) and j < len(now[0]) and ans[i][j] == 0:
            j += 1
            if j >= len(now[0]):
                j = 0
                i += 1
        if i < len(now) and j < len(now[0]):
            if now[i][j].pipe_type == ans[i][j]:
                pygame.draw.rect(screen, '#D4FAB9', (now[i][j].x, now[i][j].y, now[i][j].width, now[i][j].height))
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


def drawing(screen, objects, now_time):
    for o in objects:
        for obj in o:
            if obj != 0:
                screen.blit(obj.image, (obj.x, obj.y))
    if now_time != "test":
        font = pygame.font.SysFont(None, 40)
        i = now_time.index(".")
        s1 = str(int(now_time[:i]) % 100 % 60)
        s2 = str(int(now_time[:i]) % 100 // 60)
        if len(s1) < 2:
            s1 = "0" + s1
        if len(s2) < 2:
            s2 = "0" + s2
        txt_surface = font.render(f"{s2}:{s1}:{now_time[(i+1):]}", True, (0, 0, 0))
        screen.blit(txt_surface, (950, 50))
