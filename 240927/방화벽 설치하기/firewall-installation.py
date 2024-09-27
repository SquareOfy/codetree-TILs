"""

불은 상하좌우의 인접한 공간으로 모두 번지는 특성
기존에 이미 설치되어 있는 방화벽을 제외하고 추가로 3개의 방화벽을 설치
정확히 3개의 방화벽을 추가로 설치
불이 퍼지지 않는 영역이 최대일 때의 크기를 출력

2 불
1 방화벽
0 빈칸

"""
from collections import deque

def bfs():
    q = deque(fire_lst)
    visited = [[0]*M for _ in range(N)]
    cnt = 0
    for i, j in fire_lst:
        visited[i][j] = 1
    while q:
        cr, cc = q.popleft()

        for di, dj in (-1, 0), (0, 1), (1, 0), (0, -1):
            du = cr+di
            dv = cc+dj
            if du<0 or dv<0 or du>=N or dv>=M or visited[du][dv] or arr[du][dv]:
                continue
            visited[du][dv] = 1
            cnt+=1
            q.append((du, dv))

    return cnt


def dfs(level, idx, selected):
    global answer
    if level == 3:
        cnt = bfs()
        answer = max(answer, blank-3-cnt)
        return
    for i in range(idx, blank):
        r, c = blank_lst[i]
        arr[r][c] = 1
        dfs(level+1, i+1, selected+[i])
        arr[r][c] = 0
N, M = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
blank = 0
blank_lst = []
fire_lst = []
answer = 0
for i in range(N):
    for j in range(M):
        if arr[i][j] ==0:
            blank+=1
            blank_lst.append((i, j))
        elif arr[i][j] == 2:
            fire_lst.append((i, j))



dfs(0, 0, [])
print(answer)