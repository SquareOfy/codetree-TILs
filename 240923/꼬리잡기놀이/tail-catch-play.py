"""
코드리뷰
총 풀이시간

실행시간 246mb
메모리  26Mb


0901 문제읽기 시작
    오늘은 문제 빈틈 놓치고 설계 잘못해서 허덕이지 말자 다짐
    아침에 건님의 조언을 듣고 설계가 늦어도 괜찮으니 문제를 깊이 이해해보자! 생각했음

    문제 아무것도 적지 말고 일단 1회독 (중간에 스윽 내려서 입력 형태 먼저 보고 옴. 읽으면서 방법 생각해보려고)
    중간에 절차 읽길래 절차 주석으로 옮겨놓음
    이 때 라운드별 보는 방향 + 인덱스 순서 헷갈리겠다 싶어서 정리해놓음

0911 문제 다읽고 구현할 내용 정리 (손설계 후 주석에 정리)
    우선 이동 - 공던지기 - 사람 만났을 때 점수 더하는 로직 종이에 설계
    이동 설계하면서 팀을 deque를 가지는 길이가 m인 배열로 만들기로 함

    이후 입력이 팀 리스트를 주는게 아니라 팀 관리를 어떻게 할지 설계함
        => BFS 1,2,3 찾아서 queue에 넣고 team[m]에도 넣는 방식

    이동 deque 의 appendleft, pop() 활용하려 했고 배열 값 변경하는 것도 주의함


0932 구현시작
    - 팀배열 세팅 구현 후 중간 테스트 함
    - 이동 구현 후 중간 테스트 함
    - 라운드 진행 한번에 점수 계산까지 할 수 있었지만 로직 분리 + 테스트 편리하게 하려고 함수 분리함
    - 라운드 진행 인덱스 주의하려했음.............(결국 실수했지만)
0952 제출했으나 런타임 에러
    - 테케 보자마자, None 어쩌고 보자마자 아 throw_ball 함수에서 사람 없음 반환될 때 처리 안했구나 함
        그래도 혹시 사람 있는데 못찾는건 아니겠지 해서 team 출력해서 확인해보고
        없어서 반환 제대로 되는거 보고 if문 추가해서 사람 만날 때만 점수 계산하도록 변경

1003 또 런타임 에러
    - 주석 처리 해놓은 거 풀고 상황파악
        => 팀 하나에 사람이 아예 없다? 왜지?
        => 테케 살펴봄. 팀을 구성하는 과정에서 무조건 사방에 4가 있을 거라 생각했었음. 해당 부분 로직 수정
        => 그래서 이동하는 로직에서 4를 찾아서 없으면 3을 찾도록 로직 수정
    - 에러는 안나는데 값이 안맞는 문제 발생
        이동하는 부분 프린트 디버깅 함
        사람 똑바로 잡는지 디버깅 함 (토론의 작은 테케로)
        reverse 될 때가 이상하다 ! => reverse 해놓고 arr에 반영은 안해서 arr이 이상해짐 발견
        reverse 고치고 다시 이동부터 공 맞는거 reverse까지 차근차근 살핌... 맞다 아무리봐도 맞아
        다 맞으니까 답답해서 쓸데없이 index 부분이 틀리나 싶어서 직접 구현하는 등 의미없는 행위 함
    - 토론에서 찾은 작은 테케는 분명 다 맞다 -> 다른 테케 찾아봄
        조금 더 큰 테케!
        왜냐? 큰 테케가 안맞다 => 저 멀리멀리까지 갔을 때가 문제다? 라는 생각이 들어서
        일단 이동, 점수, reverse 문제 없는지 보고 문제 없어 보여서 라운드가 문제인가 했다
        그래서 라운드 인덱스를 살피려고 했는데 눈에 안들어와서 다른 print 싹 다 지우고 round 별로
        index를 보려고 함
        그래서 작은 테케 중에 적당히 k가 큰 값을 골라와서 살핌

        보다보니 왜 마지막 9일 때 아무 if문으로 안들어가지지? 했다.
        마지막 elif 문에서 range 범위 4*N 누락된게 이제야 보였음... 수정
1038 정답 ㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠ

피드백
    - 잘한 점
        어제의 고생에 대한 교훈으로 설계를 충분히 하고 들어감
        문제 전반적인 구현 맥락이 이해되기 전에 함부로 구현 들어가지 말 것!!!
    - 못한 점
        디버깅이 조금 더 체계적이었으면 좋겠다
        당황하는 순간 프린트 디버깅이 지저분해진다
        그래도 주변이 4가 없을 경우 같은 경우를 전혀 생각해보지 않았다는 점은 반성할 부분
            (그래도 설계를 충분히 한 덕에 테케 보고 빠르게 어디를 어떻게 고쳐야할 지 잡을 수 있었다)
    - 코드 개선
        1. 주변에 4가 없을 때 ! (길에 인간꼬리로 꽉찬 경우), 상하좌우 다 탐색해서 4 없으면 flag처리해서 3찾으러 가는데
            좀 더 개선해볼 수 있을 것 같다. .
            => 강사님 코드 참고 : 꼬리 삭제부터 진행하면 방향이 생긴다 @@@@@@2우왁
        2. 라운드 하드코딩 ....
            실수 가능성 높아짐 하지만 빠르게 구현 가능 .. (담에 또 이렇게 하긴 할듯, 그래도 다른 방법 해보기)
            => 강사님 코드 참고 :  인덱스 찾는 것만 이 방식대로 하고 공통 로직은 합치자 !!


"""

