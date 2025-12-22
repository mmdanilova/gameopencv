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

def is_like(results):
    if not results.multi_hand_landmarks:
        return False

    for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
        hand_label = handedness.classification[0].label
        landmarks = hand_landmarks.landmark

        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        thumb_mcp = landmarks[2]
        index_mcp = landmarks[5]
        index_tip = landmarks[8]

        thumb_tip_x = thumb_tip.x
        thumb_tip_y = thumb_tip.y
        index_mcp_x = index_mcp.x
        index_mcp_y = index_mcp.y

        y_diff = index_mcp_y - thumb_tip_y
        if y_diff < 0.05:
            continue

        if not (thumb_tip_y < thumb_ip.y < thumb_mcp.y):
            continue

        if index_mcp.y > index_tip.y:
            continue

        if hand_label == "Right":
            if thumb_tip_x < index_mcp_x and abs(index_tip.x - index_mcp.x) < 0.075:
                return True
        else:
            if thumb_tip_x > index_mcp_x and abs(index_mcp.x - index_tip.x) < 0.075:
                return True

    return False


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

