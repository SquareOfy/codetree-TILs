#  각 골렘은 십자 모양의 구조 . 중앙 칸을 포함해 총 5칸을 차지
# 골렘의 중앙을 제외한 4칸 중 한 칸은 골렘의 출구입니다
# 어떤 방향에서든 골렘에 탑승할 수 있지만 내릴 때에는 정해진 출구를 통해서만 내릴 수 있다


# (1) 남쪽으로 한 칸 내려갑니다.
# (2) (1)로 이동할 수 없으면 서쪽 방향으로 회전하면서 내려갑니다. 서쪽 한 칸이 모두 비어 있어야 함
# 출구가 반시계방향으로 이동
# (3) (1)과 (2)의 안되면 동쪽 방향으로 회전하면서 내려갑니다.
# 골렘을 기준으로 동쪽 한 칸이 모두 비어 있어야 함에 유의
# 출구가 시계방향으로 이동


def oob(r, c):
    return r < 0 or c < 0 or r >= R+3 or c >= C


def can_move(r, c, dk):
    if dk == 2:
        if oob(r + 2, c):
            return False
        if not arr[r + 2][c] and not arr[r + 1][c - 1] and not arr[r + 1][c + 1]:
            return True
        return False
    elif dk == 3:
        if oob(r, c - 2):
            return False
        if  not arr[r][c - 2] and not arr[r + 1][c - 1] and not arr[r - 1][c - 1]:
            return True
        return False
    elif dk == 1:
        if oob(r, c + 2):
            return False
        if not arr[r][c + 2] and not arr[r + 1][c + 1] and not arr[r - 1][c + 1]:
            return True
        return False

def move_to_exit(r, c, d):
    mx = -1
    er, ec = r + DIR[d][0], c + DIR[d][1]
    for di, dj in DIR:
        nr, nc = er + di, ec + dj
        if oob(nr, nc) or arr[nr][nc] == 0 or arr[nr][nc] == i:
            continue
        num = arr[nr][nc]
        if visited[num]: continue
        ngr, ngc, ngd = gol_info[arr[nr][nc]]
        visited[num] = 1
        tmp = move_to_exit(ngr, ngc, ngd)
        if tmp>mx:
            mx = tmp
    mx = max(r+1, mx)
    return mx


R, C, K = map(int, input().split())
arr = [[0] * C for _ in range(R+3)]
DIR = (-1, 0), (0, 1), (1, 0), (0, -1)
gol_info = [0]*(K+1)
answer = 0
for i in range(1, K + 1):
    cc, d = map(int, input().split())
    cr = 1
    cc -= 1

    while 1:
        if can_move(cr, cc, 2):
            cr += 1
        elif can_move(cr, cc, 3) and can_move(cr, cc - 1, 2):
            cr += 1
            cc -= 1
            d = (d - 1) % 4

        elif can_move(cr, cc, 1) and can_move(cr, cc + 1, 2):
            cr += 1
            cc += 1
            d = (d + 1) % 4
        else:
            break
        if cr == R+1:
            break

    if cr<4:
        arr = [[0]*C for _ in range(R+3)]
        continue
    arr[cr][cc] = i
    for di, dj in DIR:
        arr[cr+di][cc+dj] = i

    gol_info[i] = (cr, cc, d)
    visited = [0]*(K+1)
    tmp = move_to_exit(cr, cc, d)-2
    answer += tmp
    # print(f"=================={i}======================")
    # print(gol_info)
    # for k in range(R+3):
    #     print(arr[k])
    # print("===========================")

print(answer)