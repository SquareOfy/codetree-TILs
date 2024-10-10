def oob(i, j):
    return i < 0 or j < 0 or i >= L or j >= L


def is_possible(g_num, dk):
    di, dj = DIR[dk]
    r, c, h, w = gisa_info[g_num]

    if di:
        check_r = r - 1 if di < 0 else r + h
        for j in range(c, c + w):
            if oob(check_r, j) or arr[check_r][j] == 2:
                return False
            if gisa_arr[check_r][j]:
                result = is_possible(gisa_arr[check_r][j], dk)
                if not result:
                    return False
                if gisa_arr[check_r][j] not in push_lst:
                    push_lst.append(gisa_arr[check_r][j])
    else:
        check_c = c - 1 if dj < 0 else c + w
        for i in range(r, r + h):
            if oob(i, check_c) or arr[i][check_c] == 2:
                return False

            if gisa_arr[i][check_c]:
                result = is_possible(gisa_arr[i][check_c], dk)
                if not result:
                    return False
                if gisa_arr[i][check_c] not in push_lst:
                    push_lst.append(gisa_arr[i][check_c])

    return True

def move_gisa(gNum, d):
    di, dj = DIR[d]
    r, c, h, w = gisa_info[gNum]
    if di:
        delete_r = r+h-1 if di<0 else r
        append_r = r-1 if di<0 else r+h
        for j in range(c, c+w):
            if gisa_arr[delete_r][j] == gNum:
                gisa_arr[delete_r][j] = 0
            gisa_arr[append_r][j] = gNum
    else:
        delete_c = c + w - 1 if dj < 0 else c
        append_c = c - 1 if dj < 0 else c + w
        for i in range(r, r+h):
            if gisa_arr[i][delete_c] == gNum:
                gisa_arr[i][delete_c] = 0
            gisa_arr[i][append_c] = gNum
    gisa_info[gNum] = (r+di, c+dj, h, w)

def get_damage(gNum):
    r, c, h, w = gisa_info[gNum]
    damage = 0
    for i in range(r, r+h):
        for j in range(c, c+w):
            if arr[i][j] == 1:
                damage += 1

    if gisa_power[gNum]-damage <=0:
        gisa_damage[gNum] = 0
        gisa_power[gNum] = 0
        for i in range(r, r+h):
            for j in range(c, c+w):
                gisa_arr[i][j] = 0

    else:
        gisa_damage[gNum] += damage
        gisa_power[gNum] -= damage



L, N, Q = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(L)]
gisa_arr = [[0] * L for _ in range(L)]
gisa_info = [-1]
gisa_power = [0] * (N + 1)
gisa_damage = [0] * (N + 1)

DIR = (-1, 0), (0, 1), (1, 0), (0, -1)
for n in range(1, N + 1):
    r, c, h, w, k = map(int, input().split())
    r -= 1
    c -= 1
    for i in range(r, r + h):
        for j in range(c, c + w):
            gisa_arr[i][j] = n
    gisa_info.append((r, c, h, w))
    gisa_power[n] = k



for q in range(Q):
    num, d = map(int, input().split())
    if gisa_power[num] <= 0: continue
    push_lst = []
    possible = is_possible(num, d)
    if not possible: continue
    for gNum in push_lst:
        move_gisa(gNum, d)
    move_gisa(num, d)
    # print(num, push_lst)
    for gNum in push_lst:
        get_damage(gNum)

    # for t in range(L):
    #     print(gisa_arr[t])
    # print()

print(sum(gisa_damage))