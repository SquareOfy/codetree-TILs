"""

i번 줄의 결과는 무조건 i번으로 가야한다
사다리 게임의 가로선에 해당하는 것은 메모리 유실선이 있을 수 있는 위치
이를 취약 지점이라 하며 이웃한 선과만 이어질 수 있습니다.
승용이는 적절하게 메모리 유실선을 추가하여 버그를 고치고자 합니다.
메모리 유실선을 추가할 때 아래와 같이 선이 겹쳐지도록 추가하는 것은 불가능
최소한의 메모리 유실선을 추가해서 버그를 없애는 프로그램

고객의 수 n, 메모리 유실 선의 개수 m, 취약 지점의 개수 h
취약 지점이 a, 메모리 유실이 일어난 지점을 b
a번째 취약 지점에서 b번째 고객에서 (b+1)번째 고객에게로 메모리 유실이 일어났다
1번부터 시작하며 오른쪽으로 갈수록 1씩 증가

취약지점의 번호도 1번부터 시작하며 아래쪽으로 갈수록 1씩 증가

버그를 고치기 위해 필요한 메모리 유실 선의 개수의 최솟값을 출력
만약 필요한 선의 개수가 3보다 큰 값이거나 버그를 고치는 것이 불가능하다면 -1을 출력
"""

# oob
def oob(i, j):
    return i<0 or i>=H or j<0 or j>=N

# 타고 내려가는 함수
def down():
    result = [0]*(N+1)
    for j in range(1, N+1):
        col = j
        for h in range(1, H+1):
            if arr[h][col]==1:
                col +=1
            elif arr[h][col-1]==1:
                col -=1
        result[col] = j


    return result

#check 함수
def check(result):
    for i in range(1, N+1):
        if i!=result[i]:
            return False
    return True

#dfs
def dfs(level, idx):
    global answer
    if answer != -1 and answer <= level:
        return
    result = down()
    if check(result):
        answer = level
        return
    if level==3:
        return

    for i in range(idx, len(blank_lst)):
        r, c = blank_lst[i]
        if (c-1>=1 and arr[r][c-1]) or arr[r][c] or (c+1<=N and arr[r][c+1]): continue
        arr[r][c] = 1
        dfs(level+1, i+1)
        arr[r][c] = 0



#입력, 배열 세팅
N, M, H = map(int, input().split())
arr = [[0]*(N+1) for _ in range(H+1)]
for m in range(M):
    a, b = map(int, input().split())
    arr[a][b] = 1

answer = -1

#빈곳 배열 세팅
blank_lst = []
for i in range(1, H+1):
    for j in range(1, N):
        if arr[i][j] == 0:
            blank_lst.append((i, j))

dfs(0, 0)
print(answer)