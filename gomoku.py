import pygame

def generateBoard(size):
    board = []
    for i in range(1, size + 1):
        row = []
        for j in range(1, size + 1):
            row.append(0)
        board.append(row)

    return board

def countPossibleMoves(board):
    remainMoves = 0;

    for row in range(len(board)):
        for column in range(len(board[row])):
            if (board[row][column] == 0):
                remainMoves += 1
    return remainMoves

def findAllPossibleMoves(board, remainMoves):
    alreadyMoves = []
    possibleBoards = []

    for turn in range(remainMoves):
        for row in range(len(board)):
            for column in range(len(board[row])):
                if ( board[row][column] == 0 and [row, column] not in alreadyMoves):
                    alreadyMoves.append([row, column])

    return alreadyMoves 

def shapeScore(consecutive, openEnds, currentTurn):
    winGuarantee = 1000000;
    if openEnds == 0 and consecutive < 5:
        return 0;
    if (consecutive == 4):
        if openEnds == 1:
            if currentTurn:
                return winGuarantee;
            return 50;
        elif openEnds == 2:
            if currentTurn:
                return winGuarantee;
            return 50000;
    elif (consecutive == 3):
        if openEnds == 1:
            if currentTurn:
                return 7;
            return 5;
        elif openEnds == 2:
            if currentTurn:
                return 10000;
            return 50;
    elif (consecutive == 2):
        if openEnds == 1:
            return 2;
        elif openEnds == 2:
            return 5;
    elif (consecutive == 1):
        if openEnds == 1:
            return 0.5 
        elif openEnds == 2:
            return 1
    else:
        return 100000000;

def evaluateHorizontal(board, forBlack, playerTurn):
    score = 0
    consecutive = 0
    openEnds = 0

    horizontal = []
    
    for row in range(len(board)):
        boardRow = []
        for column in range(len(board[row])):
            boardRow.append(board[row][column])
        horizontal.append(boardRow)

    for horizontalRow in horizontal:
        consecutive = 0
        openEnds = 0
        for item in horizontalRow:
            if item == (2 if forBlack else 1):
                consecutive += 1
            elif item == 0 and consecutive > 0:
                openEnds += 1
                score += shapeScore(consecutive, openEnds, forBlack == playerTurn)
                consecutive = 0
                openEnds = 1
            elif item == 0:
                openEnds = 1
            elif consecutive > 0:
                score += shapeScore(consecutive, openEnds, forBlack == playerTurn)
                consecutive = 0
                openEnds = 0
            else:
                openEnds = 0
        
        if consecutive > 0:
            score += shapeScore(consecutive, openEnds, forBlack == playerTurn)

    return score

def evaluateVertical(board, forBlack, playerTurn):
    score = 0
    consecutive = 0
    openEnds = 0

    vertical = []
    columnCounter = 0
    while columnCounter < len(board[0]):
        verticalRow = []
        for row in range(len(board)):
            for column in range(len(board[row])):
                if (column == columnCounter):
                    verticalRow.append(board[row][column])
                    break;
        vertical.append(verticalRow)
        columnCounter += 1

    for verticalRow in vertical:
        consecutive = 0
        openEnds = 0
        for item in verticalRow:
            if item == (2 if forBlack else 1):
                consecutive += 1
            elif item == 0 and consecutive > 0:
                openEnds += 1
                score += shapeScore(consecutive, openEnds, forBlack == playerTurn)
                consecutive = 0
                openEnds = 1
            elif item == 0:
                openEnds = 1
            elif consecutive > 0:
                score += shapeScore(consecutive, openEnds, forBlack == playerTurn)
                consecutive = 0
                openEnds = 0
            else:
                openEnds = 0
        
        if consecutive > 0:
            score += shapeScore(consecutive, openEnds, forBlack == playerTurn)

    return score

