"""

체스판의 왼쪽 상단은 (1,1)로 시작
d는 0, 1, 2, 3 중에 하나이며 각각 위쪽, 오른쪽, 아래쪽, 왼쪽 방향을 의미

각 기사의 초기위치는 (r,c)
(r,c)를 좌측 상단으로 하며 h(높이)×w(너비) 크기의 직사각형 형태
각 기사의 체력은 k

(1) 기사 이동
    상하좌우 중 하나로 한 칸 이동할 수 있습니다

    이때 만약 이동하려는 위치에 다른 기사가 있다면
    그 기사도 함께 연쇄적으로 한 칸 밀려나게 됩니다.
    => 재귀 함수 호출

    만약 기사가 이동하려는 방향의 끝에 벽이 있다면
    모든 기사는 이동할 수 없게 됩니다
    => return False

    체스판에서 사라진 기사에게 명령을 내리면 아무런 반응이 없게 됩니다.

(2) 대결 대미지
    밀려난 기사들은 피해를 입게 됩니다.
    이때 각 기사들은 해당 기사가 이동한 곳에서
    w×h 직사각형 내에 놓여 있는 함정의 수만큼만 피해를 입게 됩니다.

    각 기사마다 피해를 받은 만큼 체력이 깎이게 되며,
    현재 체력 이상의 대미지를 받을 경우 기사는 체스판에서 사라지게 됩니다.
    명령을 받은 기사는 피해를 입지 않으며,
    기사들은 모두 밀린 이후에 대미지를 입게 됩니다.

Q 개의 명령이 진행된 이후, 생존한 기사들이 총 받은 대미지의 합
"""


# 기사 밀 수 있는지 체크하는 함수
def is_possible_push(num, d):
    r, c, h, w = gisa_lst[num]

    di, dj = DIR[d]
    if di:
        du = r + h if di > 0 else r - 1
        for dv in range(c, c + w):
            if oob(du, dv):
                return False
            if info_arr[du][dv] == 2:
                return False
            if gisa_arr[du][dv] != 0:
                if gisa_arr[du][dv] not in push_lst:
                    push_lst.append(gisa_arr[du][dv])
                if not is_possible_push(gisa_arr[du][dv], d):
                    return False
    elif dj:
        dv = c + w if dj > 0 else c - 1
        for du in range(r, r + h):
            if oob(du, dv): return False
            if info_arr[du][dv] == 2: return False
            if gisa_arr[du][dv] != 0:
                if gisa_arr[du][dv] not in push_lst:
                    push_lst.append(gisa_arr[du][dv])
                if not is_possible_push(gisa_arr[du][dv], d):
                    return False
    return True

# oob
def oob(i, j):
    return i < 0 or j < 0 or i >= L or j >= L


# 기사 옮기는 함수
def move_gisa(num, d):
    r, c, h, w = gisa_lst[num]
    di, dj = DIR[d]
    if di:
        remove_r = r if di > 0 else r + h - 1
        append_r = r + h if di > 0 else r - 1

        for dv in range(c, c + w):
            if gisa_arr[remove_r][dv] == num:
                gisa_arr[remove_r][dv] = 0
            gisa_arr[append_r][dv] = num
    elif dj:
        remove_c = c if dj > 0 else c + w - 1
        append_c = c + w if dj > 0 else c - 1
        # print(append_c)
        for du in range(r, r + h):
            if gisa_arr[du][remove_c] == num:
                gisa_arr[du][remove_c] = 0
            gisa_arr[du][append_c] = num
    gisa_lst[num] = (r + di, c + dj, h, w)

# damage 처리 함수
def get_damage(num):
    r, c, h, w = gisa_lst[num]
    for i in range(r, r + h):
        for j in range(c, c + w):
            if info_arr[i][j] == 1:
                damage_lst[num] += 1
                power_lst[num] -= 1
                if power_lst[num] == 0:
                    die_gisa(num)
                    return
def die_gisa(num):
    r, c, h, w = gisa_lst[num]
    for i in range(r, r + h):
        for j in range(c, c + w):
            gisa_arr[i][j] = 0

    gisa_lst[num] = -1
    damage_lst[num] = 0

def printa(string, arr):
    print(f"============={string}================")
    for t in range(len(arr)):
        print(arr[t])
    print("=======================================")
    print()

# 입력 및 배열 준비
DIR = (-1, 0), (0, 1), (1, 0), (0, -1)

L, N, Q = map(int, input().split())
info_arr = [list(map(int, input().split())) for _ in range(L)]
gisa_arr = [[0] * L for _ in range(L)]
gisa_lst = [-1]
damage_lst = [0] * (N + 1)
power_lst = [0] * (N + 1)

for n in range(1, N + 1):
    r, c, h, w, k = map(int, input().split())
    r -= 1
    c -= 1
    gisa_lst.append((r, c, h, w))
    power_lst[n] = k

    for i in range(r, r + h):
        for j in range(c, c + w):
            gisa_arr[i][j] = n
# printa("초기 기사 상태", gisa_arr)
for q in range(Q):
    num, d = map(int, input().split())
    # print("==================", num, d, "===================")
    if gisa_lst[num] == -1: continue
    push_lst = []
    if not is_possible_push(num, d):
        continue

    # 기사들 이동
    for pn in push_lst:
        move_gisa(pn, d)
    move_gisa(num, d)  # 명령 받은 기사 이동
    # printa("기사 이동했음", gisa_arr)

    for pn in push_lst:
        get_damage(pn)

    # printa("데미지 먹인 후 ", gisa_arr)
    # print(power_lst)
    # print(damage_lst)
    # print(gisa_lst)


print(sum(damage_lst))