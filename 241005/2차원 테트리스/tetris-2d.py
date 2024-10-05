def change_t(i):
    if t==1:
        return t
    return 2 if t==3 else 3

#블록 내린 후 배열 반환 함수
def down_block(t, c, arr):
    mxr = 5

    for i in range(6):
        if arr[i][c] == 1:
            mxr = i-1
            break
    if t==2:
        for i in range(6):
            if arr[i][c+1]==1:
                mxr = min(i-1, mxr)
                break

    lst = [mxr]
    arr[mxr][c] = 1
    if t==2:
        arr[mxr][c+1] = 1
    elif t==3:
        arr[mxr-1][c] = 1
        lst.append(mxr-1)

    return arr, lst

# 주어진 행이 지워지면 지울 행 반환하는 함수
def check_delete(arr, lst):
    delete_lst = []
    for r in lst:
        for j in range(4):
            if arr[r][j] == 0:
                break
        else:
            delete_lst.append(r)
    return delete_lst

# 연한 부분 지워지면 지울 행 반환하는 함수
def check_delete_light(arr):
    cnt = 0
    for i in range(2):
        for j in range(4):
            if arr[i][j] == 1:
                cnt+=1
                break
    lst = []
    for i in range(cnt):
        lst.append(5-i)
    return lst

# 리스트에 있는 행 지우고 아래로 내리는 함수
def delete_arr(delete_lst, arr):
    cnt = len(delete_lst)
    mxr = max(delete_lst)
    for i in range(mxr, cnt-1, -1):
        arr[i][:] = arr[i-cnt]
        arr[i-cnt] = [0]*4
    # for i in range(cnt):
    #     arr[cnt] = [0]*4
    return arr

#입력
K = int(input())
yellow = [[0]*4 for _ in range(6)]
red = [[0]*4 for _ in range(6)]
answer = 0
blocks = 0

#입력 for문 => 블록 내리기 지우기 연한부분 확인하고 지우기 반복
for k in range(K):
    t, x, y = map(int, input().split())

    yellow, yellow_fill_lst = down_block(t, y, yellow)
    red, red_fill_lst = down_block(change_t(t), x, red)

    y_delete_lst = check_delete(yellow, yellow_fill_lst)
    r_delete_lst = check_delete(red, red_fill_lst)
    answer += len(y_delete_lst)+len(r_delete_lst)

    if y_delete_lst: yellow = delete_arr(y_delete_lst, yellow)
    if r_delete_lst: red = delete_arr(r_delete_lst, red)
    y_delete_lst = check_delete_light(yellow)
    r_delete_lst = check_delete_light(red)
    if y_delete_lst:
        yellow = delete_arr(y_delete_lst, yellow)

    if r_delete_lst:
        red = delete_arr(r_delete_lst, red)
print(answer)
for r in range(6):
    blocks += sum(yellow[r]) + sum(red[r])
print(blocks)