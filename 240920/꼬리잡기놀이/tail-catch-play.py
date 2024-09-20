from collections import deque
def oob(r, c):
    return r<0 or c<0 or r>=N or c>=N

def bfs(r, c, team_num):
    visited[r][c] = 1
    q = deque([(r, c)])

    while q:
        cr, cc = q.popleft()
        team[team_num].append((cr, cc))
        num = arr[cr][cc]
        if arr[cr][cc] == 3:
            return
        for di, dj in dir:
            du = cr+di
            dv = cc+dj

            if oob(du, dv) or visited[du][dv]:
                continue
            if arr[du][dv] == num or arr[du][dv] == num+1:
                visited[du][dv] = 1
                q.append((du, dv))


def throw_ball(round):

    if round in range(N):
        row = round
        for j in range(N):
            if arr[row][j] !=0 and arr[row][j] != 4:
                return (row, j)
    elif round in range(N, 2*N):
        col = round%N

        for i in range(N-1, -1, -1):
            if arr[i][col] !=0 and arr[i][col] != 4:
                return (i, col)

    elif round in range(2*N, 3*N):
        row = N-1 - round%N

        for j in range(N-1, -1, -1):
            if arr[row][j] !=0 and arr[row][j] != 4:
                return (row, j)

    elif round in range(3*N, 4*N):
        col = N-1 - round%N

        for i in range(N):
            if arr[i][col] != 0 and arr[i][col] != 4:
                return (i, col)
    return (-1, -1)

def find(r, c):
    result = -1
    for m in range(M):
        if (r,c ) in team[m]:
            for j in range(len(team[m])):
                point = team[m][j]
                if point==(r,c):
                    result = j+1
                    break

            team[m].reverse()
            hr, hc = team[m][0]
            tr, tc = team[m][-1]
            arr[hr][hc] = 1
            arr[tr][tc] = 3

            return result

N, M, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
team = [deque([]) for _ in range(M)]
visited = [[0]*N for _ in range(N)]
answer = 0
dir = (-1, 0), (0, 1), (1, 0), (0, -1)

# 팀 배열 세팅하기
m_idx = 0
for i in range(N):
    for j in range(N):
        if arr[i][j] == 1:
            bfs(i, j, m_idx)
            m_idx+=1

#라운드 진행
for k in range(K):

    #팀 한칸씩 이동
    for m in range(M):
        #꼬리부터 이동
        tr, tc = team[m].pop()
        arr[tr][tc] = 4
        #머리 이동
        hr, hc = team[m][0]
        for di, dj in dir:
            nr, nc = hr+di, hc+dj
            if oob(nr, nc):
                continue
            if arr[nr][nc]==4:
                team[m].appendleft((nr, nc))
                arr[nr][nc] = 1
                arr[hr][hc] = 2
                blank_flag = True
                break
        ntr, ntc = team[m][-1]
        arr[ntr][ntc] = 3

    #이동 체크 완
    r, c = throw_ball(k%(4*N))
    if r!=-1 and c!=-1:
        score = find(r, c)
        answer += score **2


print(answer)