def evaluateDiagonal(board, forBlack, playerTurn):
    score = 0
    consecutive = 0
    openEnds = 0

    diagonal = []

    rowCount = 0

    # Upper Diagonal /
    for i in range(len(board)):
        diagonalRow = []
        for j in range((len(board[i]))):
            if ( i == j and i == 0):
                diagonalRow.append(board[i][j])
            elif (j == 0):
                diagonalRow.append(board[i][j])
                for row in range(i, -1, -1):
                    for column in range(j, len(board)):
                        if (row == i - 1 and column == j + 1):
                            diagonalRow.append(board[row][column])
                            i -= 1
                            j += 1
        diagonal.append(diagonalRow)

    # Bottom Diagonal /
    for i in range(len(board)):
        diagonalRow = []
        for j in range((len(board[i])) -1, -1, -1):
            if ( i == j and i == (len(board) - 1)):
                diagonalRow.append(board[i][j])
                break;
            elif (j == len(board) - 1):
                diagonalRow.append(board[i][j])
                for row in range(i, len(board)):
                    for column in range(len(board) -1, -1, -1):
                        if (row == i + 1 and column == j - 1):
                            diagonalRow.append(board[row][column])
                            i += 1
                            j -= 1
        if ( len(diagonalRow) == len(board)):
            continue   
        diagonal.append(diagonalRow)

    # Bottom Diagonal \
    for i in range(len(board) - 1, -1, -1):
        diagonalRow = []
        for j in range(0, len(board)):
            if ( i == len(board) - 1 and j == 0):
                diagonalRow.append(board[i][j])
            elif ( j == 0):
                diagonalRow.append(board[i][j])
                for row in range(i, len(board)):

                    for column in range(j, len(board)):
                        if (row == i + 1 and column == j + 1):
                            diagonalRow.append(board[row][column])
                            i += 1
                            j += 1
                    
        diagonal.append(diagonalRow)

    #Upper Diagonal \
    for i in range(len(board) - 1, -1, -1):
        anotherDiagonalRow = []
        for j in range(0, len(board)):
            if ( i == len(board) - 1 and j == 0):
                anotherDiagonalRow.append(board[j][i])
            elif ( j == 0):
                anotherDiagonalRow.append(board[j][i])
                for row in range(i, len(board)):

                    for column in range(j, len(board)):
                        if (row == i + 1 and column == j + 1):
                            anotherDiagonalRow.append(board[column][row])
                            i += 1
                            j += 1
        if ( len(anotherDiagonalRow) == len(board)):
            continue    
        diagonal.append(anotherDiagonalRow)
    

    

    for diagonalRow in diagonal:
        consecutive = 0
        openEnds = 0
        for item in diagonalRow:
            if item == (2 if forBlack else 1):
                consecutive += 1
            elif item == 0 and consecutive > 0:
                openEnds += 1
                score += shapeScore(consecutive, openEnds, forBlack == playerTurn)
                consecutive = 0
                openEnds = 1
            elif item == 0:
                openEnds = 1
            elif consecutive > 0:
                score += shapeScore(consecutive, openEnds, forBlack == playerTurn)
                consecutive = 0
                openEnds = 0
            else:
                openEnds = 0
        
        if consecutive > 0:
            score += shapeScore(consecutive, openEnds, forBlack == playerTurn)

    return score

def getScore(board, forBlack, blackTurn):
    score = 0
    score += evaluateHorizontal(board, forBlack, blackTurn)
    score += evaluateVertical(board, forBlack, blackTurn)
    score += evaluateDiagonal(board, forBlack, blackTurn)
    return score

def evaluateBoard(board, blackTurn):
    blackScore = getScore(board, True, blackTurn)
    whiteScore = getScore(board, False, blackTurn)

    if blackScore == 0:
        blackScore = 1.0
    
    return whiteScore / blackScore

def cloneBoard(board):
    clone = []

    for row in range(len(board)):
        rowClone = []
        for column in range(len(board[row])):
            rowClone.append(board[row][column])
        clone.append(rowClone)
    
    return clone

def addMoveOnBoard(board, move, black):
    board[move[0]][move[1]] = 2 if black else 1

def addMove(board, move, black):
    if board[move[0]][move[1]] != 0:
        return False 
    
    board[move[0]][move[1]] = 2 if black else 1
    return True

def searchWinningMoves(board, winScore):
    possibleMoves = findAllPossibleMoves(board, countPossibleMoves(board))

    for move in possibleMoves:
        clonedBoard = cloneBoard(board)
        addMoveOnBoard(clonedBoard, move, False)

        if getScore(clonedBoard, False, False) >= winScore:
            return move
    return None

def minimax(board, depth, isMax, alpha, beta):
    if depth == 0:
        return evaluateBoard(board, not isMax), None
    possibleMovesCount = countPossibleMoves(board)
    if possibleMovesCount == 0:
        return evaluateBoard(board, not isMax), None
    possibleMoves = findAllPossibleMoves(board, possibleMovesCount)
    bestMove = None;

    if isMax:
        bestValue = -1.0
        for move in possibleMoves:
            clonedBoard = cloneBoard(board)
            addMoveOnBoard(clonedBoard, move, False)
            value, tempMove = minimax(clonedBoard, depth - 1, not isMax, alpha, beta)
            if value > alpha:
                alpha = value 
            if value >= beta:
                return value, tempMove 
            if value > bestValue:
                bestValue = value
                bestMove = move
    else:
        bestValue = 100000000
        bestMove = possibleMoves[0]
        for move in possibleMoves:
            clonedBoard = cloneBoard(board)
            addMoveOnBoard(clonedBoard, move, True)
            value, tempMove = minimax(clonedBoard, depth - 1, not isMax, alpha, beta)
            if value < beta:
                beta = value 
            if value <= alpha:
                return value, tempMove 
            if value < bestValue:
                bestValue = value
                bestMove = move 
    return bestValue, bestMove

