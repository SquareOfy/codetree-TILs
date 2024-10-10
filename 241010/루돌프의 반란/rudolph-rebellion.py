"""
총 M 개의 턴에 걸쳐 진행 : 루돌프와 산타들이 한 번씩 움직입니다

루돌프가 한 번 움직인 뒤, 1번 산타부터 P번 산타까지 순서대로 움직이게 됩니다
거리 = (x-r)**2 + (y-c)**2

1. 루돌프의 움직임
    게임에서 탈락하지 않은 산타 중 가장 가까운 산타를 향해 1칸 돌진
     2명 이상이라면 r 좌표가 큰 산타->  c 좌표가 큰 산타를 향해 돌진

    루돌프는 상하좌우, 대각선을 포함한 인접한 8방향 중 하나로 돌진
    8방향 중 가장 가까워지는 방향으로 한 칸 돌진

    산타 있으면 충돌 발생
    산타는 루돌프와의 충돌 후 기절 (k턴이면 k+1턴 까지)
     해당 산타는 C만큼의 점수
    산타는 루돌프가 이동해온 방향으로 C 칸 만큼 밀려나게 됩니다.

    만약 P 명의 산타가 모두 게임에서 탈락하게 된다면 그 즉시 게임이 종료
2. 산타의 움직임
    1번부터 P번까지 순서대로
    기절했거나 이미 게임에서 탈락한 산타는 움직일 수 없습니다.
    루돌프에게 거리가 가장 가까워지는 방향으로 1칸 이동
    다른 산타가 있는 칸이나 게임판 밖으로는 움직일 수 없습니다.
    움직일 수 있는 칸이 없다면 산타는 움직이지 않습니다.
    만약 루돌프로부터 가까워질 수 있는 방법이 없다면 산타는 움직이지 않습니다.
    상우하좌 우선순위에 맞춰

    루돌프 있으면 충돌 발생
    산타는 루돌프와의 충돌 후 기절 (k턴이면 k+1턴 까지)
    해당 산타는 D만큼의 점수
    산타는 자신이 이동해온 반대 방향으로 D 칸 만큼 밀려나게 됩니다.
    만약 P 명의 산타가 모두 게임에서 탈락하게 된다면 그 즉시 게임이 종료
3. 상호작용 : 충돌 이후 밀려난 위치에 산타 있으면 ! (연쇄적)
    충돌 후 착지하게 되는 칸에 다른 산타가 있다면 그 산타는 1칸 해당 방향으로 밀려나게 됩니다.

4.
매 턴 이후 아직 탈락하지 않은 산타들에게는 1점씩을 추가로 부여
"""


def change(i):
    return int(i) - 1


def oob(i, j):
    return i < 0 or j < 0 or i >= N or j >= N


def cal_dist(x, y, r, c):
    return (x-r)**2 + (y-c)**2

def find_ru_move():
    # 게임에서 탈락하지 않은 산타 중 가장 가까운 산타를 향해 1칸 돌진

    mn = N*N
    nsx, nsy = -1, -1
    for p in range(1, P+1):
        if die_lst[p]: continue
        sx, sy = santa_info[p]
        dist = cal_dist(rx, ry, sx, sy)
        if dist<mn:
            mn = dist
            nsx, nsy = sx, sy
        # 2명 이상이라면 r 좌표가 큰 산타->  c 좌표가 큰 산타를 향해 돌진
        elif dist==mn and (sx, sy) > (nsx, nsy):
            nsx, nsy = sx, sy
    mn = N*N
    result_di, result_dj = None, None

    # 8방향 중 가장 가까워지는 방향으로 한 칸 돌진
    for di, dj in diagonal:
        nRx, nRy = rx+di, ry+dj
        if oob(nRx, nRy): continue
        new_dist = cal_dist(nRx, nRy, nsx, nsy)
        if mn > new_dist:
            mn = new_dist
            result_di, result_dj = di, dj
    return result_di, result_dj


