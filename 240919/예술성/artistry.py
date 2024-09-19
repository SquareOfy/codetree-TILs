"""

1. 예술 점수 구하기
    1) BFS로 visited에 num 올려가며 그룹 표시하기
        여기서 아래 배열도 채울 수 있다(append로)

            해당 그룹의 칸 수
    2) visited 탐색하며 아래 배열 값 구하기
        - near_group_cnt = [[0] * (num+1) for _ in range(num+1)]
            그룹끼리 인접한 변의 개수
        - count_arr = [0] * (num+1)
            해당 그룹의 칸 수
        - num_arr = [0] * (num +1)
        - count_arr = [0] * (num+1)
    3) 조합 뽑아서 점수에 더하기
        - dfs 함수 (level, lst, idx)
            if level ==2:
                lst에 있는 애들 점수 구해서 score(전역)에 더하기
                :return
            for in range(idx, num+1)
                dfs(level, lst+[i], i+1)
    4) 점수 출력

2. 회전하기
    1). 새 배열 만들어서 십자가 옮기기
    2) 90도 반시계 회전
    3) 네 사각형 시계 회전해서 옮기기
    4) 배열 원본 배열에 붙이기

"""
from collections import deque

def oob(i, j):
    return i<0 or j<0 or i>=n or j>=n
def bfs(r, c, num):
    q = deque([(r, c)])
    visited[r][c] = num
    k = arr[r][c]
    while q:
        cr, cc = q.popleft()

        for di, dj in dir:
            du = cr+di
            dv = cc+dj

            if oob(du, dv) or visited[du][dv]:
                continue
            if arr[du][dv] == k:
                visited[du][dv] = num
                q.append((du, dv))

# - dfs 함수 (level, lst, idx)
#             if level ==2:
#                 lst에 있는 애들 점수 구해서 score(전역)에 더하기
#                 :return
#             for in range(idx, num+1)
#                 dfs(level, lst+[i], i+1)
def dfs(level, lst, idx):
    global score
    if level == 2:
        a, b = lst[0], lst[1]
        tmp = (count_arr[a]+count_arr[b])*num_arr[a]*num_arr[b]*near_group_cnt[a][b]
        # print("lst : ", lst)
        # print("tmp : ", tmp)
        score += tmp
        return
    for i in range(idx, num+1):
        dfs(level+1, lst+[i], i+1)

#입력받기
n = int(input())
arr = [list(map(int, input().split())) for _ in range(n)]
dir = (-1, 0), (0, 1), (1, 0), (0, -1)
answer = 0
#1) BFS로 visited에 num 올려가며 그룹 표시하기
        # 여기서 아래 배열도 채울 수 있다(append로)
        # - num_arr = [0] * (num +1)
        # - count_arr = [0] * (num+1)
        #     해당 그룹의 칸 수
for i in range(4):
    visited = [[0]*(n) for _ in range(n)]
    num_arr = [0]
    num = 0
    for i in range(n):
        for j in range(n):
            #주변탐색하며 같은 그룹에 visited 표기
            if not visited[i][j]:
                num += 1
                bfs(i, j, num)
                num_arr.append(arr[i][j])

    #visited 그룹 분할 체크 완료 ########################
    # print(num)
    # for i in range(n):
    #     print(visited[i])
    # print()
    ######################################################3

    #     2) visited 탐색하며 아래 배열 값 구하기
    #         - near_group_cnt = [[0] * (num+1) for _ in range(num+1)]
    #             그룹끼리 인접한 변의 개수
    #         - count_arr = [0] * (num+1)
    #             해당 그룹의 칸 수


    near_group_cnt = [[0] * (num+1) for _ in range(num+1)]
    count_arr = [0] * (num + 1)
    for i in range(n):
        for j in range(n):
            group_num =visited[i][j]
            count_arr[group_num] += 1
            for di, dj in dir:
                du = i+di
                dv = j+dj
                if oob(du, dv):
                    continue
                near = visited[du][dv]
                if near != group_num:
                    near_group_cnt[group_num][near] += 1
#########################인접 개수, 그룹 개수 체크 완#################3
    # for i in range(num+1):
    #     print(near_group_cnt[i])
    # print()
    # print(count_arr)
    # print()
    #############################################

    # 3) 조합 뽑아서 점수에 더하기
    score = 0
    dfs(0, [], 1)
    answer += score
    # print(score)
    ### 0 회전 점수 체크 완

    # 2. 회전하기
    #     1). 새 배열 만들어서 십자가 옮기기

    new_arr = [[0]*n for _ in range(n)]
    new_arr[n//2] = arr[n//2][:] #가로 가운데 옮김
    for i in range(n):
        new_arr[i][n//2] = arr[i][n//2]

    #     2) 90도 반시계 회전
    new_arr = list(map(list, zip(*new_arr)))[::-1]

    ###########십자가 반ㅅ니계 체크 완 #############33
    # for i in range(n):
    #     print(new_arr[i])
    # print()

    ##############################################33


    #     3) 네 사각형 시계 회전해서 옮기기
    for i in range(0, n, n//2+1):
        for j in range(0, n, n//2+1):
            tmp = [[] for _ in range(n//2)]
            for k in range(n//2):
                tmp[k] = arr[i+k][j:j+n//2]

            tmp = list(map(list, zip(*tmp[::-1])))

            for k in range(n//2):
                new_arr[i+k][j:j+n//2] = tmp[k][:]

    # for i in range(n):
    #     print(new_arr[i])
    # print()
    #     4) 배열 원본 배열에 붙이기
    for i in range(n):
        arr[i] = new_arr[i][:]
print(answer)