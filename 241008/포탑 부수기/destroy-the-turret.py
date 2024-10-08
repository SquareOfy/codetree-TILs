from collections import deque
def find_attack():
    mn = float("inf")
    rr, rc = -1, -1
    for i in range(N):
        for j in range(M):
            if arr[i][j] == 0: continue
            if arr[i][j] < mn:
                rr, rc = i, j
                mn = arr[i][j]
            elif arr[i][j] == mn:
                if recent_attack[i][j] > recent_attack[rr][rc]:
                    rr, rc = i, j
                elif recent_attack[i][j] == recent_attack[rr][rc]:
                    if i+j > rr+rc:
                        rr, rc = i, j
                    elif i+j == rr+rc and j>rc:
                        rr, rc = i, j

    return rr, rc


def find_target():
    mx = 0
    rr, rc = -1, -1
    for i in range(N):
        for j in range(M):
            if arr[i][j] == 0: continue
            if i==ar and j==ac: continue
            if arr[i][j] > mx:
                rr, rc = i, j
                mx = arr[i][j]
            elif arr[i][j] == mx:
                if recent_attack[i][j] < recent_attack[rr][rc]:
                    rr, rc = i, j
                elif recent_attack[i][j] == recent_attack[rr][rc]:
                    if i + j < rr + rc:
                        rr, rc = i, j
                    elif i + j == rr + rc and j < rc:
                        rr, rc = i, j

    return rr, rc

# def oob(r, c):
#     return r<0 or c<0 or r>=N or c>=M

def laser_attack():
    q = deque([(ar, ac, [])])
    visited = [[0]*M for _ in range(N)]
    visited[ar][ac] = 1

    while q:
        cr, cc, lst = q.popleft()
        if cr ==tr and cc==tc:
            lst.pop()
            return 1, lst
        for di, dj in DIR:
            du, dv = cr+di, cc+dj
            du %= N
            dv %= M
            if visited[du][dv]:
                continue
            if arr[du][dv] == 0:
                continue
            q.append((du, dv, lst+[(du, dv)]))
            visited[du][dv] = 1
    return 0, []

def attack(r, c, power):
    global top_cnt
    if arr[r][c] == 0:
        return
    arr[r][c] -= power
    if arr[r][c] < 0:
        top_cnt-=1
        arr[r][c] = 0

def printa(string, arr):
    print(f"============={string}====================")
    for i in range(len(arr)):
        print(arr[i])
    print("=========================================")
    print()

N, M, K = map(int, input().split())
recent_attack = [[0]*M for _ in range(N)]
top_cnt = N*M

arr=  [list(map(int, input().split())) for _ in range(N)]
DIR = (0, 1), (1, 0), (0, -1), (-1, 0)
diagonal =[(-1, -1), (-1, 1), (1, -1), (1, 1)] + list(DIR)

for i in range(N):
    top_cnt -= arr[i].count(0)


for k in range(1, K+1):
    if top_cnt == 1:
        break

    #공격자 찾기(recent 갱신할 것)
    ar, ac = find_attack()
    arr[ar][ac] += (N+M)
    recent_attack[ar][ac] = k

    #타겟 찾기 ( 공격자 제외할 것)
    tr, tc = find_target()
    #
    # print("==============================")
    # print("ar, ac : ", ar, ac)
    # print("tr, tc : ", tr, tc)
    # printa("최근 공격 현황 ", recent_attack)
    # printa("현재 arr ", arr)


    #레이저 공격 가능한지 보기 (가능 여부, 공격 경로 반환)
    result, lst = laser_attack()

    #공격 과정에서 0되면 top_cnt 빼기
    #가능하면 lst에 있는 레이저 공격 하기 (공격력 절반)
    #불가하면 포탑공격하기 ( 공격자 제외하기)
    if not result:
        # print("포탑 공격 할 거임")
        for di, dj in diagonal:
            du, dv = tr+di, tc+dj
            du %= N
            dv %= M
            if du==ar and dv==ac: continue
            lst.append((du, dv))
    related = [[0]*M for _ in range(N)]
    related[ar][ac] = 1
    # print(lst)
    for r, c in lst:
        related[r][c] = 1
        attack(r, c, arr[ar][ac]//2)

    #타겟 공격하기
    attack(tr, tc, arr[ar][ac])
    related[tr][tc] = 1
    # printa("공격 후 arr ", arr)
    # print(top_cnt)

    for r in range(N):
        for c in range(M):
            if not related[r][c] and arr[r][c] !=0:
                arr[r][c] += 1
    # printa("더한 후 ", arr)

answer = 0
for t in range(N):
    answer = max(answer, max(arr[t]))
print(answer)