def oob(i, j):
    return i<0 or j<0 or i>=L or j>=N


def move(num, di, dj):
    r, c, h, w = gisa_info[num]
    if di != 0:
        du = 0 if di >0 else h-1 #지워야할 위치
        nr = r+h if di>0 else r-1
        gisa_arr[r+du][c:c+w] = [0]*w
        # print_gisa()
        gisa_arr[nr][c:c+w] = [num]*w
        # gisa_arr[r+(h-1-du)][c:c+w] = [num]*w
    else:
        dv = 0 if dj>0 else w-1
        nc = c+w if dj>0 else c-1
        # print("c+dv : ", c+dv)
        for i in range(h):
            # print("r+i : ", r+i)
            gisa_arr[r+i][c+dv] = 0
        for i in range(h):
            # print("c+(w-1-dv) : ", c+(w-1-dv))
            gisa_arr[r+i][nc] = num
    gisa_info[num] = [r+di, c+dj, h, w]


def kill(num):
    gisa_damage[num] = 0
    r, c, w, h = gisa_info[num]
    for i in range(h):
        for j in range(w):
            arr[r+i][c+j] = 0


def is_possible(push_lst, di, dj):
    #맨 마지막 애부터 쭉 이동이 가능한지 보기 !!
    for i in range(len(push_lst)-1, -1, -1):
        num = push_lst[i]
        if not check(num, 0, di, dj):
            return False
    return True

def get_damage(num):
    damage = 0
    r, c, h, w = gisa_info[num]
    for i in range(h):
        for j in range(w):
            if arr[r+i][c+j]==1:
                damage+=1
    return damage

def check(num, flag, di, dj):
    #한칸 이동 가능한지 체크!
    #flag 1이면 첫 기사를 말하는거라 아예 빈칸인지도 체크
    r, c, h, w = gisa_info[num]
    # print(r, c, h, w)
    if di != 0:
        nr = r + h if di > 0 else r - 1
        # print("nr : ", nr)
        if nr ==L or nr<0:
            # print("범위 out")
            return False
        # print("nr : ", nr)
        for j in range(c, c + w):
            if arr[nr][j] == 2:
                return False
            if flag and gisa_arr[nr][j] !=0:
                return False
    else:
        nc = c + w if dj > 0 else c - 1
        # print("nc : ", nc)
        if nc ==L or nc<0:
            # print("범위 out")
            return False
        for i in range(r, r + h):
            # print("i : ", i)
            if arr[i][nc] == 2:
                return False
            if flag and gisa_arr[i][nc] !=0:
                return False

    # print("check True")
    return True

def print_gisa():
    print("=========gisa===========")
    for i in range(L):
        print(gisa_arr[i])
    print()


L, N, Q = map(int, input().split())
# 다음 L 개의 줄에 걸쳐서 L×L 크기의 체스판에 대한 정보가 주어집니다.
# 0이라면 빈칸 / 1이라면 함정 / 2라면 벽
arr = [list(map(int, input().split())) for _ in range(L)]
# for i in range(L):
#     print(arr[i])
gisa_hp = [0]*(N+1)
gisa_info = [0] #h, w 정보
gisa_arr = [[0]*L for _ in range(L)]
gisa_damage = [0]*(N+1)
DIR = (-1, 0), (0, 1), (1, 0), (0, -1)
damage = [0]*(L+1)

# 체스판의 왼쪽 상단은 (1,1)로 시작
#  N 개의 줄에 걸쳐서 초기 기사들의 정보가 주어짐 (r,c,h,w,k) 순
# 기사의 처음 위치는 (r,c)를 좌측 상단 꼭지점으로 하며 세로 길이가 h, 가로 길이가 w인 직사각형 형태
#  초기 체력이 k

# 처음 주어지는 기사들의 위치는 기사들끼리 서로 겹쳐져 있지 않습니다.
# 또한 기사와 벽은 겹쳐서 주어지지 않습니다.
for i in range(1, N+1):
    r, c, h, w, k = map(int, input().split())
    # print(r, c, h, w, k)
    r -= 1
    c -= 1
    for y in range(r, r+h):
        for x in range(c, c+w):
            gisa_arr[y][x] = i
    gisa_hp[i] = k
    gisa_info.append([r, c, h, w])


