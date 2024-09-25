def change_idx(i):
    return int(i)-1

def oob(i, j):
    return i<0 or j<0 or i>=N or j>=N

def find_nearest_santa():
    lst = []
    mn = N ** 2
    reuslt_r, result_c = -1, -1
    # print(die_santa)
    # print(santa)
    for p in range(1, P + 1):
        if die_santa[p]==1: continue  # 이미 죽어버림
        r, c = santa[p]
        dist = (rr-r)**2 + (rc-c)**2
        if dist<mn:
            mn = dist
            lst = [(r, c)]
            # reuslt_r, result_c = r, c
        elif dist ==mn :
            lst.append((r,c))
            # reuslt_r, result_c = r, c
    lst.sort(reverse=True)
    return lst[0]

def calculate_dist(i, j, y, x):
    return (i-y)**2 + (j-x)**2

def find_move_d(rr, rc, r, c):
    move_d = -1

    mn = calculate_dist(rr, rc, r, c)
    # (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)
    for i in range(8):
        di, dj = dir_eight[i]
        nrr, nrc = rr+di, rc+dj

        if oob(nrr, nrc):
            continue
        dist = calculate_dist(nrr, nrc, r, c)
        # print("d : ", i, "일 때 dist : ", dist)
        if mn>dist:
            move_d = i
            mn=dist
    return move_d


def push_santa(r, c, di, dj, num):
    global cnt
    # 밀려난 칸에 다른 산타가 있는 경우 상호작용
    # 착지하게 되는 칸에 다른 산타가 있다면 그 산타는 1칸 해당 방향으로 밀려나게 됩니다.
    # 연쇄작업
    nr = r+di #밀리는 위치
    nc = c+dj
    if oob(nr, nc): #밖이면 죽어
        die_santa[num] = 1
        cnt+=1
        santa_arr[r][c] = 0  #원래위치도 0으로 만들어주기
        return
    if santa_arr[nr][nc]: #다음 위치에 산타 있으면
        push_santa(nr, nc, di, dj, santa_arr[nr][nc]) #얘도 밀어주고
    santa_arr[nr][nc] = num #자리 차지
    santa[num] = [nr, nc] #정보업데이트



def crush(r, c, di, dj, step):
    global cnt
    num = santa_arr[r][c]


    score[num] += step #C또는 D
    du, dv = r + di * step, c + dj * step #밀려나는 자리

    # 이동하는 도중에 충돌이 일어나지는 않고 밀려난 위치가 게임판 밖이라면
    # 산타는 게임에서 탈락
    if oob(du, dv): #범위 넘어가면 죽음
        santa_arr[r][c] = 0 #원래 자리 비워주고 죽기
        die_santa[num] = 1
        cnt+=1
        return


    if santa_arr[du][dv]: #연쇄작용
        # print("=============연쇄작용==================")
        push_santa(du, dv, di, dj, santa_arr[du][dv]) #그방향으로 쭉쭉 밀어
    santa_arr[du][dv] = santa_arr[r][c] #그 자리 차지하고
    santa_arr[r][c] = 0
    santa[num] = [du, dv] #정보 업데이트



#  N×N 크기의 격자 좌상단은 (1,1)
N, M, P, C, D = map(int, input().split())
rr, rc = map(change_idx, input().split())
santa_arr = [[0]*N for _ in range(N)]
santa = [[-1, -1] for _ in range(N+1)]
for i in range(P):
    num, r, c = map(change_idx, input().split())
    santa_arr[r][c] = num+1 #santa 번호 함수로 1빼줬으니까 다시 더해줌
    santa[num+1][0] = r
    santa[num+1][1] = c

sleep_santa = [-1]*(P+1)
score = [0]*(P+1)
die_santa = [0]*(P+1)
cnt = 0
dir_eight = (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)
# 게임은 총 M 개의 턴에 걸쳐 진행
# 거리 (r-r2)**2 + (c-c2)**2


