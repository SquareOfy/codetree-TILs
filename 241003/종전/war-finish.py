# 입력받기
N = int(input())
arr = [list(map(int, input().split())) for _ in range(N)]
answer = float("inf")
s = 0
for i in range(N):
    s += sum(arr[i])
# a, b for문으로 정하기 a : 1~N-2, b는 1~ N-1-a
# i, j 는 i는 위로 필요한 공간으로 범위 잡기 (a+b) ~ N
# j는 그냥 다 하고 continue로 거르기
for a in range(1, N):
    for b in range(1, N):
        for i in range(a + b, N):
            for j in range(N):
                if i - a - b < 0: continue
                if j + b >= N: continue
                if j - a < 0: continue
                check = [[0] * N for _ in range(N)]
                population = [0] * 5
                # 대각 체크
                r, c = i, j
                l = b
                line_lst = []  # 아래 위 위 아래
                dir_lst = ((1, 1), (-1, 1), (-1, -1), (1, -1))
                for di, dj in (-1, 1), (-1, -1), (1, -1), (1, 1):
                    lst = [(r, c)]
                    for k in range(l):
                        r += di
                        c += dj
                        check[r][c] = 1
                        lst.append((r, c))
                    l = b if l == a else a
                    line_lst.append(lst)


                for rr in range(i - a - b + 1, i):
                    flag = False
                    for cc in range(j - a, j + b):
                        if check[rr][cc] == 1 and not flag:
                            flag = True
                        elif check[rr][cc] == 0 and flag:
                            check[rr][cc] = 1
                        elif check[rr][cc] == 1 and flag:
                            break

                for k in range(4):
                    lines = line_lst[k]
                    di, dj = dir_lst[k]
                    for rr, cc in lines:
                        du = rr + di
                        while 0 <= du < N:
                            check[du][cc] = k + 2
                            du += di
                        dv = cc + dj
                        while 0 <= dv < N:
                            check[rr][dv] = k + 2
                            dv += dj

                for rr in range(N):
                    for cc in range(N):
                        k = check[rr][cc]
                        population[k - 1] += arr[rr][cc]

                answer = min(max(population) - min(population), answer)
print(answer)