"""



"""
from collections import deque

# 하나의 턴은 다음의 4가지 액션을 순서대로 수행하며, 총 K번 반복
# 만약 부서지지 않은 포탑이 1개가 된다면 그 즉시 중지
def select_attack_target():
    attack_player = (-1, -1)
    attack_step = 0

    target = (-1, -1)
    target_step = 0

    mn = 5001
    mx = - 1
    # 부서지지 않은 포탑 중 가장 약한 포탑이 공격자

    for i in range(N):
        for j in range(M):
            # 1. 공격력이 가장 낮은 포탑이 가장 약한 포탑
            if arr[i][j]==0:
                continue
            if arr[i][j]<mn:
                attack_player = (i, j)
                attack_step = recent_attack[i][j]

                mn = arr[i][j]
            elif arr[i][j] == mn:
                # 2. 가장 최근에 공격한 포탑이 가장 약한 포탑입니다 (모든 포탑은 시점 0에 모두 공격한 경험이 있음)

                if attack_step < recent_attack[i][j]:
                    attack_player =( i, j)
                    attack_step = recent_attack[i][j]

                # 3. 각 포탑 위치의 행과 열의 합이 가장 큰 포탑이 가장 약한 포탑입니다.
                # 4. 각 포탑 위치의 열 값이 가장 큰 포탑이 가장 약한 포탑입니다.
                elif attack_step == recent_attack[i][j] and \
                        (sum(attack_player)<i+j or (sum(attack_player)==i+j and attack_player[1]<j)):
                    attack_player = (i, j)
                    attack_step = recent_attack[i][j]

            # 1. 공격력이 가장 높은 포탑이 가장 강한 포탑
    for i in range(N):
        for j in range(M):
            if (i, j)==attack_player: continue
            if arr[i][j]>mx:
                mx = arr[i][j]
                target_player = (i, j)
                target_step = recent_attack[i][j]
            elif arr[i][j] == mx:
                # 2. 공격한지 가장 오래된 포탑이 가장 강한 포탑 (모든 포탑은 시점 0에 모두 공격한 경험이 있음.)
                if target_step > recent_attack[i][j]:
                    target_player = (i, j)
                    target_step = recent_attack[i][j]
                # 3. 각 포탑 위치의 행과 열의 합이 가장 작은 포탑이 가장 강한 포탑
                # 4. 각 포탑 위치의 열 값이 가장 작은 포탑이 가장 강한 포탑

                elif target_step == recent_attack[i][j] and \
                        (sum(target_player) > i+j or (sum(target_player)==i+j and target_player[1]>j)):
                    target_player = (i, j)
                    target_step = recent_attack[i][j]
    return attack_player, target_player

def get_bfs_attack_lst(ar, ac, tr, tc):
    visited = [[0]*M for _ in range(N)]
    visited[ar][ac] = 1
    q = deque([(ar, ac, [])])

    while q:
        cr, cc, lst = q.popleft()

        if cr == tr and cc == tc:
            return lst
        for di, dj in (0, 1), (1, 0), (0, -1), (-1, 0):
            du = (cr+di)%N
            dv = (cc+dj)%M

            if visited[du][dv] or arr[du][dv]==0:
                continue
            visited[du][dv] = 1
            q.append((du, dv, lst+[(du,dv)]))


    return []




def get_attack_lst(tr, tc):
    # # 추가적으로 주위 8개의 방향에 있는 포탑도 피해를 입는데, 공격자 공격력의 절반 만큼의 피해를 받습니다
    # 만약 가장자리에 포탄이 떨어졌다면, 위에서의 레이저 이동처럼 포탄의 추가 피해가 반대편 격자에 미치게 됩니다.
    result = []
    for di, dj in (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1):
        du = (tr+di)%N
        dv = (tc+dj)%M
        if arr[du][dv] == 0:
            continue
        result.append((du, dv))
    return result


