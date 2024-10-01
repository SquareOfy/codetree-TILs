"""
Routine
1. 문제 그냥 정독
2. 문제 주석 복사
4. 테스트케이스 외에 고려해야할 사항 생각해보기 + 설계에 반영
    :
5. 종이에 손설계
6. 주석으로 구현할 영역 정리 :
7. 구현 :
8.테스트케이스 단계별 디버깅 확인 :
9. 1시간 지났는데 디버깅 헤매는 중이면 리셋!!

"""

#calculate 함수
def calculate(a, b, o):
    if o==0:
        return a+b
    if o==1:
        return a-b
    if o==2:
        return a*b

#dfs
def dfs(level, num):
    global mn_ans, mx_ans
    if level == N:
        mn_ans = min(mn_ans, num)
        mx_ans = max(mx_ans, num)
        return

    for i in range(3):
        if cnt_lst[i]==0: continue
        cnt_lst[i]-= 1
        nxt_num = calculate(num, numbers[level], i)
        dfs(level+1, nxt_num)
        cnt_lst[i]+= 1



#입력
N = int(input())
numbers = list(map(int, input().split()))
mn_ans = max(numbers)**N
mx_ans = -max(numbers)**N

cnt_lst = list(map(int, input().split()))
#함수 실행
dfs(1, numbers[0])
print(mn_ans, mx_ans)