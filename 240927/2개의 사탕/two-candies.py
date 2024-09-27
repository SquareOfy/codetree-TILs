"""
N, M
. 빈칸
# 장애물
R : 빨간사탕
B : 파란사탕
O : 출구

바깥 부분 모두 장애물로 막힘

상하좌우로 기울임. 기울어진 방향으로 사탕 끝까지 미끄러짐.
미끄러지는 도중에 상자를 다른 방향으로 기울일 수는 없습니다

빨간색 사탕을 밖으로 빼야 하지만, 파란색 사탕이 밖으로 나와서는 안됩니다.
빨간색 사탕이 나오기 전에 파란색 사탕이 먼저 나오면 안되며
빨간색 사탕이 나올 때 파란색 사탕이 동시에 나오는 것도 안됩니다.
"""
from collections import deque

def bfs():
    q = deque([(br, bc, rr, rc, -1, -1, 0)])
    step = 0

    while q:
        cbr, cbc, crr, crc, bdi, bdj, rank= q.popleft()

        if rank==10:
            return -1
        if bdi == -1:
            DIR = (-1, 0), (0, 1), (1, 0), (0, -1)
        elif bdi:
            DIR = (0, 1), (0, -1)
        else:
            DIR = (-1, 0), (1, 0)

        for di, dj in DIR:
            nbr, nbc = move(cbr, cbc, di, dj)
            if arr[nbr][nbc] == 'O':
                continue
            nrr, nrc = move(crr, crc, di, dj)
            if arr[nrr][nrc]=='O':
                return rank+1

            if nbr==nrr and nbc == nrc:
                if di<0 or dj<0: #상 또는 좌로 이동
                    if cbr<crr or cbc < crc: #파랑이 위쪽 또는 왼쪽에 있으면
                        nrr -= di
                        nrc -= dj #빨강을 뒤로 물러주기
                    else:
                        nbr-=di
                        nbc-=dj
                else:
                    if cbr<crr or cbc < crc: #
                        nbr -= di
                        nbc -= dj
                    else:
                        nrr -= di
                        nrc -= dj
            if nbr==cbr and nbc==cbc and nrr == crr and nrc == crc:
                continue
            q.append((nbr, nbc, nrr, nrc, di, dj, rank+1))
    return -1
def move(r, c, di, dj):
    du, dv = r, c
    while arr[du][dv] != '#':
        du += di
        dv += dj
        if arr[du][dv] == 'O':
            return du, dv
    du-=di
    dv-=dj
    return du,dv

N, M = map(int, input().split())
arr = [list(input()) for _ in range(N)]

for i in range(N):
    for j in range(M):
        if arr[i][j] == 'R':
            rr, rc = i, j
            arr[i][j] = '.'
        elif arr[i][j] == 'B':
            br, bc = i, j
            arr[i][j] = '.'

answer = bfs()
print(answer)