# 다음 Q 개의 줄에 걸쳐 왕의 명령  (i,d) 형태
# 이는 i번 기사에게 방향 d로 한 칸 이동하라는 명령
# i는 1 이상 N 이하의 값을 갖으며, 이미 사라진 기사 번호가 주어질 수도 있음에 유의
# d는 0, 1, 2, 3 중에 하나  / 위쪽, 오른쪽, 아래쪽, 왼쪽 방향


for q in range(Q):
    i, d = map(int, input().split())
    # print(f"=================={i}번 기사를 {DIR[d]} 방향으로 밀기 ===============")

    # 체스판에서 사라진 기사에게 명령을 내리면 아무런 반응이 없게 됩니다
    if gisa_hp[i]<=0:
        continue

    # (1) 기사 이동
    #  기사는 상하좌우 중 하나로 한 칸 이동
    r, c, h, w = gisa_info[i]
    di, dj = DIR[d]

    flag = False
    #내가 이동할 칸이 모오두 빈 칸인지 체크(기사가 있는지 없는지 !! )
    #기사도 벽도 아예 없다. 한칸 이동 가능이야
    if check(i, 1, di, dj):
        # print("그냥 이동 가능")
        move(i, di, dj)
        # print_gisa()
        continue

    #밀 기사나 벽이 잇다면
    push_lst = []
    visited = [0] * (N + 1)
    nr, nc = r, c
    if di != 0:
        nr = r + h - 1 if di > 0 else r
        line_visited= [0]*w
    else:
        nc = c + w - 1 if dj > 0 else c
        line_visited= [0]*h

    while 1:
        if di!=0:
            #이 라인 밀 기사 다 체크
            for j in range(c, c + w):
                if line_visited[j-c]:
                    continue
                if gisa_arr[nr][c]==0:
                    line_visited[j-c] = 1
                    continue
                if gisa_arr[nr][j] != 0 and gisa_arr[nr][j] != i and not visited[gisa_arr[nr][j]]:
                    push_lst.append(gisa_arr[nr][j])
                    visited[gisa_arr[nr][j]] = 1
            nr += di
            if not (0<=nr<L):
                break
        else:
            for j in range(r, r + h):
                if line_visited[j-r]:
                    continue
                if gisa_arr[j][nc]==0:
                    line_visited[j-r] = 1
                    continue
                if gisa_arr[j][nc] != 0  and gisa_arr[j][nc] != i and not visited[gisa_arr[j][nc]]:
                    push_lst.append(gisa_arr[j][nc])
                    visited[gisa_arr[j][nc]] = 1
            nc += dj
            if not (0<=nc<L):
                break
    # print("push lst")
    # print(push_lst)

    #모든 기사 이동불가 벽 만남
    if not push_lst:
        # print("밀어낼 기사가 없다")
        continue
    #이동 불가일 경우
    if not is_possible(push_lst, di, dj):
        # print("이동이 불가능하다")
        continue

    # 만약 이동하려는 위치에 다른 기사가 있다면 그 기사도 함께 연쇄적으로 한 칸 밀려나
    # 그 옆에 또 기사가 있다면 연쇄적으로 한 칸씩 밀리게 됩니다
    # print("이동해보자 !!!!!!!!!!1")
    while push_lst:
        num = push_lst.pop()
        # print("num : ", num , "이동")
        move(num, di, dj)

        # print_gisa()

        # (2) 대결 대미지
        # 밀려난 기사들은 피해
        # 기사가 이동한 곳에서 w×h 직사각형 내에 놓여 있는 함정의 수만큼만 피해
        #  피해를 받은 만큼 체력이 깎이게 되며, 현재 체력 이상의 대미지를 받을 경우
        # 단, 명령을 받은 기사는 피해를 입지 않으며, 기사들은 모두 밀린 이후에 대미지를 입게 됩니다.

        damage = get_damage(num)
        # print("damage : ", damage)
        gisa_damage[num] += damage
        gisa_hp[num] -= damage
        if gisa_hp[num]<=0:
            kill(num)

    # print('=============자기 자신 이동=========')
    move(i, di, dj)
    #
    # print_gisa()
    #
    # print("damage 정보")
    # print(gisa_damage)
    # print('hp 정보')
    # print(gisa_hp)
    # print('gisa info')
    # print(gisa_info)

    # print("=========================================")



#  Q 번의 대결이 모두 끝난 후 생존한 기사들이 총 받은 대미지의 합을 출력
print(sum(gisa_damage))