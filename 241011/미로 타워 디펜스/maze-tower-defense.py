def set_route_lst():
    r, c = N // 2, N // 2
    l = 1
    cnt = 0

    while 1:
        for di, dj in (0, -1), (1, 0), (0, 1), (-1, 0):
            for t in range(l):
                r += di
                c += dj
                route_lst.append((r, c))
                if r == 0 and c == 0:
                    return
            cnt += 1
            if cnt == 2:
                l += 1
                cnt = 0

def pull():
    k = 0
    while k<N*N-1:
        r, c = route_lst[k]
        if arr[r][c]!=0:
            k+=1
            continue
        idx = k
        du, dv = r, c
        while arr[du][dv]==0 :

            idx += 1
            if idx>=N*N-1: break
            du, dv = route_lst[idx]

        if idx==N*N-1:
            break
        arr[r][c] = arr[du][dv]
        arr[du][dv] = 0



def oob(r, c):
    return r < 0 or c < 0 or r >= N or c >= N


def printa(string, arr):
    print(f"====================={string} ===================")
    for i in range(N):
        print(arr[i])
    print("=================================================")
    print()

N, M = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
route_lst = []
DIR = (0, 1), (1, 0), (0, -1), (-1, 0)
C_r, C_c = N // 2, N // 2
answer = 0
# print(route_lst)

set_route_lst()


def find_continuous(i):
    r, c = route_lst[i]
    num = arr[r][c]
    cnt = 1
    idx = i+1
    while idx<N*N-1:
        nr, nc = route_lst[idx]
        if arr[nr][nc] != num:
            break
        cnt+=1
        idx+=1
    return cnt

for m in range(M):
    d, s = map(int, input().split())

    tr, tc = N // 2, N // 2
    di, dj = DIR[d]
    for t in range(1, s+1):
        tr += di
        tc += dj
        if oob(tr, tc): break
        answer += arr[tr][tc]
        arr[tr][tc] = 0
    # printa("공격 후 ", arr)
    #당기기
    pull()
    # printa("당긴 후 ", arr)


    while 1:
        flag = False
        #4개 이상인지 개수 찾기
        for i in range(N*N -1):
            r, c = route_lst[i]
            if arr[r][c] == 0: break
            cnt = find_continuous(i)
            if cnt<4: continue
            flag = True
            answer += (cnt * arr[r][c])
            for j in range(i, i+cnt):
                du, dv = route_lst[j]
                arr[du][dv] = 0
        if not flag:
            break
        pull()

    # printa("제거 후 ", arr)

    lst = []
    pointer = 0
    while 1:
        r, c = route_lst[pointer]
        num = arr[r][c]
        if num==0:
            break
        cnt = find_continuous(pointer)
        lst.extend([cnt, num])
        if len(lst) >= N*N-1:
            lst = lst[:N*N-1]
            break
        pointer += cnt
        if pointer>=N*N-1:
            break

    while len(lst)<N*N-1:
        lst.append(0)

    for i in range(N*N-1):
        r, c = route_lst[i]
        arr[r][c] = lst[i]
    # printa("완료 후 ", arr)
print(answer)