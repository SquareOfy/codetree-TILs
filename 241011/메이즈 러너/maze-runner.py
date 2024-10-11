"""
20분
최단거리는 ∣x1−x2∣+∣y1−y2∣로 정의

1. 참가자 이동
    1초마다 모든 참가자는 한 칸씩 움직입니다.
    동시에
    상하좌우
    벽이 없는 곳으로 이동할 수 있습니다.
    움직인 칸은 현재 머물러 있던 칸보다 출구까지의 최단 거리가 가까워야 합니다.
    움직일 수 있는 칸이 2개 이상이라면, 상하로 움직이는 것을 우선시
    참가가가 움직일 수 없는 상황이라면, 움직이지 않습니다.
    한 칸에 2명 이상의 참가자가 있을 수 있습니다.

2. 미로 회전
    한 명 이상의 참가자와 출구를 포함한 가장 작은 정사각형
    정사각형이 2개 이상이라면, 좌상단 r 좌표가 작은 것 ->  c 좌표가 작은 것이 우선
    시계방향으로 90도 회전
    회전된 벽은 내구도가 1씩 깎입니다.

게임종료
        K초 지나거나
        K초 전에 모든 참가자가 탈출에 성공한다면, 게임이 끝납니다.
출력
    모든 참가자들의 이동 거리 합과 출구 좌표를 출력
"""


def oob(i, j):
    return i < 0 or j < 0 or i >= N or j >= N


def cal_dist(i, j, x, y):
    return abs(i - x) + abs(j - y)

def find_square():
    mn_l = N + 1
    mn_r, mn_c = N, N

    for m in range(M):
        if out_lst[m]: continue
        x, y = runner_info[m]
        l = max(abs(E_r - x), abs(E_c - y))+1
        tmp_r = max(max(E_r, x) - l+1, 0)
        tmp_c = max(max(E_c, y) - l+1, 0)
        if l < mn_l or (l == mn_l and (mn_r, mn_c) > (tmp_r, tmp_c)):
            mn_l = l
            mn_r, mn_c = tmp_r, tmp_c
    return mn_l, mn_r, mn_c

def rotate_point(r, c, sr, sc, l):
    tr, tc = r-sr, c-sc
    tr, tc = tc, l-1-tr

    return tr+sr, tc+sc

N, M, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
runner_info = []
out_lst = [0] * M
DIR = (-1, 0), (1, 0), (0, -1), (0, 1)
for m in range(M):
    x, y = map(lambda x: int(x) - 1, input().split())
    runner_info.append((x, y))

E_r, E_c = map(lambda x: int(x) - 1, input().split())

answer = 0
for k in range(K):
    # 참가자 이동
    for m in range(M):
        if out_lst[m]: continue
        x, y = runner_info[m]
        origin = cal_dist(x, y, E_r, E_c)
        for di, dj in DIR:
            du, dv = x + di, y + dj
            if oob(du, dv): continue
            dist = cal_dist(du, dv, E_r, E_c)
            if origin <= dist: continue
            if arr[du][dv] != 0:
                continue
            runner_info[m] = (du, dv)
            answer += 1
            if du==E_r and dv==E_c:
                out_lst[m] = 1
            break
    if sum(out_lst) == M:
        break

    # 미로 회전 정사각형 시작 좌표, 길이 잡기
    l, sr, sc = find_square()
    # 미로 회전하기
    tmp = [[] for _ in range(l)]
    for i in range(l):
        tmp[i] = arr[sr+i][sc:sc+l]
    tmp = list(map(list, zip(*tmp[::-1])))
    for i in range(l):
        for j in range(l):
            if tmp[i][j] > 0:
                tmp[i][j] -= 1

    for i in range(l):
        arr[sr+i][sc:sc+l] = tmp[i][:]

    # 사람 위치 바꾸기, 출구 좌표 바꾸기
    E_r, E_c = rotate_point(E_r, E_c, sr, sc, l)
    for m in range(M):
        if out_lst[m]: continue
        x, y = runner_info[m]
        if x in range(sr, sr+l) and y in range(sc, sc+l):
            nx, ny = rotate_point(x, y, sr, sc, l)
            runner_info[m] = (nx, ny)

print(answer)
print(E_r+1, E_c+1)