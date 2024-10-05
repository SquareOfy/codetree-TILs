"""
n x n으로 이뤄진 나선형 미로 속에 1번, 2번, 3번 몬스터들이 침략

1. 플레이어는 상하좌우 방향 중 주어진 공격 칸 수만큼 몬스터를 공격하여 없앨 수 있습니다.
     삭제되는 몬스터의 번호는 점수에 합쳐집니다.

2. 비어있는 공간만큼 몬스터는 앞으로 이동하여 빈 공간을 채웁니다.

3. 이때 몬스터의 종류가 4번 이상 반복하여 나오면 해당 몬스터 또한 삭제됩니다.
   삭제되는 몬스터의 번호는 점수에 합쳐집니다.
    해당 몬스터들은 동시에 사라집니다.
    삭제된 이후에는 몬스터들을 앞으로 당겨주고, 4번 이상 나오는 몬스터가 있을 경우 또 삭제를 해줍니다.
    4번 이상 나오는 몬스터가 없을 때까지 반복해줍니다.

4.삭제가 끝난 다음에는 몬스터를 차례대로 나열했을 때 같은 숫자끼리 짝을 지어줍니다.
    이후 각각의 짝을 (총 개수, 숫자의 크기)로 바꾸어서 다시 미로 속에 집어넣습니다.

새로 생긴 배열이 원래 격자의 범위를 넘는다면 나머지 배열은 무시합니다.

"""
#달팽이 만드는 함수
def make_route():
    r, c = N//2, N//2
    route_lst.append((r, c))
    l = 1
    cnt = 0
    idx = 1
    while 1:
        for di, dj in (0, -1), (1, 0), (0, 1), (-1, 0):
            for k in range(l):
                r += di
                c += dj
                route_lst.append((r, c))
                idx_arr[r][c] = idx
                idx+=1
                if r==0 and c==0:
                    return
            cnt+=1
            if cnt==2:
                cnt=0
                l+=1

def make_lst():
    for i in range(1, N*N):
        r, c = route_lst[i]
        if arr[r][c] == 0: continue
        lst.append(arr[r][c])
    while len(lst)<N*N:
        lst.append(0)

#입력
N, M = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
idx_arr = [[0]*N for _ in range(N)]
DIR = (0, 1), (1, 0), (0, -1), (-1, 0)
route_lst = []
lst = [-1]
answer = 0
#초기 lst 세팅
make_route()
# print(route_lst)
# print(len(route_lst))
make_lst()

mr, mc = N//2, N//2
#라운드
for m in range(M):
    d, p = map(int, input().split())

    #공격하고 그자리 땡기기 ! (없애버려)
    di, dj = DIR[d]
    nr, nc = mr, mc
    for k in range(p):

        nr += di
        nc += dj
        idx = idx_arr[nr][nc]

        if lst[idx] == 0:
            continue
        answer += lst[idx]
        lst[idx:idx+1]=[]
        lst.append(0)

    #while flag로 관리
    #앞에서부터 4개 이상 연속인 애들 개수 세서 점수 더하기 + 없애기
    flag = True

    new_lst = [-1]
    while flag:
        bf = -1
        cnt = 0
        flag = False
        for i in range(1, len(lst)):
            last_flag = False
            if lst[i]==0:
                continue
            if bf == lst[i]:
                cnt += 1
            else:
                score = bf
                bf = lst[i]
                if cnt>=4:
                    flag = True
                    last_flag= True
                    answer += cnt*score
                else:
                    new_lst.extend([score]*cnt)
                cnt = 1

        if not flag:
            break
        if not last_flag:
            new_lst.extend([bf]*cnt)
        lst = new_lst[:]
        new_lst = [-1]
    lst = lst[:]+[0]*(N*N-len(lst))


    #배열 개수, 숫자 만들기
    bf = -1
    cnt = 0
    new_lst = [-1]
    for i in range(1, len(lst)):
        if lst[i]==0:
            continue
        if bf == lst[i]:
            cnt += 1
        else:
            if cnt!=0:
                new_lst.extend([cnt, bf])
                if len(new_lst)>=N*N:
                    lst = new_lst[:N*N+1]
                    break
            bf = lst[i]
            cnt = 1

    if cnt!=0: new_lst.extend([cnt, bf])
    lst = new_lst[:]+[0]*(N*N-len(new_lst))
print(answer)