"""

1.  먼저 각 팀은 머리사람을 따라서 한 칸 이동합니다.

2. 각 라운드마다 공이 정해진 선을 따라 던져집니다.
    1   ~  n   round : 행 by 행 오른쪽 방향 (열 : 0 ~ n-1)
    n+1 ~  2n  round : 열 by 열 위쪽 방향   (행 : n-1 ~ 0)
    2n+1 ~ 3n  round : 행 by 행 왼쪽 방향   (열 : n-1 ~ 0)
    3n+1 ~ 4n  round : 열 by 열 아래쪽 방향  (행 : 0 ~ n-1)

3. 공이 던져지는 라인에 사람 있으면 최초의 사람 팀만 점수 얻기(1명만)
    그 사람이 팀에서 k번째 사람이면 k**2 점수 획득
    그 팀 방향 바꾸기 ( 방향 반대, 머리사람 꼬리사람 change)



team = deque m 개 가진 리스트

1. 팀 찾아서 배열로 만들기?
m_idx = 0
    for i in range(N):
        for j in range(N):
            if arr[i][j]==1: #머리 !!
                team[m].append((i, j)
                bfs! visited 해가면서 1, 2, 3 중에 찾고 3이면 끝내기

2. 이동
    team의 m개의 deque에서 아래 수행
    머리위치에서 사방탐색해서 4 찾기 그 위치가 새로운 머리위치 (r, c)
    새로운 머리 위치 appendleft((r,c))
    pop()하고 그 자리 사로 만들기
    1~끝 -1 까지 arr[i][j] = 2로 만들고 끝은 3으로 만들기

3. round 돌리기
    throw 함수 : round 매개변수 (4N모듈 해야함)

    if 문으로 round 동작 설계
    (0, N)이면
        row = round
        for j in range(0, N):
            사람 찾으면 점수 계산 후 break

    (N, 2N)이면
        col = round%N
        for i in range(N-1, -1, -1)

    (2N, 3N)
        row = N-1 - round%N
        for j in range(N-1, -1, -1)

    (3N, 4N)
        col = N-1 - round%N
        for i in range(0, N)

"""

from collections import deque


def oob(r, c):
    return r < 0 or c < 0 or r >= N or c >= N


def bfs(r, c, team_num):
    visited[r][c] = 1
    q = deque([(r, c)])

    while q:
        cr, cc = q.popleft()
        team[team_num].append((cr, cc))
        num = arr[cr][cc]
        if arr[cr][cc] == 3:
            return
        for di, dj in dir:
            du = cr + di
            dv = cc + dj

            if oob(du, dv) or visited[du][dv]:
                continue
            if arr[du][dv] == num or arr[du][dv] == num + 1:
                visited[du][dv] = 1
                q.append((du, dv))


def find_idx(round):
    # 방향 우, 상, 좌, 하 순
    d = (round//N) % 4
    round_mod = round % N
    if d == 0:
        sr, sc = round_mod, 0
    elif d == 1:
        sr, sc = N - 1, round_mod
    elif d == 2:
        sr, sc = N - 1 - round_mod, N - 1
    else:
        sr, sc = 0, N - 1 - round_mod
    return sr, sc, d


def throw_ball(round):
    sr, sc, d = find_idx(round)
    di, dj = dir[d]
    for j in range(N):
        if 0 <= sr < N and 0 <= sc < N and arr[sr][sc]!=0 and arr[sr][sc] != 4:
            return (sr, sc)
        sr += di
        sc += dj
    return (-1, -1)


def find(r, c):
    result = -1
    for m in range(M):
        if (r, c) in team[m]:
            for j in range(len(team[m])):
                point = team[m][j]
                if point == (r, c):
                    result = j + 1
                    break

            team[m].reverse()
            hr, hc = team[m][0]
            tr, tc = team[m][-1]
            arr[hr][hc] = 1
            arr[tr][tc] = 3

            return result


N, M, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
team = [deque([]) for _ in range(M)]
visited = [[0] * N for _ in range(N)]
answer = 0
# dir = (-1, 0), (0, 1), (1, 0), (0, -1)
dir = (0, 1), (-1, 0), (0, -1), (1, 0)
# 팀 배열 세팅하기
m_idx = 0
for i in range(N):
    for j in range(N):
        if arr[i][j] == 1:
            bfs(i, j, m_idx)
            m_idx += 1

# 라운드 진행
for k in range(K):

    # 팀 한칸씩 이동
    for m in range(M):
        # 꼬리부터 이동
        tr, tc = team[m].pop()
        arr[tr][tc] = 4
        # 머리 이동
        hr, hc = team[m][0]
        for di, dj in dir:
            nr, nc = hr + di, hc + dj
            if oob(nr, nc):
                continue
            if arr[nr][nc] == 4:
                team[m].appendleft((nr, nc))
                arr[nr][nc] = 1
                arr[hr][hc] = 2
                blank_flag = True
                break
        ntr, ntc = team[m][-1]
        arr[ntr][ntc] = 3

    # 이동 체크 완
    r, c = throw_ball(k)

    if r != -1 and c != -1:
        score = find(r, c)
        answer += score ** 2

print(answer)