for k in range(1, M+1):

    # 매 턴마다 루돌프와 산타들이 한 번씩 움직임

    # 루돌프가 한 번 움직인 뒤,
        # 게임에서 탈락하지 않은 산타 중 가장 가까운 산타를 향해 1칸 돌진
        # r 좌표가 큰 산타를 향해 돌진합니다. r이 동일한 경우, c 좌표가 큰 산타
    # print(f'==================================={k}번째 턴===================================')
    r, c = find_nearest_santa()
    # 루돌프는 상하좌우, 대각선을 포함한 인접한 8방향 중 하나로 돌진할 수 있습니다.
    move_d = find_move_d(rr, rc, r, c)
    di, dj = dir_eight[move_d]

    # print("원래 위치 : ", rr, rc)
    # print()
    # for i in range(N):
    #     print(santa_arr[i])
    # print()
    rr, rc = rr+di, rc+dj

    # print(f"{r}, {c}에 있는 산타랑 가깝도록 {rr}, {rc}로 루돌프 이동 ")
    #충돌
    # 해당 산타는 C 만큼의 점수를 얻게 됩니다.
    #이와 동시에 산타는 루돌프가 이동해온 방향으로 C 칸 만큼 밀려나게 됩니다.
    # 기절 k 넣기
    if santa_arr[rr][rc]:
        sleep_santa[santa_arr[rr][rc]] = k
        crush(rr, rc, di, dj, C) #상호작용 이 안에서 호출
        # print("충돌 발생함 !!!!", santa_arr[rr][rc])

        # print("===========충돌 후 정보 ==========")
        # for i in range(N):
        #     print(santa_arr[i])
        # print()
        # print("santa : ")
        # print(santa)
        # print()
        # print("score: ", score)
        # print()
        # print("sleep: ", sleep_santa)
        # print("die : " ,die_santa)
    if cnt == P:
        break
    # print("====================루돌프 움직임 종료==============")
    # 1번 산타부터 P번 산타까지 순서대로 움직이게 됩니다.
        # 산타는 다른 산타가 있는 칸이나 게임판 밖으로는 움직일 수 없습니다.
        # 움직일 수 있는 칸이 없다면 산타는 움직이지 않습니다.
        # 움직일 수 있는 칸이 있더라도 만약 루돌프로부터 가까워질 수 있는 방법이 없다면
    # 산타는 움직이지 않습니다.??????????????????????????

    for p in range(1, P+1):
        # print("=======", p, "번 산타 이동해보자")
        # 기절해있거나(k-1이면) 격자 밖으로 빠져나가 게임에서 탈락한 산타들은 움직일 수 없습니다.
        if die_santa[p]==1 or sleep_santa[p] in (k, k-1):
            # print("죽거나 기절")
            continue
        # 산타는 루돌프에게 거리가 가장 가까워지는 방향으로 1칸 이동
        # 가장 가까워질 수 있는 방향이 여러 개라면, 상우하좌 우선순위
        r, c= santa[p]
        # print("r, c : ", r, c)


        min_dist = calculate_dist(rr, rc, r, c)
        move_d = (-1, -1)
        du, dv = r, c


        for di, dj in (-1, 0), (0, 1), (1, 0), (0, -1):
            nr, nc = r+di, c+dj
            if oob(nr, nc) or santa_arr[nr][nc]:
                # print("범위 벗어나거나 santa가 있다")
                # for i in range(N):
                #     print(santa_arr[i])
                continue
            dist = calculate_dist(nr, nc, rr, rc)
            if min_dist>dist:
                min_dist = dist
                du, dv = nr, nc
                move_d = (di, dj)


        #du, dv로 이동
        if du==r and dv ==c:
            continue
        santa_arr[r][c] = 0 # 원래 위치 복구
        # print("du, dv ", du, dv) #
        santa_arr[du][dv] = p #새로운 위치로 이동
        santa[p] = [du, dv] #새로운 위치 저장
        # print("새로운 위치 : " , du, dv)

        if du==rr and dv ==rc:
            # 루돌프와 충돌하면 해당 산타는 D만큼의 점수를 얻게 됩니다.
            # 동시에 산타는 자신이 이동해온 반대 방향으로 D 칸 만큼 밀려나게 됩니다.
            # 충돌 후 기절 k 넣기
            # print(p , "충돌 !!!!!!!!!!!!!!!!!!!!")
            crush(du, dv, -move_d[0], -move_d[1], D)
            sleep_santa[p] = k
    # print("===============모든 산타 이동 후 ===================")
    # for i in range(N):
    #     print(santa_arr[i])

    # print("score")
    # print(score)
    # print()
    # print("sleep")
    # print(sleep_santa)
    #
    # print()
    # print("============")
    if cnt == P:
        break

    for i in range(1, P + 1):
        if die_santa[i] !=1 :
            score[i] += 1

print(*score[1:])