from collections import deque

# n*n 크기의 격자
# 0의 경우에는 빈 공간, 1의 경우에는 베이스캠프
# 각 사람마다 가고 싶은 편의점의 위치는 겹치지 않으며,
# 편의점의 위치와 베이스캠프의 위치도 겹치지 않습니다
N, M = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
goal_store = [(-1, -1)] * (M + 1)
DIR = (-1, 0), (0, -1), (0, 1), (1, 0)
for i in range(1, M + 1):
    x, y = map(lambda x: int(x) - 1, input().split())
    goal_store[i] = (x, y)

time = 0
cnt = 0
people = []
finished = [0] * (M + 1)


def oob(r, c):
    return r < 0 or c < 0 or r >= N or c >= N


def move_one(sr, sc, gr, gc):
    #  최단 거리로 움직이는 방법이 여러가지라면
    #  ↑, ←, →, ↓ 의 우선 순위로 움직이게 됩니다.
    # 상하좌우 인접한 칸 중 이동가능한 칸으로만 이동하여 도달하기까지
    # 거쳐야 하는 칸의 수가 최소가 되는 거리
    q = deque([(sr, sc, 0, None)])
    visited = [[0] * N for _ in range(N)]
    visited[sr][sc] = 1
    rr, rc = N, N
    while q:
        # print(q)
        cr, cc, rank, move = q.popleft()
        # print("find goal_step")
        # print(cr, cc, rank, move)
        if cr == gr and cc == gc:
            # print("===================!!!!=============")
            # print("편의점 도착 ", move)
            mr, mc = move
            if mr < rr:
                rr, rc = mr, mc
            elif mr == rr and mc < rc:
                rr, rc = mr, mc
            continue
        for di, dj in DIR:
            du = cr + di
            dv = cc + dj

            if oob(du, dv) or arr[du][dv] == -1 or visited[du][dv]:
                continue

            visited[du][dv] = 1
            if rank + 1 == 1:
                q.append((du, dv, rank + 1, (du, dv)))
            else:
                q.append((du, dv, rank + 1, move))
    # print("return rr, rc ", rr, rc)
    return rr, rc


def find_base(t):
    # t번째 사람이 들어갈 베이스캠프 구하기
    # 0의 경우에는 빈 공간, 1의 경우에는 베이스캠프를 의미
    # -1은 못감

    sr, sc = goal_store[t]
    visited = [[0] * N for _ in range(N)]
    q = deque([(sr, sc, 0)])
    visited[sr][sc] = 1

    min_rank = N * N + 1
    rr, rc = N, N

    while q:
        cr, cc, rank = q.popleft()
        if rank < min_rank and arr[cr][cc] == 1:
            min_rank = rank
            rr, rc = cr, cc
            continue
        if rank == min_rank and arr[cr][cc] == 1:
            # 지금 행이 더 작거나 행 같은데 왼쪽인 경우 갱신
            if cr < rr or (rr == cr and cc < rc):
                rr, rc = cr, cc
                continue
        for di, dj in DIR:
            du = cr + di
            dv = cc + dj

            if oob(du, dv) or arr[du][dv] == -1 or visited[du][dv]:
                continue
            visited[du][dv] = 1
            q.append((du, dv, rank + 1))
    return rr, rc


def printt():
    if debug:
        for i in range(N):
            print(arr[i])
        print()

debug= False
while 1:
    time += 1
    if cnt == M :
        printt()
        # print(people)
        # print(finished)
        break
    # m번 사람은 정확히 m 분에 각자의 베이스캠프에서 출발하여
    # 편의점으로 이동하기 시작합니다
    # 사람들은 출발 시간이 되기 전까지 격자 밖에 나와있으며,
    # 사람들이 목표로 하는 편의점은 모두 다릅니다

    arrived_lst = []

    # 이 3가지 행동은 총 1분 동안 진행되며, 정확히 1, 2, 3 순서로 진행되어야 함

    # 격자에 있는 사람들 모두가 본인이 가고 싶은 편의점 방향을 향해서 1 칸 움직입니다.
    # 이동하는 도중 동일한 칸에 둘 이상의 사람이 위치하게 되는 경우 역시 가능함에 유의합니다
    # print(people)
    # print(finished)
    for k in range(len(people)):
        num, cr, cc = people[k]
        # 이미 편의점 도착한 사람 continue
        if finished[num]:
            continue
        gr, gc = goal_store[num]
        nr, nc = move_one(cr, cc, gr, gc)
        people[k] = [num, nr, nc]
        # print(nr, rc)
        if nr == gr and nc == gc:
            arrived_lst.append((gr, gc))
            cnt += 1
            finished[num] = 1
    # 만약 편의점에 도착한다면 해당 편의점에서 멈추게 되고,
    # 이때부터 다른 사람들은 해당 편의점이 있는 칸을 지나갈 수 없게 됩니다.
    # 격자에 있는 사람들이 모두 이동한 뒤에 해당 칸을 지나갈 수 없어짐에 유의합니다.
    # 움직이지 못하게 막기
    for r, c in arrived_lst:
        arr[r][c] = -1

    # 현재 시간이 t분이고 t ≤ m를 만족한다면,
    # t번 사람은 자신이 가고 싶은 편의점과 가장 가까이 있는 베이스 캠프에 들어갑니다.
    # 여기서 가장 가까이에 있다는 뜻 역시 1에서와 같이 최단거리에 해당하는 곳을 의미합니다.
    # 가장 가까운 베이스캠프가 여러 가지인 경우에는 그 중 행이 작은 베이스캠프,
    # 행이 같다면 열이 작은 베이스 캠프로 들어갑니다.
    # t번 사람이 베이스 캠프로 이동하는 데에는 시간이 전혀 소요되지 않습니다.

    if time >= 1 and time <= M:
        br, bc = find_base(time)
        arr[br][bc] = -1
        people.append((time, br, bc))
    #  해당 턴 격자에 있는 사람들이 모두 이동한 뒤에 해당 칸을 지나갈 수 없어짐에 유의
    #  t번 사람이 편의점을 향해 움직이기 시작했더라도
    #  해당 베이스 캠프는 앞으로 절대 지나갈 수 없음에 유의합니다.


# 총 몇 분 후에 모두 편의점에 도착하는지

print(time-1)