def attack_break(tr, tc, attack_lst):
    global cnt
    arr[tr][tc] = max(arr[tr][tc]-power, 0)
    related_arr[tr][tc] = 1
    if arr[tr][tc]==0:
        cnt-=1
        if cnt==1:
            return True
    for r, c in attack_lst:
        arr[r][c] = max(arr[r][c]-power//2, 0)
        related_arr[r][c] = 1
        if arr[r][c] ==0:
            cnt-=1
            if cnt==1:
                return True
    return False


# N×M 격자가 있고, 모든 위치에는 포탑이 존재
# 최초에 공격력이 0인 포탑 즉, 부서진 포탑이 존재할 수 있습니다.
# 공격력이 0 이하가 된다면, 해당 포탑은 부서지며 더 이상의 공격을 할 수 없습니다
N, M, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
###############입력 ###############
# for i in range(N):
#     print(arr[i])

##################################3
cnt = 0 #전체 포탑개수로 1개 되면 아래 즉시 중지 시킬 것
recent_attack = [[0]*M for _ in range(N)]

for i in range(N):
    for j in range(M):
        if arr[i][j]!=0:
            cnt+=1

for k in range(1, K+1):
    related_arr = [[0]*M for _ in range(N)]

    attack_player, target_player = select_attack_target()
    ar, ac = attack_player
    tr, tc = target_player

    #관계된 애들 기록
    related_arr[ar][ac] = 1

    #최근 공격시간 기록
    recent_attack[ar][ac] = k

    # 핸디캡이 적용되어 N+M만큼의 공격력이 증가
    arr[ar][ac] += N+M
    power = arr[ar][ac]

    #공격자, 타겟 선정 체크완#################
    # print("===============================================================")
    # print("===========atack and target ==========")
    # print("attack : ", attack_player)
    # print("target : ", target_player)
    # print("power : ", power)
    # print("========================================")
    # print()
    # ############################################


    # 3. 레이저공격 (안 된다면 포탄 공격)
    #      공격자의 위치에서 공격 대상 포탑까지의 최단 경로로 공격
    #  똑같은 최단 경로가 2개 이상이라면, 우/하/좌/상의 우선순위대로 먼저 움직인 경로가 선택
    # 공격 대상을 제외한 레이저 경로에 있는 포탑도 공격을 받게 되는데,
    # 이 포탑은 공격자 공격력의 절반 만큼의 공격을 받습니다

    #   상하좌우의 4개의 방향으로 움직일 수 있습니다.
    # 부서진 포탑이 있는 위치는 지날 수 없습니다.
    # 가장자리에서 막힌 방향으로 진행하고자 한다면, 반대편으로 나옵니다(바운더리 연결!!!)
    # 4. 포탄공격
    #  공격 대상에 포탄을 던집니다. 공격 대상은 공격자 공격력 만큼의 피해를 받습니다
    #  주위 8개는  절반만

    attack_lst = get_bfs_attack_lst(ar, ac, tr, tc)
    #리스트 비어있으면 포탄공격
    if not attack_lst:
        # print("포탑공격해야해!!!")
        attack_lst = get_attack_lst(tr, tc)
        attack_lst.append((tr, tc))
    attack_lst.pop() #공격자는 여기서 빼기

    # print('--------atack lst----------')
    # print(attack_lst)
    # print('---------------------------')
    # 5. 포탑 부서짐
    #     공격력 0 이하 된 포탑 부서짐
    if attack_break(tr, tc, attack_lst):
        break

    # print()
    # print("==============after attack =================")
    # for i in range(N):
    #     print(arr[i])
    # print("=========================================")
    # print()
    # 6. 포탑 정비
    #  공격자도 아니고, 공격에 피해를 입은 포탑 공격력이 1씩 올라갑니다
    for i in range(N):
        for j in range(M):
            if not related_arr[i][j] and arr[i][j]!=0:
                arr[i][j] +=1

    # print("===============after update====================")
    # for i in range(N):
    #     print(arr[i])
    # print("===============================================")
    # print()


answer = 0
for i in range(N):
    for j in range(M):
        if arr[i][j] !=0 and arr[i][j]>answer:
            answer = arr[i][j]

print(answer)