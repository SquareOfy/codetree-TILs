"""

n * n개의 격자에 1 * 1 크기의 계란틀
계란틀을 이루는 4개의 선은 분리가 가능

계란의 양이 너무 차이나지 않게 하기 위해
하나의 선을 맞대고 있는 두 계란틀의 계란의 양의 차이가 L 이상 R 이하라면
계란틀의 해당 선을 분리합니다.

모든 계란틀에 대해 검사를 실시하고 위의 규칙에 해당하는 모든 계란틀의 선을 분리합니다.

선의 분리를 통해 합쳐진 계란틀의 계란은 하나로 합치고 이후에 다시 분리합니다.

합쳤다 다시 분리한 이후의 각 계란틀별 계란의 양은
 (합쳐진 계란의 총 합)/(합쳐진 계란틀의 총 개수)가 됩니다. 편의상 소숫점은 버립니다.

계란의 이동이 더 이상 필요 없을 때까지 해당 과정
"""
from collections import deque

def bfs(i, j):
    q = deque([(i, j)])
    visited[i][j] = 1
    e_sum = 0
    lst = []
    while q:
        cr, cc = q.popleft()
        v = arr[cr][cc]
        lst.append((cr, cc))
        e_sum+= arr[cr][cc]
        for di, dj in (-1, 0), (0, 1), (1, 0), (0, -1):
            du = cr+di
            dv = cc+dj
            if du<0 or dv<0 or du>=N or dv>=N:
                continue
            if visited[du][dv]:
                continue
            if L<= abs(v-arr[du][dv]) <=R:
                visited[du][dv] = 1
                q.append((du, dv))
    if len(lst)>1:
        return (e_sum, lst)
    visited[i][j] = 0
    return 0, []

N, L, R = map(int, input().split())

arr = [list(map(int, input().split())) for _ in range(N)]
answer = 0
while 1:

    visited = [[0]*N for _ in range(N)]
    eggs_lst = [] #계란 합, 좌표lst 담을 것
    # 합칠 계란틀 lst 준비
    for i in range(N):
        for j in range(N):
            if not visited[i][j]:
                e_sum, lst = bfs(i, j)
                if lst:
                    eggs_lst.append((e_sum, lst))

    #lst 비어있으면 종료
    if not eggs_lst:
        break
    #아니면 돌면서 배열 갱신
    for sum_, lst in eggs_lst:
        v = sum_ // len(eggs_lst)
        for r, c in lst:
            arr[r][c] = v
    answer += 1
print(answer)