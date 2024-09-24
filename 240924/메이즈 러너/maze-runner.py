from collections import deque
def control_idx(i):
    return int(i)-1

def oob(i, j):
    return i<0 or j<0 or i>=N or j>=N

# 미로는 N×N 크기의 격자  좌상단은 (1,1)
# 벽
    # 참가자가 이동할 수 없는 칸입니다.
    # 1이상 9이하의 내구도를 갖고 있습니다.
    # 회전할 때, 내구도가 1씩 깎입니다.
    # 내구도가 0이 되면, 빈 칸으로 변경됩니다.
N, M, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
people = [list(map(control_idx, input().split())) for _ in range(M)]
er, ec = map(control_idx, input().split())
cnt = M
answer = 0

# K초 동안 위의 과정을 계속 반복됩니다.
def bfs(r, c):
    q = deque([(r, c, 0, -1, -1)])
    visited=  [[0]*N for _ in range(N)]
    visited[r][c] = 1
    while q:
        cr, cc, rank, one_r, one_c = q.popleft()
        if cr==er and cc==ec:
            # print("도착하긴 하는데 ")
            if arr[one_r][one_c]==0:
                return one_r, one_c
            continue
        for di, dj in (-1, 0), (1, 0), (0, -1), (0, 1):
            du = cr+di
            dv = cc+dj
            if oob(du, dv) or visited[du][dv]:
                continue

            visited[du][dv] = rank+1

            if rank==0:
                q.append((du, dv, rank+1, du, dv))
            else:
                q.append((du, dv, rank+1, one_r, one_c))

    return -1, -1


def dist_bfs():
    q = deque([(er, ec, 0)])
    min_dist = 2*N
    visited = [[0]*N for _ in range(N)]
    visited[er][ec] = 1
    result_r, result_c = -1, -1
    while q:
        cr, cc, rank = q.popleft()
        if [cr, cc] in people:
            if rank < min_dist:
                result_r, result_c = cr, cc
                min_dist = rank
            elif rank == min_dist:
                #현재 행이 작거나, 행이 같을 때 열이 더작으면 갱신
                if result_r > cr or (result_r == cr and cc < result_r):
                    result_r, result_c = cr, cc
            continue
        for di, dj in (-1, 0), (0, -1), (1, 0), (0, 1):
            du = cr+di
            dv = cc+dj
            if oob(du, dv) or visited[du][dv]:
                continue
            q.append((du, dv, rank+1))
            visited[du][dv] =1

    return result_r, result_c, min_dist+1


def rotate(r, c, dist):
    return c, dist-1-r


for k in range(1, K+1):
    # print(f"====================={k}===================")

    # 1. 움직임
    # 1초마다 모든 참가자는 한 칸씩 움직임
    # 모든 참가자는 동시에 움직입니다.
    # 상하좌우로 움직일 수 있으며, 벽이 없는 곳으로 이동할 수 있습니다.
    # 움직인 칸은 현재 머물러 있던 칸보다 출구까지의 최단 거리가 가까워야 합니다.
    # 움직일 수 있는 칸이 2개 이상이라면, 상하로 움직이는 것을 우선시합니다.
    # 참가가가 움직일 수 없는 상황이라면, 움직이지 않습니다.
    # 한 칸에 2명 이상의 참가자가 있을 수 있습니다.
    for i in range(M):
        r, c = people[i]
        if r==-1: continue
        nr, nc = bfs(r, c)
        if nr == -1:
            continue
        answer+=1
        if nr == er and nc == ec:
            cnt-=1
            people[i] = [-1, -1]
        else:
            people[i] = [nr, nc]

    # print("===========이동===========")
    # print(people)
    # print(answer)
    # print("남은 사람 수 : ", cnt)
    # print("========================")

    # 만약 K초 전에 모든 참가자가 탈출에 성공한다면, 게임이 끝납니다.
    #움직이고 나서 사람 수 체크 후 break
    if cnt == 0:
        break

    # 2. 미로회전
        # 한 명 이상의 참가자와 출구를 포함한 가장 작은 정사각형
        # 가장 작은 크기를 갖는 정사각형이 2개 이상이라면,
        # 좌상단 r 좌표가 작은 것이 우선되고, 그래도 같으면 c 좌표가 작은 것이 우선됩니다.
        # 선택된 정사각형은 시계방향으로 90도 회전하며, 회전된 벽은 내구도가 1씩 깎입니다.
    pr, pc, dist = dist_bfs()
    # print(pr, pc, dist)
    if pr==er:
        sr = max(er-dist+1, 0)
    else:
        sr = min(pr, er)

    if pc==ec:
        sc = max(ec-dist+1, 0)
    else:
        sc = min(pc, ec)

    if sr+dist >=N:
        sr = N-dist
    if sc+dist >=N:
        sc = N-dist

    # print("============회전 범위 =================")
    # print(sr, sc, dist)
    # print("===================================")
    # print()
    # print("==================회전 전 =============")
    # for i in range(N):
    #     print(arr[i])
    # print("========================================")
    # print()

    #정사각형 회전
    # print(k)
    # print(sr, sc, dist)
    tmp = [[] for _ in range(dist)]
    for i in range(dist):
        # print(i)
        tmp[i] = arr[sr+i][sc:sc+dist]
        # print(tmp[i])
    for i in range(dist):
        for j in range(dist):
            if tmp[i][j]>0:
                tmp[i][j] -=1

    tmp = list(map(list, zip(*tmp[::-1])))
    for i in range(dist):
        arr[sr+i][sc:sc+dist] = tmp[i][:]

    # print("==================회전 후 =============")
    # for i in range(N):
    #     print(arr[i])
    # print("========================================")
    # print()
    # print('============회전 전 출구 =============')
    # print(er, ec)
    # print()

    er_tmp = er-sr
    ec_tmp = ec-sc
    er_tmp, ec_tmp = rotate(er_tmp, ec_tmp, dist)
    er, ec = er_tmp+sr, ec_tmp+sc
    #출구좌표 회전
    # print('============회전 후 출구 =============')
    # print(er, ec)
    # print('===================================')
    # print('============회전 전 사람 =============')
    # print(people)
    # print('===================================')
    # print()
    #저 안에 들어있는 사람 회전
    for i in range(M):
        r, c = people[i]
        if r==-1: continue
        if r in range(sr, sr+dist) and c in range(sc, sc+dist):
            tmp_r, tmp_c = rotate(r-sr, c-sc, dist)
            r, c = tmp_r+sr, tmp_c+sc
            people[i] = [r, c]
    # print('============회전 후 사람 =============')
    # print(people)
    # print('===================================')
    # print()

print(answer)
print(er+1, ec+1)