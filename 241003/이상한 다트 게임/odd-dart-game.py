"""


Routine
1. 문제 그냥 정독 ok
2. 문제 주석 복사 ok
4. 테스트케이스 외에 고려해야할 사항 생각해보기 + 설계에 반영

5. 종이에 손설계 OK
6. 주석으로 구현할 영역 정리 : ok !
7. 구현 : ok
8.테스트케이스 단계별 디버깅 확인 : ok 했지만 굉장히 눈 똑바로 안뜨고 본듯
9. 1시간 지났는데 디버깅 헤매는 중이면 리셋!!

"""

"""
게임판은 중심은 모두 같고 반지름이 차이나는 원판들로 구성
원판의 반지름이 r이라고 할 때, 그 원판을 r번째 원판
각각의 원판에는 m개의 정수가 적혀있고, r번째 원판에 적힌 m번째 정수를 (r, m)


각각 원판의 회전은 독립적
회전 요청은 회전하는 원판의 종류 x, 방향 d, 회전 칸 수 k

 x의 경우 회전하는 원판의 번호가 x의 배수일 경우 회전
 d의 경우 시계 방향과 반시계 방향으로 주어지며 k의 경우 몇 칸을 회전시킬지 결정함
 
 시계 방향일 경우 1번째 정수를 1+k번째 정수 위치에 위치하도록 돌리는 것을 의미
반시계 방향일 경우에는 m번째 정수를 m-k번째 정수 위치에 위치하도록 돌리는 것을 의미

인접 
원판끼리는 1, n 연결 x
원판 안에서는 1, n 연결 !! 

 1번부터 n번까지의 원판에 지워지는 수가 없는 경우에는 원판 전체에 적힌 수의 평균을 구해서 정규화
 전체 원판에서 평균보다 큰 수는 1을 빼고, 작은 수는 1을 더해주는 과정
 평균을 구할 때는 편의상 소숫점 아래의 수는 버립니다.


출력 
원판을 q번 회전시킨 후 원판에 남아있는 수의 합
"""
from collections import deque


# bfs 구현

def bfs(i, j):
    q = deque([(i, j)])
    visited[i][j] = 1
    lst = [(i, j)]

    while q:
        cr, cc = q.popleft()
        for di, dj in (-1, 0), (0, 1), (1, 0), (0, -1):
            du, dv = cr + di, cc + dj
            if du < 1 or du > N: continue  # 원판은 1, N 연결 안됨
            dv %= M

            if visited[du][dv] or arr[du][dv] != arr[i][j]: continue
            visited[du][dv] = 1
            q.append((du, dv))
            lst.append((du, dv))

    if len(lst) > 1:
        for r, c in lst:
            arr[r][c] = -1
    return len(lst) - 1


# 입력 / 배열 준비
N, M, Q = map(int, input().split())
arr = [-1] + [deque(list(map(int, input().split()))) for _ in range(N)]

# for 문 (Q번 진행)
for q in range(Q):
    # 입력
    x, d, k = map(int, input().split())
    d = 1 if d == 0 else -1
    # 회전시키기
    for t in range(x, N + 1, x):
        # print(k)
        arr[t].rotate(d * k)

    # print("==============회전 테스트 ==================")
    # for t in range(1, N+1):
    #     print(arr[t])
    # print("=========================================")

    # 인접 같은 숫자 삭제 -> BFS 활용 . -1 로 만들기
    # 삭제 여부 flag 활용
    flag = False
    visited = [[0] * M for _ in range(N+1)]
    for i in range(1, N + 1):
        for j in range(M):
            if not visited[i][j]:
                result = bfs(i, j)
                if result: flag = 1

    # print("==============수 지우기 테스트 =====================")
    # for t in range(1, N+1):
    #     print(arr[t])
    # print("==============================================")

    # 삭제된 적 없으면 정규화를 위한 평균 구하기
    if flag: continue
    s = 0
    cnt = 0
    for i in range(1, N+1):
        for j in range(M):
            if arr[i][j]==-1:
                continue
            cnt+=1
            s += arr[i][j]
    # cnt == 0 이면 정규화 안함
    if cnt == 0: break
    # 정규화하기
    arr_mean = s//cnt
    for i in range(1, N+1):
        for j in range(M):
            if arr[i][j] == -1: continue
            if arr[i][j]>arr_mean:
                arr[i][j] -= 1
            elif arr[i][j]<arr_mean:
                arr[i][j]+=1
ans = 0
for i in range(1, N+1):
    for j in range(M):
        if arr[i][j]==-1: continue
        ans += arr[i][j]

print(ans)