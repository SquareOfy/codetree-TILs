"""

"""
from collections import deque


def oob(i, j):
    return i < 0 or j < 0 or i >= N or j >= N


def bfs(i, j, g_num):
    q = deque([(i, j)])
    n = arr[i][j]
    cnt = 0
    visited[i][j] = group_num
    lst = []

    while q:
        cr, cc = q.popleft()
        cnt += 1
        flag = False
        for di, dj in DIR:
            du, dv = cr + di, cc + dj
            if oob(du, dv): continue
            if visited[du][dv]:
                continue
            if arr[du][dv] == n:
                q.append((du, dv))
                visited[du][dv] = g_num
            else:
                flag = True
        if flag:
            lst.append((cr, cc))
    return cnt, lst


N = int(input())
arr = [list(map(int, input().split())) for _ in range(N)]
DIR = (-1, 0), (0, 1), (1, 0), (0, -1)
answer = []


def calculate_score(a, b):
    cnt_sum = cnt_lst[a]+cnt_lst[b]
    line_cnt = line_arr[a][b] + line_arr[b][a]
    return cnt_sum*num_lst[a]*num_lst[b]*line_cnt



for i in range(4):
    # 예술 점수 구하기

    # 현재 배열에서 같은 그룹 구하기
    check_arr = [-1]
    visited = [[0] * N for _ in range(N)]
    num_lst = [-1]
    group_num = 0
    cnt_lst = [-1]
    for r in range(N):
        for c in range(N):
            if visited[r][c]: continue
            num = arr[r][c]
            group_num += 1
            cnt, lst = bfs(r, c, group_num)
            cnt_lst.append(cnt)
            check_arr.append(lst)
            num_lst.append(num)
    line_arr = [[0]*(group_num +1) for _ in range(group_num+1)]
    for k in range(1, group_num+1):
        lst = check_arr[k]
        for r, c in lst:
            for di, dj in DIR:
                nr, nc = r+di, c+dj
                if oob(nr, nc): continue
                if visited[nr][nc]>k:
                    line_arr[k][visited[nr][nc]] += 1

    # for k in range(group_num+1):
    #     print(line_arr[k])
    # print("===========================")
    score = 0
    for a in range(1, group_num+1):
        for b in range(a+1, group_num+1):
            score += calculate_score(a, b)
    answer.append(score)
    if i == 3:
        break

    # 배열 회전하기
    tmp = [[0]*N for _ in range(N)]
    for t in range(N):
        tmp[t][N//2] = arr[t][N//2]
        tmp[N//2][t] = arr[N//2][t]

    tmp = list(map(list, zip(*arr)))[::-1]
    sub_tmp = [[] for _ in range(N//2)]
    for u in range(2):
        for v in range(2):
            sr, sc = (N//2+1)*u, (N//2+1)*v
            for t in range(N//2):
                sub_tmp[t] = arr[sr+t][sc:sc+N//2]
            sub_tmp = list(map(list, zip(*sub_tmp[::-1])))
            for t in range(N//2):
                tmp[sr+t][sc:sc+N//2] = sub_tmp[t][:]
    for t in range(N):
        arr[t] = tmp[t][:]


print(sum(answer))