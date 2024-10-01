"""
크기가 n * n인 인도 / 보도블럭의 높이

경사로는 높이가 1이며 길이 L

경사로는 높이 차이가 1이 나는 보도블럭에 설치가능하며, 낮은 칸에 설치
경사로의 길이 L동안 바닥에 접촉해야하며,
경사로가 놓인 보도블럭의 높이는 모두 같아야 합니다.


다음과 같은 경우에는 경사로를 놓을 수 없습니다.
높이 차이가 1 보다 큰 경우
경사로의 길이만큼 낮은 칸의 보도블럭이 연속하지 않는 경우
경사로를 놓은 곳에 또 경사로를 놓은 경우
"""
def is_possible_row(i):
    for j in range(1, N):
        if visited[i][j]: continue
        if abs(arr[i][j-1] - arr[i][j]) >1:
            return False
        if arr[i][j-1] == arr[i][j]: continue
        if arr[i][j-1]>arr[i][j]:
            #앞으로 총 L칸 확인하기
            if j+L >=N:
                return False
            for k in range(0, L):
                if arr[i][j+k] != arr[i][j] or visited[i][j+k]:
                    return False
                visited[i][j+k] = 1
        elif arr[i][j-1]<arr[i][j]:
            #뒤로 총 L칸 확인하기 (나 미포함)
            if j-L < 0:
                return False
            for k in range(1, L+1):
                if arr[i][j-k] != arr[i][j] or visited[i][j-k]:
                    return False
                visited[i][j-k] = 1
    return True

def is_possible_col(j):
    for i in range(1, N):
        if abs(arr[i-1][j] - arr[i][j]) >1:
            return False
        if arr[i-1][j] == arr[i][j]: continue
        if arr[i-1][j]>arr[i][j]:
            #앞으로 총 L칸 확인하기
            if i+L >=N:
                return False
            for k in range(0, L):
                if arr[i+k][j] != arr[i][j] or visited[i+k][j]:
                    return False
                visited[i+k][j] = 1
            visited[i][j] =1
        elif arr[i-1][j]<arr[i][j]:
            #뒤로 총 L칸 확인하기
            if i-L < 0:
                return False

            for k in range(1, L+1):
                if arr[i-k][j] != arr[i-1][j] or visited[i-k][j]:
                    return False
                visited[i-k][j] = 1
            visited[i][j] =1
    return True


N, L = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
visited = [[0]*N for _ in range(N)]
answer = 0
for i in range(N):
    #i행 가능한지 열 점검
    if is_possible_row(i):
        answer+=1

visited = [[0] * N for _ in range(N)]
for i in range(N):
    if is_possible_col(i):
        answer+=1

print(answer)