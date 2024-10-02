"""

Routine
1. 문제 그냥 정독 ok
2. 문제 주석 복사 ok
4. 테스트케이스 외에 고려해야할 사항 생각해보기 + 설계에 반영
    : lst 거꾸로 돌아야한다는 것
5. 종이에 손설계 OK
6. 주석으로 구현할 영역 정리 : ok
7. 구현 : ok
8.테스트케이스 단계별 디버깅 확인 : 디버깅할게 없었음
9. 1시간 지났는데 디버깅 헤매는 중이면 리셋!!
"""

"""
n * n 격자판에 m개의 몬스터와 하나의 전투로봇
한 칸에는 몬스터가 최대 하나만 존재
초기의 전투로봇의 레벨은 2,  전투로봇은 1초에 상하좌우로 인접한 한 칸씩 이동

자신의 레벨보다 큰 몬스터가 있는 칸은 지나칠 수 없고, 나머지 칸은 모두 지날 수 있습니다. 
전투로봇은 자신의 레벨보다 낮은 몬스터만 없앨 수 있습니다. 

없앨 수 있는 몬스터가 있다면 해당 몬스터를 없애러 갑니다.
없앨 수 있는 몬스터가 하나 이상이라면, 거리가 가장 가까운 몬스터를 없애러 갑니다.
    거리는 해당 칸으로 이동할 때 지나야하는 칸의 개수의 최솟값
    가장 가까운 거리의 없앨 수 있는 몬스터가 하나 이상
    => 가장 위에 존재하는 몬스터 ->  가장 왼쪽에 존재하는 몬스터
없앨 수 있는 몬스터가 없다면 일을 끝냅니다.

전투로봇이 한 칸 이동하는데에는 1초
몬스터를 없애는 시간은 없다.  몬스터가 있는 칸에 도달하면 바로 몬스터가 없어집니다. 
몬스터를 없애면 해당 칸은 빈칸
전투 로봇은 본인의 레벨과 같은 수의 몬스터를 없앨 때마다 레벨이 상승

전투 로봇이 일을 끝내기 전까지 걸린 시간
"""
from collections import deque

def oob(i, j):
    return i<0 or j<0 or i>=N or j>=N

def find_monster():
    q= deque([(r, c, 0)])
    visited=  [[0]*N for _ in range(N)]
    visited[r][c] = 1
    ar, ac = N, N
    arank = N*N
    while q:
        cr, cc, rank = q.popleft()
        if arr[cr][cc] != 0 and arr[cr][cc] < level and arank>=rank:
            if arank>rank or (arank==rank and (ar, ac)>(cr, cc)):
                ar, ac = cr, cc
                arank = rank

            continue
        for di, dj in (-1, 0), (0, 1), (1, 0), (0, -1):
            du, dv = cr+di, cc+dj
            if oob(du, dv): continue
            if visited[du][dv]: continue
            if arr[du][dv]>level: continue
            q.append((du, dv, rank+1))
            visited[du][dv] = 1

    return ar, ac, arank

N = int(input())
arr = [list(map(int, input().split())) for _ in range(N)]
for i in range(N):
    for j in range(N):
        if arr[i][j] == 9:
            r, c = i, j
            arr[i][j] = 0
level = 2
cnt = 0
answer = 0
while 1:

    nr, nc, time = find_monster()
    if nr==N:
        break

    r, c = nr, nc
    answer += time
    arr[r][c] = 0
    cnt+=1
    if cnt==level:
        level+=1
        cnt=0
print(answer)