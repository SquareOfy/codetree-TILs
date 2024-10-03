"""
1차
풀이 시간 : 3시간 30분
시도 횟수 : 3회
실행 시간 : 172 ms
메모리 : 113084 kb

2차
풀이 시간 : 40분
시도 횟수 : 1회
실행 시간 : 176 ms
메모리 : 113084 kb

- 실수 모음
- 말이 이동할 때 한꺼번에 이동되는데, 이 때 info배열도 함께 수정해줘야함을 놓침
    1,2차 모두 또옥같이 실수함;;

Routine
1. 문제 그냥 정독 ok
2. 문제 주석 복사 ok
4. 테스트케이스 외에 고려해야할 사항 생각해보기 + 설계에 반영
: 파란색 반대편으로 이동할 때 코드 안더러워지게 주의하기
: 방향 배열 바꿨다가 디버깅 때 더 헷갈리니까 그냥 있는거 사용하기
5. 종이에 손설계 OK
6. 주석으로 구현할 영역 정리 : ok !
7. 구현 : ok
8.테스트케이스 단계별 디버깅 확인 : ok
9. 1시간 지났는데 디버깅 헤매는 중이면 리셋!!


"""

"""
1이상 100이하의 숫자로만 이루어져 있는 n * n 크기의 격자 정보
격자의 숫자들은 지역별 인구수
다섯 개의 부족이 땅을 나눠가지기로 했습니다.
땅을 나누기 위해 기울어진 직사각형을 이용


기울어진 직사각형이란, 
격자내에 있는 한 지점으로부터 체스의 비숍처럼 대각선으로 움직이며 반시계 순회를 했을 때 지나왔던 지점들의 집합
반드시 아래에서 시작해서 1, 2, 3, 4번 방향순으로 순회
각 방향으로 최소 1번은 움직여야 합니다
이동하는 도중 격자 밖으로 넘어가서는 안됩니다.

1번 부족
기울어진 직사각형의 경계와 그 안에 있는 지역

2번 부족
기울어진 직사각형의 좌측 상단 경계의 윗부분에 해당하는 지역
위쪽 꼭짓점의 위에 있는 칸들은 모두 포함하지만 왼쪽 꼭짓점의 왼쪽에 있는 칸들은 포함하지 않습니다.

3번 부족
기울어진 직사각형의 우측 상단 경계의 윗부분에 해당하는 지역
오른쪽 꼭짓점의 오른쪽에 있는 칸들은 모두 포함하지만 윗쪽 꼭짓점의 위쪽에 있는 칸들은 포함하지 않습니다.

4번 부족
기울어진 직사각형의 좌측 하단 경계의 아랫부분에 해당하는 지역
왼쪽 꼭짓점의 왼쪽애 있는 칸들은 모두 포함하지만 아랫쪽 꼭짓점의 아래쪽에 있는 칸들은 포함하지 않습니다.

5번 부족
기울어진 직사각형의 우측 하단 경계의 아랫부분에 해당하는 지역
아랫쪽 꼭짓점의 아랫쪽에 있는 칸들은 모두 포함하지만 오른쪽 꼭짓점의 오른쪽에 있는 칸들은 포함하지 않습니다.


각 부족장이 관리하는 인구 수의 최댓값과 최솟값의 차이가 가장 작을 때의 값
"""

# 입력받기
N = int(input())
arr = [list(map(int, input().split())) for _ in range(N)]
answer = float("inf")
# a, b for문으로 정하기 a : 1~N-2, b는 1~ N-1-a
# i, j 는 i는 위로 필요한 공간으로 범위 잡기 (a+b) ~ N
# j는 그냥 다 하고 continue로 거르기
for a in range(1, N - 1):
    for b in range(1, N - a):
        for i in range(a + b, N):
            for j in range(N):
                if j + b >= N: continue
                if j - a < 0: continue
                check = [[0] * N for _ in range(N)]
                population = [0]*5
                # 대각 체크
                r, c = i, j
                l = b
                for di, dj in (-1, 1), (-1, -1), (1, -1), (1, 1):
                    for k in range(l):
                        r += di
                        c += dj
                        check[r][c] = 1
                        population[0] += arr[r][c]
                    l = b if l==a else a

                ################## 중간체크 함 #########################33
                # print()
                # for k in range(N):
                #     print(check[k])
                # print()
                # print(population)


                for rr in range(i-a-b+1, i):
                    flag = False
                    # print("i : ", rr , "j 범위 : ")
                    # print(j-a, j+b)
                    for cc in range(j-a, j+b):
                        if check[rr][cc] ==1 and not flag:
                            flag = True
                            # break
                        elif check[rr][cc]==0 and flag:
                            check[rr][cc] = 1
                            # print(rr, cc)
                            # print(arr[rr][cc])
                            population[0] += arr[rr][cc]
                        elif check[rr][cc] ==1 and flag:
                            break

                # print(population)


                # 2,3,4,5 부족 체크
                for rr in range(N):
                    for cc in range(N):
                        if check[rr][cc]==1:
                            continue

                        if rr in range(i-a) and cc in range(j+b-a+1):
                            population[1]+= arr[rr][cc]
                            check[rr][cc] = 2
                        elif rr in range(i-b+1) and cc in range(j+b-a+1, N):
                            population[2] += arr[rr][cc]
                            check[rr][cc] = 3
                        elif rr in range(i-a, N) and cc in range(j):
                            population[3] += arr[rr][cc]
                            check[rr][cc]= 4
                        else:
                            population[4] += arr[rr][cc]
                            check[rr][cc] = 5
                # print()
                # for k in range(N):
                #     print(check[k])
                answer = min(max(population)-min(population), answer)
print(answer)