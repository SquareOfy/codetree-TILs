"""

n * n 격자판
격자판은 흰색, 빨간색, 파란색 중 하나의 색
말은 총 k개가 주어지며, 모두 격자판의 한 지점에 놓여있습니다
1번부터 k번까지 번호가 지정되어 있으며 이동 방향 또한 미리 정해져있습니다.
상하좌우의 4가지 방향으로 움직일 수 있습니다.

쌓여있는 말을 이동하는 경우에는 본인 위에 있는 말과 함께 이동

말이 이동하려는 칸이 흰색인 경우에는 해당 칸으로 이동
    이동하려는 칸에 말이 이미 있는 경우에는 해당 말 위에 이동하려던 말을 올려둡니다
    이미 말이 올려져 있는 상태에도 말을 올릴 수 있습니다.

이동하려는 칸이 빨간색인 경우에는 해당 칸으로 이동하기 전 (옮길 말들의) 순서를 뒤집습니다.
    이동하려는 칸에 말이 있는 경우에는 흰색 칸과 같이 그 위에 쌓아둡니다.

이동하려는 칸이 파란색일 경우에는 이동하지 않고 방향을 반대로 전환한 뒤 이동
    만일 반대 방향으로 전환한 뒤 이동하려는 칸도 파란색이라면 방향만 반대로 전환한 뒤 이동하지 않고 가만히 있습니다.
    이동하려는 말에 다른 말들이 쌓여있을 경우에 이동하려는 말만 방향을 반대로 바꿔야 함

격자판의 범위를 벗어나는 이동일 경우 파란색으로 이동하려는 것과 똑같이 생각하여 처리

아직 한 턴이 다 끝나지 않은 경우더라도 말이 4개 이상 겹쳐지는 경우가 생긴다면 그 즉시 게임을 종료
 게임이 종료되는 순간의 턴의 번호

 1: 오른쪽
 2: 왼쪽
 3: 위쪽
 4: 아래쪽


"""


def change_direction(i):
    if i in (1, 2):
        return 3 - i
    else:
        return 7 - i

def oob(i, j):
    return i<0 or j<0 or i>=N or j>=N

def find_place(k):
    for i in range(N):
        for j in range(N):
            if k in mal_arr[i][j]:
                return i, j
def move():
    for k in range(1, K + 1):
        # r, c, d = mal_info[k]
        r, c = find_place(k)
        d = mal_info[k]
        result = move_to_point(k, r, c, d, 0)
        if result:
            return result
    return False

def move_to_point(k, r, c, d, flag):

    di, dj = DIR[d]
    du, dv = r+di, c+dj
    if oob(du, dv) or arr[du][dv] == 2:
        if not flag:
            return move_to_point(k, r, c, change_direction(d), 1)
        else:
            mal_info[k] =d
            du, dv = r, c

    elif arr[du][dv] == 0:
        idx = mal_arr[r][c].index(k)
        mal_arr[du][dv].extend(mal_arr[r][c][idx:])
        mal_arr[r][c][idx:] = []
        mal_info[k] = d

    elif arr[du][dv] == 1:
        idx = mal_arr[r][c].index(k)
        tmp = mal_arr[r][c][idx:]
        mal_arr[r][c][idx:] = []
        tmp = tmp[::-1]
        mal_arr[du][dv].extend(tmp)
        mal_info[k] =d


    return len(mal_arr[du][dv])>=4
# 입력 받기
N, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
mal_arr = [[[] for _ in range(N)] for _ in range(N)]
mal_info = [-1]
DIR = (-1, ), (0, 1), (0, -1), (-1, 0), (1, 0)

for k in range(1, K + 1):
    x, y, d = map(int, input().split())
    x -= 1
    y -= 1
    mal_arr[x][y].append(k)
    mal_info.append(d)

turn = 0
# while (turn 진행)
while 1:
    # turn +
    turn += 1
    # 종료조건
    if turn > 1000:
        turn = -1
        break
    # 말 옮기기
    result = move()
    if result:
        break

print(turn)