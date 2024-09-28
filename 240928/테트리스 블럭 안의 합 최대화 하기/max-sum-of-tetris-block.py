"""
Routine
1. 문제 그냥 정독 OK
2. 문제 주석 복사 OK
4. 테스트케이스 외에 고려해야할 사항 생각해보기 + 설계에 반영 :
5. 종이에 손설계
6. 주석으로 구현할 영역 정리
7. 구현
8.테스트케이스 단계별 디버깅 확인
9. 예외될 상황 테스트케이스 만들어서 확인
10. 1시간 지났는데 디버깅 헤매는 중이면 리셋!!


Debugging CheckPoint
- N, M / 행 열 index 오타 실수 점검
- max, min 구할 때 초기값 체크
- 배열 사용 목적 확인 후 배열 변수 실수 확인
- 조건분기문 복사한 경우 모두 바꿨는지 체크
- 디버깅해서 바꾼 코드 부분 혹은 로직이 있다면 그 부분 중심으로 전반적으로 재점검
- 문제 조건 + 코드 로직 같이 따라가며 이상한 로직 없는지 점검
- 로직이 맞는데 답이 이상하다면 아주 사소한 순서 문제는 없을지 점검

Reset Timing
- 1시간 ~ 1시간 반 : 코드 다 짰는데 테케 정답이 엉망진창?
    문제 이해 미흡, 설계 미흡일 확률 높으므로 문제 다시 읽고 리셋할 모듈 찾을지 전체 리셋할지 판단하기
- 1시간 반 쯤에 코드 대부분이 잘 돌아가는데 특정 포인트에서 안되는 것 같다?
    - 특수한 테케가 있는지 1차로 점검해보고 디버깅
    - 오타 찾아야할 것 같다 => 그냥 리셋해버리자


"""


"""
n×m크기의 이차원 영역의 각 위치에 자연수 하나가 적혀있습니다.

다섯가지 종류의 테트리스 블럭 중 한 개를 적당히 올려놓아
 블럭이 놓인 칸 안에 적힌 숫자의 합이 최대가 될 때의 결과를 출력
 주어진 테트리스 블럭은 자유롭게 회전하거나 뒤집을 수 있습니다.
 
 BFS로 4가지 모양 탐색. ㅏ ㅓ ㅗ ㅜ 는 조건분기문으로 해결
 
 
"""

def oob(i, j):
    return i<0 or j<0 or i>=N or j>=M


#함수 dfs
def dfs(level, r, c, s):
    global answer
    if s+(4-level)*mx_arr <= answer:
        return

    if level ==4:
        answer = max(s, answer)
        return

    for di, dj in (-1, 0), (0, 1), (1, 0):
        du = r+di
        dv = c+dj
        if oob(du, dv) or visited[du][dv]:
            continue
        visited[du][dv] = 1
        dfs(level+1, du, dv, s+arr[du][dv])
        visited[du][dv] = 0



#입력 받기
N, M = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
answer = 0
mx_arr = 0
visited = [[0]*M for _ in range(N)]
#arr의 mx 계산
for i in range(N):
    for j in range(M):
        mx_arr = max(arr[i][j], mx_arr)

#dfs 실행
for i in range(N):
    for j in range(M):
        visited[i][j] = 1
        dfs(1, i, j, arr[i][j])
        visited[i][j] = 0
#ㅏ ㅓ ㅗ ㅜ 조건분기 체크
for i in range(N):
    for j in range(M):
        s = arr[i][j]
        #ㅏ
        if not (oob(i-1, j) or oob(i, j+1) or oob(i+1, j)):
            answer = max(answer, s+arr[i-1][j]+arr[i][j+1]+arr[i+1][j])
        #ㅗ
        if not (oob(i-1, j) or oob(i, j-1) or oob(i, j+1)):
            answer = max(answer, s+arr[i-1][j]+arr[i][j-1]+arr[i][j+1])
        #ㅓ
        if not (oob(i-1, j) or oob(i, j-1) or oob(i+1, j)):
            answer = max(answer, s+arr[i-1][j]+arr[i][j-1]+arr[i+1][j])
        #ㅜ
        if not (oob(i+1, j) or oob(i, j+1) or oob(i, j-1)):
            answer = max(answer, s+arr[i+1][j]+arr[i][j+1]+arr[i][j-1])

print(answer)