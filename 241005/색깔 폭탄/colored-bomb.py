from collections import deque
#bfs
    # 빨간색 lst 받아서 visited 해제 + len 반환
def bfs(i, j):
    q = deque([(i, j)])
    visited[i][j] = 1
    lst = []
    red_lst = []

    while q:
        cr, cc = q.popleft()
        lst.append((cr, cc))

        for di, dj in DIR:
            du, dv = cr+di, cc+dj
            if oob(du, dv) or visited[du][dv] or arr[du][dv] < 0: continue
            if arr[du][dv]>0 and arr[du][dv]!=arr[i][j]: continue

            if arr[du][dv] == 0:
                red_lst.append((du, dv))
            q.append((du, dv))
            visited[du][dv] = 1
    #빨간색 체크 해제
    for r, c in red_lst:
        visited[r][c] = 0
    if len(lst) <2:
        lst = []

    return lst, len(red_lst)
#gravity
    #밑에서부터 -2 찾아서 끌어내릴 숫자 찾으면 끌어내리는 방식
def gravity(arr):
    for c in range(N):
        #밑에서부터 보면서 빈칸이 나오는 순간(r)에 땡겨올 폭탄(0 또는 1~M)(nr) 찾아서 땡기기
        r = N # 1빼고 시작할거라 1부터 시작
        while r>0:
            r -= 1
            if arr[r][c] != -2: continue
            nr = r-1
            while not oob(nr, c) and arr[nr][c] == -2:
                nr -= 1
            #땡겨올 애가 없으면 다음칸 보기
            if oob(nr, c) or arr[nr][c] == -1:
                r = nr
                continue
            arr[r][c] = arr[nr][c]
            arr[nr][c] = -2
    return arr

#oob
def oob(r, c):
    return r<0 or c<0 or r>=N or c>=N

def pr(string):
    print(f"================={string}=============")
    for i in range(N):
        print(arr[i])
    print("=======================================")
    print()
#입력
N, M = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
DIR = (-1, 0), (0, 1), (1, 0), (0, -1)

answer = 0
#while
while 1:
    visited = [[0]*N for _ in range(N)]
    bomb_cand_lst = []
    #1. 폭탄 리스트 찾아서 터질 폭탄 구하기
    #전체 돌며 visited
    for i in range(N-1, -1, -1): #행이 클수록 기준점
        for j in range(N): #열이 작을수록 기준점
            if not visited[i][j] and arr[i][j]>0:
                lst, cnt = bfs(i, j)
                if not lst: continue
                bomb_cand_lst.append((lst, cnt))


    #폭탄 후보 비어있으면 break
    if not bomb_cand_lst:
        break

    bomb_cand_lst.sort(key = lambda x:(-len(x[0]), x[1], -x[0][0][0], x[0][0][1]))
    bomb_lst = bomb_cand_lst[0][0]
    #2. 폭탄 터뜨리기 + 중력
    for r, c in bomb_lst:
        arr[r][c] = -2
    # pr("폭탄 터트린 후 ")

    arr = gravity(arr)
    # pr("1차 중력 후 1!!")
    #3. 회전
    arr = list(map(list, zip(*arr)))[::-1]
    # pr("회전 후")
    #4. 중력
    arr = gravity(arr)
    # pr("마지막 중력 후 ")
    #점수 더하기
    answer += (len(bomb_lst))**2
print(answer)