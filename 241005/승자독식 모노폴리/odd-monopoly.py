# dir 번호 감소 함수
def change_dir_idx(i):
    return int(i) - 1


def oob(i, j):
    return i < 0 or j < 0 or i >= N or j >= N

def pr_arr(string, arr):
    print(f"====================={string}===================")
    print("=======================arr=======================")
    for i in range(N):
        print(arr[i])
    print("================================================")
    print()
def pr_cnt_arr(string):
    print(f"====================={string}===================")
    print("=======================cnt_arr=======================")
    for i in range(N):
        print(cnt_arr[i])
    print("================================================")
    print()
# 입력
N, M, K = map(int, input().split())

# 필요배열 준비
arr = [list(map(int, input().split())) for _ in range(N)]
DIR = (-1, 0), (1, 0), (0, -1), (0, 1)
player_dir_lst = [-1]+list(map(change_dir_idx, input().split())) # 초기방향
priority_info = [-1]
for m in range(M):
    p_lst = [list(map(change_dir_idx, input().split())) for _ in range(4)]
    priority_info.append(p_lst)
cnt_arr = [[[0] * 2 for _ in range(N)] for _ in range(N)]  # 독점 횟수 cnt할 배열
turn = 0
cnt = M
# while 문
while 1:
    # 내 자리 독점하기
    for i in range(N):
        for j in range(N):
            if arr[i][j] == 0: continue
            cnt_arr[i][j] = [arr[i][j], K]

    # 종료조건
    if cnt == 1:
        break
    if turn > 1000:
        turn = -1
        break
    # 턴 추가
    turn += 1
    tmp = [[0] * N for _ in range(N)]
    # arr 돌면서 플레이어 이동(tmp 생성)
    for i in range(N):
        for j in range(N):
            if arr[i][j] == 0: continue  # 플레이어 없으면 지나가기
            n = arr[i][j]
            my_d = player_dir_lst[n]
            # 내 우선순위 방향 배열 찾아오기
            dir_lst = priority_info[n][my_d]

            # 빈칸 찾기 : 이동 시 사람 있으면 대소비교 cnt -=1
            for d in dir_lst:
                di, dj = DIR[d]
                du, dv = i + di, j + dj
                if oob(du, dv): continue
                if cnt_arr[du][dv] != [0, 0]: continue
                # 빈칸이면 가보기
                # tmp에 이미 누군가가 있다면?
                if tmp[du][dv]:
                    cnt -= 1
                    if n < tmp[du][dv]:
                        tmp[du][dv] = n
                        player_dir_lst[n] = d
                else:
                    tmp[du][dv] = n
                    player_dir_lst[n] = d
                break
            # 빈칸 없으면 내자리 찾기 : 이동 시 사람 있으면 대소비교 cnt -=1
            else:
                for d in dir_lst:
                    di, dj = DIR[d]
                    du, dv = i + di, j + dj
                    if oob(du, dv): continue
                    if cnt_arr[du][dv][0] == n:
                        tmp[du][dv] = n #다른 놈이 와있을리 없으니 그냥 내가 가기
                        player_dir_lst[n] = d
                        break

    # 이동 완료 후 기존 cnt배열 감소시키기
    for i in range(N):
        for j in range(N):
            if cnt_arr[i][j][0]!=0:
                cnt_arr[i][j][1]-=1
                if cnt_arr[i][j]==0:
                    cnt_arr[i][j] = [0, 0]

    # tmp에 사람 있으면 갱신하기
    for i in range(N):
        arr[i] = tmp[i][:]
print(turn)