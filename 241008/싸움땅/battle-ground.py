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
# printa("초기 플레이어위치 ", player_arr)
# print("gun : ", player_gun_lst)
# print("dir : ", player_dir_lst)
# print("loc : ", player_loc_lst)
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
        player_arr[x][y] = 0
        player_loc_lst[i] = (du, dv)
        player_dir_lst[i] = d
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

            player_arr[du][dv] = i

            # print("=================i : ", i, "======================")
            # printa("이동했다 !! ", player_arr)
            # print("gun : ", player_gun_lst)
            # print("dir : ", player_dir_lst)
            # print("loc : ", player_loc_lst)
        else: #사람 있으면 싸워
            # print(f"{du}, {dv}에서 싸울거야 !!!!!!!!!!!!")
            my_power = player_power_lst[i]+player_gun_lst[i]
            your_num = player_arr[du][dv]
            your_power = player_power_lst[your_num]+player_gun_lst[your_num]
            # print("=================i : ", i, "======================")
            # printa("싸웠다 !! ", player_arr)
            # print("상대편 : ", your_num)
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
            # print("power : ", player_power_lst)
            # print("gun : " , player_gun_lst)
            # print("winner : ", winner)
            # print("loser : ", loser)
            # print("mypower : ", my_power)
            # print("yourPower : ", your_power)
            # print(point_lst)

            #패자 되돌아가기
            #총 있으면 내놔
            if player_gun_lst[loser]:
                gun_arr[du][dv].append(player_gun_lst[loser])
            player_gun_lst[loser] = 0
            loser_d = player_dir_lst[loser]
            lnr, lnc = du, dv
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
            if gun_arr[du][dv]:
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