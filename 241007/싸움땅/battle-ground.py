"""

초기에는 무기들이 없는 빈 격자에 플레이어들이 위치하며 각 플레이어는 초기 능력치를 가짐


1. 이동
    첫 번째 플레이어부터 순차적으로 본인이 향하고 있는 방향대로 한 칸만큼 이동
    해당 방향으로 나갈 때 격자를 벗어나는 경우에는 정반대 방향으로 방향을 바꾸어서 1만큼 이동

2. 도착 -> 총 줍기 또는 싸움
     이동한 방향에 플레이어가 없다면 총을 획득
     플레이어가 이미 총을 가지고 있는 경우에는 놓여있는 총들과 플레이어가 가지고 있는 총 가운데
     공격력이 더 쎈 총을 획득하고, 나머지 총들은 해당 격자에 둡니다.

    이동한 방향에 플레이어가 있는 경우
    해당 플레이어의 초기 능력치와 가지고 있는 총의 공격력의 합을 비교하여 더 큰 플레이어가 이기게 됩니다.
    이 수치가 같은 경우에는 플레이어의 초기 능력치가 높은 플레이어가 승리

    이긴 플레이어
        각 플레이어의 초기 능력치와 가지고 있는 총의 공격력의 합의 차이만큼을 포인트로
        승리한 칸에 떨어져 있는 총들과 원래 들고 있던 총 중 가장 공격력이 높은 총을 획득
        기존 총은  해당 격자에 내려 놓습니다.

    진 플레이어
        본인이 가지고 있는 총을 해당 격자에 내려놓고, 해당 플레이어가 원래 가지고 있던 방향대로 한 칸 이동
        만약 이동하려는 칸에 다른 플레이어가 있거나 격자 범위 밖인 경우에는
        오른쪽으로 90도씩 회전하여 빈 칸이 보이는 순간 이동
        이동 후, 해당 플레이어는 가장 공격력이 높은 총을 획득하고 나머지 총들은 해당 격자에 내려 놓습니다.

k 라운드 동안 게임을 진행하면서 각 플레이어들이 획득한 포인트를 출력

"""
def oob(i, j):
    return i<0 or j<0 or i>=N or j>=N

def printa(string, arr):
    print(f"================{string}===============")
    for i in range(N):
        print(arr[i])
    print("============================================")
    print()
N, M, K = map(int, input().split())
gun_arr = [[[] for _ in range(N)] for _ in range(N)]

for r in range(N):
    lst = list(map(int, input().split()))
    for c in range(N):
        if lst[c] == 0: continue
        gun_arr[r][c].append(lst[c])

player_arr = [[0]*N for _ in range(N)]
player_loc_lst = [-1]
player_power_lst = [-1]
player_dir_lst = [-1]
player_gun_lst = [0]*(M+1)
point_lst = [0]*(M+1)

DIR = (-1, 0), (0, 1), (1, 0), (0, -1)

for m in range(1, M+1):
    x, y, d, s = map(int, input().split())
    x -= 1
    y -= 1
    player_arr[x][y] = m
    player_loc_lst.append((x, y))
    player_dir_lst.append(d)
    player_power_lst.append(s)

for k in range(K):

    # print(f"===============================k : {k} ==========================")
    for i in range(1, M+1):
        x, y = player_loc_lst[i]
        d = player_dir_lst[i]
        di, dj = DIR[d]
        du, dv = x+di, y+dj
        if oob(du, dv):
            d = (d+2)%4
            du -= di*2
            dv -= dj*2

        #사람 없으면 총 줍기
        if not player_arr[du][dv]:
            #총 있으면
            if gun_arr[du][dv]:
                if player_gun_lst[i]:
                    gun_arr[du][dv].append(player_gun_lst[i])
                gun_arr[du][dv].sort()
                mx = gun_arr[du][dv].pop()
                player_gun_lst[i] = mx

            #이동하기
            player_loc_lst[i] = (du, dv)
            player_dir_lst[i] = d
            player_arr[x][y] = 0
            player_arr[du][dv] = i

            # print("=================i : ", i, "======================")
            # printa("이동했다 !! ", player_arr)
            # print("gun : ", player_gun_lst)
            # print("dir : ", player_dir_lst)
            # print("loc : ", player_loc_lst)
        else: #사람 있으면 싸워
            my_power = player_power_lst[i]+player_gun_lst[i]
            your_num = player_arr[du][dv]
            your_power = player_power_lst[your_num]+player_gun_lst[your_num]
            player_arr[x][y] = 0
            # print("=================i : ", i, "======================")
            # printa("싸웠다 !! ", player_arr)
            # print("gun : ", player_gun_lst)
            # print("dir : ", player_dir_lst)
            # print("loc : ", player_loc_lst)
            #승패 가리기
            if my_power>your_power:
                winner = i
                loser = your_num
            elif my_power<your_power:
                winner = your_num
                loser = i
            else:
                if player_power_lst[i] < player_power_lst[your_num]:
                    winner = your_num
                    loser = i
                else:
                    winner = i
                    loser = your_num

            #점수 더해주기
            point_lst[winner] += abs(my_power-your_power)
            # print("winner : ", winner)
            # print("mypower : ", my_power)
            # print("yourPower : ", your_power)
            # print(point_lst)

            #패자 되돌아가기
            #총 있으면 내놔
            if player_gun_lst[loser]:
                gun_arr[du][dv].append(player_gun_lst[loser])
            player_gun_lst[loser] = 0
            loser_d = player_dir_lst[loser]
            #되돌아가. 안돼면 4방 탐색해
            for t in range(4):
                nd = (loser_d+t)%4
                ldi, ldj = DIR[nd]
                lnr, lnc = du+ldi, dv+ldj
                if oob(lnr, lnc) or player_arr[lnr][lnc]:
                    continue

                #이동하기
                player_loc_lst[loser] = (lnr, lnc)
                player_dir_lst[loser] = nd
                player_arr[lnr][lnc] = loser
                break
            if gun_arr[lnr][lnc]:
                gun_arr[lnr][lnc].sort()
                player_gun_lst[loser] = gun_arr[lnr][lnc].pop()

            #승자 총줍기
            if player_gun_lst[winner]:
                gun_arr[du][dv].append(player_gun_lst[winner])
            gun_arr[du][dv].sort()
            mx = gun_arr[du][dv].pop()
            player_gun_lst[winner] = mx
            player_loc_lst[winner] = (du, dv)
            player_arr[du][dv] = winner

            # printa("싸웠다 !! ", player_arr)
            # printa("총 보자 ! ", gun_arr)
            # print("gun : ", player_gun_lst)
            # print("dir : ", player_dir_lst)
            # print("loc : ", player_loc_lst)

print(*point_lst[1:])