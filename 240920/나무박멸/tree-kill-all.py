"""

1. 인접한 네 개의 칸 중 나무가 있는 칸의 수만큼 나무가 성장합니다. 성장은 모든 나무에게 동시에 일어납니다.
2. 기존에 있었던 나무들은 인접한 4개의 칸 중 벽, 다른 나무, 제초제 모두 없는 칸에 번식을 진행
    나무 그루 수 // 상하좌우 중 빈칸의 수(벽, 나무, 제초제 x) 만큼
    "동시에!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

3. 나무가 가장 많이 박멸되는 칸에 제초제를 뿌립니다
    나무가 없는 칸에 제초제를 뿌리면 박멸되는 나무가 전혀 없는 상태로 끝이 나지만,
    나무가 있는 칸에 제초제를 뿌리게 되면 4개의 대각선 방향으로 k칸만큼 전파
    단 전파되는 도중 벽이 있거나 나무가 아얘 없는 칸이 있는 경우, 그 칸 까지는 제초제가 뿌려지고
    그 이후의 칸으로는 제초제가 전파되지 않습니다.

     여기서 그 칸까지는 뿌려지는게 포인트1!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
     제초제가 뿌려진 칸에는 c년만큼 제초제가 남아있다가
     c+1년째가 될 때 사라지게 됩니다.
     제초제가 뿌려진 곳에 다시 제초제가 뿌려지는 경우에는 새로 뿌려진 해로부터 다시 c년동안 제초제가 유지됩니다.

     제초제 빼는 타이밍 주의 !!!!!!!!!!!!!!!!!!!!!!!!!!!!1
"""
def oob(r, c):
    return r<0 or c<0 or r>=N or c>=N

def print_arr():
    for i in range(N):
        print(arr[i])
    print()

#입력 받기
N, M, K, C = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
visited = [[0]*N for _ in range(N)]
dir = (-1, 0), (0, 1), (1, 0), (0, -1)
diagonal = (-1, -1), (-1, 1), (1, -1), (1, 1)
answer = 0

# M년 반복
for m in range(M):

    #성장
    # 상하좌우 보고 나무 있는 칸 수 세서 그만큼 더하기
    for i in range(N):
        for j in range(N):
            if arr[i][j]>0 and not visited[i][j]:
                cnt = 0
                for di, dj in dir:
                    du, dv = i+di, j+dj
                    if oob(du, dv): continue
                    if arr[du][dv]>0:
                        cnt+=1
                arr[i][j] += cnt
    # print_arr()
    ##############체크 완


    #번식
    # 리스트 만들어서 번식할 목록 넣어놓고 한번에 반영할 것
    # 제초제, 벽, 나무 없는지 확인하고 얘네 없는 칸에 그 칸 수 만큼 나눈 나무 더하기
    spread_lst = []
    for i in range(N):
        for j in range(N):
            if arr[i][j]>0:
                cnt =0
                lst = []

                for di, dj in dir:
                    du, dv = i+di, j+dj
                    if oob(du, dv): continue
                    if visited[du][dv]: continue #제초제 없고
                    if arr[du][dv] ==0: #나무 없는 칸(벽도 아니고 나무도 있는 것도 아님)
                        cnt += 1
                        lst.append((du, dv))
                if cnt ==0:
                    continue
                tree_cnt = arr[i][j] // cnt
                spread_lst.append((tree_cnt, lst))
    for tree_cnt, lst in spread_lst:
        for i, j in lst:
            arr[i][j]+= tree_cnt

    # print("=============번식확인=================")
    # print_arr()
    ############################확인 완

    kill_lst = []
    #제초제 뿌릴 후보 찾자
    for i in range(N):
        for j in range(N):
            lst = []
            kill_cnt = arr[i][j] if arr[i][j] >0 else 0 #나무 있는 칸이면 나무개수 아니면 0
            lst.append((i, j))
            if arr[i][j] <=0:
                kill_lst.append((kill_cnt, i, j, lst))
                continue
            for di, dj in diagonal:
                du, dv = i, j
                #대각선 방향으로 k칸만큼 간다
                for k in range(K):
                    du += di
                    dv += dj
                    if oob(du, dv): continue
                    if arr[du][dv] !=-1 and arr[du][dv] !=0: #나무가 있는 칸이면
                        kill_cnt += arr[du][dv]
                    lst.append((du, dv))
                    if arr[du][dv]==-1 or arr[du][dv]==0:#벽이거나 나무가 없으면 이 칸까지만 하고 끝
                        break
            kill_lst.append((kill_cnt, i, j, lst))

    kill_lst.sort(key=lambda x:(-x[0], x[1], x[2]))
    # print("=========================제초제 후보 ==========================")
    # for t in kill_lst:
    #     print(t)
    # print("========================================================")

    # 제초제 감소
    for i in range(N):
        for j in range(N):
            if visited[i][j]:
                visited[i][j]-= 1


    # 제초제 뿌리기 : C로 갱신하기 위해 감소부터 해준다
    for i, j in kill_lst[0][3]:
        visited[i][j] = C
        arr[i][j] = 0

    answer += kill_lst[0][0]

print(answer)