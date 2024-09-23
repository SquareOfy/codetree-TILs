"""
플레이어 N*N 배열에 위치 넣기
플레이어 위치에 그 플레이어의 번호 넣기
플레이어의 방향과 초기 능력치는 dict로 관리  key : num // value : (x, y, 방향, 초기 능력치)

gun = 플레이어가 현재 들고 있는 총의 공격력
point = 플레이어별 획득한 포인트 ( 출력 배열)



"""
import heapq

def oob(x, y):
    return x<0 or y<0 or x>=N or y>=N

# ↑, →, ↓, ←
DIR = (-1, 0), (0, 1), (1, 0), (0, -1)
#입력
# 첫 번째 줄에 n, m, k가 공백을 사이에 두고 주어집니다.
# n은 격자의 크기, m은 플레이어의 수, k는 라운드의 수를 의미합니다.
N, M, K = map(int, input().split())
arr = [[[] for _ in range(N)] for _ in range(N)]
player_arr = [[0]*N for _ in range(N)]
player_dict = {}
point = [0]*(M+1)
gun = [0]*(M+1)

# n개의 줄에 걸쳐 격자에 있는 총의 정보가 주어집니다
# 숫자 0은 빈 칸, 0보다 큰 값은 총의 공격력
# 3차원으로 만들기
# arr = [list(map(int, input().split())) for _ in range(N)]
for i in range(N):
    lst = list(map(int, input().split()))
    for j in range(N):
        if lst[j] ==0: continue
        heapq.heappush(arr[i][j], lst[j])
        # arr[i][j].append(lst[j])
    # print(arr[i])


#  m개의 줄에 걸쳐 플레이어들의 정보 x, y, d, s가 공백을 사이에 두고 주어집니다
# (x, y)는 플레이어의 위치, d는 방향, s는 플레이어의 초기 능력치를 의미
# 각 플레이어의 초기 능력치는 모두 다릅니다.
#  방향 d는 0부터 3까지 순서대로 ↑, →, ↓, ←을 의미
for i in range(1, M+1):
    x, y, d, s = map(int, input().split())
    x -=1
    y -=1
    player_dict[i] = (x, y, d, s)
    player_arr[x][y] = i

# 플레이어의 초기 위치에는 총이 존재하지 않습니다.



#라운드
for k in range(K):
    #  첫 번째 플레이어부터 순차적으로 본인이 향하고 있는 방향대로 한 칸만큼 이동합니다
    # 해당 방향으로 나갈 때 격자를 벗어나는 경우에는 정반대 방향으로 방향을 바꾸어서 1만큼 이동
    # print(f"====================================={k}========================================")
    for i in range(1, M+1):
        x, y, d, s = player_dict[i]
        player_arr[x][y] = 0
        # print(f"=================={i}번째 player 이동 =========================")
        # print(x, y, d, s)
        di, dj = DIR[d]
        if oob(x+di, y+dj):
            d+=2
            d%=4
            di, dj = DIR[d]
        nx, ny = x+di, y+dj
        # print("다음 위치 : ", nx, ny)
        # 만약 이동한 방향에 플레이어가 있는 경우에는 두 플레이어가 싸우게 됩니다.
        # 해당 플레이어의 초기 능력치와 가지고 있는 총의 공격력의 합을 비교하여 더 큰 플레이어가 이기게 됩니다
        # 만일 이 수치가 같은 경우에는 플레이어의 초기 능력치가 높은 플레이어가 승리하게 됩니다.
        # 이긴 플레이어는 각 플레이어의 초기 능력치와 가지고 있는 총의 공격력의 합의 차이만큼을 포인트로 획득
        if player_arr[nx][ny]:
            # print("싸우자 ! ")
            enemy_num = player_arr[nx][ny]
            enemy_power = player_dict[enemy_num][3]+gun[enemy_num]
            my_power = s+gun[i]

            if enemy_power<my_power or (enemy_power==my_power and  player_dict[enemy_num][3]<s):
                winner = i
                loser = enemy_num
                player_dict[i] = (nx, ny, d, s)
                player_arr[nx][ny] = winner
                loser_d = player_dict[loser][2]
                loser_s = player_dict[loser][3]
            else:
                winner = enemy_num
                loser = i
                loser_d, loser_s = d, s


            point[winner] += abs(enemy_power-my_power) #점수획득

            #  진 플레이어는 본인이 가지고 있는 총을 해당 격자에 내려놓고, 해당 플레이어가 원래 가지고 있던 방향대로 한 칸 이동합니다.
            # 만약 이동하려는 칸에 다른 플레이어가 있거나 격자 범위 밖인 경우에는
            # 오른쪽으로 90도씩 회전하여 빈 칸이 보이는 순간 이동합니다.
            #  해당 칸에 총이 있다면,
            #  해당 플레이어는 가장 공격력이 높은 총을 획득하고 나머지 총들은 해당 격자에 내려 놓습니다.
            # ?????????이동한 후 칸이군

            # 총내려놓기
            if gun[loser]:
                heapq.heappush(arr[nx][ny], gun[loser])
            gun[loser] = 0

            #회전하며 빈칸 탐색
            for t in range(4):
                new_d = (loser_d+t)%4
                di, dj = DIR[new_d]
                if oob(nx+di, ny+dj) or player_arr[nx+di][ny+dj]:
                    continue
                player_dict[loser] = (nx + di, ny + dj, new_d, loser_s)
                player_arr[nx+di][ny+dj] = loser
                # print("loser 정보 갱신 ", loser)
                # print(player_dict[loser])

                #가장 높은 총 얻기
                if arr[nx+di][ny+dj]:
                    gun[loser] = heapq.heappop(arr[nx+di][ny+dj])
                # print("gun : ", gun)
                break

            # . 이긴 플레이어는 승리한 칸에 떨어져 있는 총들과 원래 들고 있던 총 중
            # 가장 공격력이 높은 총을 획득하고, 나머지 총들은 해당 격자에 내려 놓습니다.
            if arr[nx][ny]:
                mx_gun = heapq.heappop(arr[nx][ny])
                heapq.heappush(arr[nx][ny], min(mx_gun, gun[winner]))
                gun[winner] = max(mx_gun, gun[winner])



        #  만약 이동한 방향에 플레이어가 없다면 해당 칸에 총이 있는지 확인합니다.
        # 총이 있는 경우, 해당 플레이어는 총을 획득합니다.
        # 플레이어가 이미 총을 가지고 있는 경우에는 놓여있는 총들과 플레이어가 가지고 있는
        # 총 가운데 공격력이 더 쎈 총을 획득하고, 나머지 총들은 해당 격자에 둡니다.
        else:
            if arr[nx][ny]:
                # print("총 줍자 ")
                if gun[i] == 0:
                    gun[i] = heapq.heappop(arr[nx][ny])
                else:
                    # print("바꿔치기")
                    mx_gun = heapq.heappop(arr[nx][ny])
                    heapq.heappush(arr[nx][ny], min(gun[i], mx_gun))
                    gun[i] = max(mx_gun, gun[i])
            player_arr[nx][ny] = i
            player_dict[i] = (nx, ny, d, s)


        # print(player_dict)
        # for t in range(N):
        #     print(player_arr[t])
        # print()
        # print("gun _ arr")
        # for t in range(N):
        #     print(arr[t])
        # print()
        # print("gun ")
        # print(gun)
        # print()
        # print("point ")
        # print(point)
        # print()

    # k 라운드 동안 게임을 진행하면서 각 플레이어들이 획득한 포인트
print(*point[1:])