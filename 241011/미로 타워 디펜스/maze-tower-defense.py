def oob(i, j):
    return i < 0 or j < 0 or i >= N or j >= N


N, M = map(int, input().split())

arr = [list(map(int, input().split())) for _ in range(N)]
answer = 0
DIR = (0, 1), (1, 0), (0, -1), (-1, 0)


def set_lst():
    r, c = N // 2, N // 2
    cnt = 0
    l = 1
    result_lst = []
    while 1:
        for di, dj in (0, -1), (1, 0), (0, 1), (-1, 0):
            for t in range(l):
                r += di
                c += dj

                if arr[r][c] != 0:
                    result_lst.append(arr[r][c])
                if r == 0 and c == 0:
                    return result_lst
            cnt += 1
            if cnt == 2:
                l += 1
                cnt = 0
    return result_lst


def delete_continuous(lst):
    global answer
    result_lst = []
    tmp_lst = []
    bf = -1
    flag = False
    for i in range(len(lst)):
        if lst[i] != bf:
            if len(tmp_lst) < 4:
                result_lst.extend(tmp_lst)
            else:
                answer += bf * len(tmp_lst)
                flag = True
            tmp_lst = [lst[i]]
            bf = lst[i]
        else:
            tmp_lst.append(lst[i])
    if len(tmp_lst)>=4:
        answer += bf*len(tmp_lst)
    else:
        result_lst.extend(tmp_lst)
    return result_lst, flag


def make_new_lst(lst):
    result_lst = []
    tmp_lst = []
    bf = -1
    for i in range(len(lst)):
        if bf == lst[i]:
            tmp_lst.append(lst[i])
        else:
            if bf!=-1: result_lst.extend([len(tmp_lst), bf])
            tmp_lst = [lst[i]]
            bf = lst[i]

    if bf!=-1: result_lst.extend([len(tmp_lst), bf])
    return result_lst


def set_arr(lst):
    r, c = N // 2, N // 2
    cnt = 0
    l = 1
    idx = 0
    while 1:
        for di, dj in (0, -1), (1, 0), (0, 1), (-1, 0):
            for t in range(l):
                r += di
                c += dj
                arr[r][c] = lst[idx]
                idx += 1
                if idx == len(lst):
                    return
                if r == 0 and c == 0:
                    return
            cnt += 1
            if cnt == 2:
                l += 1
                cnt = 0


for m in range(M):
    d, p = map(int, input().split())
    di, dj = DIR[d]
    r, c = N // 2, N // 2
    for s in range(p):
        r += di
        c += dj
        if oob(r, c): break
        answer += arr[r][c]
        arr[r][c] = 0


    # 0제외한 숫자 목록
    lst = set_lst()


    # lst에서 연속인 수 제거하고 당기기
    while 1:
        lst, flag = delete_continuous(lst)

        if not flag:
            break

    # 같은 수 체크해서 새로 lst만들기
    lst = make_new_lst(lst)
    arr = [[0] * N for _ in range(N)]
    set_arr(lst)

print(answer)