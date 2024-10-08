"""
격자는 가장 위를 1행, 가장 아래를 R행
총 K명의 정령은 각자 골렘을 타고 숲을 탐색

골렘은 십자 모양의 구조
골렘의 중앙을 제외한 4칸 중 한 칸은 골렘의 출구

정령은 어떤 방향에서든 골렘에 탑승할 수 있지만
골렘에서 내릴 때에는 정해진 출구를 통해서만 내릴 수 있습니다.

골렘은 숲의 가장 북쪽에서 시작
골렘의 중앙이 ci 열이 되도록 하는 위치에서 내려오기 시작
초기 골렘의 출구는 d 의 방향에 위치

(1) 남쪽으로 한 칸 내려갑니다.
    [r+1][c-1], [r+2][c] , [r+1][c+1]

(2) (1)의 방법으로 이동할 수 없으면 서쪽 방향으로 회전하면서 내려갑니다.
    서쪽 : [r-1][c-1] [r][c-2] [r+1][c-1]

(3) (1)과 (2)의 방법으로 이동할 수 없으면 동쪽 방향으로 회전하면서 내려갑니다.
    동쪽 : [r-1][c+1] [r][c+2] [r+1][c+1]


"""
from collections import deque

def printa(string, arr):
    print(f"=============={string}==============")
    for i in range(len(arr)):
        print(arr[i])
    print("====================================")
    print()
def oob(i, j):
    return i < 0 or j < 0 or i >= R + 3 or j >= C


def check(cd, r, c):
    if cd == 0:  # 남쪽 체크
        if oob(r + 2, c):
            return False
        if arr[r + 1][c - 1] or arr[r + 2][c] or arr[r + 1][c + 1]:
            return False
    elif cd == 1:  # 서쪽 체크
        if oob(r + 1, c - 2):
            return False
        if arr[r - 1][c - 1] or arr[r][c - 2] or arr[r + 1][c - 1]:
            return False
    else:  # 동쪽 체크
        if oob(r + 1, c + 2):
            return False
        if arr[r - 1][c + 1] or arr[r][c + 2] or arr[r + 1][c + 1]:
            return False
    return True


def move_near_gol(gol_num, r):
    global answer
    visited = [0] * (K + 1)
    visited[gol_num] = 1
    q = deque([gol_num])
    mx = r
    while q:
        num = q.popleft()
        cr, cc, cd = gol_info[num]
        mx = max(mx, cr+1)
        cdi, cdj = DIR[cd]
        cr+=cdi
        cc+=cdj
        for di, dj in DIR:
            du, dv = cr+di, cc+dj
            if oob(du, dv): continue
            if arr[du][dv] == 0: continue
            G_num = arr[du][dv]
            if visited[G_num]: continue

            q.append(G_num)
            visited[G_num] = 1
    return mx

R, C, K = map(int, input().split())
DIR = (-1, 0), (0, 1), (1, 0), (0, -1)
arr = [[0] * C for _ in range(R + 3)]

answer = 0

gol_info = [[] for _ in range(K + 1)]
for k in range(1, K + 1):
    c, d = map(int, input().split())
    c -= 1
    r = 1

    while 1:
        if check(0, r, c):
            r += 1
        elif check(1, r, c) and check(0, r, c-1):
            r += 1
            c -= 1
            d = (d - 1) % 4
        elif check(2, r, c) and check(0, r, c+1):
            r += 1
            c += 1
            d = (d + 1) % 4
        else:
            break
        if r == R + 1:
            break

    if r < 4:
        arr = [[0] * C for _ in range(R + 3)]
        continue
    gol_info[k] = (r, c, d)
    arr[r][c] = k
    for di, dj in DIR:
        du, dv = r + di, c + dj
        arr[du][dv] = k
    # printa(f"{k}", arr)
    answer += move_near_gol(k, r) -2
    # print("answer : ", answer)
print(answer)