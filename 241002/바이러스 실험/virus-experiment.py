"""
n * n 격자 무늬의 배지에 바이러스를 배양

초기에 각 칸에 5만큼의 양분  m개의 바이러스
입력으로 주어지는 바이러스의 위치는 모두 서로 다르다고 가정


k 사이클 이후에 살아남은 바이러스의 수

1.
각각의 바이러스는 본인이 속한 1 * 1 크기의 칸에 있는 양분을 섭취
본인의 나이만큼 양분을 섭취
같은 칸에 여러 개의 바이러스가 있을 때에는 나이가 어린 바이러스부터 양분을 섭취
양분을 섭취한 바이러스는 나이가 1 증가
양분이 부족하여 본인의 나이만큼 양분을 섭취할 수 없다면 그 즉시 죽습니다.

2. 모든 바이러스가 섭취를 끝낸 후 죽은 바이러스가 양분으로 변합니다.
죽은 바이러스마다 나이를 2로 나눈 값이 바이러스가 있던 칸에 양분으로 추가

3.  바이러스가 번식을 진행
번식은 5의 배수의 나이를 가진 바이러스에게만 진행
인접한  상하좌우와 대각선 8개의 칸에 나이가 1인 바이러스가 생깁니다.
배지 범위를 벗어난 곳에는 바이러스가 번식하지 않습니다.
주어진 양분의 양에 따라 칸에 양분이 추가됩니다.
"""


#입력받기
N, M, K = map(int, input().split())
plus = [list(map(int, input().split())) for _ in range(N)]
virus_arr = [[[] for _ in range(N)] for _ in range(N)]
arr = [[5]*N for _ in range(5)]
DIR = (-1, -1), (-1, 1), (1, -1), (1, 1), (1, 0), (0, 1), (-1, 0), (0, -1)
for m in range(M):
    r, c, a = map(int, input().split())
    r-=1
    c-=1
    virus_arr[r][c].append(a)

for k in range(K):
    #양분 먹거나 죽거나
    die_lst = []
    for i in range(N):
        for j in range(N):
            if not virus_arr[i][j]: continue
            tmp = []
            for a in virus_arr[i][j]:
                if arr[i][j]-a <0:
                    die_lst.append((i, j, arr[i][j]//2))
                else:
                    arr[i][j] -= a
                    tmp.append(a+1)
            virus_arr[i][j] = tmp[:]

    #양분 뿌리기
    for i, j, v in die_lst:
        arr[i][j] += v


    #바이러스 번식과 양분추가
    for i in range(N):
        for j in range(N):
            for a in virus_arr[i][j]:
                if a%5 == 0:
                    for di, dj in DIR:
                        du, dv = i+di, j+dj
                        if du<0 or dv<0 or du>=N or dv>=N:
                            continue
                        virus_arr[du][dv].append(1)
            arr[i][j] += plus[i][j]


    #바이러스 나이순 정렬
    for i in range(N):
        for j in range(N):
            if not virus_arr[i][j]: continue
            virus_arr[i][j].sort()

    # for i in range(N):
    #     print(arr[i])
    #
    # print(" == ")
    #
    # for i in range(N):
    #     print(virus_arr[i])
    #
    # print()
    # print("=======================")

answer = 0
for i in range(N):
    for j in range(N):
        answer += len(virus_arr[i][j])
print(answer)