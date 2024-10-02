"""
크기가 3 * 3인 격자판

연산
- 행의 개수가 열의 개수보다 크거나 같은 경우
    모든 행에 대하여 정렬을 수행
    정렬 기준은 출현 빈도 수가 적은 순서대로 정렬
    출현하는 횟수가 같은 숫자가 있는 경우에는 해당 숫자가 작은 순서대로 정렬을 수행
    정렬을 수행할 때 숫자와 해당하는 숫자의 출현 빈도 수를 함께 출력

- 행의 개수가 열의 개수보다 작은 경우
    모든 열에 대해 위의 과정을 수행해줍니다.
행이나 열의 길이가 100을 넘어가는 경우에는 처음 100개의 격자를 제외하고는 모두 버립니다.

특정 A[r][c]의 값이 원하는 값이 되는데까지 걸리는 시간을 구하는 프로그램
A[r][c]의 값이 k가 되기 위한 최소 시간을 출력
목표 숫자에 도달하는 것이 불가능하거나 답이 100초를 초과한다면 -1을 출력
"""

R, C, K = map(int, input().split())
R-=1
C-=1
arr = [list(map(int, input().split())) for _ in range(3)]
answer = 0

while 1:
    if answer > 100:
        answer = -1
        break

    row_len = len(arr)
    col_len = len(arr[0])
    if R<row_len and C < col_len and arr[R][C]==K:
        break

    answer+=1
    mx_len = min(row_len, col_len)

    if row_len < col_len:
        arr = list(map(list, zip(*arr)))

    for i in range(len(arr)):
        visited = [0]*101
        tmp = []
        for j in range(len(arr[i])):
            v = arr[i][j]
            if v ==0 or visited[v]: continue
            visited[v] = 1
            tmp.append([v, arr[i].count(v)])
        tmp.sort(key = lambda x : (x[1], x[0]))
        new_lst = []
        for x in tmp:
            new_lst.extend(x)
            if len(new_lst)==100:
                break
        arr[i] = new_lst[:]
        mx_len = max(mx_len, len(arr[i]))

    for i in range(len(arr)):
        while len(arr[i]) < mx_len:
            arr[i].append(0)

    if row_len < col_len:
        arr = list(map(list, zip(*arr)))


print(answer)