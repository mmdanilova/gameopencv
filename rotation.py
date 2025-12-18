import cv2
import pics
import config
import numpy as np
import math

def drawing(screen, objects):
    screen.fill((102, 100, 105))
    for o in objects:
        for obj in o:
            if obj != 0:
                screen.blit(obj.image, (obj.x, obj.y))
def check_solution(now, ans):
    for i in range(len(now)):
        for j in range(len(now[i])):
            if now[i][j].pipe_type != ans[i][j] and ans[i][j] != 0:
                return False
    return True

def get_hands(cap, handsDetector):
    ret, frame = cap.read()
    flipped = np.fliplr(frame)
    flippedRGB = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
    results = handsDetector.process(flippedRGB)
    return results, flippedRGB

def f(array):
    objects = []
    for i in range(len(array)):
        line = []
        for j in range(len(array[i])):
            if array[i][j] == 1 or array[i][j] == 2:
                line.append(pics.picture(pics.pipe_t1, j * 100 + 50, i * 100 + 50, 100, 100, 1))
            elif array[i][j] == 0:
                line.append(0)
            else:
                line.append(pics.picture(pics.pipe_t3, j * 100 + 50, i * 100 + 50, 100, 100, 3))
        objects.append(line)
    return objects


def change_rotation(angle, objects, object_index):
    if objects[object_index[0]][object_index[1]].pipe_type == 1 or objects[object_index[0]][object_index[1]].pipe_type == 2:
        if abs(angle) == 0 or abs(angle) == 180:
            objects[object_index[0]][object_index[1]].pipe_type = 2
            objects[object_index[0]][object_index[1]].image = pics.pic[objects[object_index[0]][object_index[1]].pipe_type]
        else:
            objects[object_index[0]][object_index[1]].pipe_type = 1
            objects[object_index[0]][object_index[1]].image = pics.pic[objects[object_index[0]][object_index[1]].pipe_type]
    elif objects[object_index[0]][object_index[1]].pipe_type != 0:
        if abs(angle) == 0:
            objects[object_index[0]][object_index[1]].pipe_type = 5
            objects[object_index[0]][object_index[1]].image = pics.pic[
                objects[object_index[0]][object_index[1]].pipe_type]
        if abs(angle) == 90:
            objects[object_index[0]][object_index[1]].pipe_type = 6
            objects[object_index[0]][object_index[1]].image = pics.pic[
                objects[object_index[0]][object_index[1]].pipe_type]
        if abs(angle) == 180:
            objects[object_index[0]][object_index[1]].pipe_type = 3
            objects[object_index[0]][object_index[1]].image = pics.pic[
                objects[object_index[0]][object_index[1]].pipe_type]
        if abs(angle) == 270:
            objects[object_index[0]][object_index[1]].pipe_type = 4
            objects[object_index[0]][object_index[1]].image = pics.pic[
                objects[object_index[0]][object_index[1]].pipe_type]
