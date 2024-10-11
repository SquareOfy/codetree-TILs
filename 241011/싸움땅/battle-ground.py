"""
각 플레이어의 초기 능력치는 모두 다릅니다.

1-1. 첫 번째 플레이어부터 순차적으로 본인이 향하고 있는 방향대로 한 칸만큼 이동
    격자를 벗어나는 경우에는 정반대 방향으로 방향을 바꾸어서 1만큼 이동
2-1.  이동한 방향에 플레이어가 없다면 해당 칸에 총이 있는지 확인
    이미 총을 가지고 있는 경우에는 놓여있는 총들과 플레이어가 가지고 있는
     총 가운데 공격력이 더 쎈 총을 획득
     나머지 총들은 해당 격자에 둡니다.

2-2-1. 만약 이동한 방향에 플레이어가 있는 경우에는 두 플레이어가 싸우게 됩니다.
    해당 플레이어의 초기 능력치와 가지고 있는 총의 공격력의 합을 비교
    이 수치가 같은 경우에는 플레이어의 초기 능력치가 높은 플레이어가 승리
    이긴 플레이어는 각 플레이어의 초기 능력치와 가지고 있는 총의 공격력의 합의 차이만큼을
    포인트로 획득
2-2-2. 진 플레이어는 본인이 가지고 있는 총을 해당 격자에 내려놓고,
        해당 플레이어가 원래 가지고 있던 방향대로 한 칸 이동
        이동하려는 칸에 다른 플레이어가 있거나 격자 범위 밖인 경우
            오른쪽으로 90도씩 회전하여 빈 칸이 보이는 순간 이동
        이동한 칸에서, 진 플레이어는 가장 공격력이 높은 총을 획득
2-2-3. 이긴 플레이어는 승리한 칸에 떨어져 있는 총들과 원래 들고 있던 총 중 가장 공격력이 높은 총을 획득
    나머지 총들은 해당 격자에 내려 놓습니다.

k 라운드 동안 게임을 진행하면서 각 플레이어들이 획득한 포인트를 출력
"""


def oob(i, j):
    return i < 0 or j < 0 or i >= N or j >= N

def change_gun(r, c, m):
    if player_gun_lst[m] != 0:
        gun_arr[r][c].append(player_gun_lst[m])
    gun_arr[r][c].sort()
    player_gun_lst[m] = gun_arr[r][c].pop()

def printa(string, arr):
    print(f"================={string}==================")
    for i in range(len(arr)):
        print(arr[i])
    print("============================================")
    print()
N, M, K = map(int, input().split())
gun_arr = [[[] for _ in range(N)] for _ in range(N)]
DIR = (-1, 0), (0, 1), (1, 0), (0, -1)
player_arr = [[0] * N for _ in range(N)]
player_info = [-1]
player_gun_lst = [0] * (M + 1)
score_lst = [0] * (M + 1)
player_power = [0] * (M + 1)
for i in range(N):
    lst = list(map(int, input().split()))
    for j in range(N):
        if lst[j]==0: continue
        gun_arr[i][j].append(lst[j])

for m in range(1, M + 1):
    x, y, d, s = map(int, input().split())
    x -= 1
    y -= 1
    player_info.append((x, y, d))
    player_arr[x][y] = m
    player_power[m] = s
for k in range(K):
    for m in range(1, M + 1):
        x, y, d = player_info[m]

        di, dj = DIR[d]
        du, dv = x + di, y + dj

        if oob(du, dv):
            d = (d + 2) % 4
            du -= di * 2
            dv -= dj * 2

        player_arr[x][y] = 0
        player_info[m] = (du, dv, d)
        if not player_arr[du][dv]:
            player_arr[du][dv] = m
            player_info[m] = (du, dv, d)
            if gun_arr[du][dv]:
                change_gun(du, dv, m)

        else:
            your_num = player_arr[du][dv]
            your_power = player_power[your_num]+player_gun_lst[your_num]
            my_power = player_power[m]+player_gun_lst[m]
            if my_power > your_power:
                winner = m
                loser = your_num
            elif my_power < your_power:
                winner = your_num
                loser = m
            else:
                if player_power[m]<player_power[your_num]:
                    winner=your_num
                    loser=m
                else:
                    winner = m
                    loser = your_num
            #점수 계산
            score_lst[winner]+= abs(your_power-my_power)


            #loser 총 내려놓고 이동
            if player_gun_lst[loser]:
                gun_arr[du][dv].append(player_gun_lst[loser])
                player_gun_lst[loser] = 0

            loser_d = player_info[loser][2]
            for t in range(4):
                nd = (loser_d+t)%4
                di, dj = DIR[nd]
                nlr, nlc = du+di, dv+dj
                if oob(nlr, nlc): continue
                if player_arr[nlr][nlc]: continue
                player_arr[nlr][nlc] = loser
                br, bc = player_info[loser][0], player_info[loser][1]
                player_arr[br][bc] = 0
                player_info[loser] = (nlr, nlc, nd)
                break

            #이동해서 총줍기
            if gun_arr[nlr][nlc]:
                change_gun(nlr, nlc, loser)

            #winner 총 교체
            if gun_arr[du][dv]:
                change_gun(du, dv, winner)
            #winner 자리 정리
            player_arr[du][dv] = winner
        # printa(f"{m}번 player 이동 후 PLAYER arr", player_arr)
        # printa(f"{m}번 player 이동 후", gun_arr)

    # printa(f"{k}번째 후 PLAYER arr", player_arr)
    # printa(f"{k}번째 후 GUN arr", gun_arr)
print(*score_lst[1:])