def findNextMove(board, depth, winScore):
    move = [-1, -1]
    bestMove = searchWinningMoves(board, winScore=winScore)
    if bestMove is not None:
        move[0] = bestMove[0]
        move[1] = bestMove[1]
    else:
        value, bestMove = minimax(board, depth, True, -1.0, 100000000)
        if bestMove is None:
            move = None
        else:
            move[0] = bestMove[0]
            move[1] = bestMove[1]
    
    return move

def checkWinner(board, winScore):
    if (getScore(board, True, False) >= winScore):
        return 2
    if (getScore(board, False, True) >= winScore):
        return 1
    return 0

class Chessboard:

    def __init__(self):
        self.grid_size = 26
        self.start_x, self.start_y = 50, 80
        self.edge_size = self.grid_size / 2
        self.grid_count = 12
        self.piece = 2
        self.winner = None
        self.game_over = False
        self.winScore = 100000000
        self.depth = 1

        self.grid = generateBoard(self.grid_count)
        self.grid[6][6] = 2;
        self.piece = 1;

    def handle_key_event(self, e):
        origin_x = self.start_x - self.edge_size
        origin_y = self.start_y - self.edge_size
        size = (self.grid_count - 1) * self.grid_size + self.edge_size * 2
        pos = e.pos
        if origin_x <= pos[0] <= origin_x + size and origin_y <= pos[1] <= origin_y + size:
            if not self.game_over:
                x = pos[0] - origin_x
                y = pos[1] - origin_y
                r = int(y // self.grid_size)
                c = int(x // self.grid_size)
                if self.set_piece(r, c):
                    self.check_win(r, c)
                    return True

    def set_piece(self, r, c):

        if self.grid[r][c] == 0:
            self.grid[r][c] = self.piece

            if self.piece == 1:
                self.piece = 2
            else:
                self.piece = 1

            return True
        return False

    def check_win(self, r, c):
        if (checkWinner(self.grid, self.winScore)):
            self.winner = self.grid[r][c]
            self.game_over = True

    def draw(self, screen):
        #(185, 122, 87)
        pygame.draw.rect(screen, (0, 122, 230),
                         [self.start_x - self.edge_size, self.start_y - self.edge_size,
                          (self.grid_count - 1) * self.grid_size + self.edge_size * 2, (self.grid_count - 1) * self.grid_size + self.edge_size * 2], 0)

        for r in range(self.grid_count):
            y = self.start_y + r * self.grid_size
            pygame.draw.line(screen, (0, 0, 0), [self.start_x, y], [self.start_x + self.grid_size * (self.grid_count - 1), y], 2)

        for c in range(self.grid_count):
            x = self.start_x + c * self.grid_size
            pygame.draw.line(screen, (0, 0, 0), [x, self.start_y], [x, self.start_y + self.grid_size * (self.grid_count - 1)], 2)

        for r in range(self.grid_count):
            for c in range(self.grid_count):
                piece = self.grid[r][c]
                if piece != 0:
                    if piece == 1:
                        color = (255, 255, 255)
                    else:
                        color = (0, 0, 0)

                    x = self.start_x + c * self.grid_size
                    y = self.start_y + r * self.grid_size
                    pygame.draw.circle(screen, color, [x, y], self.grid_size // 2)

class Gomoku():

    def __init__(self):

        self.screen = pygame.display.set_mode((400, 500))
        pygame.display.set_caption("Gomoku")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(r"./consola.ttf", 24)
        self.going = True

        self.chessboard = Chessboard()


    def loop(self):
        while self.going:
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()

    def update(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.going = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if (self.chessboard.handle_key_event(e)):
                    self.draw()

                    if (self.chessboard.winner == 1 or self.chessboard.winner == 2):
                        return;

                    move = findNextMove(self.chessboard.grid, self.chessboard.depth, self.chessboard.winScore)
                    if move is None or move[0] == -1:
                        self.chessboard.game_over = True
                        return;

                    self.chessboard.set_piece(move[0], move[1])
                    self.chessboard.check_win(move[0], move[1])


    def draw(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.font.render("FPS: {0:.2F}".format(self.clock.get_fps()), True, (0, 0, 0)), (10, 10))
        self.screen.blit(self.font.render("Black: {0}".format(getScore(self.chessboard.grid, True, True)), True, (0, 0, 0)), (10, 400))
        self.screen.blit(self.font.render("White: {0}".format(getScore(self.chessboard.grid, False, True)), True, (0, 0, 0)), (10, 440))

        self.chessboard.draw(self.screen)
        if self.chessboard.game_over:
            self.screen.blit(self.font.render("{0} Win".format("Black" if self.chessboard.winner == 2 else "White"), True, (0, 0, 0)), (10, 40))
            

        pygame.display.update()

pygame.init()
gomoku = Gomoku()
gomoku.loop()