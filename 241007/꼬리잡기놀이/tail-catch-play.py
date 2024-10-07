"""
각 팀의 이동 선은 끝이 이어져있습니다.
각 팀의 이동 선은 서로 겹치지 않습니다.

1. 머리 사람을 따라서 한칸 이동
    - 머리 꼬리 붙어있는 경우에 대비하여
        꼬리 먼저 이동하기
    - 머리는 사방 중 경로인 곳 따라 가기

2. 라운드마다 공  선따라 던지기
    - 선 순서 주의
    4n번째 라운드를 넘어가는 경우에는
    다시 1번째 라운드의 방향으로 돌아갑니다.

3. 공이 던져지는 경우에 해당 선에 사람이 있으면 최초에
    만나게 되는 사람만이 공을 얻게 되어 점수를 얻게 됩니다.
    점수는 해당 사람이 머리사람을 시작으로 팀 내에서 k번째 사람이라면
    k의 제곱만큼 점수를 얻게 됩니다.
    아무도 공을 받지 못하는 경우에는 아무 점수도 획득하지 못합니다

    공을 획득한 팀의 경우에는 머리사람과 꼬리사람이 바뀝니다.
    즉 방향을 바꾸게 됩니다.
    => 머리랑 꼬리 위치만 바꾸기 !!

출력
k번의 라운드 동안 각 팀이 얻게되는 점수의 총합


"""
from collections import deque

def printa(string, arr):
    print(f"==============={string}=================")
    for i in range(len(arr)):
        print(arr[i])
    print("=========================================")
    print()
def oob(i, j):
    return i < 0 or j < 0 or i >= N or j >= N


# 꼬리라인 찾고 visited에 팀 번호 세팅
def bfs(i, j):
    q = deque([(i, j)])
    visited[i][j] = team_cnt
    lst = []
    while q:
        cr, cc = q.popleft()
        if arr[cr][cc] != 4: lst.append((cr, cc))

        for di, dj in DIR:
            du, dv = cr + di, cc + dj
            if oob(du, dv): continue
            if visited[du][dv]: continue
            if arr[du][dv] == 0: continue
            if arr[du][dv] != 4 and abs(arr[du][dv] - arr[cr][cc]) >= 2: continue
            visited[du][dv] = team_cnt
            q.append((du, dv))
    return lst


# 라운드따라 탐색을 시작할 r, c, 방향벡터 반환하는 함수
def get_round_idx(k):
    dd = k % (4 * N) //N
    if dd == 0:
        rr = k % (4 * N) % N
        cc = 0
    elif dd == 1:
        rr = N - 1
        cc = k % (4 * N) % N
    elif dd == 2:
        rr = N - 1 - (k % (4 * N) % N)
        cc = N - 1

    else:
        rr = 0
        cc = N - 1 - (k % (4 * N) % N)

    return rr, cc, dd

# 입력
N, M, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
visited = [[0] * N for _ in range(N)]
team = [-1]
team_cnt = 0
answer = 0
DIR = (0, 1), (-1, 0), (0, -1), (1, 0)

# 배열 준비 team_arr 세팅, visited 세팅
for i in range(N):
    for j in range(N):
        if arr[i][j] == 1:
            team_cnt += 1
            team_lst = bfs(i, j)
            team.append(deque(team_lst))
# print(team)
# for ii in range(N):
#     print(visited[ii])


# 라운드 돌리기
for k in range(K):

    # 팀별로 칸 이동
    for t in range(1, M + 1):

        # 꼬리 먼저 이동
        tr, tc = team[t].pop()
        arr[tr][tc] = 4
        ntr, ntc = team[t][-1]
        arr[ntr][ntc] = 3

        # 머리에서 4 찾아 늘리기
        hr, hc = team[t][0]
        for di, dj in DIR:
            du, dv = hr + di, hc + dj
            if oob(du, dv): continue
            if arr[du][dv] == 4:
                team[t].appendleft((du, dv))
                arr[hr][hc] = 2
                arr[du][dv] = 1
                break
    # printa("팀 이동 완료 ", arr)

    # printa("팀 정보 ", team)
    # 라운드 진행
    r, c, d = get_round_idx(k)
    # print("r, c, d :" , r, c, d)
    di, dj = DIR[d]
    for s in range(N):
        dr, dc = r+di*s, c+dj*s
        if 0< arr[dr][dc] < 4:
            # print("dr, dc  : ", dr, dc)
            team_num = visited[dr][dc]
            # print("잡힌 팀!!! : ", team_num)
            point = team[team_num].index((dr, dc))+1
            # print("point : ", point)
            answer += point **2
            # 점수 얻으면 그 팀 뒤집기
            team[team_num].reverse()
            hr, hc = team[team_num][0]
            tr, tc = team[team_num][-1]
            arr[hr][hc] = 1
            arr[tr][tc] = 3

            break
    # printa("라운드 진행 완료 ", arr)
    # printa("라운드 진행 후 팀", team)
print(answer)