from collections import deque


def oob(i, j):
    return i < 0 or j < 0 or i >= N or j >= N


def check_end():
    for r, c in office_lst:
        if cool_arr[r][c] <K:
            return False
    return True

def bfs(r, c, dk):
    air_arr[r][c] += 5
    q = deque([(r, c, 4)])
    lst = air_dir_dict[dk]
    visited = [[0] * N for _ in range(N)]
    while q:
        cr, cc, v = q.popleft()
        if v == 0: continue

        for cdi, cdj in lst:
            du = cr + cdi
            dv = cc + cdj
            if oob(du, dv): continue
            if visited[du][dv]:
                continue
            # 바람 갈 수 있는지 체크하기
            # 상하일 때
            if dk in (1, 3):
                if cdi and not cdj:
                    p = prime_dict[(cdi, cdj)]
                    if wall_arr[cr][cc] % p == 0:
                        continue
                else:
                    p1 = prime_dict[(0, cdj)]
                    p2 = prime_dict[(cdi, 0)]
                    if wall_arr[cr][cc] % p1 == 0:
                        continue
                    if wall_arr[cr][dv] % p2 == 0:
                        continue

            else:
                if cdj and not cdi:  # 좌우로만 보낼 때
                    p = prime_dict[(cdi, cdj)]
                    if wall_arr[cr][cc] % p == 0:
                        continue
                else:
                    p1 = prime_dict[(cdi, 0)]
                    p2 = prime_dict[(0, cdj)]
                    if wall_arr[cr][cc] % p1 == 0:
                        continue
                    if wall_arr[du][cc] % p2 == 0:
                        continue

            air_arr[du][dv] += v
            q.append((du, dv, v - 1))
            visited[du][dv] = 1

def printa(string, arr):
    print(f"================{string} ====================")
    for i in range(N):
        print(arr[i])
    print("===============================================")
    print()

N, M, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
air_arr = [[0] * N for _ in range(N)]
wall_arr = [[1] * N for _ in range(N)]
cool_arr = [[0]*N for _ in range(N)]
DIR = (0, -1), (-1, 0), (0, 1), (1, 0)
prime_dict = {(0, -1): 2, (-1, 0): 3, (0, 1): 5, (1, 0): 7}
air_dir_dict = {0: [(-1, -1), (0, -1), (1, -1)], 1: [(-1, -1), (-1, 0), (-1, 1)],
                2: [(-1, 1), (0, 1), (1, 1)], 3: [(1, -1), (1, 0), (1, 1)]}


for m in range(M):
    x, y, s = map(int, input().split())
    x -= 1
    y -= 1
    if s==0:
        wall_arr[x-1][y] *= 7
        wall_arr[x][y]*=3
    else:
        wall_arr[x][y-1]*=5
        wall_arr[x][y]*=2

office_lst = []
for i in range(N):
    for j in range(N):
        if arr[i][j] == 0: continue
        if arr[i][j] == 1:
            office_lst.append((i, j))
            continue
        d = arr[i][j] - 2
        di, dj = DIR[d]
        ni, nj = i + di, j + dj
        if oob(ni, nj): continue
        bfs(ni, nj, d)

# printa("default air : ", air_arr)
time = 0
while 1:
    if time>100:
        break

    if check_end():
        break

    time+=1

    for i in range(N):
        for j in range(N):
            cool_arr[i][j]+=air_arr[i][j]

    tmp = [[0]*N for _ in range(N)]
    #공기 섞이기
    for i in range(N):
        for j in range(N):
            for di, dj in (0, 1), (1, 0):
                du, dv = i+di, j+dj
                if oob(du, dv): continue
                p = prime_dict[(di, dj)]
                if wall_arr[i][j]%p ==0: continue
                gap = abs(cool_arr[i][j]-cool_arr[du][dv])
                if cool_arr[i][j]>cool_arr[du][dv]:
                    tmp[i][j] -= gap//4
                    tmp[du][dv] += gap//4
                else:
                    tmp[i][j] += gap//4
                    tmp[du][dv] -= gap//4
    # printa("바람 불고 나서", cool_arr)
    # printa("순환 양 보자 ", tmp)
    for i in range(N):
        for j in range(N):
            cool_arr[i][j] += tmp[i][j]
    # printa("공기순환 ", cool_arr)
    for i in range(1, N):
        cool_arr[0][i] = max(cool_arr[0][i]-1, 0)
        cool_arr[i][N-1] = max(cool_arr[i][N-1]-1, 0)
        cool_arr[N-1][i-1] = max(cool_arr[N-1][i-1]-1, 0)
        cool_arr[i-1][0] = max(cool_arr[i-1][0]-1, 0)
    # printa("외벽 감소", cool_arr)
    #
    # print("=================================")

print(time if time<=100 else -1)