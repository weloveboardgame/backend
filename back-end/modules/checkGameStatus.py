# 현재 보드의 4목 성공 여부 판정
# OUTPUT:
# 0 -> 4목 실패 상황, 승자 현재 없음.
# 1 -> 플레이어 1 승리
# 2 -> 플레이어 2 승리

def checkGameStatus(board):
    flag = 0
    # 가로세로 판정
    for i in range(7):
        for j in range(4):
            if board[i][j] == board[i][j+1] and board[i][j] == board[i][j+2] and board[i][j] == board[i][j+3] and board[i][j] != 0:
                flag = board[i][j]
            if board[j][i] == board[j+1][i] and board[j][i] == board[j+2][i] and board[j][i] == board[j+3][i] and board[j][i] != 0:
                flag = board[i][j]

    # 우 하향 대각선 판정
    for i in range(4):
        for j in range(4):
            if board[i][j] == board[i+1][j+1] and board[i][j] == board[i+2][j+2] and board[i][j] == board[i+3][j+3] and board[i][j] != 0:
                flag = board[i][j]

    # 좌 하양 대각선 판정
    for i in range(0,4):
        for j in range(3,7):
            if board[i][j] == board[i+1][j-1] and board[i][j] == board[i+2][j-2] and board[i][j] == board[i+3][j-3] and board[i][j] != 0:
                flag = board[i][j]

    return flag


# CODE FOR TESTING
 board = [
     [0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0],
     [0,1,0,0,0,0,0],
     [0,0,1,0,0,0,0],
     [0,0,0,1,0,0,0],
     [0,0,0,0,0,0,0]
 ]

# print(checkGameStatus(board))
