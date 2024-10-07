"""
빵을 구하고자 하는 m명의 사람

 1번 사람은 정확히 1분에,...,
  m번 사람은 정확히 m 분에 각자의 베이스캠프에서 출발하여 편의점으로 이동

사람들이 목표로 하는 편의점은 모두 다릅니다.

1.
격자에 있는 사람들 모두가 본인이 가고 싶은 편의점 방향을 향해서 1 칸 움직입니다.
최단거리 : 상하좌우 인접한 칸 중 이동가능한 칸으로만 이동하여
        도달하기까지 거쳐야 하는 칸의 수가 최소가 되는 거리

2.
편의점에 도착한다면 해당 편의점에서 멈추게 되고
다른 사람들은 해당 편의점이 있는 칸을 지나갈 수 없게 됩니다
격자에 있는 사람들이 모두 이동한 뒤에 해당 칸을 지나갈 수 없어짐

3.
시간이 t분이고 t ≤ m를 만족
t번 사람은 자신이 가고 싶은 편의점과 가장 가까이 있는 베이스 캠프에 들어갑니다.
우선순위 : 행이 작은 베이스캠프, 행이 같다면 열이 작은 베이스 캠프로
이때부터 다른 사람들은 해당 베이스 캠프가 있는 칸을 지나갈 수 없게 됩니다.


"""
from collections import deque


def calculate_dist(r, c, sr, sc):
    return abs(r - sr) + abs(c - sc)


def get_move_loc(i, j, gi, gj):
    q = deque([(i, j, 0, -1, -1)])
    visited = [[0] * N for _ in range(N)]
    visited[i][j] = 1

    while q:
        cr, cc, rank, fr, fc = q.popleft()
        if cr == gi and cc == gj:
            return fr, fc
        for di, dj in DIR:
            du, dv = cr + di, cc + dj
            if oob(du, dv): continue
            if arr[du][dv] < 0: continue
            if visited[du][dv]: continue
            visited[du][dv] = 1
            if rank == 0:
                q.append((du, dv, rank + 1, du, dv))
            else:
                q.append((du, dv, rank + 1, fr, fc))


def oob(i, j):
    return i < 0 or j < 0 or i >= N or j >= N


# 인덱스 1부터 시작!!
N, M = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
# move_arr =[[[] for _ in range(N)] for _ in range(N)]
store_lst = [-1]
moving_lst = []
arrived_cnt = 0
DIR = (-1, 0), (0, -1), (0, 1), (1, 0)
time = 0
for m in range(M):
    x, y = map(lambda x: int(x) - 1, input().split())
    store_lst.append((x, y))


def find_base(sr, sc):
    q = deque([(sr, sc, 0)])
    visited = [[0] * N for _ in range(N)]
    visited[sr][sc] = 1
    rr, rc = N, N
    mn_dist = N*N

    while q:
        cr, cc, rank = q.popleft()
        if arr[cr][cc] == 1:
            if rank< mn_dist:
                rr, rc = cr, cc
                mn_dist = rank
            elif rank == mn_dist and (rr, rc) > (cr, cc):
                rr, rc = cr, cc
            continue
        for di, dj in DIR:
            du, dv = cr + di, cc + dj
            if oob(du, dv): continue
            if visited[du][dv]: continue
            q.append((du, dv, rank+1))
            visited[du][dv] = 1

    return rr, rc


while arrived_cnt < M:
    time += 1
    # 이동
    # print("=================움직이기 전 =====================")
    # print(moving_lst)
    for m in range(len(moving_lst)):
        if moving_lst[m] == -1:
            continue

        num, r, c = moving_lst[m]
        sr, sc = store_lst[num]
        # print(f"움직일 애 : {num} = ({r}, {c})")
        nr, nc = get_move_loc(r, c, sr, sc)
        # print(f"목적지 : ({sr}, {sc})")

        if nr == sr and nc == sc:
            arrived_cnt+=1
            moving_lst[m] = -1
            arr[sr][sc] = -1

        else:
            moving_lst[m] = (num, nr, nc)
    # print("=================움직인 후 =====================")
    # print(moving_lst)
    # 새로운 애 투입
    if time <= M:
        sr, sc = store_lst[time]
        br, bc = find_base(sr, sc)
        arr[br][bc] = -1
        moving_lst.append((time, br, bc))
print(time)