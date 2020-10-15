from pulp import *

N = 8

prob = LpProblem(f"{N}_Queens", LpMaximize)
board = [[LpVariable(f"{x},{y}", cat=LpBinary) for x in range(N)] for y in range(N)]

for i in range(N):
    # Exactly one queen per column
    prob += lpSum([board[x][i] for x in range(N)]) == 1

    # Exactly one queen per row
    prob += lpSum([board[i][y] for y in range(N)]) == 1

    # At most one queen per positive diagonal
    prob += lpSum([board[x][i - x] for x in range(i + 1)]) <= 1
    prob += lpSum([board[x][N - x + i] for x in range(i + 1, N)]) <= 1
    
    # At most one queen per negative diagonal
    prob += lpSum([board[x][x - i - 1] for x in range(i + 1, N)]) <= 1
    prob += lpSum([board[x][N - 1 - i + x] for x in range(i + 1)]) <= 1

status = prob.solve()
if LpStatus[status] == "Optimal":
    for row in board:
        print(" ".join(["Q" if value(v) else "." for v in row]))
