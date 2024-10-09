"""


1. 인접한 네 개의 칸 중 나무가 있는 칸의 수만큼 나무가 성장

2. 기존에 있었던 나무들은 인접한 4개의 칸 중 벽, 다른 나무, 제초제 모두 없는 칸에 번식을 진행
     각 칸의 나무 그루 수에서 총 번식이 가능한 칸의 개수만큼 나누어진 그루 수만큼 번식
     번식의 과정은 모든 나무에서 동시에 일어나게 됩니다.


3.각 칸 중 제초제를 뿌렸을 때 나무가 가장 많이 박멸되는 칸에 제초제를 뿌립니다
    박멸되는 나무 수 같으면 행이 작은 순서대로 / 그것도 같으면 열이 작은 칸에

    나무가 없는 칸에 제초제를 뿌리면 박멸되는 나무가 전혀 없는 상태로 끝
    나무가 있는 칸에 제초제를 뿌리게 되면 4개의 대각선 방향으로 k칸만큼 전파
        전파되는 도중 벽이 있거나 나무가 아얘 없는 칸이 있는 경우,
        그 칸 까지는 제초제가 뿌려지며 그 이후의 칸으로는 제초제가 전파되지 않습니다.
    제초제가 뿌려진 칸에는 c년만큼 제초제가 남아있다가 c+1년째가 될 때 사라지게 됩니다.
    제초제가 뿌려진 곳에 다시 제초제가 뿌려지는 경우에는 새로 뿌려진 해로부터 다시 c년동안 제초제가 유지

"""


def oob(i, j):
    return i < 0 or j < 0 or i >= N or j >= N

def printa(string, arr):
    print(f"==============={string}=====================")
    for i in range(len(arr)):
        print(arr[i])
    print("===============================================")
    print()

N, M, K, C = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
killed_arr = [[0] * N for _ in range(N)]
answer = 0
DIR = (-1, 0), (0, 1), (1, 0), (0, -1)
diagonal = (1, 1), (1, -1), (-1, 1), (-1, -1)

for m in range(1, M + 1):

    # 나무 성장
    for i in range(N):
        for j in range(N):
            if arr[i][j] > 0:
                cnt = 0
                for di, dj in DIR:
                    du, dv = i + di, j + dj
                    if oob(du, dv): continue
                    if arr[du][dv] > 0:
                        cnt += 1
                arr[i][j] += cnt
    # printa("나무 성장 후 ", arr)
    # 나무 번식
    tmp = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if arr[i][j] <= 0: continue
            lst = []
            for di, dj in DIR:
                du, dv = i + di, j + dj
                if oob(du, dv): continue
                if arr[du][dv] == 0 and (killed_arr[du][dv] == 0):
                    lst.append((du, dv))
            if not lst: continue
            v = arr[i][j] // len(lst)
            for r, c in lst:
                tmp[r][c] += v

    for i in range(N):
        for j in range(N):
            arr[i][j]+= tmp[i][j]

    # printa("나무 번식 후 ", arr)
    killed_cnt = -1
    spray_R, spray_C = -1, -1
    lst = []
    # 제초제 뿌릴 위치 찾기
    for i in range(N):
        for j in range(N):
            if arr[i][j] <0: continue  # 벽
            # if killed_arr[i][j] != 0 and m - killed_arr[i][j] <= C: continue  # 제초제
            cnt = arr[i][j]
            tmp_lst = [(i, j)]
            if cnt!=0:
                for di, dj in diagonal:
                    du, dv = i, j
                    for k in range(K):
                        du+=di
                        dv+=dj
                        if oob(du, dv):
                            break
                        if arr[du][dv] > 0: cnt += arr[du][dv]
                        tmp_lst.append((du, dv))

                        if arr[du][dv] <= 0:
                            break
            # print("====================")
            # print("i , j : ", i, j)
            # print('죽이는 나무 수 : ', cnt)
            # print(tmp_lst)
            # print("=======================")
            if cnt > killed_cnt:
                killed_cnt = cnt
                lst = tmp_lst[:]
                spray_R = i
                spray_C = j

    for i in range(N):
        for j in range(N):
            if killed_arr[i][j]:
                killed_arr[i][j]-=1
    # 정해진 위치에 제초제 뿌리기
    for r, c in lst:
        if arr[r][c] > 0: arr[r][c] = 0
        killed_arr[r][c] = C
    answer += killed_cnt
    # printa("제초제 뿌린 후 ", killed_arr)
    # printa("제초제 뿌린 후 나무 ", arr)
print(answer)