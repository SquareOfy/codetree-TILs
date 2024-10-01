"""
사람, 병원 혹은 빈 칸으로 이루어져 있는 n×n 크기의 도시
각 사람의 병원 거리는 가장 가까운 병원까지의 거리
두 점 사이의 거리 = abs(x1-x2)+abs(y1-y2)

m개의 병원만을 남겨두고 나머지를 폐업
남은 m개의 병원에 대한 각 사람들의 병원 거리의 총 합이 최소
병원 m개를 남겼을 때 가능한 각 사람들의 병원 거리 총 합 중 최솟값

빈 칸인 경우 0,
사람인 경우 1
병원인 경우 2
"""
#dfs 구현하기
def dfs(level, idx):
    global answer
    #종료조건
    if level == M:
        tmp = 0
        #사람으로부터 병원 거리 탐색해서 최솟값의 합 구하기
        for pr, pc in people_lst:
            mn = N*2+1
            for k in range(K):
                if not visited[k]: continue
                hr, hc = hospital_lst[k]
                mn = min(get_dist(pr, pc, hr, hc), mn)
            tmp += mn
        answer = min(answer, tmp)
        #answer 갱신
        return
    #병원 후보들 탐색하며 고르기
    for i in range(idx, K):
        visited[i] = 1
        dfs(level+1, i+1)
        visited[i] = 0

def get_dist(x1, y1, x2, y2):
    return abs(x1-x2)+abs(y1-y2)

#입력 받기
N, M = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]

#사람 lst, 병원 lst 준비하기
hospital_lst = []
people_lst = []
answer = float("inf")

for i in range(N):
    for j in range(N):
        if arr[i][j] == 1:
            people_lst.append((i, j))
        elif arr[i][j] == 2:
            hospital_lst.append((i, j))
K = len(hospital_lst)
visited = [0]*K
#dfs
dfs(0, 0)
print(answer)