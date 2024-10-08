# 1623 풀이 시작
# 1723 풀이 끝
# 종료(출력값)
# 첫 번째 줄에 K번의 턴이 종료된 후 남아있는 포탑 중 가장 강한 포탑의 공격력을 출력합니다.
# 함수화
# 1. 가장 약한 포탑 고르기
# 2. 가장 강한 포탑 고르기
# 3. 레이저 공격
# 4. 포탑 공격
# 5. 포탑 정비

dr = [0, 1, 0, -1, 1, -1, 1, -1]  # 우/하/좌/상의 우선순위
dc = [1, 0, -1, 0, 1, -1, -1, 1]


def select_attacker():
    cand = []
    for r in range(N):
        for c in range(M):
            if turret_arr[r][c] <= 0: continue
            cand.append((turret_arr[r][c], attack_arr[r][c], r + c, c, r, c))
    cand.sort(key=lambda x: (x[0], -x[1], -x[2], -x[3]))

    return cand[0][4:]


def select_defender():
    cand = []
    for r in range(N):
        for c in range(M):
            if turret_arr[r][c] <= 0: continue
            cand.append((turret_arr[r][c], attack_arr[r][c], r + c, c, r, c))
    cand.sort(key=lambda x: (-x[0], x[1], x[2], x[3]))

    return cand[0][4:]


def find_laser_route(r, c):
    used1 = [[0] * M for _ in range(N)]
    q = [(r, c, [])]
    used1[r][c] = 1
    while q:
        nq = []
        for pr, pc, route in q:
            if (pr, pc) == (tr, tc):
                return route

            for i in range(4):
                nr, nc = (pr + dr[i]) % N, (pc + dc[i]) % M
                if used1[nr][nc] or turret_arr[nr][nc] <= 0: continue
                used1[nr][nc] = 1
                q.append((nr, nc, route + [(nr, nc)]))
        q = nq


N, M, K = map(int, input().split())
turret_arr = [list(map(int, input().split())) for _ in range(N)]
attack_arr = [[0] * M for _ in range(N)]  # 모든 포탑은 시점 0에 모두 공격한 경험이 있다고 가정
INF = float('inf')

for k in range(1, K + 1):
    is_related = [[0] * M for _ in range(N)]
    # -------------------- 1. 가장 약한 포탑 선정하기 ---------------------------------
    ar, ac = select_attacker()
    attack_arr[ar][ac] = k
    is_related[ar][ac] = 1
    # -------------------- 2. 가장 강한 포탑 선정하기 ---------------------------------
    tr, tc = select_defender()
    # print('공격자 :', ar, ac)
    # print('수비자 :', tr, tc)
    # 종료 조건
    if (ar, ac) == (tr, tc):
        break
    # print('공격 전 포탑')
    # for r in range(N):
    #     print(turret_arr[r])
    # print()
    is_related[tr][tc] = 1

    turret_arr[ar][ac] += N + M  # N*M 만큼의 공격력이 증가합니다.

    # --------------------- 3. 레이저 공격 -----------------------------------
    laser_route = find_laser_route(ar, ac)
    damage = turret_arr[ar][ac]

    turret_arr[tr][tc] -= damage  # 공격자의 공격력 만큼의 피해를 입히며,
    # print(laser_route)
    if laser_route:
        for lr, lc in laser_route:
            is_related[lr][lc] = 1
            if (lr, lc) == (tr, tc):
                continue
            turret_arr[lr][lc] -= damage // 2  # 공격력의 절반 만큼의 공격을 받습니다.


    # ---------------------- 4. 포탑 공격 ----------------------------------
    else:
        for i in range(8):
            ntr, ntc = (tr + dr[i]) % N, (tc + dc[i]) % M  # 반대편 격자에 미치게 됩니다.
            is_related[ntr][ntc] = 1
            if (ntr, ntc) == (ar, ac): continue
            turret_arr[ntr][ntc] -= damage // 2  # 공격자 공격력의 절반 만큼의 피해를 받습니다.

    # --------------------- 5. 포탑 정비 -----------------------------------
    for r in range(N):
        for c in range(M):
            if turret_arr[r][c] <= 0 or is_related[r][c]: continue  # 부서지지 않은 포탑 중 공격과 무관했던 포탑
            turret_arr[r][c] += 1  # 공격력이 1씩 올라갑니다.
    # print('공격 후 포탑')
    # for r in range(N):
    #     print(turret_arr[r])
    # print()
print(max(map(max, turret_arr)))