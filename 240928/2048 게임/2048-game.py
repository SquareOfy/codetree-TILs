"""
Routine
1. 문제 그냥 정독 ok
2. 문제 주석 복사 ok
4. 테스트케이스 외에 고려해야할 사항 생각해보기 + 설계에 반영 : 딱히 없음
5. 종이에 손설계 ok
6. 주석으로 구현할 영역 정리 ok
7. 구현
8.테스트케이스 단계별 디버깅 확인
9. 예외될 상황 테스트케이스 만들어서 확인

Debugging CheckPoint
- N, M / 행 열 index 오타 실수 점검
- max, min 구할 때 초기값 체크
- 배열 사용 목적 확인 후 배열 변수 실수 확인
- 조건분기문 복사한 경우 모두 바꿨는지 체크
- 디버깅해서 바꾼 코드 부분 혹은 로직이 있다면 그 부분 중심으로 전반적으로 재점검
- 문제 조건 + 코드 로직 같이 따라가며 이상한 로직 없는지 점검
- 로직이 맞는데 답이 이상하다면 아주 사소한 순서 문제는 없을지 점검



 4 * 4 격자 안에서 이루어지는 게임
  상하좌우 중 한 방향을 정하게 되면, 모든 숫자들이 해당 방향으로 전부 밀리게 됩니다.

같은 숫자끼리 만나게 되는 경우 두 숫자가 합쳐지게 됩니다
단 한 번의 중력작용으로 이미 합쳐진 숫자가 연쇄적으로 합쳐지진 않습니다.
세 개 이상의 같은 숫자가 중력작용 방향으로 놓여 있으면, 중력에 의해 부딪히게 될 벽(바닥)에서 가까운 숫자부터 두 개씩만 합쳐집니다.
바닥에 가까운 순서대로 한 쌍씩 짝을 이뤄 합쳐집니다.



출력
5번 움직인 이후에 격자판에서 가장 큰 값의 최댓값


"""

def printa(string, arr):
    print(f"===================={string}======================")
    for k in range(N):
        print(arr[k])
    print()

#dfs
def gravity(d, arr):
    di, dj = DIR[d]
    st, ed, step = idx_dict[d]
    cnt = 0
    if di:
        for c in range(N):
            idx = st
            for r in range(st, ed+step, step):
                if arr[r][c] ==0: continue
                arr[idx][c] = arr[r][c]
                if idx!= r:
                    arr[r][c] = 0
                    cnt += 1
                idx += step


        # for k in range(N):
        #     print(arr[k])
        # print()

    else:
        for r in range(N):
            idx = st
            for c in range(st, ed+step, step):
                if arr[r][c] ==0: continue
                if idx != c:
                    arr[r][idx] = arr[r][c]
                    arr[r][c] = 0
                    cnt+=1
                idx += step
    return arr, cnt

def dfs(level, arr, mx, bd):
    global answer
    # level 5일 때 return .
    if level == 5:
        # printa("완료 후 !! ", arr)
        answer = max(mx, answer)
        return
    #상하좌우 중에 움직여보기
    for i in range(4):
        if i==bd: continue
        # printa("움직이기 전 !!!!!!!!!!!!!!", arr)
        #수 합치면서 mx 가져오기
        changed_arr, new_mx, change1 = merge(i, arr, mx)
        #gravity
        changed_arr, change2 = gravity(i, changed_arr)
        # printa(f"{DIR[i]}로 움직인 후 ", changed_arr)
        # 움직임 없으면 다음 dfs 부르지 말자
        if change1 == 0 and change2 : continue
        dfs(level+1, changed_arr, new_mx, i)


#merge
def merge(d, arr, mx):
    result = mx
    st, ed, step = idx_dict[d]
    change = 0
    di, dj = DIR[d]

    if di:
        for c in range(N):
            for r in range(st, ed, step):
                if arr[r][c] ==0: continue
                if arr[r][c] == arr[r-di][c]:
                    arr[r][c] *= 2
                    arr[r-di][c] = 0
                    result = max(arr[r][c], result)
                    change+=1

    else:
        for r in range(N):
            for c in range(st, ed, step):
                if arr[r][c] ==0: continue
                if arr[r][c] == arr[r][c+step]:
                    arr[r][c] *= 2
                    arr[r][c+step] =0
                    result = max(arr[r][c], result)
                    change+=1
    return arr, result, change



#gravity


#입력 받기
N = int(input())
arr = [list(map(int, input().split())) for _ in range(N)]
idx_dict = {0:(0, N-1, 1), 1:(N-1, 0, -1), 2:(N-1, 0, -1), 3:(0, N-1, 1)}
DIR = (-1, 0), (0, 1), (1, 0), (0, -1)
answer = 0
for i in range(N):
    for j in range(N):
        if arr[i][j]>answer:
            answer = arr[i][j]
#함수 실행
dfs(0, arr, answer, -1)
#출력
print(answer)