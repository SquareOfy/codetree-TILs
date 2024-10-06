"""

n * n 크기의 격자 술래는 처음 정중앙

m명의 도망자.
    도망자는 중앙에서 시작하지는 않습니다.
    도망자의 종류는 1. 좌우로만 움직이는 유형과 2. 상하로만 움직이는 유형
    좌우로 움직이는 사람은 항상 오른쪽을 보고 시작하며, 상하로 움직이는 사람은 항상 아래쪽을 보고 시작
도망자가 1턴 그리고 이어서 술래가 1턴 진행하는 것을 총 k번 반복
    도망자가 움직일 때 현재 술래와의 거리가 3 이하인 도망자만 움직입니다
    두 사람간의 거리는 |x1 - x2| + |y1 - y2|로 정의

    현재 바라보고 있는 방향으로 1칸 움직인다 했을 때 격자를 벗어나지 않는 경우
        움직이려는 칸에 술래가 있는 경우라면 움직이지 않습니다.
        움직이려는 칸에 술래가 있지 않다면 해당 칸으로 이동합니다. 해당 칸에 나무가 있어도 괜찮습니다.

    현재 바라보고 있는 방향으로 1칸 움직인다 했을 때 격자를 벗어나는 경우
        먼저 방향을 반대로 틀어서 방향으로 1칸 이동 ( 술래 없다면)
        있으면 안움직임

    술래 움직임
    처음 위 방향으로 시작하여 달팽이 모양으로 움직입니다.
     끝에 도달하게 되면 다시 거꾸로 중심으로 이동
     다시 중심에 오게 되면 처음처럼 위 방향으로 시작하여 시계뱡향으로 도는 것을 k턴에 걸쳐 반복
    1번의 턴 동안 정확히 한 칸 해당하는 방향으로 이동
    이동 후의 위치가 만약 이동방향이 틀어지는 지점이라면, 방향을 바로 틀어줍니다.
    (끝점, 시작점에서도 !! )

    턴을 넘기기 전에 시야 내에 있는 도망자를 잡게 됩니다
    술래의 시야는 항상
    나무가 놓여 있는 칸이라면, 해당 칸에 있는 도망자는 나무에 가려져 보이지 않게 됩니다.
    점수 += t번째 턴에 잡힌 도망자수 * t

"""


# 달팽이 모양 go 배열 만들고 back은 뒤집기
# go_dir, back_dir도 세팅하는 함수
def set_route_lst():
    r, c = N // 2, N // 2
    go_route_lst.append((r, c))
    l = 1
    cnt = 0
    # idx = 1
    while 1:
        for i in range(4):
            di, dj = DIR[i]
            for k in range(l):
                r += di
                c += dj
                go_route_lst.append((r, c))
                if r == 0 and c == 0:
                    go_dir_lst.append((i + 2) % 4)
                    return
                go_dir_lst.append(i)
            cnt += 1
            if cnt == 2:
                l += 1
                cnt = 0


def oob(i, j):
    return i < 0 or j < 0 or i >= N or j >= N


# 거리 계산 함수
def get_dist(i, j, x, y):
    return abs(i - x) + abs(j - y)


def change_idx(i):
    return int(i) - 1


def get_sul_info():
    if go_flag:
        sr, sc = go_route_lst[s_idx]
        sd = go_dir_lst[s_idx]
    else:
        sr, sc = back_route_lst[s_idx]
        sd = back_route_lst[s_idx]

    return sr, sc, sd

def printa(string ,arr):
    print(f"============={string} ==============")
    for i in range(N):
        print(arr[i])
    print("=====================================")
    print()

def printl(string, lst):
    print(f"============={string} ==============")

    print(lst)
    print("=====================================")
    print()


# 입력
N, M, H, K = map(int, input().split())
DIR = (-1, 0), (0, 1), (1, 0), (0, -1)

# 필요한 배열 준비 (도망자 정보 받기)
tree_arr = [[0] * N for _ in range(N)]
runner_lst = [-1]
runner_arr = [[[] for _ in range(N)] for _ in range(N)]

go_route_lst = []
back_route_lst = []
go_dir_lst = []
back_dir_lst = []

set_route_lst()
back_route_lst = go_route_lst[::-1]
back_dir_lst = [(i + 2) % 4 for i in go_dir_lst[::-1]]
back_dir_lst[0] = 2
back_dir_lst[-1] = 0

s_idx = 0
go_flag = True
answer = 0

for m in range(1, M + 1):
    x, y, d = map(change_idx, input().split())
    d = 2 if d == 1 else 1  # 인덱스 1씩 마이너스. -> 0일 때 오른쪽 / 1일 때 아래쪽 보고 시작
    runner_lst.append((x, y, d))
    runner_arr[x][y] = m

for h in range(H):
    x, y = map(change_idx, input().split())
    tree_arr[x][y] = 1

# k번의 턴
for k in range(1, K+1):

    sr, sc, sd = get_sul_info()

    # 도망자 이동
    for m in range(1, M+1):
        if runner_lst[m] == -1:
            continue
        x, y, d = runner_lst[m]

        dist = get_dist(x, y, sr, sc)
        if dist>3: continue

        # 술래 이동
        di, dj = DIR[d]
        nr, nc = x+di, y+dj
        if oob(nr, nc):
            d =(d+2)%4
            di, dj = DIR[d]
            nr += 2*di
            nc += 2*dj

        if nr==sr and nc == sc:
            runner_lst[m] = (x, y, d)
            continue
        runner_lst[m] = (nr, nc, d)
    #움직임 마쳤으면 배열에 반영
    runner_arr = [[[] for _ in range(N)] for _ in range(N)]
    for m in range(1, M+1):
        if runner_lst[m] == -1:
            continue
        x, y, d = runner_lst[m]
        runner_arr[x][y].append(m)

    # printa("도망자 이동 후 ", runner_arr)
    # print(runner_lst)

    #술래 움직이기
    s_idx+=1
    s_idx%=N
    sr, sc, sd = get_sul_info()

    sdi, sdj = DIR[sd]
    # print('===========================')
    # print(f'술래 위치, 방향 : ', sr, sc, f"({sdi}, {sdj})" )
    # print("=============================")
    #도망자 잡기
    for i in range(3):
        sight_r, sight_c = sr+sdi*i, sc+sdj*i
        if oob(sight_r, sight_c):
            continue
        if tree_arr[sight_r][sight_c]:
            continue
        answer +=  len(runner_arr[sight_r][sight_c])*k
        # print("잡힌 애들 : ", runner_arr[sight_r][sight_c])
        for runner in runner_arr[sight_r][sight_c]:
            runner_lst[runner] = -1
        runner_arr[sight_r][sight_c] = []
    # 술래 route 관리
    if s_idx==N*N-1:
        go_flag = False if go_flag else True
print(answer)