from collections import deque

dr = [1, 0, -1, 0]
dc = [0, 1, 0, -1]


def make_groups():
    global num
    for r in range(N):
        for c in range(N):
            if vi[r][c] == 0:
                num_board[r][c] = num
                bfs(r, c, board[r][c])
                num += 1

    groups = [[] for _ in range(num)]  # 그룹의 좌표를 저장할 배열
    group_info = [[0, 0] for _ in range(num)] # 그룹의 정보를 저장할 배열(그룹 크기, 그룹 안의 숫자)

    for r in range(N):
        for c in range(N):
            groups[num_board[r][c]].append((r, c))

    for i in range(1, num):
        group_info[i] = [len(groups[i]), board[groups[i][0][0]][groups[i][0][1]]]

    return groups, group_info, num


def rotate():
    new_board = [[0] * N for _ in range(N)]
    new_board[N // 2] = board[N // 2][:]  # 가로 가운데 옮김
    for i in range(N):
        new_board[i][N // 2] = board[i][N // 2]

    new_board = list(map(list, zip(*new_board)))[::-1]
    for i in range(0, N, N//2+1):
        for j in range(0, N, N//2+1):
            tmp = [[] for _ in range(N//2)]
            for k in range(N//2):
                tmp[k] = board[i+k][j:j+N//2]

            tmp = list(map(list, zip(*tmp[::-1])))

            for k in range(N//2):
                new_board[i+k][j:j+N//2] = tmp[k][:]

    return new_board


def make_comb():
    for i in range(1, num - 1):
        for j in range(i + 1, num):
            comb.append((i, j))


def bfs(r, c, n):
    q = deque([(r, c)])
    vi[r][c] = 1
    while q:
        pr, pc = q.popleft()

        for i in range(4):
            nr, nc = pr + dr[i], pc + dc[i]
            if nr < 0 or nr >= N or nc < 0 or nc >= N: continue
            if vi[nr][nc]: continue
            if board[nr][nc] == n:
                vi[nr][nc] = 1
                num_board[nr][nc] = num
                q.append((nr, nc))


def cal_harmony():
    global harmony
    for i, j in comb:  # 작은 수, 큰 수
        a, b, c, d = groups[i], groups[j], group_info[i], group_info[j]
        cnt = 0  # 몇 칸 인접해 있는지 체크할 변수
        for r1, c1 in a:
            for r2, c2 in b:
                if abs(r1 - r2) + abs(c1 - c2) == 1:  # 인접해 있다면 카운트 증가한다.
                    cnt += 1
        harmony += (c[0] + d[0]) * c[1] * d[1] * cnt


N = int(input())
board = [list(map(int, input().split())) for _ in range(N)]
num_board = [[0] * N for _ in range(N)] # 그룹 번호 저장
comb = []
harmony = 0

for i in range(4):
    vi = [[0] * N for _ in range(N)] # 그룹 만들 때 사용할 방문 배열
    num = 1

    groups, group_info, num = make_groups()
    make_comb()
    cal_harmony()
    board = rotate()

print(harmony)