def kill_santa(s_num):
    die_lst[s_num] = 1
    x, y = santa_info[s_num]
    santa_arr[x][y] = 0
    santa_info[s_num] = -1


def interact(di, dj, s_num):
    sx, sy = santa_info[s_num]
    nsx, nsy = sx+di, sy+dj
    if oob(nsx, nsy):
        kill_santa(s_num)
        return
    if santa_arr[nsx][nsy]:
        interact(di, dj, santa_arr[nsx][nsy])

    santa_arr[sx][sy] = 0
    santa_arr[nsx][nsy]=s_num
    santa_info[s_num] = (nsx, nsy)



def crush(step, di, dj, s_num):
    #현재 산타 위치
    Sx, Sy = santa_info[s_num]

    #밀려날 위치
    nSx, nSy = Sx+step*di, Sy+step*dj

    score_lst[s_num] += step #점수 더하기
    santa = s_num
    if oob(nSx, nSy):
        kill_santa(santa)
        return
    if santa_arr[nSx][nSy]:
        interact(di, dj, santa_arr[nSx][nSy])

    santa_arr[Sx][Sy] = 0 #현재 위치 없애기
    santa_arr[nSx][nSy] = s_num
    santa_info[santa] = (nSx, nSy)

def printa(string, arr):
    print(f"============={string}===========")
    print("루돌프 위치 : ", rx, ry)
    print()
    for i in range(N):
        print(arr[i])
    print()
    print("================================")

N, M, P, C, D = map(int, input().split())
santa_arr = [[0] * N for _ in range(N)]
santa_info = [[] for _ in range(P+1)]
sleep_lst = [-1] * (P+1)
die_lst = [0] * (P+1)
score_lst = [0] * (P+1)

rx, ry = map(change, input().split())
DIR = (-1, 0), (0, 1), (1, 0), (0, -1)
diagonal = (-1, 0), (0, 1), (1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)


for p in range(1, P+1):
    num, sr, sc = map(change, input().split())
    santa_info[num+1] = (sr, sc)
    santa_arr[sr][sc] = num+1




for m in range(1, M+1):

    # 가장 가까운 산타로 이동할 방향 구하기
    rdi, rdj = find_ru_move()

    # 이동하기
    rx += rdi
    ry += rdj
    #산타 있으면 충돌 발생
    if santa_arr[rx][ry]:
        sleep_lst[santa_arr[rx][ry]] = m
        crush(C, rdi, rdj, santa_arr[rx][ry])


    #산타 다 죽었나 확인하고 게임 종료
    if sum(die_lst) == P:
        break

    #산타 이동하기
    for p in range(1, P+1):
        #죽었거나 기절이면 continue
        if die_lst[p] or sleep_lst[p] in (m, m-1):
            continue
        sx, sy = santa_info[p]
        sdi, sdj = None, None
        origin = cal_dist(sx, sy, rx, ry)
        mn = origin
        #상우하좌 중 루돌프와 가장 가까워지는 방향 구하기
        for di, dj in DIR:
            nSx, nSy = sx+di, sy+dj
            if oob(nSx, nSy): continue
            if santa_arr[nSx][nSy]: continue
            dist = cal_dist(nSx, nSy, rx, ry)
            if mn>dist:
                mn = dist
                sdi, sdj = di, dj

        #원래 거리랑 동일하면 stay
        if mn == origin:
            continue
        #이동하기
        santa_arr[sx][sy] = 0
        sx, sy = sx+sdi, sy+sdj
        santa_info[p] = (sx, sy)

        #루돌프 위치면 충돌 발생
        if sx==rx and sy==ry:
            sleep_lst[p] = m
            crush(D, -sdi, -sdj, p)
        else:
            santa_arr[sx][sy] = p

    # 다 죽었나 확인하고 게임종료
    if sum(die_lst) == P:
        break

    #살아있는 산타에게 점수 1 더해주기
    for i in range(1, P+1):
        if die_lst[i]: continue
        score_lst[i] += 1


print(*score_lst[1:])