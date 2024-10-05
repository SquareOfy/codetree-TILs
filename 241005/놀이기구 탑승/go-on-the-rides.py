def oob(i, j):
    return i<0 or j<0 or i>=N or j>=N
#입력
N = int(input())
arr = [[0]*N for _ in range(N)]
DIR = (-1, 0), (0, 1), (1, 0), (0, -1)
like_arr = [None]*(N*N+1)
for _ in range(N*N):
    num, *like_lst = map(int, input().split())
    like_arr[num] = like_lst
    # print(num, like_lst) ############ 입력 확인
    candi_lst =[]
    for i in range(N):
        for j in range(N):
            if arr[i][j]: continue
            blank_cnt = 0
            like_cnt = 0
            for di, dj in DIR:
                du, dv = i+di, j+dj
                if oob(du, dv): continue
                if arr[du][dv] ==0:
                    blank_cnt+=1
                elif arr[du][dv] in like_lst:
                    like_cnt+=1
            candi_lst.append((like_cnt, blank_cnt, i, j))
    candi_lst.sort(key=lambda x: (-x[0], -x[1], x[2], x[3]))

    r, c = candi_lst[0][2], candi_lst[0][3]
    arr[r][c] = num

answer = 0

for i in range(N):
    for j in range(N):
        cnt = 0
        num = arr[i][j]
        for di, dj in DIR:
            du, dv = i+di, j+dj
            if oob(du, dv): continue
            if arr[du][dv] in like_arr[num]:
                cnt+=1
        answer += int(10**(cnt-1))
print(answer)