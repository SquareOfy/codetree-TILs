"""
 좌상단은 (1,1)
거리 : (r1-r2)**2 + (c1-c2)**2
루돌프가 한 번 움직인 뒤,
1번 산타부터 P번 산타까지 순서대로 움직이게 됩니다

1. 루돌프 이동
    루돌프는 게임에서 탈락하지 않은 산타 중  가장 가까운 산타를 향해 1칸 돌진
    r 좌표가 큰 산타를 향해 돌진
    c 좌표가 큰 산타를 향해 돌진
    루돌프는 상하좌우, 대각선을 포함한 인접한 8방향 중 하나로 돌진
    산타와 루돌프가 같은 칸에 있게 되면 충돌이 발생
    루돌프가 움직여서 충돌이 일어난 경우, 해당 산타는 C만큼의 점수를 얻게 됩니다.
    산타는 루돌프가 이동해온 방향으로 C 칸 만큼 밀려나게 됩니다.
    밀려나는 것은 이동하는 도중에 충돌이 일어나지는 않고  원하는 위치에 도달
    밀려난 위치가 게임판 밖이라면 산타는 게임에서 탈락
    밀려난 칸에 다른 산타가 있는 경우 상호작용이 발생
        충돌 후 착지하게 되는 칸에 다른 산타가 있다면 그 산타는 1칸 해당 방향으로 밀려나게 됩니다.
          그 옆에 산타가 있다면 연쇄적으로 1칸씩 밀려나는 것을 반복
          게임판 밖으로 밀려나오게 된 산타의 경우 게임에서 탈락
2. 산타
    기절해있거나 격자 밖으로 빠져나가 게임에서 탈락한 산타들은 움직일 수 없습니다.
    상하좌우로 인접한 4방향 중 한 곳으로 움직일 수 있습니다.
    루돌프에게 거리가 가장 가까워지는 방향으로 1칸 이동
    가장 가까워질 수 있는 방향이 여러 개라면, 상우하좌 우선순위에 맞춰 움직입니다.
    움직일 수 있는 칸이 없다면 산타는 움직이지 않습니다.


"""
from collections import deque
def change(i):
    return int(i)-1

def oob(i, j):
    return i<0 or j<0 or i>=N or j>=N

def get_dist(r1, c1, r2, c2):
    return (r1-r2)**2 + (c1-c2)**2

#충돌함수
def crush(step, di, dj, m):
    r, c = santa_info[m]
    nr, nc = r+di*step, c+dj*step
    score_lst[m] += step
    if oob(nr, nc):
        die_lst[m] = 1
        santa_arr[r][c] = 0
        return
    if santa_arr[nr][nc]:
        interact(santa_arr[nr][nc], di, dj)

    santa_arr[nr][nc] = m
    santa_arr[r][c] = 0
    santa_info[m]= (nr, nc)

#연쇄작용 함수
def interact(m, di, dj):
    r, c = santa_info[m]
    nr, nc = r+di, c+dj
    if oob(nr, nc):
        die_lst[m] = 1
        return
    if santa_arr[nr][nc]:
        interact(santa_arr[nr][nc], di, dj)
    santa_arr[nr][nc] = m
    santa_arr[r][c] = 0
    santa_info[m] = (nr, nc)


#가장 가까운 산타에게 가기 위한 방향 반환
def find_ru_dir():
    mn_dist = N*N
    santa_r, santa_c = -1, -1
    for m in range(1, P+1):
        if die_lst[m]: continue
        r, c = santa_info[m]
        dist = get_dist(rr, rc, r, c)
        if dist < mn_dist:
            mn_dist = dist
            santa_r, santa_c = r, c
        elif dist == mn_dist:
            if (santa_r, santa_c) < (r, c):
                santa_r, santa_c = r, c

    mn = get_dist(rr, rc, santa_r, santa_c)
    rdi, rdj = -1, -1
    #산타 위치 정해졌으므로 8방 탐색하며 이동할 곳 찾기
    for di, dj in ru_dir:
        nr, nc = rr+di, rc+dj
        if oob(nr, nc): continue
        dist = get_dist(nr, nc, santa_r, santa_c)
        if dist<mn:
            mn = dist
            rdi, rdj = di, dj
    return rdi, rdj


def find_santa_move(p):
    r, c = santa_info[p]
    mn = get_dist(r, c, rr, rc)
    result_d = 4

    for d in range(4):
        di, dj = santa_dir[d]
        du, dv = r + di, c + dj
        if oob(du, dv): continue
        if santa_arr[du][dv]: continue

        dist = get_dist(du, dv, rr, rc)
        if dist >= mn:
            continue
        mn = dist
        result_d = d
    return result_d


def move_santa():
    for p in range(1, P + 1):
        if (sleep_lst[p] != 0 and sleep_lst[p] in (turn, turn - 1)) or die_lst[p]: continue
        # print(f"===================={p}번 santa  이동 =========================")
        sd = find_santa_move(p)
        if sd == 4:
            continue
        sdi, sdj = santa_dir[sd]
        # print("sdi, sdj : ", sdi, sdj)

        scr, scc = santa_info[p]
        snr, snc = scr + sdi, scc + sdj
        santa_info[p] = (snr, snc)
        santa_arr[snr][snc] = p
        santa_arr[scr][scc] = 0
        # 루돌프 만나면
        if snr == rr and snc == rc:
            sleep_lst[p] = turn
            crush(D, -sdi, -sdj, p)
            if sum(die_lst)==P:
                return False
    return True


def printa(string, arr):
    print(f"=================={string}====================")
    for j in range(len(arr)):
        print(arr[j])
    print("==============================================")
    print()


#루돌프에게 가기 위한 방향 반환

N, M, P, C, D = map(int, input().split())
santa_dir = (-1, 0), (0, 1), (1, 0), (0, -1), (0, 0)
ru_dir = (-1, 0), (0, 1), (1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)
score_lst = [0]*(P+1)
sleep_lst = [0]*(P+1)
die_lst = [0]*(P+1)
santa_info = [[] for _ in range(P+1)]
santa_arr = [[0]*N for _ in range(N)]
rr, rc = map(change, input().split())
for p in range(P):
    num, sr, sc = map(change, input().split())
    num += 1
    santa_arr[sr][sc] = num
    santa_info[num] = (sr, sc)




for turn in range(1, M+1):
    # 루돌프 이동하기
    rdi, rdj = find_ru_dir()
    rr += rdi
    rc += rdj
    # print("===========루돌프 이동 ==============")
    # print(rr, rc)
    #이동한 곳에 산타 있나 확인
    if santa_arr[rr][rc]:
        #충돌했으면 기절
        sleep_lst[santa_arr[rr][rc]] = turn
        crush(C, rdi, rdj, santa_arr[rr][rc])
        if sum(die_lst)==P:
            break

    # 산타 이동하기
    result = move_santa()
    if not result:
        break
    # printa("산타이동", santa_arr)
    # print('산타 죽은거 정보 ', die_lst)
    # print("산타 점수 정보 : ", score_lst[1:])

    for p in range(1, P+1):
        if die_lst[p]: continue
        score_lst[p]+=1

    # print("한턴 끝나고 !! ", score_lst[1:])

print(*score_lst[1:])