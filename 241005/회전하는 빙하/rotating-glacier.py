from collections import deque
def rotate_(L, flag):
    rotate_tmp = [[0]*N for _ in range(N)]
    #큰 사각형 회전
    for i in range(0, N, L):
        for j in range(0, N, L):
            tmp = [[0]*L for _ in range(L)]
            for k in range(L):
                tmp[k] = arr[i+k][j:j+L]
            if flag:
                tmp = list(map(list, zip(*tmp[::-1])))
            else:
                tmp = list(map(list, zip(*tmp)))[::-1]

            for k in range(L):
                rotate_tmp[i+k][j:j+L] = tmp[k][:]
    return rotate_tmp


def oob(i, j):
    return i<0 or j<0 or i>=N or j>=N

def bfs(i, j):
    visited[i][j] = 1
    q = deque([(i, j)])
    size = 0

    while q:
        cr, cc = q.popleft()
        size+=1
        for di, dj in DIR:
            du, dv = cr+di, cc+dj
            if oob(du, dv) or arr[du][dv] ==0 or visited[du][dv]:
                continue
            q.append((du, dv))
            visited[du][dv] =1
    return size
n, Q = map(int, input().split())
N = 2**n
#배열 받기
arr = [list(map(int, input().split())) for _ in range(N)]
order_lst = list(map(int, input().split()))
DIR = (-1, 0), (0, 1), (1, 0), (0, -1)
ice = [[0] * N for _ in range(N)]

for q in order_lst:
    if q!=0:
        L = 2**q
        arr = rotate_(L, 1)
        #부분 사각형 반시계 회전
        arr = rotate_(L//2, 0)

  #############################부분체크
    # for i in range(N):
    #     print(arr[i])
    # print()
    ############################
    for i in range(N):
        for j in range(N):
            if arr[i][j]==0: continue
            cnt = 0
            #상하좌우 인접 빙하 개수 체크
            for di, dj in DIR:
                du, dv = i+di, j+dj
                if oob(du, dv): continue
                if arr[du][dv] ==0: continue
                cnt+=1
                if cnt==3:
                    break
            if cnt<3:
                ice[i][j] -=1
    for i in range(N):
        for j in range(N):
            arr[i][j] += ice[i][j]
            ice[i][j] = 0



mx_size = 0
ice_sum = 0
visited = [[0]*N for _ in range(N)]

for i in range(N):
    for j in range(N):
        ice_sum += arr[i][j]
        if arr[i][j]>0 and not visited[i][j]:
            mx_size = max(mx_size, bfs(i, j))

print(ice_sum)
print(mx_size)