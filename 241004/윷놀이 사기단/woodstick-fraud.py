"""
 윷을 던질 수 있는 횟수는 10  각 횟수마다 나오는 이동 칸 수도 정해져 있습니다.

계산을 하여 주어진 이동 횟수에 나갈 말의 종류를 잘 조합하여 얻을 수 있는 점수의 최댓값을 얻고자

처음에는 시작 칸에 말 4개
말은 게임판에 그려진 화살표를 따라서만 이동할 수 있습니다

 파란색 칸에서 이동을 시작한다면 빨간색 화살표를 타야되고,
 이동하는 도중이거나 파란색 칸이 아닌 곳에서 이동을 시작하면 검은색 화살표를 따라서 가야합니다

 말이 도착 칸으로 이동하면 남은 이동 횟수와 관계 없이 이동을 마칩니다.

 게임은 10개의 턴으로 이뤄지고 도착칸에 도착하지 않은 말을 골라
 원하는 이동횟수만큼 이동할 수 있습니다.

 시작칸과 도착칸을 제외하고는 칸에 말들을 겹쳐서 올릴 수 없습니다.
 특정 말을 움직였을 때 도달하게 되는 위치에 다른 말이 이미 있다면,
 이는 불가능한 이동임을 의미

 10개의 이동할 수 있는 칸 수가 순서대로 주어질 때 얻을 수 있는 점수의 최댓값
"""


# dfs 구현
def dfs(level, finish_lst, score, cur_lst):
    # print(f"==============level : {level}==================")
    # print(finish_lst)
    # print(cur_lst)
    # print(visited)
    # print("score :", score)
    global answer
    if level == 10:
        answer = max(answer, score)
        return

    for i in range(4): #4개의 말 중 하나 선택
        if finish_lst[i]: continue #이미 도착한 말 선택 ㄴㄴ

        tmp_finish = finish_lst[:]
        tmp_cur = cur_lst[:]

        r, c = cur_lst[i]
        before_vi = idx_arr[r][c]
        if score_arr[r][c] in(10, 20, 30) and r==0:
            r = score_arr[r][c]//10
            c = lst[level]-1
        else:
            c += lst[level]

        if c >= len(score_arr[r])-1: #도착이면
            tmp_finish[i] =1
            c = len(score_arr[r])-1

        vi = idx_arr[r][c]
        # print(vi)

        if not tmp_finish[i] and visited[vi]: continue #말 있으면 안간다
        visited[vi] = 1
        visited[before_vi] = 0
        tmp_cur[i] = [r, c]
        dfs(level+1, tmp_finish, score+score_arr[r][c], tmp_cur)
        visited[vi] = 0
        visited[before_vi] = 1


#배열 준비
score_arr =[
    [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 0],
    [13, 16, 19, 25, 30, 35, 40, 0],
    [22, 24, 25, 30, 35, 40, 0],
    [28, 27, 26, 25, 30, 35, 40, 0]
]

idx_arr = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 33],
    [21, 22, 23, 24, 25, 26, 20, 33],
    [27, 28, 24, 25, 26, 20, 33],
    [29, 30, 31, 32, 24, 25, 26, 20, 33]
]

visited = [0]*34
finish_lst = [0]*4
cur_lst = [(0,0), (0,0), (0,0), (0,0)]
answer = 0

lst = list(map(int, input().split()))

#dfs 실행
dfs(0, finish_lst, 0, cur_lst)
#출력
# print('-------------')
print(answer)