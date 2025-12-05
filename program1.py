# решение задачи о том как расставить трубы правильно и возможно ли это
# 0 - нет трубы
# 1 - прямая труба вправо
# 2 - прямая труба в лево
# 3 - труба верх лево
# 4 - трубаверх право
# 5 - трубавниз вправо
# 6 - трубавниз влево

n, m, g = map(int, input().split())
a = []

for i in range(n):
    a.append(list(map(int, input().split())))

for i in range(n):
    for j in range(m):
        ans = -1
        if a[i][j] == 0:
            ans = 0
        elif a[i][j] == 1 or a[i][j] == 2:
            up = 0
            left = 0
            if i > 0:
                if a[i-1][j] == 3 or a[i-1][j] == 4 or a[i-1][j] == 0 or a[i-1][j] == 1:
                    left += 1
                else:
                    up += 1
            else:
                left += 1
            if j-1 >= 0:
                if a[i][j-1] == 1 or a[i][j-1] == 4 or a[i][j-1] == 5:
                    left += 1
                else:
                    up += 1
            else:
                up += 1
            if left > 0 and up > 0:
                print("NO")
                exit(0)
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
                if a[i-1][j] == 1 or a[i-1][j] == 3 or a[i-1][j] == 4 or a[i-1][j] == 0:
                    down += 1
                else:
                    up += 1
            else:
                down += 1

            if j-1 >= 0:
                if a[i][j-1] == 2 or a[i][j-1] == 3 or a[i][j-1] == 6 or a[i][j-1] == 0:
                    right += 1
                else:
                    left += 1
            else:
                right += 1

            if left > 0 and right > 0:
                print("NO")
                exit(0)
            elif up > 0 and down > 0:
                print("NO")
                exit(0)
            elif (down > 0 and i == n-1) or (up > 0 and i == 0) or (left > 0 and j == 0) or (right > 0 and j == m-1):
                print("NO")
                exit(0)
            elif up > 0 and right > 0:
                ans = 4
            elif up > 0 and left > 0:
                ans = 3
            elif down > 0 and right > 0:
                ans = 5
            elif down > 0 and left > 0:
                ans = 6
        a[i][j] = ans
print("YES")
for i in a:
    print(*i)
