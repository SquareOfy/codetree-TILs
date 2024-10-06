"""

4 x 4 격자에 m개의 몬스터와 1개의 팩맨
각각의 몬스터는 상하좌우, 대각선 방향 중 하나를 가집니다.

턴 단위 진행

1. 몬스터 복제 시도
    현재의 위치에서 자신과 같은 방향을 가진 몬스터를 복제
    아직은 부화되지 않은 상태로 움직이지 못합니다. => 다른 배열에 따로 관리하다가 부화할 때 옮겨주자
    복제된 몬스터는 현재 시점을 기준으로 각 몬스터와 동일한 방향을 지니게 되며,
    이후 이 알이 부화할 시 해당 방향을 지닌 채로 깨어나게 됩니다.

2. 몬스터 이동
    몬스터는 현재 자신이 가진 방향대로 한 칸 이동
    움직이려는 칸에 몬스터 시체가 있거나, 팩맨이 있는 경우거나 격자를 벗어나는 방향일 경우에는
    반시계 방향으로 45도를 회전한 뒤 해당 방향으로 갈 수 있는지 판단
    가능할 때까지 반시계 방향으로 45도씩 회전
    만약 8 방향을 다 돌았는데도 불구하고, 모두 움직일 수 없었다면 해당 몬스터는 움직이지 않습니다.

3. 팩맨 이동
    팩맨의 이동은 총 3칸을 이동
     각 이동마다 상하좌우의 선택지를 가지게 됩니다.
     이 중 몬스터를 가장 많이 먹을 수 있는 방향으로 움직이게 됩니다.
     가장 많이 먹을 수 있는 방향이 여러개라면 상-좌-하-우의 우선순위를 가지며
     이동하는 과정에 격자 바깥을 나가는 경우는 고려하지 않습니다.
     알은 먹지 않으며, 움직이기 전에 함께 있었던 몬스터도 먹지 않습니다.

4. 시체 소멸
    몬스터의 시체는 총 2턴동안만 유지
    시체가 생기고 나면 시체가 소멸되기 까지는 총 두 턴을 필요

"""


def change_idx(i):
    return int(i) - 1


def oob(i, j):
    return i < 0 or j < 0 or i >= 4 or j >= 4


def dfs(level, r, c, cnt, lst):
    global mx_cnt, selected
    if level == 3:
        if mx_cnt < cnt:
            mx_cnt = cnt
            selected = lst[:]
        return

    for dk in range(4):
        di, dj = DIR[dk]
        nr, nc = r + di, c + dj
        if oob(nr, nc): continue
        if visited[nr][nc]: continue
        visited[nr][nc] = 1
        dfs(level + 1, nr, nc, cnt + len(monster_arr[nr][nc]), lst +[dk])
        visited[nr][nc] = 0


M, T = map(int, input().split())
pr, pc = map(change_idx, input().split())
DIR = (-1, 0), (0, -1), (1, 0), (0, 1)
diagonal = (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)

monster_arr = [[[] for _ in range(4)] for _ in range(4)]
egg_arr = [[[] for _ in range(4)] for _ in range(4)]
die_arr = [[0] * 4 for _ in range(4)]

visited = [[0] * 4 for _ in range(4)]

for m in range(M):
    r, c, d = map(change_idx, input().split())
    monster_arr[r][c].append(d)

for t in range(1, T+1):
    # 알 낳기
    for i in range(4):
        for j in range(4):
            for monster in monster_arr[i][j]:
                egg_arr[i][j].append(monster)

    # 몬스터 이동
    new_monster_arr = [[[] for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            for d in monster_arr[i][j]:

                for dk in range(8):
                    nd = (d + dk) % 8
                    di, dj = diagonal[nd]
                    nr, nc = i + di, j + dj
                    if oob(nr, nc): continue
                    if nr == pr and nc == pc: continue
                    if m - die_arr[nr][nc] <= 2: continue
                    new_monster_arr[nr][nc].append(nd)
                    break
                else:
                    new_monster_arr[i][j].append(d)

    for i in range(4):
        for j in range(4):
            monster_arr[i][j] = new_monster_arr[i][j][:]

    selected = []
    mx_cnt = 0
    # 팩맨이동 구하기 (dfs구현)
    visited[pr][pc] = 1
    dfs(0, pr, pc, 0, [])
    visited[pr][pc] = 0

    # 팩맨 이동결과 arr 에 반영
    for move in selected:
        di, dj = DIR[move]
        pr += di
        pc += dj
        monster_arr[pr][pc] = []
        die_arr[pr][pc] = t

    for i in range(4):
        for j in range(4):
            for d in egg_arr[i][j]:
                monster_arr[i][j].append(d)
            egg_arr[i][j] = []

answer = 0
for i in range(4):
    for j in range(4):
        answer += len(monster_arr[i][j])
print(answer)