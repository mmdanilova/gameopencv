import pics
import pygame

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
