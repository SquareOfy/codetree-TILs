"""

#배열 인덱스 그대로 따라가면 되겠군
좌표평면은 x 값이 위에서 아래로 갈수록 증가하며 0에서부터 시작하며,
y는 왼쪽에서 오른쪽으로 갈수록 증가하며 0에서부터 시작


0차 드래곤 커브는 길이가 1인 선분
n차 드래곤 커브는 n-1차 드래곤 커브의 끝점에

n-1차 드래곤 커브를 복제한 뒤 시계 방향으로 90도 회전시킨 뒤 연결한 도형

n개의 드래곤 커브가 주어질 때 만들어지는 단위 정사각형의 개수
x값과 y값의 범위는 0 ≤ x, y ≤ 100
만들어지는 정사각형이란 정사각형의 네 꼭지점이 모두 드래곤 커브에 속하는 도형
"""
#입력
DIR = (0, 1), (-1, 0), (0, -1), (1, 0)
N = int(input())
arr = [[0]*101 for _ in range(101)]
#N번 반복
for n in range(N):
    #드래곤 커브 정보 입력
    x, y, d, g = map(int, input().split())
    lst = [d]
    #세대 수만큼 lst 거꾸로 돌면서 d 시계회전 시킨 값 넣기 (d+1)
    for ger in range(g):
        for k in range(len(lst)-1, -1, -1):
            cur = lst[k]
            lst.append((cur+1)%4)
    arr[x][y] = 1
    #lst 다 돌면서 arr에 찍기
    for cd in lst:
        di, dj = DIR[cd]
        x+= di
        y+= dj
        arr[x][y] = 1

answer = 0
#arr 다 돌며 단위정사각형 개수 세기
for i in range(100):
    for j in range(100):
        if arr[i][j] and arr[i+1][j] and arr[i][j+1] and arr[i+1][j+1]:
            answer+=1
print(answer)