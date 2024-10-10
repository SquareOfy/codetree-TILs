"""
도망자의 종류
    좌우로만 움직이는 유형  오른쪽을 보고 시작
    상하로만 움직이는 유형 아래쪽을 보고 시작
    도망자는 중앙에서 시작하지는 않습니다.

h개의 나무  도망자와 초기에 겹쳐져 주어지는 것 가능


도망자가 1턴 그리고 이어서 술래가 1턴 진행하는 것을 총 k번 반복

    1. 도망자 움직임
        현재 술래와의 거리가 3 이하인 도망자만 움직입니다.
        두 사람간의 거리는 |x1 - x2| + |y1 - y2|로 정의

        현재 바라보고 있는 방향으로 1칸 움직인다 했을 때 격자를 벗어나는 경우
             방향을 반대로 틀어줍니다.
             바라보고 있는 방향으로 1칸 움직인다 했을 때
             해당 위치에 술래가 없다면 1칸 앞으로 이동
             있으면 스테이

        현재 바라보고 있는 방향으로 1칸 움직인다 했을 때 격자를 벗어나지 않는 경우
            움직이려는 칸에 술래가 있는 경우라면 움직이지 않습니다.
            움직이려는 칸에 술래가 있지 않다면 해당 칸으로 이동합니다.
            나무가 있어도 괜찮습니다.
    2. 술래 움직임
        달팽이 모양으로 움직입니다. ( 상 우 하 좌 )
         끝에 도달하게 되면 다시 거꾸로 중심으로 이동
        중심에 오게 되면 처음처럼 위 방향으로 시작하여 시계뱡향으로 도는 것을 k턴에 걸쳐 반복
         위치가 만약 이동방향이 틀어지는 지점이라면, 방향을 바로 틀어줍니다.

        2-2 도망자 잡기
             술래의 시야는 현재 바라보고 있는 방향을 기준으로 현재 칸을 포함하여 총 3칸입니다
             나무가 놓여 있는 칸이라면, 해당 칸에 있는 도망자는 나무에 가려져 보이지 않게 됩니다.
              t x 현재 턴에서 잡힌 도망자의 수만큼의 점수
"""

def change(i):
    return int(i)-1


def oob(i, j):
    return i<0 or j<0 or i>=N or j>=N

def cal_dist(i, j, x, y):
    return abs(i-x) + abs(j-y)

def set_route_dir():
    global back_Route_lst, back_Dir_lst
    r, c = N//2, N//2
    go_Route_lst.append((r,c))
    l = 1
    cnt =0
    while 1:
        for dk in range(4):
            di, dj = DIR[dk]
            go_Dir_lst[-1]= dk
            for lk in range(l):
                r+=di
                c+=dj
                go_Dir_lst.append(dk)
                back_Dir_lst.append((dk+2)%4)
                go_Route_lst.append((r,c))
                if r==0 and c==0:
                    go_Dir_lst[-1]=2
                    back_Dir_lst = back_Dir_lst[::-1]
                    back_Dir_lst[-1] = 0
                    back_Route_lst = go_Route_lst[::-1]
                    return
            cnt +=1
            if cnt==2:
                cnt=0
                l+=1



N, M, H, K = map(int, input().split())

runner_info = [-1]
runner_arr = [[[] for _ in range(N)] for _ in range(N)]
tree_arr = [[0]*N for _ in range(N)]
DIR = (-1, 0), (0, 1), (1, 0), (0, -1)

go_Route_lst = []
back_Route_lst = []

go_Dir_lst = [0]
back_Dir_lst = [2]

for m in range(M):
    x, y, d = map(change, input().split())
    d = 1 if d==0 else 2
    runner_info.append((x, y, d))
    runner_arr[x][y].append(m)

set_route_dir()
s_idx = 0
go_flag = 1
answer = 0
for h in range(H):
    x, y = map(change, input().split())
    tree_arr[x][y] = 1

for k in range(1, K+1):

    sr, sc = go_Route_lst[s_idx] if go_flag else back_Route_lst[s_idx]
    for m in range(1, M+1):
        if runner_info[m]==-1:
            continue
        Rx, Ry, Rd = runner_info[m]
        dist = cal_dist(sr, sc, Rx, Ry)
        if dist>3: continue

        Rdi, Rdj = DIR[Rd]
        nRx, nRy = Rx+Rdi, Ry+Rdj
        if oob(nRx, nRy):
            Rd = (Rd+2)%4
            nRx -= Rdi*2
            nRy -= Rdj*2
        if sr == nRx and sc == nRy:
            runner_info[m] = (Rx, Ry, Rd)
        else:
            runner_info[m] = (nRx, nRy, Rd)

    runner_arr =[[[] for _ in range(N)] for _ in range(N)]
    for m in range(1, M+1):
        if runner_info[m] == -1:
            continue
        x, y, d = runner_info[m]
        runner_arr[x][y].append(m)

    s_idx +=1
    if s_idx == N*N -1:
        go_flag = not go_flag
        s_idx = 0

    sr, sc = go_Route_lst[s_idx] if go_flag else back_Route_lst[s_idx]
    sd = go_Dir_lst[s_idx] if go_flag else back_Dir_lst[s_idx]
    sdi, sdj = DIR[sd]
    for t in range(3):
        nSr, nSc = sr+sdi*t, sc+sdj*t
        if oob(nSr, nSc): break
        if tree_arr[nSr][nSc]: continue
        answer += k*len(runner_arr[nSr][nSc])
        for m in runner_arr[nSr][nSc]:
            runner_info[m] = -1
print(answer)