from collections import deque

def oob(i, j ):
    return i>=5 or j>=5 or i<0 or j<0


def find_rotate():

    mx = 0
    selected_r, selected_c, rotate_cnt = -1, -1, -1
    # 배열 복사
    tmp = [[] for _ in range(5)]
    for t in range(5):
        tmp[t] = arr[t][:]
    for j in range(1, 4):
        for i in range(1, 4):
            # 회전할 부분 복사
            selected_tmp = [[] for _ in range(3)]
            for t in range(3):
                selected_tmp[t] = tmp[i - 1 + t][j - 1:j + 2]

            # 오른쪽으로 90도 회전 3번은 bfs 1번은 배열 원상복구용
            for t in range(4):
                # 오른쪽으로 90
                selected_tmp = list(map(list, zip(*selected_tmp[::-1])))

                # tmp 배열에 붙여넣기
                for tt in range(3):
                    tmp[i - 1 + tt][j - 1:j + 2] = selected_tmp[tt][:]

                if t == 4: break  # tmp 원상복구 해놓고 다음 경우 고려하러 가기
                value = calculate_value(tmp)

                if mx < value:
                    selected_r, selected_c, rotate_cnt = i, j, t
                    mx = value

                elif mx == value and t<rotate_cnt:
                    selected_r, selected_c, rotate_cnt = i, j, t

    return selected_r, selected_c, rotate_cnt


def check_bfs(i, j, tmp):
    q = deque([(i, j)])
    visited[i][j] = 1
    cnt = 0
    while q:
        cr, cc = q.popleft()
        cnt += 1
        for di, dj in DIR:
            du = cr + di
            dv = cc + dj
            if oob(du, dv) or visited[du][dv]:
                continue
            if tmp[du][dv] == tmp[i][j]:
                visited[du][dv] = 1
                lst.append((du, dv))
                q.append((du, dv))

    return cnt

def calculate_value(tmp):
    global visited
    visited = [[0]*5 for _ in range(5)]
    value = 0

    for i in range(5):
        for j in range(5):
            if visited[i][j]: continue
            v =  check_bfs(i, j, tmp)
            if v>=3:
                value+= v
    return value


def delete_value(num, i, j):
    visited[i][j] = 1
    q = deque([(i, j)])
    del_lst = []

    while q:
        cr, cc = q.popleft()
        del_lst.append((cr, cc))
        for di, dj in DIR:
            du = cr+di
            dv = cc+dj

            if oob(du, dv) or visited[du][dv]:
                continue
            if arr[du][dv] == num:
                q.append((du, dv))
                visited[du][dv] = 1
    if len(del_lst) >= 3:
        for r, c in del_lst:
            arr[r][c] = 0
        return len(del_lst)
    return 0

def get_value():
    global visited
    visited = [[0]*5 for _ in range(5)]
    value = 0
    for i in range(5):
        for j in range(5):
            if not visited[i][j]:
                value += delete_value(arr[i][j], i, j)
    return value

def new_piece():
    global idx
    for j in range(5):
        for i in range(4, -1, -1):
            if arr[i][j] == 0:
                arr[i][j] = lst[idx]
                idx+=1


# 5×5 격자 형태  ||| 유물 조각은 총 7가지 종류 1부터 7
K, M = map(int, input().split())

arr = [list(map(int, input().split())) for _ in range(5)]
lst = list(map(int, input().split()))
idx = 0 #새로운 유물 조각 시작 idx
DIR = (-1, 0), (0, 1), (1, 0), (0, -1)
# 총 K 번의 턴에 걸쳐 진행
answer_lst = []
for k in range(K):
    answer = 0 #매턴마다 출력이므로

    visited = [[0]*5 for _ in range(5)]
    r, c, rotate_cnt = find_rotate()

    if r==-1 and c==-1:
        break

    # 회전할 부분 복사 후 회전 - 원배열에 붙여넣기
    selected_tmp = [[] for _ in range(3)]
    for t in range(3):
        selected_tmp[t] = arr[r - 1 + t][c - 1:c + 2]

    for tt in range(rotate_cnt+1):
        selected_tmp = list(map(list, zip(*selected_tmp[::-1])))

    for tt in range(3):
        arr[r - 1 + tt][c - 1:c + 2] = selected_tmp[tt][:]

    while 1:
        #유물 획득하기
        answer += get_value()
        # 새로운 조각 넣기
        new_piece()

        v = calculate_value(arr)
        if v==0:
            break
    if answer == 0:
        break
    answer_lst.append(answer)

print(*answer_lst)