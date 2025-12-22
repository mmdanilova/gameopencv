import config
import cv2
import numpy as np
import math


def get_hands(cap, handsDetector):
    ret, frame = cap.read()
    flipped = np.fliplr(frame)
    flippedRGB = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
    results = handsDetector.process(flippedRGB)
    return results, flippedRGB


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

