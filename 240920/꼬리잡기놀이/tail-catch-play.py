"""

1.  먼저 각 팀은 머리사람을 따라서 한 칸 이동합니다.

2. 각 라운드마다 공이 정해진 선을 따라 던져집니다.
    1   ~  n   round : 행 by 행 오른쪽 방향 (열 : 0 ~ n-1)
    n+1 ~  2n  round : 열 by 열 위쪽 방향   (행 : n-1 ~ 0)
    2n+1 ~ 3n  round : 행 by 행 왼쪽 방향   (열 : n-1 ~ 0)
    3n+1 ~ 4n  round : 열 by 열 아래쪽 방향  (행 : 0 ~ n-1)

3. 공이 던져지는 라인에 사람 있으면 최초의 사람 팀만 점수 얻기(1명만)
    그 사람이 팀에서 k번째 사람이면 k**2 점수 획득
    그 팀 방향 바꾸기 ( 방향 반대, 머리사람 꼬리사람 change)



team = deque m 개 가진 리스트

1. 팀 찾아서 배열로 만들기?
m_idx = 0
    for i in range(N):
        for j in range(N):
            if arr[i][j]==1: #머리 !!
                team[m].append((i, j)
                bfs! visited 해가면서 1, 2, 3 중에 찾고 3이면 끝내기

2. 이동
    team의 m개의 deque에서 아래 수행
    머리위치에서 사방탐색해서 4 찾기 그 위치가 새로운 머리위치 (r, c)
    새로운 머리 위치 appendleft((r,c))
    pop()하고 그 자리 사로 만들기
    1~끝 -1 까지 arr[i][j] = 2로 만들고 끝은 3으로 만들기

3. round 돌리기
    throw 함수 : round 매개변수 (4N모듈 해야함)

    if 문으로 round 동작 설계
    (0, N)이면
        row = round
        for j in range(0, N):
            사람 찾으면 점수 계산 후 break

    (N, 2N)이면
        col = round%N
        for i in range(N-1, -1, -1)

    (2N, 3N)
        row = N-1 - round%N
        for j in range(N-1, -1, -1)

    (3N, 4N)
        col = N-1 - round%N
        for i in range(0, N)

"""

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

# for i in range(M):
#     print(team[i])
#########################완료

#라운드 진행
for k in range(K):

    #팀 한칸씩 이동
    for m in range(M):
        hr, hc = team[m][0]
        #머리 이동

        blank_flag = False
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
        if blank_flag:
            tr, tc = team[m].pop()
            arr[tr][tc] = 4

        #꼬리로 이동해야 한다
        else:
            for di, dj in dir:
                nr, nc = hr + di, hc + dj
                if oob(nr, nc):
                    continue
                if arr[nr][nc] == 3:
                    team[m].appendleft((nr, nc))
                    arr[nr][nc] = 1
                    arr[hr][hc] = 2
                    break
            team[m].pop() #꼬리 자리에 머리 자리가 왔으므로 arr은 안바꿈


        ntr, ntc = team[m][-1]
        arr[ntr][ntc] = 3 #이 풀이라면 굳이 필요없을 것 같긴 함

    #이동 체크 완
    # for i in range(M):
    #     print(team[i])
    ##########################완료
    # print(f"================이동 후 arr {k+1}===================")
    # for i in range(N):
    #     print(arr[i])
    # print()
    # print("=============================================")
    r, c = throw_ball(k%(4*N))
    # print("맞은 사람 위치 : " , r, c)
    # print("============team ============")
    if r!=-1 and c!=-1:
        score = find(r, c)
        answer += score **2


print(answer)