"""

1. 도망자 움직이기
    현재 바라보고 있는 방향으로 1칸 움직일 때
        격자를 벗어나지 않는 경우
            술래가 있는 경우라면 움직이지 않습니다.
            술래 없다면 해당 칸으로 이동.  나무가 있어도 괜찮

        격자를 벗어나는 경우
            방향을 반대로 틀어주기.
            바라보고 있는 방향으로 1칸 움직인다 했을 때
            해당 위치에 술래가 없다면 1칸 앞으로 이동합니다.

2. 술래 움직이기
    가운데에서 시작해서 상 우 하 좌 순으로 달팽이 모양으로 움직임
    도달하면 반대로 움직여서 중심으로 오기

    ************주의 !!!!!!!!!!!!!!!!!!!!!111
    한칸 이동 후 방향을 트는 곳이라면 방향을 바로 틀어준다 !!!!!!! !!
    ********************************************8
나무의 역할이 뭐지 ?
만약 나무가 놓여 있는 칸이라면, 해당 칸에 있는 도망자는 나무에 가려져 보이지 않게 됩니다.
술래가 보고 있는 방향을 끝까지 보고 나무 있는 칸의 도망자는 살아남고 아니면 잡힌다 !

점수
    t번째 턴일 때, t*잡힌 도망자 수



1. 도망자 움직이기
    도망자 위치 배열에 담아두기 ( arr 배열에는 도망자 번호로 넣어두기!!!)
    도망자 배열 탐색하며 다음 위치 새 배열에 넣기 (술래와의 거리 3이하인지 확인하고 움직이기, 아니면 그대로)
        oob 활용
        oob 아닐 때 술래 위치 idx 로 기억해둔 것 활용

2. 술래 이동
    달팽이 모양(술래 위치 순서) 배열에 담아두기
    그 때의 방향 배열 만들어 두기

    술래 현 위치가 끝점이면 위치 index 1 빼기
    아니면 index +1

    index 변경 시킨 후 방향도 방향 배열의 값으로 갱신해두기

    그리고 그 방향에서 사람 있나 쭈우우욱 보고 잡기 + 점수 더하기
"""
def oob(i, j):
    return i<0 or j<0 or i>=N or j>=N

def get_distance(i, j, x, y):
    return abs(i-x)+abs(j-y)

#인덱스 1부터 시작하니까 꼭 1 빼기 !!!!!!!!!!!!!!!!!!!!!!!!!!!
N, M, H, K = map(int, input().split())

arr = [[[] for _ in range(N)] for _ in range(N)]
tree = [[0]*N for _ in range(N)]
runner = []
route = []
d_by_route = []
dir = (-1, 0),(0, 1), (1, 0), (0, -1) #상 / 우 / 하 / 좌 (1, 2그대로 유지! )
answer = 0

#도망자 입력 받기
for i in range(M):
    x, y, d = map(int, input().split())
    runner.append([x-1, y-1, d])
    arr[x-1][y-1].append(i)

for j in range(H):
    x, y = map(int, input().split())
    tree[x-1][y-1] = 1


#술래 이동 route 배열 만들어 놓기
r = N//2
c = N//2
l = 1
cnt = 0
route.append((r,c))
d_by_route.append(0)
d = 0
while 1:
    di, dj = dir[d]
    for k in range(l):
        r += di
        c += dj
        route.append((r, c))
        d_by_route.append(d)
        if r==0 and c==0:
            break

    cnt += 1
    if cnt ==2:
        l+=1
        cnt = 0
    d += 1
    d %= 4
    d_by_route[-1] = d
    if r==0 and c==0:
        d_by_route[-1] = 2
        break
######################달팽이 확인 완
# print(route)
# print(d_by_route)
####################################33

# 1. 도망자 움직이기
#     도망자 배열 탐색하며 다음 위치 새 배열에 넣기 (술래와의 거리 3이하인지 확인하고 움직이기, 아니면 그대로)
#         oob 활용
#         oob 아닐 때 술래 위치 idx 로 기억해둔 것 활용
#         격자를 벗어나지 않는 경우
#             술래가 있는 경우라면 움직이지 않습니다.
#             술래 없다면 해당 칸으로 이동.  나무가 있어도 괜찮
#
#         격자를 벗어나는 경우
#             방향을 반대로 틀어주기.
#             바라보고 있는 방향으로 1칸 움직인다 했을 때
#             해당 위치에 술래가 없다면 1칸 앞으로 이동합니다.
#현재 술래 정보
idx = 0
r = 1

for k in range(1, K+1):
    if not runner:
        break
    # print(f"==================={k}===================")
    cr, cc = route[idx]
    d = d_by_route[idx]
    # print("시작 cr , cc ", cr, cc)
    # print("술래 방향 : ", dir[d])
    new_arr = [[[] for _ in range(N)] for _ in range(N)]
    new_runner = []
    runner_idx = 0
    # print("==========도망치기 전 ===================")
    # for i in range(N):
    #     print(arr[i])
    # print()
    for i,j,run_d in runner:
        # print("runner ")
        # print(i, j, run_d)
        if i== -1 and j==-1:
            continue


        #움직임 가능성 체크
        dist = get_distance(i, j, cr, cc)
        if dist > 3:
            # print("그대로 반영")
            new_runner.append([i, j, run_d])
            new_arr[i][j].append(runner_idx)
            runner_idx += 1
            continue
        di, dj = dir[run_d]
        du = i+di
        dv = j+dj
        if oob(du, dv): #
            run_d = (run_d+2)%4
            du -= di*2
            dv -= dj*2


        # dist = get_distance(du, dv, cr, cc)
        # if dist > 4:
        #     # print("그대로 반영")
        #     new_runner.append([du, dv, run_d])
        #     new_arr[i][j].append(runner_idx)
        #     runner_idx += 1
        #     continue

        #술래가 있으면 ...
        if du == cr and dv == cc:
            # print("그대로 반영")
            new_runner.append([i, j, run_d])
            new_arr[i][j].append(runner_idx)
            runner_idx+= 1
            continue

        new_arr[du][dv].append(runner_idx)
        runner_idx+=1
        new_runner.append([du, dv, run_d])

    #옮긴 도망자 원본 배열에 다시 반여하기
    for i in range(N):
        for j in range(N):
            arr[i][j] = new_arr[i][j][:]
    runner = new_runner[:]
    # print("==========도망친 후 ===================")
    # for i in range(N):
    #     print(arr[i])
    # print()
    #술래 옮기기
    if idx == N*N -1 and r==1:
        r*= -1
    elif idx == 0 and r==-1:
        r*= -1
    idx += r
    #술래의 옮긴 위치와 방향
    cr, cc = route[idx]
    di, dj = dir[d_by_route[idx]]
    # print("술래 이동 후 ============================")
    # print("cr, cc " , cr, cc)
    # print(di, dj)
    # print("===================")

    catch = 0

    # du, dv = cr, cc
    for t in range(3):
        du = cr + di*t
        dv = cc + dj*t

        if oob(du, dv):
            break
        if tree[du][dv]:
            continue
        if arr[du][dv]:
            catch += len(arr[du][dv])
            for u in arr[du][dv]:
                runner[u] = [-1, -1, 0]
            arr[du][dv] = []
            # print("잡앗다 !!!!!!!!!!!!!!!!!!", catch)


    answer += k*catch
print(answer)