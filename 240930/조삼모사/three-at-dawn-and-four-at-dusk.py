def dfs(level, idx, s):
    if level == N//2:
        global answer
        answer = min(abs(total-s), answer)
        return

    for i in range(idx, N):
        plus = sum(arr[i])
        for j in range(N):
            plus+= arr[j][i]
        dfs(level+1, i+1, s+plus)

N = int(input())
arr = [list(map(int, input().split())) for _ in range(N)]
total = 0
answer = 100*N*N
for i in range(N):
    total+= sum(arr[i])

dfs(0, 0, 0)
print(answer)