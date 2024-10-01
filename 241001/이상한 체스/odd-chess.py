"""

각각의 말들은 네 방향 중 한 가지 방향을 선택
선택하는 방향에 따라 이동할 수 있는 격자의 범위가 달라집니다.
 체스판에 놓인 말들의 방향을 적절히 설정하여 갈 수 없는 격자의 크기를 최소화

 본인의 말은 뛰어넘어서 지나갈 수 있습니다.
 다만 상대편의 말은 뛰어넘어서 지나갈 수 없습니다
이후 갈 수 없는 격자의 크기를 계산할 때 상대편 말이 있는 격자는 계산하지 않습니다.

1~5의 경우 자신의 말의 종류를 의미
6은 상대편의 말을 의미



1 ≤ n, m ≤ 8
자신의 말의 개수는 최대 8개를 넘지 않는다고 가정해도 좋습니다.
최대 4**8 보다 작음

비어있음에도 자신의 말을 이용해서 갈 수 없는 체스판의 영역 넓이의 총 합의 최솟값

"""


def oob(i, j):
    return i<0 or j<0 or i>=N or j>=M

def check_visited(r, c, dir_lst, v):
    cnt = 0
    for d in dir_lst:
        di, dj = DIR[d]
        du, dv = r + di, c + dj
        while not oob(du, dv) and arr[du][dv] != 6:
            if arr[du][dv] == 0:
                visited[du][dv] += v
            du += di
            dv += dj
            if oob(du, dv) or arr[du][dv]==6:
                break
    return cnt
# dfs
def dfs(level, value):
    if level == K:
        global answer
        cnt = 0
        for k in range(N):
            for v in range(M):
                if not visited[k][v] and arr[k][v] ==0:
                    cnt += 1
        answer = min(answer, cnt)

        return

    r, c = my_mal_lst[level]
    mal_num = arr[r][c]

    for dir_lst in dir_dict[mal_num]:

        cnt = check_visited(r, c, dir_lst, 1)

        dfs(level+1, value+cnt)
        check_visited(r, c, dir_lst, -1)





# input
N, M = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
visited = [[0] * M for _ in range(N)]

# dict 준비
dir_dict = {1: ((0,), (1,), (2,), (3, )), 2: ((0, 2), (1, 3)), 3:((0, 1), (1, 2), (2, 3), (3, 0)), \
    4: ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)), 5 : ((0, 1, 2, 3), )}
DIR = (-1, 0), (0, 1), (1, 0), (0, -1)

# blank, my_mal_lst 준비
blank = 0
my_mal_lst = []
answer = N*M
for i in range(N):
    for j in range(M):
        if arr[i][j]==0:
            blank += 1
        elif arr[i][j] <6 :
            my_mal_lst.append((i, j))


K = len(my_mal_lst)
dfs(0, 0)
print(answer)