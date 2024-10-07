"""
좌상단은 (1,1)

벽
    1이상 9이하의 내구도
    회전할 때, 내구도가 1씩 깎입니다.
    내구도가 0이 되면, 빈 칸으로 변경

출구
    참가자가 해당 칸에 도달하면, 즉시 탈출


모든 참가자가 이동을 끝냈으면, 다음 조건에 의해 미로가 회전
    한 명 이상의 참가자와 출구를 포함한 가장 작은 정사각형 회전
    가장 작은 크기를 갖는 정사각형이 2개 이상이라면,
        좌상단 r 좌표가 작은 것이 우선
        그래도 같으면 c 좌표가 작은 것이 우선
    선택된 정사각형은 시계방향으로 90도 회전
        회전된 벽은 내구도가 1씩 깎입니다.
"""
def oob(i, j):
    return i<0 or j<0 or i>=N or j>=N
def change(i):
    return int(i)-1

def get_square(i, j, er, ec):
    h = abs(i-er)+1
    w = abs(j-ec)+1
    l = max(h, w)
    sr = max(max(i, er)-l+1, 0)
    sc = max(max(j, ec)-l+1, 0)
    return l, sr, sc

def get_rotate_loc(sr, sc, l, x, y):
    tr = x-sr
    tc = y-sc
    return sr+tc, sc+(l-1-tr)
def get_dist(i, j, x, y):
    return abs(i-x) + abs(j-y)
def printa(string, arr):
    print(f"============{string}===============")
    for i in range(len(arr)):
        print(arr[i])
    print("===================================")
    print()

N, M, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
runner_arr = [[[] for _ in range(N)] for _ in range(N)]
finished_lst = [0]*(M+1)
runner_info = [-1]
for m in range(1, M+1):
    x, y = map(change, input().split())
    runner_info.append((x, y))
er, ec = map(change, input().split())
answer = 0




for k in range(K):
    #m명 이동
    for n in range(1, M+1):
        if finished_lst[n]:
            continue
        #이동할 칸 구하기
        i, j = runner_info[n]
        origin = get_dist(i, j, er, ec)
        for di, dj in (-1, 0), (1, 0), (0, -1), (0, 1):
            du, dv = i+di, j+dj
            if oob(du, dv) or arr[du][dv] !=0:
                continue
            dist = get_dist(du, dv, er, ec)
            if origin<=dist:
                continue
            answer+=1
            if du==er and dv==ec:
                runner_info[n] = -1
                finished_lst[n] = 1
            else:
                runner_info[n] = (du, dv)
            break

    if sum(finished_lst[1:]) == M:
        break
    #사각형 찾아 !!
    mn_l = N
    sr, sc = N, N
    for m in range(1, M+1):
        if finished_lst[m]: continue
        i, j = runner_info[m]
        tl, tsr, tsc = get_square(i, j, er, ec)
        if mn_l>tl:
            mn_l = tl
            sr, sc = tsr, tsc
        elif mn_l == tl and (sr, sc)>(tsr, tsc):
            sr, sc = tsr, tsc

    tmp = [[0]*mn_l for _ in range(mn_l)]

    # 시계방향 90도 회전해
    for r in range(mn_l):
        tmp[r] = arr[sr+r][sc:sc+mn_l]
    tmp = list(map(list, zip(*tmp[::-1])))
    #내구도 감소 후 다시 붙이기
    for r in range(mn_l):
        for c in range(mn_l):
            if tmp[r][c] >0:
                tmp[r][c] -= 1
        arr[sr+r][sc:sc+mn_l] = tmp[r][:]

    #사람 좌표 회전
    for m in range(1, M+1):
        if finished_lst[m]: continue
        x, y = runner_info[m]
        if x not in range(sr, sr+mn_l) or y not in range(sc, sc+mn_l):
            continue
        nx, ny = get_rotate_loc(sr, sc, mn_l, x, y)
        runner_info[m] = (nx, ny)
    er, ec = get_rotate_loc(sr, sc, mn_l, er, ec)

print(answer)
print(er+1, ec+1)