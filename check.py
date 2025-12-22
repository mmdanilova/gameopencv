import pics

# решение задачи о том как расставить трубы правильно и возможно ли это
# 0 - нет трубы
# 1 - прямая труба вправо
# 2 - прямая труба в лево
# 3 - труба верх лево
# 4 - трубаверх право
# 5 - трубавниз вправо
# 6 - трубавниз влево

def solution(n: int, m: int, a1: list[list]):
    a2 = a1.copy()
    for i in range(n):
        for j in range(m):
            ans = -1
            if a2[i][j] == 0:
                ans = 0
            elif a2[i][j] == 1 or a2[i][j] == 2:
                up = 0
                left = 0
                if i > 0:
                    if a2[i - 1][j] == 3 or a2[i - 1][j] == 4 or a2[i - 1][j] == 0 or a2[i - 1][j] == 1:
                        left += 1
                    else:
                        up += 1
                else:
                    left += 1
                if j-1 >= 0:
                    if a2[i][j - 1] == 1 or a2[i][j - 1] == 4 or a2[i][j - 1] == 5:
                        left += 1
                    else:
                        up += 1
                else:
                    up += 1
                if left > 0 and up > 0:
                    return 0

                elif left > 0:
                    ans = 1
                else:
                    ans = 2
            else:
                up = 0
                down = 0
                left = 0
                right = 0
                if i > 0:
                    if a2[i - 1][j] == 1 or a2[i - 1][j] == 3 or a2[i - 1][j] == 4 or a2[i - 1][j] == 0:
                        down += 1
                    else:
                        up += 1
                else:
                    down += 1

                if j-1 >= 0:
                    if a2[i][j - 1] == 2 or a2[i][j - 1] == 3 or a2[i][j - 1] == 6 or a2[i][j - 1] == 0:
                        right += 1
                    else:
                        left += 1
                else:
                    right += 1

                if left > 0 and right > 0:
                    return 0

                elif up > 0 and down > 0:
                    return 0

                elif ((down > 0 and i == n-1) or (up > 0 and i == 0) or (left > 0 and j == 0)
                      or (right > 0 and j == m-1)):
                    return 0
                elif up > 0 and right > 0:
                    ans = 4
                elif up > 0 and left > 0:
                    ans = 3
                elif down > 0 and right > 0:
                    ans = 5
                elif down > 0 and left > 0:
                    ans = 6
            a2[i][j] = ans
    return a2


def check_solution(now, ans):
    for i in range(len(now)):
        for j in range(len(now[i])):
            if now[i][j] != 0:
                if now[i][j].pipe_type != ans[i][j] and ans[i][j] != 0:
                    return False
    return True


def read_level(ind):
    with open('levels.txt', 'r', encoding='utf-8') as f:
        line = f.readlines()[ind]
        a1 = line.split()
        a = [[] for i in range(5)]
        for i in range(5):
            for j in range(10):
                a[i].append(int(a1[j+i*10]))
    return a

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
