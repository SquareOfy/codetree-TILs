"""

Routine
1. 문제 그냥 정독 ok
2. 문제 주석 복사 ok
4. 테스트케이스 외에 고려해야할 사항 생각해보기 + 설계에 반영
    : deque 쓰자
    : N칸 도착하자마자 내리는 거 놓치지 말기!!
5. 종이에 손설계 : ok
6. 주석으로 구현할 영역 정리 : ok
7. 구현 : ok
8.테스트케이스 단계별 디버깅 확인
    : 답 다르길래 deque 사람 움직이기 전 후로 프린트+종이테케 따라가기로
    틀린 부분 찾음
9. 1시간 지났는데 디버깅 헤매는 중이면 리셋!!
"""

N, M, K = map(int, input().split())
arr = [[[] for _ in range(N)] for _ in range(N)]
DIR = (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)
for m in range(M):
    x, y, m, s, d = map(int, input().split())
    x -= 1
    y -= 1
    arr[x][y].append((m, s, d))

for k in range(K):
    tmp = [[[] for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if not arr[i][j]: continue
            # print(arr[i][j])
            for t in range(len(arr[i][j])):
                m, s, d = arr[i][j][t]
                nr = (i + DIR[d][0] * s) % N
                nc = (j + DIR[d][1] * s) % N
                tmp[nr][nc].append((m, s, d))
    for i in range(N):
        for j in range(N):
            if len(tmp[i][j]) < 2: continue
            mm = 0
            ss = 0
            multiple_d = 1
            sum_d = 0
            for m, s, d in tmp[i][j]:
                mm += m
                ss += s
                multiple_d *= d
                sum_d += d

            new_m = mm//5
            new_s = ss//len(tmp[i][j])
            tmp[i][j] = []
            if new_m ==0:
                continue
            new_d = [0, 2, 4, 6] if sum_d==0 or multiple_d==1 else [1, 3, 5, 7]

            for k in range(4):
                tmp[i][j].append((new_m, new_s, new_d[k]))



    for i in range(N):
        for j in range(N):
            arr[i][j] = tmp[i][j][:]
        # print(arr[i])

answer = 0
for i in range(N):
    for j in range(N):
        for m, s, d in arr[i][j]:
            answer+= m

print(answer)