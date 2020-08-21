# 중력 변경에 따른 현재 보드 상태를 변경하는 모듈
# Player A: 1
# Player B: 2
# No stone: 0

# PARAMETER
# board: 7*7 2차원 list
# gravityD(Direction): N or S or W or E (char)



def appplyGravity(board, gravityD):
    if gravityD == 'W':
        newBoard = [0 for i in range(7)]
        tempBoard = [0 for i in range(7)]

        for i in range(0,7):
            tempBoard = [0 for i in range(7)]
            flag = 0
            for j in range(0,7):
                if board[i][j] != 0:
                    tempBoard[flag] = board[i][j]
                    flag += 1
            newBoard[i] = tempBoard
        return newBoard
    if gravityD == 'E':
        newBoard = [0 for i in range(7)]
        tempBoard = [0 for i in range(7)]
        for i in range(0,7):
            tempBoard = [0 for i in range(7)]
            flag = 0
            for j in range(0,7):
                if board[i][j] != 0:
                    tempBoard[6-flag] = board[i][j]
                    flag += 1
            newBoard[i] = tempBoard
        return newBoard
    if gravityD == 'N':
        newBoard = [[0 for col in range(7)] for row in range(7)]
        for i in range(0,7):
            flag = 0
            for j in range(0,7):
                if board[j][i] != 0:
                    newBoard[flag][i] = board[j][i]
                    flag += 1
        return newBoard
    if gravityD == 'S':
        newBoard = [[0 for col in range(7)] for row in range(7)]
        for i in range(0,7):
            flag = 0
            for j in range(0,7):
                if board[j][i] != 0:
                    newBoard[6-flag][i] = board[j][i]
                    flag += 1
        return newBoard

# CODE FOR TESTING
# board = [
#     [0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0],
#     [0,0,1,2,0,0,2],
#     [0,1,0,2,0,0,0],
#     [0,0,0,0,0,0,1],
#     [0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0]
# ]

# for i in range(7):
#     print(appplyGravity(board, 'S')[i])