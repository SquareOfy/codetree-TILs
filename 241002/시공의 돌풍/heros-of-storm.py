"""
Routine
1. 문제 그냥 정독 ok
2. 문제 주석 복사 ok
4. 테스트케이스 외에 고려해야할 사항 생각해보기 + 설계에 반영
    : 행열 우선순위 bfs순서로 해결 안되는 것 주의
5. 종이에 손설계 OK
6. 주석으로 구현할 영역 정리 : no. 구현량이 많지 않았음
7. 구현 : ok
8.테스트케이스 단계별 디버깅 확인 : no... 왜 안했지 ,, 반성
9. 1시간 지났는데 디버깅 헤매는 중이면 리셋!!

"""

"""
n * m 크기의 격자칸
돌풍은 항상 1번 열에 설치  크기는 두 칸을 차지

1초 동안 방에는 다음과 같은 일이 일어납니다.

1. 먼지가 인접한 4방향의 상하좌우 칸으로 확산됩니다.
    인접한 방향에 시공의 돌풍이 있거나, 
    방의 범위를 벗어난다면 해당 방향으로는 확산이 일어나지 않습니다.
    확산되는 양은 원래 칸의 먼지의 양에 5를 나눈 값이며, 편의상 소숫점은 버립니다.
    각 칸에 확산될 때마다 원래 칸의 먼지의 양은 확산된 먼지만큼 줄어듭니다.
    . 확산된 먼지는 방에 있는 모든 먼지가 확산을 끝낸 다음에 해당 칸에 더해지게 됩니다.
    
2. 시공의 돌풍이 청소를 시작합니다.
    시공의 돌풍의 윗칸에서는 반시계 방향으로 바람
    아랫칸에서는 시계 방향으로 바람
    바람이 불면 먼지가 바람의 방향대로 모두 한 칸씩 이동합니다.
    시공의 돌풍으로 들어간 먼지는 사라집니다
    
시공의 돌풍이 설치되어 있는 칸은 -1로 표시
 항상 맨 왼쪽에 위치하며, 두 칸을 차지
 
 출력 : t초가 지난 이후 방에 남아있는 먼지의 양
 
"""
def oob(i, j):
    return i<0 or j<0 or i>=N or j>=M


def find_tornado():
    # 돌풍위치 찾기
    for i in range(N):
        for j in range(M):
            if arr[i][j] == -1:
                return i, i+1


#입력
N, M, T = map(int, input().split())

arr = [list(map(int, input().split())) for _ in range(N)]
up, down = find_tornado()

for t in range(T):
    tmp = [[0]*M for _ in range(N)]
    #먼지 확산
    for i in range(N):
        for j in range(M):
            if arr[i][j]==-1:
                tmp[i][j] = -1
                continue
            v = arr[i][j]//5
            cnt = 0
            for di, dj in (-1, 0), (0, 1), (1, 0), (0, -1):
                du, dv = i+di, j+dj
                if oob(du, dv) or arr[du][dv]==-1:
                    continue
                tmp[du][dv] += v
                cnt+=1
            tmp[i][j] += arr[i][j]-cnt*v

    #임시배열 반영
    for i in range(N):
        arr[i] = tmp[i][:]

    #돌풍


    cr, cc = up-1, 0
    k = 0
    #윗쪽
    for di, dj in (-1, 0), (0, 1), (1, 0), (0, -1):
        while 1:
            nr, nc = cr+di, cc+dj
            if oob(nr, nc): break #범위 아웃
            if nr==down: break
            if nr==up and nc==0: break
            arr[cr][cc] = arr[nr][nc]
            cr, cc = nr, nc
    arr[cr][cc] = 0

    #아랫쪽
    cr, cc = down +1, 0
    for di, dj in (1, 0), (0, 1), (-1, 0), (0, -1):
        while 1:
            nr, nc = cr + di, cc + dj
            if oob(nr, nc): break  # 범위 아웃
            if nr == up: break
            if nr == down and nc == 0: break
            arr[cr][cc] = arr[nr][nc]
            cr, cc = nr, nc
    arr[cr][cc] = 0

#출력
answer = 0
for i in range(N):
    for j in range(M):
        if arr[i][j] != -1:
            answer+= arr[i][j]
    # print(arr[i])
print(answer)