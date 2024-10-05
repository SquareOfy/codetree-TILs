# 입력
N, M = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
DIR = (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1)
diagonal = (-1, 1), (-1, -1), (1, 1), (1, -1)
nutrition_lst = [(N - 2, 0), (N - 1, 0), (N - 2, 1), (N - 1, 1)]
visited = [[0] * N for _ in range(N)]

for m in range(M):
    visited = [[0] * N for _ in range(N)]

    # 이동 입력
    d, p = map(int, input().split())
    d -= 1
    di, dj = DIR[d]
    # 영양제 이동!! OOB안하고 모듈!
    # 이동한 위치에서 visited 처리하고, +1, 상하좌우 개수 세서 개수만큼 +
    move_lst = []
    for r, c in nutrition_lst:
        nr, nc = r + di * p, c + dj * p
        nr %= N
        nc %= N
        arr[nr][nc] += 1
        visited[nr][nc] = 1
        move_lst.append((nr, nc))
    new_move_lst = []
    for rr, cc in move_lst:
        cnt = 0
        for ddi, ddj in diagonal:
            du, dv = rr + ddi, cc + ddj
            if du < 0 or dv < 0 or du >= N or dv >= N:
                continue
            if arr[du][dv]>0:
                cnt +=1
        new_move_lst.append((rr, cc, cnt))
    for r, c, value in new_move_lst:
        arr[r][c] += (value)

    # visited 아닌곳, 2이상인 곳을 새로운 영양제로!!
    # 영양제 배열 교체
    nutrition_lst= []
    for i in range(N):
        for j in range(N):
            if visited[i][j] or arr[i][j]<2:
                continue
            arr[i][j]-=2
            nutrition_lst.append((i, j))
answer =0
for i in range(N):
    answer += sum(arr[i])
print(answer)