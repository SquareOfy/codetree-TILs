L, N, Q = map(int, input().split())


arr = [list(map(int, input().split())) for _ in range(L)]
gisa = [[0] * L for _ in range(L)]
gisa_info = [-1]
hp = [0] * (N + 1)
damage_lst = [0] * (N + 1)
DIR = (-1, 0), (0, 1), (1, 0), (0, -1)

for n in range(1, N + 1):
    r, c, h, w, k = map(int, input().split())
    r -= 1
    c -= 1
    for i in range(h):
        for j in range(w):
            gisa[r + i][c + j] = n
    gisa_info.append([r, c, h, w])
    hp[n] = k


def is_possible_push(num, di, dj):
    r, c, h, w = gisa_info[num]
    if di:
        du = r + h if di > 0 else r - 1
        if du < 0 or du >= L:
            return False

        for j in range(c, c + w):
            if arr[du][j] == 2:
                return False
            if gisa[du][j] != 0 and gisa[du][j] not in push_lst:
                if not is_possible_push(gisa[du][j], di, dj):
                    return False
                push_lst.append(gisa[du][j])
        return True
    else:
        dv = c + w if dj > 0 else c - 1
        if dv < 0 or dv >= L:
            return False
        for j in range(r, r + h):
            if arr[j][dv] == 2:
                return False
            if gisa[j][dv] and gisa[j][dv] not in push_lst:
                if not is_possible_push(gisa[j][dv], di, dj):
                    return False
                push_lst.append(gisa[j][dv])
        return True


def push(num, di, dj):
    r, c, h, w = gisa_info[num]
    gisa_info[num] = [r + di, c + dj, h, w]

    if di:
        delete_r = r if di > 0 else r + h - 1
        new_r = r + h if di > 0 else r - 1
        for j in range(c, c + w):
            gisa[delete_r][j] = 0
            gisa[new_r][j] = num
    else:
        delete_c = c if dj > 0 else c + w - 1
        new_c = c + w if dj > 0 else c - 1
        
        for j in range(r, r + h):
            gisa[j][delete_c] = 0
            gisa[j][new_c] = num


def kill(num):
    r, c, h, w = gisa_info[num]
    for i in range(r, r + h):
        for j in range(c, c + w):
            gisa[i][j] = 0
    damage_lst[num] = 0
    gisa_info[num] = -1


def get_damage(num):
    r, c, h, w = gisa_info[num]
    tmp = 0
    for i in range(r, r + h):
        for j in range(c, c + w):
            if arr[i][j] == 1:
                tmp += 1
    hp[num] -= tmp
    if hp[num] <= 0:
        kill(num)
    else:
        damage_lst[num] += tmp


for q in range(Q):

    q_i, d = map(int, input().split())

    if hp[q_i] <= 0: continue 

    r, c, h, w = gisa_info[q_i]
    di, dj = DIR[d]
    push_lst = []

    is_possible = is_possible_push(q_i, di, dj)


    if not is_possible:
        continue

    for k in range(len(push_lst)):
        num = push_lst[k]
        push(num, di, dj)

    push(q_i, di, dj)

    for num in push_lst:
        get_damage(num)

print(sum(damage_lst))