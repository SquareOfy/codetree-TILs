"""
1이상 6이하 중 임의의 숫자가 그려진 n * n 격자판에  한 면이 1 * 1 크기인 정육면체
m번에 걸쳐 주사위를 계속 1칸씩 굴리게 됩니다.
마주보는 면에 적혀있는 숫자의 합은 정확히 7
항상 초기에 격자판의 1행 1열에 놓여져 있고, 처음에는 항상 오른쪽으로 움직입니다.

주사위를 움직일때마다, 격자판 위 주사위가 놓여있는 칸에 적혀있는 숫자와
 상하좌우로 인접하며 같은 숫자가 적혀있는 모든 칸의 합만큼 점수를 얻게 됩니다.

 주사위의 아랫면이 보드의 해당 칸에 있는 숫자보다 크면 현재 진행방향에서 90' 시계방향으로 회전
 주사위의 아랫면의 숫자가 더 작다면 현재 진행방향에서 90' 반시계방향으로 회전

 만약 진행 도중 다음과 같이 격자판을 벗어나게 된다면,
 반사되어 방향이 반대로 바뀌게 된 뒤 한 칸 움직이게 됩니다.

 n * n 크기의 격자판의 상태가 주어졌을 때, m번 진행하며 얻게되는 점수의 총 합

"""
from collections import deque


def oob(i, j):
    return i < 0 or j < 0 or i >= N or j >= N


# 1. 점수판 배열 구하기
def bfs(i, j):
    q = deque([(i, j)])
    visited[i][j] = 1
    lst = []
    score = 0
    num = arr[i][j]

    while q:
        cr, cc = q.popleft()
        lst.append((cr, cc))
        score += num

        for di, dj in DIR:
            du, dv = cr + di, cc + dj
            if oob(du, dv): continue
            if visited[du][dv]: continue
            if arr[du][dv] != num: continue
            q.append((du, dv))
            visited[du][dv] = 1

    for r, c in lst:
        visited[r][c] = score


# 2. 주사위 굴리는 함수 만들기
def move_dice(d):
    global bottom
    tmp = bottom
    bottom = side[d]
    side[d] = 7 - tmp
    side[(d + 2) % 4] = 7 - side[d]


N, M = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
visited = [[0] * N for _ in range(N)]
DIR = (0, 1), (-1, 0), (0, -1), (1, 0)

bottom = 6
side = [3, 5, 4, 2]
r, c = 0, 0
d = 0
answer = 0
for i in range(N):
    for j in range(N):
        if not visited[i][j]:
            bfs(i, j)

for m in range(M):
    di, dj = DIR[d]
    r += di
    c += dj
    if oob(r, c):
        d = (d + 2) % 4
        di, dj = DIR[d]
        r += di * 2
        c += dj * 2
    move_dice(d)
    answer += visited[r][c]
    if arr[r][c] > bottom:
        d = (d + 1) % 4

    elif arr[r][c] < bottom:
        # 시계 회전
        d = (d - 1) % 4
print(answer)