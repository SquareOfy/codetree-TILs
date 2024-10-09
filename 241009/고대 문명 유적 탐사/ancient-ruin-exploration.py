"""

아래를 총 K번의 턴 진행
1. 5×5 격자 내에서 3×3 격자를 선택하여 격자를 회전

    선택된 격자는 시계 방향으로 90도, 180도, 270도 중 하나의 각도만큼 회전

    (1) 유물 1차 획득 가치를 최대화
    (2) 회전한 각도가 가장 작은 방법
    (3) 회전 중심 좌표의 열이 가장 작은 구간
    (4) 열이 같다면 행이 가장 작은 구간

    2. 유물 1차 획득
        상하좌우로 인접한 같은 종류의 유물 조각,  3개 이상 연결된 경우
        조각이 모여 유물이 되고 사라집니다.

        유물의 가치는 모인 조각의 개수

    3. 조각이 사라진 위치에는 유적의 벽면에 적혀있는 순서대로 새로운 조각
         (1) 열 번호가 작은 순으로 조각이 생겨납니다.
         (2) 행 번호가 큰 순으로 조각
         유적의 벽면에 써 있는 숫자를 사용한 이후에는 다시 사용할 수 없으므로 이후 부터는 남은 숫자부터 순서대로 사용합니다.

    4. 유물 연쇄 획득
        새로운 유물 조각이 생겨난 이후에도 조각들이 3개 이상 연결될 수 있습니다.
        더 이상 조각이 3개 이상 연결되지 않아 유물이 될 수 없을 때까지 반복됩니다.

출력 : 각 턴마다 획득한 유물의 가치의 총합
"""
from collections import deque


def remove_piece():
    visited = [[0] * 5 for _ in range(5)]
    result = 0
    for r in range(5):
        for c in range(5):
            if arr[r][c] == 0: continue

            q = deque([(r, c)])
            lst = []
            visited[r][c] = 1

            while q:
                cr, cc = q.popleft()
                lst.append((cr, cc))
                for di, dj in DIR:
                    du, dv = cr + di, cc + dj
                    if oob(du, dv): continue
                    if visited[du][dv]: continue
                    if arr[du][dv] != arr[r][c]: continue
                    q.append((du, dv))
                    visited[du][dv] = 1

            if len(lst) >= 3:
                for i, j in lst:
                    arr[i][j] = 0
                result += len(lst)
    return result


def oob(i, j):
    return i < 0 or j < 0 or i >= 5 or j >= 5


def cal_value():
    visited = [[0] * 5 for _ in range(5)]

    result = 0

    for r in range(5):
        for c in range(5):
            if visited[r][c]: continue

            q = deque([(r, c)])
            cnt = 0
            visited[r][c] = 1

            while q:
                cr, cc = q.popleft()
                cnt += 1

                for di, dj in DIR:
                    du, dv = cr + di, cc + dj
                    if oob(du, dv): continue
                    if visited[du][dv]: continue
                    if arr[du][dv] != arr[r][c]: continue
                    q.append((du, dv))
                    visited[du][dv] = 1
            if cnt >= 3:
                result += cnt
    return result


def fill_piece():
    global idx
    for c in range(5):
        for r in range(4, -1, -1):
            if arr[r][c] == 0:
                arr[r][c] = piece_lst[idx]
                idx += 1
                # idx %= M

def printa(string, arr):
    print(f"================={string}=================")
    for i in range(5):
        print(arr[i])
    print('========================================')
    print()


K, M = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(5)]

piece_lst = list(map(int, input().split()))
idx = 0
answer = []

DIR = (-1, 0), (0, 1), (1, 0), (0, -1)

for k in range(K):
    # 갱신할 회전정보
    value = 0
    rotate_cnt = 0
    Rr, Rc = -1, -1
    # 회전 위치 찾기
    for c in range(1, 4):
        for r in range(1, 4):
            # 회전영역
            tmp = [[] for _ in range(3)]
            for i in range(r - 1, r + 2):
                tmp[i - r + 1] = arr[i][c - 1:c + 2]

            for t in range(4):
                tmp = list(map(list, zip(*tmp[::-1])))

                # 회전한거 붙여넣기
                for i in range(r - 1, r + 2):
                    arr[i][c - 1:c + 2] = tmp[i - r + 1][:]

                if t == 3: break

                cnt = cal_value()
                if cnt > value:
                    value = cnt
                    Rr, Rc = r, c
                    rotate_cnt = t + 1
                elif cnt == value and rotate_cnt > t + 1:
                    rotate_cnt = t + 1
                    Rr, Rc = r, c

    # 회전하기
    tmp = [[] for _ in range(3)]
    for i in range(Rr - 1, Rr + 2):
        tmp[i - Rr + 1] = arr[i][Rc - 1:Rc + 2]

    for t in range(rotate_cnt):
        tmp = list(map(list, zip(*tmp[::-1])))


    for i in range(Rr - 1, Rr + 2):
        arr[i][Rc - 1:Rc + 2] = tmp[i - Rr + 1][:]

    score = 0
    if value == 0:
        break
    while 1:
        # 유물 없애기
        value = remove_piece()
        # 없앤 유적 없으면 break
        if value == 0:
            break
        score += value
        # 채우기
        fill_piece()
    answer.append(score)
print(*answer)