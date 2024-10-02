"""

 n * m 격자판

 1. 첫번째 열부터 탐색을 시작합니다.
 2. 해당 열의 위에서 아래로 내려가며 탐색할 때 제일 빨리 발견한 곰팡이를 채취
    곰팡이를 채취하고 나면 해당 칸은 빈칸이 되며,
    해당 열에서 채취할 수 있는 곰팡이가 없는 경우도 있을 수 있음

3. 열에서 채취 시도가 끝나고 나면 곰팡이는 이동을 시작
    주어진 방향과 속력으로 이동하며 격자판의 벽에 도달하면
    반대로 방향을 바꾸고 속력을 유지한 채로 이동
    벽에 도달하면 반대로 방향을 바꾸고 속력을 유지한 채로 이동합니다.

4. 모든 곰팡이가 이동을 끝낸 후에
    한 칸에 곰팡이가 두마리 이상일 때는 크기가 큰 곰팡이가 다른 곰팡이를 모두 잡아먹습니다.

해당 격자판에 있는 모든 열을 검사했을 때, 채취한 곰팡이 크기의 총합


d는 1~4까지의 정수
1인 경우는 위
2인 경우는 아래
3인 경우는 오른쪽
4인 경우는 왼쪽


"""
#입력
N, M, K = map(int, input().split())
#곰팡이 정보 dict 준비 (크기로 구분)
gom_dict = {}
#곰팡이 나타내는 위치 arr 준비
arr = [[0]*M for _ in range(N)]

#방향배열
DIR = (-1, (-1, 0), (1, 0), (0, 1), (0, -1))
for k in range(K):
    r, c, s, d, b = map(int, input().split())
    r-=1
    c-=1
    gom_dict[b] = (r, c, s, d)
    arr[r][c] = b

answer = 0
for c in range(M):

    #곰팡이 잡기
    for r in range(N):
        if arr[r][c] !=0:
            v = arr[r][c]
            answer+= v
            arr[r][c] = 0
            gom_dict[v] = -1
            break
    # print("===========곰팡이 잡음 =============")
    # print("answer : ", answer)
    # for z in range(N):
    #     print(arr[z])
    # print("=================================")

    #곰팡이 이동

    tmp = [[0]*M for _ in range(N)]

    for k, v in gom_dict.items():
        if v==-1: continue #이미 잡힌 곰팡이

        r, c, s, d = v
        di, dj = DIR[d]

        nr, nc = r, c
        if di:
           nr += s*di
           if nr < 0:
               nr += nr // (2 * N - 1)

           nr %= (2*N-1)
           if nr>=N:
               d = 3-d
               nr = (2*N-2-nr)
        else:
            nc += s*dj
            if nc <0 :
                nc += nc //(2*M-1)
            nc %= (2*M-1)

            if nc>=M:
                d=7-d
                nc=(2*M-2-nc)

        if tmp[nr][nc] != 0:
            if tmp[nr][nc] > k:
                gom_dict[k] = -1
                continue
            else:
                gom_dict[tmp[nr][nc]] = -1
        tmp[nr][nc] = k
        gom_dict[k] = (nr, nc, s, d)
    for t in range(N):
        arr[t] = tmp[t][:]
    # print("===============곰팡이 이동 후 ================")
    # for z in range(N):
    #     print(arr[z])
    # print(gom_dict)
    # print("==============================================")
print(answer)