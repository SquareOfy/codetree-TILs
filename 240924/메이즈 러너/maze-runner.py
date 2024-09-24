from collections import deque
def control_idx(i):
    return int(i)-1

def oob(i, j):
    return i<0 or j<0 or i>=N or j>=N




# def bfs(r, c):
#     q = deque([(r, c, 1, -1, -1)])
#     visited = [[N*N]*N for _ in range(N)]
#     visited[r][c] = 1
#     min_dist = N*N+1
#     while q:
#         cr, cc, rank, one_r, one_c = q.popleft()
#         if cr==er and cc==ec:
#             if rank <= min_dist:
#                 min_dist = rank
#                 if arr[one_r][one_c]==0 :
#                     return one_r, one_c
#             continue
#         for di, dj in (-1, 0), (1, 0), (0, -1), (0, 1):
#             du = cr+di
#             dv = cc+dj
#             if oob(du, dv) or visited[du][dv] < rank:
#                 continue
#
#             visited[du][dv] = rank
#
#             if rank==1:
#                 q.append((du, dv, rank+1, du, dv))
#             else:
#                 q.append((du, dv, rank+1, one_r, one_c))
#
#     return -1, -1

def find_sr_sc():
    result_r, result_c = N, N
    for pr, pc in p_lst:
        if abs(er-pr)==dist:
            sr = min(er, pr)
        else:
            if max(er, pr)-dist+1>=0:
                sr = max(er, pr)-dist+1
            else:
                sr = 0
        if abs(ec-pc)==dist:
            sc = min(ec, pc)
        else:
            if max(ec, pc)-dist+1>=0:
                sc = max(ec, pc)-dist+1
            else:
                sc = 0
        if sr<result_r:
            result_r=sr
            result_c=sc
        elif sr==result_r and sc<result_c:
            result_r = sr
            result_c = sc
    return result_r, result_c

def rotate(r, c, dist):
    return c, dist-1-r


# 미로는 N×N 크기의 격자  좌상단은 (1,1)
# 벽
    # 참가자가 이동할 수 없는 칸입니다.
    # 1이상 9이하의 내구도를 갖고 있습니다.
    # 회전할 때, 내구도가 1씩 깎입니다.
    # 내구도가 0이 되면, 빈 칸으로 변경됩니다.
N, M, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
people = [list(map(control_idx, input().split())) for _ in range(M)]
er, ec = map(control_idx, input().split())
cnt = M
answer = 0
# for i in range(N):
#     print(arr[i])

# K초 동안 위의 과정을 계속 반복됩니다.


for k in range(1, K+1):

    # 1. 움직임
    # 1초마다 모든 참가자는 한 칸씩 움직임
    # 모든 참가자는 동시에 움직입니다.
    # 상하좌우로 움직일 수 있으며, 벽이 없는 곳으로 이동할 수 있습니다.
    # 움직인 칸은 현재 머물러 있던 칸보다 출구까지의 최단 거리가 가까워야 합니다.
    # 움직일 수 있는 칸이 2개 이상이라면, 상하로 움직이는 것을 우선시합니다.
    # 참가가가 움직일 수 없는 상황이라면, 움직이지 않습니다.
    # 한 칸에 2명 이상의 참가자가 있을 수 있습니다.
    for i in range(M):
        r, c = people[i]
        if r==-1: continue
        nr, nc = r, c
        if er<r and arr[r-1][c]==0:
            nr = r-1
        elif er>r and arr[r+1][c] == 0:
            nr = r+1
        elif ec<c and arr[r][c-1]==0:
            nc = c-1
        elif ec>c and arr[r][c+1]==0:
            nc = c+1
        if nr==r and nc==c:
            continue
        answer+=1
        if nr == er and nc == ec:
            cnt-=1
            people[i] = [-1, -1]
        else:
            people[i] = [nr, nc]
    # 만약 K초 전에 모든 참가자가 탈출에 성공한다면, 게임이 끝납니다.
    #움직이고 나서 사람 수 체크 후 break
    if cnt == 0:
        break

    # 2. 미로회전
        # 한 명 이상의 참가자와 출구를 포함한 가장 작은 정사각형
        # 가장 작은 크기를 갖는 정사각형이 2개 이상이라면,
        # 좌상단 r 좌표가 작은 것이 우선되고, 그래도 같으면 c 좌표가 작은 것이 우선됩니다.
        # 선택된 정사각형은 시계방향으로 90도 회전하며, 회전된 벽은 내구도가 1씩 깎입니다.

    dist = 2*N
    p_lst = []
    for m in range(M):
        r, c = people[m]
        if r==-1: continue
        tmp = max(abs(er-r), abs(ec-c))+1 #이 사람과 정사각형을 만들 때 한변의 길이 사람이 M명이니까 그 중 최소인 걸 찾아야하고
        if tmp<dist: #최소 갱신!!
            p_lst = [(r, c)]
            dist = tmp
        elif tmp==dist:
            p_lst.append((r, c))

    sr, sc = find_sr_sc()


    #정사각형 회전
    tmp = [[] for _ in range(dist)]
    for i in range(dist):
        tmp[i] = arr[sr+i][sc:sc+dist]
    for i in range(dist):
        for j in range(dist):
            if tmp[i][j]>0:
                tmp[i][j] -=1

    tmp = list(map(list, zip(*tmp[::-1])))
    for i in range(dist):
        arr[sr+i][sc:sc+dist] = tmp[i][:]


    er_tmp = er-sr
    ec_tmp = ec-sc
    er_tmp, ec_tmp = rotate(er_tmp, ec_tmp, dist)
    er, ec = er_tmp+sr, ec_tmp+sc
    #출구좌표 회전


    #저 안에 들어있는 사람 회전
    for i in range(M):
        r, c = people[i]
        if r==-1: continue
        if r in range(sr, sr+dist) and c in range(sc, sc+dist):
            tmp_r, tmp_c = rotate(r-sr, c-sc, dist)
            r, c = tmp_r+sr, tmp_c+sc
            people[i] = [r, c]
    # print('============회전 후 출구 =============')
    # print(er, ec)
    # print('===================================')
    #
    # print('============회전 후 사람 =============')
    # print(people)
    # print('===================================')
    # print()

print(answer)
print(er+1, ec+1)