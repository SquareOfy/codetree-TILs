"""
n * n 크기의 격자에서 진행
술래는 처음 정중앙

술래잡기 게임에는 m명의 도망자 도망자는 중앙에서 시작하지는 않습니다.
좌우로만 움직이는 유형 항상 오른쪽을 보고 시작
상하로만 움직이는 유형 항상 아래쪽을 보고 시작

술래잡기 게임에는 h개의 나무
도망자와 초기에 겹쳐져 주어지는 것 역시 가능

도망자가 1턴 그리고 이어서 술래가 1턴 진행하는 것을 총 k번 반복

    도망자 이동
        현재 술래와의 거리가 3 이하인 도망자만 움직입니다.
        두 사람간의 거리는 |x1 - x2| + |y1 - y2|로 정의

        격자를 벗어나지 않는 경우
            움직이려는 칸에 술래가 있는 경우라면 움직이지 않습니다.
            움직이려는 칸에 술래가 있지 않다면 해당 칸으로 이동
            나무가 있어도 괜찮습니다.
        격자를 벗어나는 경우
            방향을 반대로 틀어줍니다.
            이후 바라보고 있는 방향으로 1칸 움직인다 했을 때
            해당 위치에 술래가 없다면 1칸 앞으로 이동


    술래 이동
        처음 위 방향으로 시작하여 달팽이 모양으로 움직입니다.
         끝에 도달하게 되면 다시 거꾸로 중심으로 이동
         중심에 오게 되면 처음처럼 위 방향으로 시작
         치가 만약 이동방향이 틀어지는 지점이라면, 방향을 바로 틀어줍니다.
    술래는 턴을 넘기기 전에 시야 내에 있는 도망자를 잡게 됩니다
    술래의 시야는 현재 바라보고 있는 방향을 기준으로
      현재 칸을 포함하여 총 3칸
    만약 나무가 놓여 있는 칸이라면,
    해당 칸에 있는 도망자는 나무에 가려져 보이지 않게 됩니다.

    잡힌 도망자는 사라지게 되고, 술래는 현재 턴을 t번째 턴이라고 했을 때
     t x 현재 턴에서 잡힌 도망자의 수만큼의 점수를 얻게 됩니다
"""


def change(i):
    return int(i) - 1


def get_sul_loc():
    if go_flag:
        sr, sc = go_route_lst[s_idx]
        sd = go_dir_lst[s_idx]
    else:
        sr, sc = back_route_lst[s_idx]
        sd = back_route_lst[s_idx]
    return sr, sc, sd


def set_route_lst():
    global back_route_lst, back_dir_lst
    r, c = N // 2, N // 2
    go_route_lst.append((r, c))
    back_route_lst.append((r, c))
    go_dir_lst.append(0)
    back_dir_lst.append(0)
    l = 1
    cnt = 0
    while 1:
        for i in range(4):
            di, dj = DIR[i]
            go_dir_lst[-1] = i
            back_dir_lst[-1] = (i + 2) % 4
            for k in range(l):
                r += di
                c += dj
                go_route_lst.append((r, c))

                go_dir_lst.append(i)
                # back_dir_lst.append((i+2)%4)

                if r == 0 and c == 0:
                    go_dir_lst[0] = 0
                    go_dir_lst[-1] = 2
                    back_route_lst = go_route_lst[::-1]
                    return
            cnt += 1
            if cnt == 2:
                l += 1
                cnt = 0


def calculate_d(x, y, r, c):
    return abs(x - r) + abs(y - c)


def oob(i, j):
    return i >= N or j >= N or i < 0 or j < 0

def printa(string, arr):
    print(f"================{string}===================")
    for z in range(N):
        print(arr[z])
    print("============================================")
    print()

N, M, H, K = map(int, input().split())
runner_lst = [-1]
runner_arr = [[[] for _ in range(N)] for _ in range(N)]
tree_arr = [[0] * N for _ in range(N)]
DIR = (-1, 0), (0, 1), (1, 0), (0, -1)

for m in range(1, M + 1):
    x, y, d = map(change, input().split())
    d = 1 if d == 0 else 2  # 좌우로 움직이면(d==0) 오른쪽보기 아니면 아래쪽
    runner_arr[x][y].append(m)
    runner_lst.append((x, y, d))

for h in range(H):
    x, y = map(change, input().split())
    tree_arr[x][y] = 1

go_flag = True
go_route_lst = []
back_route_lst = []
go_dir_lst = []
back_dir_lst = []

set_route_lst()
back_dir_lst = [(i + 2) % 4 for i in go_dir_lst[N * N - 2::-1]] + [0]

# print(go_route_lst)
# print(go_dir_lst)
# print(len(go_dir_lst))
#
# print()
# print(back_route_lst)
# print(back_dir_lst)
s_idx = 0
answer = 0
for k in range(1, K+1):

    sr, sc, sd = get_sul_loc()
    # 도망자 이동시키기
    for m in range(1, M + 1):
        if runner_lst[m] == -1: continue
        x, y, d = runner_lst[m]
        dist = calculate_d(x, y, sr, sc)

        if dist > 3:
            continue

        di, dj = DIR[d]
        du, dv = x + di, y + dj
        if oob(du, dv):
            d = (d + 2) % 4
            du -= di * 2
            dv -= dj * 2
        if du == sr and dv == sc:
            runner_lst[m] = (x, y, d)
        else:
            runner_lst[m] = (du, dv, d)

    runner_arr = [[[] for _ in range(N)] for _ in range(N)]
    for m in range(1, M+1):
        if runner_lst[m] == -1:
            continue
        x, y, d = runner_lst[m]
        runner_arr[x][y].append(m)
    # printa("도망자 이동 후", runner_arr)
    # print(runner_lst)
    # print()

    s_idx += 1
    s_idx %= N * N
    sr, sc, sd = get_sul_loc()
    sdi, sdj = DIR[sd]

    if s_idx==N*N-1:
        go_flag = not go_flag
    # print("술래 현 위치 ", sr, sc, sdi, sdj)
    for t in range(3):
        sight_r, sight_c = sr + sdi * t, sc + sdj * t
        if oob(sight_r, sight_c):
            break
        if tree_arr[sight_r][sight_c]:
            continue
        # print("잡은 애들 : ", runner_arr[sight_r][sight_c])
        if runner_arr[sight_r][sight_c]:
            answer += k*len(runner_arr[sight_r][sight_c])
            for runner in runner_arr[sight_r][sight_c]:
                runner_lst[runner] = -1

print(answer)