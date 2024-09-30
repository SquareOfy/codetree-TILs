"""
Routine
1. 문제 그냥 정독
2. 문제 주석 복사 ok
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
4개의 팔각 의자 두 지역에서 온 사람들 N과 S 
팔각 의자는 왼쪽에서부터 오른쪽까지 각각 1번부터 4번까지의 번호

각각의 의자를 총 k번 회전
한 번 회전할 때 45도씩 즉 한 칸을 움직임
회전은 시계 방향과 반시계 방향 모두 가능

회전 요청 규칙
n번째 의자가 회전하기 전 인접한 의자(n-1번째와 n+1번쨰)에 있던 의자에서 제일 가깝게 마주치는
두 명의 사람의 출신 지역이 다르다면 n번째 의자가 회전할 때 인접한 의자 또한 반대 방향으로 회전하게 됩니다.

회전 요청에 따라 의자를 회전시킨 후  그로 인해 일어나는 모든 회전이 끝날 때까지 기다립니다.
 한 번 회전한 의자는 다시 회전하지 않습니다.
 
 남쪽지방 사람 착석여부를 각 테이블에 대하여 s1, s2, s3, s4라고 할 때 1*s1 + 2*s2 + 4*s3 + 8*s4를 출력
 
"""

from collections import deque

chair_lst = [deque(list(map(int, list(input())))) for _ in range(4)]
K = int(input())
for k in range(K):
    n, d = map(int, input().split())
    n-=1
    rotate_lst = [0]*4
    rotate_lst[n] = d
    for i in range(n+1, 4):
        if chair_lst[i-1][2] == chair_lst[i][6]:
            break
        rotate_lst[i] = rotate_lst[i-1]*(-1)
    for i in range(n-1, -1, -1):
        if chair_lst[i+1][6] == chair_lst[i][2]:
            break
        rotate_lst[i] = rotate_lst[i+1]*(-1)
    for i in range(4):
        if rotate_lst[i] == 0:
            continue
        chair_lst[i].rotate(rotate_lst[i])
answer = 0
for i in range(4):
    if chair_lst[i][0] == 1:
        answer += 2**i
print(answer)