#  L×L 크기 왼쪽 상단은 (1,1)
# 0 빈칸  || 1  함정  ||  2 벽
# 기사 :  (r,c)를 좌측 상단으로 하며 h(높이)×w(너비) 크기의 직사각형 형태 / 기사의 체력은 k
L, N, Q = map(int, input().split())

# 필요한 배열 세팅(입력배열)
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
    # print("====================== is_possible 호출 ======================")
    # print("num ", num)
    # print("di, dj : ", di, dj)

    r, c, h, w = gisa_info[num]
    if di:

        du = r + h if di > 0 else r - 1
        #바로 다음이 벽이다? 못 가.
        if du < 0 or du >= L:
            return False
        line_visited = [0] * w

            # if du < 0 or du >= L:
            #     break
        for j in range(c, c+w):
            if line_visited[j-c]:
                continue
            if arr[du][j] == 2:
                return False
            if gisa[du][j] != 0 and gisa[du][j]!=num:
                if not is_possible_push(gisa[du][j], di, dj):
                    return False
                if gisa[du][j] not in push_lst:
                    push_lst.append(gisa[du][j])
            elif arr[du][j] == 0 and gisa[du][j] == 0:
                line_visited[j-c] = 1

        return True
    else:

        dv = c + w if dj > 0 else c - 1
        if dv < 0 or dv >= L:
            return False
        line_visited = [0] * h

        # if dv<0 or dv>=L:
        #     print("여기도 아니고")

        for j in range(r, r+h):
            # print("여기 들어옴?", j, dv, r, h)
            # print(line_visited)
            # print(arr[j][dv])
            if line_visited[j-r]:
                # print("continue 당함")
                continue
            if arr[j][dv] == 2:
                # print("벽만나서 못가는데")
                return False
            if gisa[j][dv] != 0 and gisa[j][dv] !=num:
                # print("다음 함수 호출")
                if not is_possible_push(gisa[j][dv], di, dj):
                    # print("여기서 안되고")
                    return False
                if gisa[j][dv] not in push_lst:
                    push_lst.append(gisa[j][dv])
            elif arr[j][dv] == 0 and gisa[j][dv] == 0:
                line_visited[j-r] = 1


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
    for i in range(r, r+h):
        for j in range(c, c+h):
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
    if hp[num]<=0:
        kill(num)
    else:
        damage_lst[num] += tmp
for q in range(Q):

    q_i, d = map(int, input().split())

    if hp[q_i] <= 0: continue  # 죽었으면 넘어가

    # (1) 기사 이동
    # 체스판에서 사라진 기사에게 명령을 내리면 아무런 반응이 없게 됩니다.
    # 기사는 상하좌우 중 하나로 한 칸 이동
    # 기사가 이동하려는 방향의 끝에 벽이 있다면 모든 기사는 이동할 수 없게 됩니다.
    # 만약 이동하려는 위치에 다른 기사가 있다면 그 기사도 함께 연쇄적으로 한 칸 밀려나
    # 그 옆에 또 기사가 있다면 연쇄적으로 한 칸씩 밀림
    # print(f'===================={q}=====================')
    # print(q_i, d)
    r, c, h, w = gisa_info[q_i]
    di, dj = DIR[d]
    push_lst = []
    is_possible = is_possible_push(q_i, di, dj)
    # 밀 수 없다
    # print("밀 수 있다=========밀기 전")
    # for k in range(L):
    #     print(gisa[k])
    # print()

    if not is_possible:
        # print("밀 수 없다@@@@@@@@@@@@@@@@@@@@@@@@@")
        continue

    # print("밀 수 있다=========밀기 전")
    # for k in range(L):
    #     print(gisa[k])
    # print()

    for k in range(len(push_lst) - 1, -1, -1):
        num = push_lst[k]
        push(num, di, dj)

    push(q_i, di, dj)
    # print("================밀고 난 후 ===============")
    # for k in range(L):
    #     print(gisa[k])
    # print()
    # (2) 대결 대미지
    # 밀려난 기사들은 피해
    # 이동한 곳에서 w×h 직사각형 내에 놓여 있는 함정의 수만큼만 피해
    # 기사마다 피해를 받은 만큼 체력이 깎이게 되며,
    # 현재 체력 이상의 대미지를 받을 경우 기사는 체스판에서 사라짐
    # 명령을 받은 기사는 피해를 입지 않으며, 기사들은 모두 밀린 이후에 대미지를 입게 됩니다.
    for num in push_lst:
        get_damage(num)
        # print("밀린게 있다 !! ")

    # print("hp ")
    # print(hp)
    # print("===damage")
    # print(damage_lst)
# 출력
# Q 번의 대결이 모두 끝난 후 생존한 기사들이 총 받은 대미지의 합
print(sum(damage_lst))