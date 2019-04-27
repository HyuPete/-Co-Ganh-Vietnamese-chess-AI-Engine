# Student Name: Duong Quang Huy
# ID: 1611244

# ======================== Class Player =======================================
import statistics

Initial_Board = [
                  ['b', 'b', 'b', 'b', 'b'], \
                  ['b', '.', '.', '.', 'b'], \
                  ['b', '.', '.', '.', 'r'], \
                  ['r', '.', '.', '.', 'r'], \
                  ['r', 'r', 'r', 'r', 'r'], \
                ]

    # 4 : r r r r r
    # 3 : r . . . r
    # 2 : b . . . r
    # 1 : b . . . b
    # 0 : b b b b b
    #     0 1 2 3 4

init_bIdxL = [0, 1, 2, 3, 4, 5, 9, 10]
init_bPosL = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 4), (2, 0)]
init_rIdxL = [14, 15, 19, 20, 21, 22, 23, 24]
init_rPosL = [(2, 4), (3, 0), (3, 4), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
#======================================================================
# Create dictionary for future use
neighborDict = {}
adjacentDict = {}
neighborPosL = []
adjacentPosL = []
for r in range(5):
    for c in range(5):
        neighborPosL = [(r, c - 1), (r, c + 1), (r - 1, c), (r + 1, c), (r - 1, c - 1), (r + 1, c + 1), (r - 1, c + 1), (r + 1, c - 1)]
        if (r % 2 == 0 and c % 2 != 0) or (r % 2 != 0 and c % 2 == 0):
            adjacentPosL = [(r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c)]
            adjacentPosL = list( filter(lambda x: (0 <= x[0] < 5) and (0 <= x[1] < 5), adjacentPosL) )
            neighborPosL = list( filter(lambda x: (0 <= x[0] < 5) and (0 <= x[1] < 5), neighborPosL) )
            neighborDict[r*5 + c] = neighborPosL
            adjacentDict[r*5 + c] = adjacentPosL
        else:
            adjacentPosL = neighborPosL = list( filter(lambda x: (0 <= x[0] < 5) and (0 <= x[1] < 5), neighborPosL) )
            adjacentDict[r*5 + c] = neighborDict[r*5 + c] = neighborPosL
        
        adjacentPosL = neighborPosL = []
            
def board_copy(board):
    new_board = [[]]*5
    for i in range(5):
        new_board[i] = [] + board[i]
    return new_board
            
def board_print(board, move=[], num=0):

    print("====== The current board(", num, ") is (after move): ======")
    if move: # move not empty
        print("move = ", move)
    for i in [4, 3, 2, 1, 0]:
        print(i, ":", end=" ")
        for j in range(5):
            print(board[i][j], end=" ")
        print()
    print("   ", 0, 1, 2, 3, 4)
    print("")
            
def traverse_CHET(startPos, currColor, oppColor, state, q = []):
    # startPos: starting position for traversing; (r, c)
    # currColor: current player's color
    # oppColor: opponent's color
    # state: board game
    # q: list saving opponents' positions of which colors were changed
    # return True if no way out, else False
    
    # index = startPos[0]*5 + startPos[1]
    # aL = adjacentDict[index]
    #state[ startPos[0] ][ startPos[1] ] = currColor
    
    ############################### DFS

    state[ startPos[0] ][ startPos[1] ] = currColor
    q.append(startPos)
    for x in adjacentDict[ startPos[0]*5 + startPos[1] ]:
        if (state[ x[0] ][ x[1] ] == '.') or ( state[ x[0] ][ x[1] ] == oppColor and ( not traverse_CHET(x, currColor, oppColor, state, q) ) ):
            while(q[-1] != startPos):
                state[ q[-1][0] ][ q[-1][1] ] = oppColor
                q.pop()
            state[ startPos[0] ][ startPos[1] ] = oppColor
            q.pop()
            return False
            
    return True

class Player:
    
            
    # student do not allow to change two first functions
    def __init__(self, str_name):
        self.str = str_name
        self.oppColor = 'r' if str_name == 'b' else 'b'
        #self.isStarter = None # ???
        self.isTrapping = False
        self.oppDict = {}
        self.sameDict = {}
        self.isInit = False
    
    def __str__(self):
        return self.str
    
    
    def doit(self, move, a):
        # move: a list of two tuples
            # (row0, col0): current position of selected piece
            # (row1, col1): new position of selected piece
        # state: a list of 5 list, simulating the game board
        # a: a 3-tuple (if needed) ( state, {playerPosDict}, {OpponentPosDict} )
        
        row0 = move[0][0]
        col0 = move[0][1]
        row1 = move[1][0]
        col1 = move[1][1]
        
        #else: # check if two points are adjacent
        index0 = row0*5 + col0
        index1 = row1*5 + col1
        
        state = a[0]
        playerPosDict = a[1]
        #print(playerPosDict)
        oppPosDict = a[2]
        #if move[0] not in playerPosDict: board_print(state, num = -1)
        playerPosDict[ move[1] ] = adjacentDict[ index1 ]
        del playerPosDict[ move[0] ]
        
        #else: # the move is valid except when previous move is a trapping move, we should do more check @@
        if self.isInit: # starting point of the game, the first move
            #a.append([]) # list of tuples containing positions of traps created by previous move
            
            #TODO: make some changes to the state
            # create new board for the legal move
            self.isInit = False
            new_state = board_copy(state)
            new_state[row0][col0] = '.'
            new_state[row1][col1] = state[row0][col0]
            
            return new_state, playerPosDict, oppPosDict, [ [x, y] for x, v in oppPosDict.items() for y in v if new_state[ y[0] ][ y[1] ] == '.' ], False
            
        #else: # should check the previous move and compare the previous state with the current state
        # if a[-1]: # trapped turn
            # if move[1] not in a[-1]: # previous move is a trapping move, so check for the current move correctness
                # return None
            # a[-1] = [] # no need of saving these traps anymore
            
        #TODO: make some changes to the state
        
        currColor = state[row0][col0]
        oppColor = 'r' if currColor == 'b' else 'b'
        
        new_state = board_copy(state)
        new_state[row1][col1] = currColor
        new_state[row0][col0] = '.'
        
        
        #print(aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa)
        sameL = []
        oppL = []
        pointL = []
        for x in adjacentDict[index1]:
            if new_state[ x[0] ][ x[1] ] == oppColor:
                oppL.append(x)
                #print(x in oppPosDict)
            elif new_state[ x[0] ][ x[1] ] == currColor:
                sameL.append(x)
            elif x != move[0]:
                pointL.append(x)
        
        isChanged = False
        
        ################################# "Ganh":
        
        changedL = [] # list saving chessman positions of which colors are changed
        newOppL = []
        for x in oppL:
            #print(xxxxxxxxxxxxxxxxxxxxxxxxxxx)
            if new_state[ x[0] ][ x[1] ] == oppColor:
                yR = row1*2 - x[0] # find the
                yC = col1*2 - x[1] # symmetric point
                if ( 0 <= yR < 5 ) and ( 0 <= yC < 5 ) and (new_state[ yR ][ yC ] == oppColor): # then "ganh"
                    new_state[ x[0] ][ x[1] ] = currColor
                    new_state[ yR ][ yC ] = currColor
                    isChanged = True
                    changedL.append(x)
                    changedL.append( (yR, yC) )
                    # print(x)
                    # print(oppPosDict)
                    #print(yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy)
                    playerPosDict[x] = oppPosDict[x]
                    playerPosDict[(yR, yC)] = oppPosDict[(yR, yC)]
                    del oppPosDict[x], oppPosDict[(yR, yC)]
                else:
                    newOppL.append(x)
            
        ############################### "Chet":
        if isChanged:
            #oppL = list(filter(lambda x: new_state[ x[0] ][ x[1] ] == oppColor, adjacentDict[index1]))
            if index1 % 2 != 0:
                # Only 1 case could happen to be "Chet" 
                yR = col1 - col0 + row1
                yC = row0 - row1 + col1
                zR = col0 - col1 + row1
                zC = row1 - row0 + col1
                if ( (0 <= yR < 5) and (0 <= yC < 5) and (new_state[yR][yC] != currColor) ):
                    pass
                elif ( (0 <= zR < 5) and (0 <= zC < 5) and (new_state[zR][zC] != currColor) ):
                    pass
                else:
                    for x in newOppL:
                        if traverse_CHET(x, currColor, oppColor, new_state):
                            isChanged = True
                        
            #elif index0 % 2 != 0:
            else:
                for x in newOppL:
                    if traverse_CHET(x, currColor, oppColor, new_state):
                        isChanged = True
            
            for x in changedL:
                for y in adjacentDict[ x[0]*5 + x[1] ]:
                    if (new_state[ y[0] ][ y[1] ] == oppColor) and ( traverse_CHET(y, currColor, oppColor, new_state) ):
                        isChanged = True
            
            
        else: # not "ganh" # isChanged == False
            if index1 % 2 != 0:
                # Only 1 case could happen to be "Chet" 
                yR = col1 - col0 + row1
                yC = row0 - row1 + col1
                zR = col0 - col1 + row1
                zC = row1 - row0 + col1
                if ( (0 <= yR < 5) and (0 <= yC < 5) and (new_state[yR][yC] != currColor) ):
                    pass
                elif ( (0 <= zR < 5) and (0 <= zC < 5)  and (new_state[zR][zC] != currColor) ):
                    pass
                else:
                    for x in oppL:
                        if traverse_CHET(x, currColor, oppColor, new_state):
                            isChanged = True
                        
            #elif index0 % 2 != 0:
            else:
                for x in oppL:
                    if traverse_CHET(x, currColor, oppColor, new_state):
                        isChanged = True
            #else: #(row0*5 + col0) % 2 == 0:
        
        for x in list(oppPosDict):
            if new_state[ x[0] ][ x[1] ] == currColor:
                playerPosDict[x] = oppPosDict[x]
                del oppPosDict[x]
        
        ################################ "Bay":
        trapL = []
        if not isChanged: # this move didn't change any piece's color
            #TODO: check whether there is any trap created by this move. If yes, save that position.
            
            sameL = []
            oppL = []
            isOppExist = False
            for x in adjacentDict[index0]:
                if new_state[ x[0] ][ x[1] ] == currColor:
                    sameL.append(x)
                elif new_state[ x[0] ][ x[1] ] == oppColor:
                    isOppExist = True
                    oppL.append(x)
            
            if isOppExist: # if exist an opponent which can reach that position
                isOppExist = False
                for x in sameL:
                    yR = row0*2 - x[0]
                    yC = col0*2 - x[1]
                    if (0 <= yR < 5) and (0 <= yC < 5) and ( new_state[ yR ][ yC ] == currColor ):
                        for x in oppL:
                            trapL.append( [ x, move[0] ] )
                        break
            
            # isOppExist == False
            d = {}
            for x in pointL: # excluded move[0]
                for y in adjacentDict[ x[0]*5 + x[1] ]:
                    if new_state[ y[0] ][ y[1] ] == oppColor:
                        isOppExist = True
                        if x not in d:
                            d[x] = [y]
                        else:
                            d[x].append(y)
                
                if isOppExist:
                    isOppExist = False
                    yR = x[0]*2 - row1
                    yC = x[1]*2 - col1
                    if (0 <= yR < 5) and (0 <= yC < 5) and ( new_state[ yR ][ yC ] == currColor ):
                        for y in d[x]:
                            trapL.append( [y, x] )
            
        ########################################
        if trapL:
            return new_state, playerPosDict, oppPosDict, trapL, True
        else:
            return new_state, playerPosDict, oppPosDict, [ [x, y] for x, v in oppPosDict.items() for y in v if new_state[ y[0] ][ y[1] ] == '.' ], False
    
    def checkGANH(self, state, move, isMe = True):
        if isMe:
            pass
        else:
            pass
    
    def checkCHET(self, move, isMe = True):
        pass
    
    def checkBeTrapped(self, state, isMe = True):
        # return [list of possible moves]
        
        if not isMe:
            currColor = self.oppColor
            oppColor = self.str
            sameDict = self.oppDict
            oppDict = self.sameDict
        else:
            currColor = self.str
            oppColor = self.oppColor
            sameDict = self.sameDict
            oppDict = self.oppDict
        
        isTrapped = True
        for x in list(sameDict):
            if state[ x[0] ][ x[1] ] == oppColor:
                isTrapped = False
                oppDict[x] = sameDict[x]
                del sameDict[x]
        
        
        if not isTrapped:
            for x in oppDict:
                if state[ x[0] ][ x[1] ] == '.':
                    for y in oppDict[x]:
                        if state[ y[0] ][ y[1] ] == oppColor and y not in oppDict:
                            oppDict[y] = adjacentDict[ y[0]*5 + y[1] ]
                            del oppDict[x]
                            return []
                            #return [ [x, y] for x, v in sameDict.items() for y in v if state[ y[0] ][ y[1] ] == '.' ]
        else:
            isTrapped = False
            move = []
            for x in oppDict:
                if state[ x[0] ][ x[1] ] == '.': # compare with previous state
                    move.append( x )
                    trapL = []
                    sameL = []
                    oppL = []
                    pointL = []
                    isOppExist = False
                    for y in oppDict[x]:
                        if state[ y[0] ][ y[1] ] == oppColor:
                            if y not in oppDict:
                                move.append(y)
                                oppDict[y] = adjacentDict[ y[0]*5 + y[1] ]
                                for z in oppDict[y]:
                                    if state[ z[0] ][ z[1] ] == '.' and z != x:
                                        pointL.append(z)
                                        
                            sameL.append(y)
                        elif state[ y[0] ][ y[1] ] == currColor:
                            isOppExist = True
                            oppL.append(y)
                        
                    if isOppExist: # if exist an opponent which can reach that position
                        isOppExist = False
                        for z in sameL: # == oppColor
                            yR = x[0]*2 - z[0]
                            yC = x[1]*2 - z[1]
                            if (0 <= yR < 5) and (0 <= yC < 5) and ( state[ yR ][ yC ] == oppColor ):
                                isTrapped = True
                                for z in oppL:
                                    trapL.append( [z, x] )
                                break
                                
                    # isOppExist == False
                    d = {}
                    for z in pointL: # excluded move[0]
                        for y in adjacentDict[ z[0]*5 + z[1] ]:
                            if state[ y[0] ][ y[1] ] == currColor:
                                isOppExist = True
                                if z in d:
                                    d[z].append(y)
                                else:
                                    d[z] = [y]
                        
                        if isOppExist:
                            isOppExist = False
                            yR = z[0]*2 - move[1][0]
                            yC = z[1]*2 - move[1][1]
                            if (0 <= yR < 5) and (0 <= yC < 5) and ( state[ yR ][ yC ] == oppColor ):
                                isTrapped = True
                                for t in d[z]:
                                    trapL.append( [t, z] )
                    
                    del oppDict[x]
                    #if isTrapped:
                    return trapL
                    #else:
                    #    return 
        return []
        
    # create all possible moves for a specific state
    def generateMove(self, state, isMe = True):
        if isMe:
            return [ [x, y] for x, v in self.sameDict.items() for y in v if state[ y[0] ][ y[1] ] == '.' ]
        else:
            return [ [x, y] for x, v in self.oppDict.items() for y in v if state[ y[0] ][ y[1] ] == '.' ]
        
    def evaluateBoard(self, playerPD, oppPD):
        # if isMe:
        result = 0
        for x in playerPD:
            if x in ( (1, 1), (1, 3), (3, 1), (3, 3), (2, 2) ):
                result += 1.5
            else:
                result += 1
        for x in oppPD:
            if x in ( (1, 1), (1, 3), (3, 1), (3, 3), (2, 2) ):
                result -= 1.5
            else:
                result -= 1
        return result #len(playerPD) - len(oppPD)
        # else:
            # return len(oppPD) - len(playerPD)

    def minimaxSearch(self, depth, state, trapL = [], isMe = True):
        #player,
        #opp = 'b' if player == 'r' else 'r'

        #trapMove = []
        #if state != self.previous_state:
        #    trapMove = self.getTrapMove(player,state,self.previous_state)
        
        # if isMe:
            # oppColor = self.oppColor
            # currColor = self.str

        # else:
            # oppColor = self.str
            # currColor = self.oppColor
        #print(trapL)
        #print(self.sameDict)
        mvL = trapL if trapL else self.generateMove(state, isMe)
        if not mvL:
            return []
        # print(mvL)
        # print(self.oppDict)
        #print(self.sameDict)
        # Minimax
        bestMove = None
        bestValue = -999
        alpha = -999
        beta = 999
        #isTrappingMove = False
        playerPD = None
        oppPD = None
        if isMe:
            for move in mvL:
                new_state, playerPosDict, oppPosDict, possibleMvL, isTrapping = self.doit( move, ( state, self.sameDict.copy(), self.oppDict.copy() ) )
                
                #print(mvL)
                boardValue = self.minimax(depth - 1, new_state, oppPosDict, playerPosDict, possibleMvL, alpha, beta, not isMe)
                
                if (boardValue > bestValue):
                    bestValue = boardValue
                    bestMove = move
                    #isTrappingMove = isTrapping
                    playerPD = playerPosDict
                    oppPD = oppPosDict
                    
                alpha = max(alpha, bestValue)
                if alpha >= beta:
                    break
        # else:
            # for move in mvL:
                # new_state, playerPosDict, oppPosDict, possibleMvL, isTrapping = self.doit( move, ( state, self.oppDict.copy(), self.sameDict.copy() ) )
                
                # #print(mvL)
                # boardValue = self.minimax(depth - 1, new_state, oppPosDict, playerPosDict, possibleMvL, -100, 100, not isMe)

                # if (boardValue > bestValue):
                    # bestValue = boardValue
                    # bestMove = move
                    # isTrappingMove = isTrapping
        
        #if isMe:
            #self.isTrapping = isTrappingMove
            #print(self.sameDict)
            self.sameDict = playerPD
            self.oppDict = oppPD
            #print(self.sameDict)
            
        return bestMove

    def minimax(self, depth, state, playerPosDict, oppPosDict, moveList, alpha, beta, isMe = True):
        #print(moveList)
        if (depth == 0) or not moveList:
            return ( self.evaluateBoard(playerPosDict, oppPosDict) ) if isMe else -self.evaluateBoard(playerPosDict, oppPosDict)
        # if not moveList:
            # return self.evaluateBoard(playerPosDict, oppPosDict) if isMe else -self.evaluateBoard(playerPosDict, oppPosDict) #???
            
        # Minimax
        
        #opp = 'b' if player == 'r' else 'r'

        if isMe:
            bestVal = -999
            for move in moveList:
                new_state, playerPD, oppPD, mvL, isTrapping = self.doit( move, ( state, playerPosDict.copy(), oppPosDict.copy() ) )
                
                bestVal = max( bestVal, self.minimax(depth - 1, new_state, oppPD, playerPD, mvL, alpha, beta, not isMe) )

                alpha = max(alpha, bestVal)
                #if bestVal > beta
                
                
                if beta <= alpha:
                    return bestVal
            
            return bestVal
            
            # valL = []
            # for move in moveList:
                # new_state, playerPD, oppPD, mvL, isTrapping = self.doit( move, ( state, playerPosDict.copy(), oppPosDict.copy() ) )
                
                # valL.append( self.minimax(depth - 1, new_state, oppPD, playerPD, mvL, alpha, beta, not isMe) )
            
            # return mean(valL)

        else:
            # bestVal = 999
                
            # for move in moveList:
                # new_state, playerPD, oppPD, mvL, isTrapping = self.doit( move, ( state, playerPosDict.copy(), oppPosDict.copy() ) )
                # bestVal = min( bestVal, self.minimax(depth - 1, new_state, oppPD, playerPD, mvL, alpha, beta, not isMe) )

                # beta = min(beta, bestVal)
                # #alpha = max(alpha, bestVal)
                
                # # if bestVal < alpha:
                    # # return -999
                
                # if beta <= alpha:
                    # return bestVal
            # return bestVal
            
            valL = []
            for move in moveList:
                new_state, playerPD, oppPD, mvL, isTrapping = self.doit( move, ( state, playerPosDict.copy(), oppPosDict.copy() ) )
                
                valL.append( self.minimax(depth - 1, new_state, oppPD, playerPD, mvL, alpha, beta, not isMe) )
            
            beta = statistics.mean(valL)
            
            return beta
            
    # Student MUST implement this function
    # The return value should be a move that is denoted by a list of tuples:
    # [(row1, col1), (row2, col2)] with:
        # (row1, col1): current position of selected piece
        # (row2, col2): new position of selected piece
    def next_move(self, state):
        if not self.sameDict: # we are the first to move a piece.
            if state == Initial_Board: # start from the initial board
                if self.oppColor == 'r':
                    self.oppDict = dict([(x, adjacentDict[ x[0]*5 + x[1] ]) for x in init_rPosL]) # [ [ (pos), [adjacentPosL] ] ]
                    self.sameDict = dict([(x, adjacentDict[ x[0]*5 + x[1] ]) for x in init_bPosL]) # [ [ (pos), [adjacentPosL] ] ]
                    # self.oppL = init_rPosL[:]
                    # self.sameL = init_bPosL[:]
                    
                else:
                    self.oppDict = dict([(x, adjacentDict[ x[0]*5 + x[1] ]) for x in init_bPosL]) # [ [ (pos), [adjacentPosL] ] ]
                    self.sameDict = dict([(x, adjacentDict[ x[0]*5 + x[1] ]) for x in init_rPosL]) # [ [ (pos), [adjacentPosL] ] ]
                    # self.oppL = init_bPosL[:]
                    # self.sameL = init_rPosL[:]
                
                self.isInit = True
                
                #return self.minimaxSearch(state)
                
            else: # start from an arbitrary board different from the initial one
                for r in range(5):
                    for c in range(5):
                        if state[r][c] == self.str:
                            self.sameDict[(r, c)] = adjacentDict[r*5 + c]
                        elif state[r][c] == self.oppColor:
                            self.oppDict[(r, c)] = adjacentDict[r*5 + c]
                        
                #return self.minimaxSearch(state)
            return self.minimaxSearch(4, state)
        
        ######## not a first move, in the middle of the fight )))
        
        ############################ 
        # Check if opponent take a "Bay" move (trapping move)
        #if not self.isTrapping: # if we didn't setup traps in our previous turn
        trapL = self.checkBeTrapped(state)
    
        return self.minimaxSearch(4, state, trapL)

            #print(self.sameDict)
        #return self.minimaxSearch(4, state)
        # #result = [(2, 0), (3, 1)]
        # return result


    # Theo như code trong file co_ganh.py, ở hàm next_move chỉ nhận một tham số ngoài self là state (tức trạng thái bàn cờ hiện tại). Như vậy, ở mỗi lượt chơi của mình, người chơi không biết được một cách nhanh chóng là ở nước đi trước đối phương có đi nước cờ bẫy hay không để đi theo đúng luật. Ví dụ: ở lượt xanh, xanh đi nước gánh, sau đó đến lượt đỏ, đỏ đi nước bẫy mong muốn xanh đi theo ý mình, sau đó quay lại đến lượt xanh. Lúc này vì xanh chỉ có thể biết được trạng thái bàn cờ hiện tại, nên để biết được ở nước đi trước, đỏ đã đi nước cờ bẫy, em nghĩ mình buộc phải có một biến toàn cục hoặc một biến thuộc tính của class Player trong file co_ganh.py lưu giữ trạng thái bàn cờ ngay ở lượt trước để so sánh, kiểm tra xem đỏ có đi nước cờ bẫy hay không và nếu có bẫy đó nằm ở đâu để xanh biết đi theo đúng luật.