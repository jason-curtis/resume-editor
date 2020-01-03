#tic-tac-toe game
#
#with AI version 5
#added alpha-beta pruning of search tree
#
#
#by Jason Curtis
#Mar 3 2011

import random
from time import clock

#global variables are used only for algorithm analysis.
statesEvaluated = [0]*10
statesScored = [0]*10
statesSymmetrized = [0]*10
statesPruned = [0]*10
timeScoring = 0.0
timeSymmetrizing = 0.0

def algoReport(elapsed):
    global statesEvaluated 
    global statesScored
    global statesSymmetrized
    global statesPruned
    global timeScoring
    global timeSymmetrizing
    totalEvals = sum(statesEvaluated)
    print(
        "states pondered:",totalEvals,"(distribution:", statesEvaluated,\
        "\n  in", round(elapsed, 4), "seconds of CPU time",\
        "\n ",    round(elapsed/totalEvals,10),"secs/board",\
        "\n ",    sum(statesScored),"terminal states scored (distribution:", statesScored,".",\
                    timeScoring, "seconds spent)",\
        "\n ",    sum(statesSymmetrized),"states and their children pruned with symmetry checking.",\
        "\n  (distribution:", statesSymmetrized,".",\
                    timeSymmetrizing, "seconds spent)",\
        "\n  alpha-beta pruning applied", sum(statesPruned),"times (distribution:", statesScored,")"
    )

def resetGlobals():
    global statesEvaluated
    global statesScored
    global statesSymmetrized
    global timeScoring
    global timeSymmetrizing
    statesEvaluated = [0]*10
    statesScored = [0]*10
    statesSymmetrized = [0]*10
    statesPruned = [0]*10
    timeScoring = 0.0
    timeSymmetrizing = 0.0


def score(board, d = 0, winCheck = 0, terminal = 0):
    #algo stuff:
    global timeScoring
    tStart = clock()
    
    f = 0;
    #value heuristic: 
    # f=100+d if x in winning position; +d is to value quicker wins
    # f=-100-d if o in winning position; -d is to value quicker wins
    # +1 for each row, col or diag with 1 x & no o's 
    # -1 for each row, col or diag with 1 o & no xes 
    # +2 for row/col/diag with 2 xes & no o's
    # -2 for row/col/diag with 2 o's & no xes 
    
    #back-of-envelope calculation says that, in non-winning conditions,
    # f ranges from:
    # (8 rows, cols and diags) * (max score of 2 for each) = +16 to -16
    # don't think these are technically acheivable without a winning condition
    
    line1 = [board[0],board[1],board[2]]
    line2 = [board[3],board[4],board[5]]
    line3 = [board[6],board[7],board[8]]
    
    col1 = [board[0],board[3],board[6]]
    col2 = [board[1],board[4],board[7]]
    col3 = [board[2],board[5],board[8]]
    
    diag1 = [board[0],board[4],board[8]]
    diag2 = [board[2],board[4],board[6]]
    
    lines = [line1,line2,line3,col1,col2,col3,diag1,diag2]
    
    for line in lines:
        xes = line.count(1)
        os = line.count(-1)
        if winCheck:
            if xes == 3:
                return 1
            if os == 3:
                return -1
        else:
            if xes == 3:
                    f = 100 + d
                    break
            if os == 3:
                    f = -100 - d
                    break
            
            if not terminal: #these only matter if state is not terminal
                if xes == 0:
                    if os == 2:
                        f -= 2
                    elif os == 1:
                        f -= 1
                elif os == 0:
                    if xes == 2:
                        f += 2
                    elif xes == 1:
                        f += 1

    if winCheck: return 0;
    else:
        timeScoring += clock() - tStart
        return f;

def boardPrint(board, showNums = 0):
    strBoard = ""
    for i in range(len(board)):
        #place the 'x'es and 'o's
        if board[i]:
            strBoard += "x" if (board[i] == 1) else "o"
        elif showNums:
            strBoard += str(i)
        else: 
            strBoard += " "
        
        #now place the lines:
        if i != 8:
            if (i+1)%3 == 0:
                strBoard += "\n-----\n"
            else:
                strBoard += "|"
    print(strBoard)

def playMove(oldBoard, d, player, AIplayer):
    print("\ncurrent player:", pName(player))
    if d:
        if player == AIplayer:
            t1 = clock()#for elapsed time
            Move = chooseMove(oldBoard, 9, player)[1] # run AI
            elapsed = clock()-t1
            
            algoReport(elapsed)
            resetGlobals()
            
        else:
            Move = askForMove(oldBoard)#get human player's decision
        
        newBoard = oldBoard[:Move] + [player] + oldBoard[Move+1:] #stick the x or o in place
        print("taking square #", str(Move), ":")
        boardPrint(newBoard)
        
        s = score(newBoard, winCheck = 1)
        if s == 1:
            print("x wins!")
            gameOver()
        elif s == -1:
            print("o wins!")
            gameOver()
        else:
            playMove(newBoard, d-1, -player, AIplayer)
    else: gameOver()

def symmetryCheck(boardList, board): # could use some optimization
    #if there is an equivalent board in the list, returns True and that score
    #else returns False and 0
    
    #boardList should be a list like:
    # [ [[board array],score] , [[board array],score] , ... ]
    
    #algo analysis stuff
    global timeSymmetrizing
    tStart = clock()
    
    #warning: atm this is a crappy algorithm with a shitton of comparisons.
    #           edit: it's a little better but it still could use work.
    #principle: 
    #   each tic-tac-toe game state belongs to a family of 8 isomorphic states.
    #eg.     
    # 012                   210
    # 345 is isomorphic to  543 (board flipped left-to-right)
    # 678                   876  
    # and these two are also isomorphic with 6 other states.
    
    # each of these sets is used to translate a state 
    # to one of the other 7 states in its 'family'.
    # we skip spot 4 here since it is always in the same place.
    isomorphs = \
        [[2,1,0,
          5,  3,
          8,7,6],[0,3,6,1,7,2,5,8],
                 [6,3,0,7,1,8,5,2],
                 [6,7,8,3,5,0,1,2],
                 [8,7,6,5,3,2,1,0],
                 [2,5,8,1,7,0,3,6],
                 [8,5,2,7,1,6,3,0]]
                 
    translationSets = []
    for set in isomorphs:
        set = zip(set,[0,1,2,3,5,6,7,8])
        translationSets.append(set)
    
    middleMatchstates = []
    for (b,s) in boardList:
        if b[4] == board[4]:# check that the center matches
            
            for set in translationSets: # test for each of 7 isomorphisms
                match = True #to begin with
                for (m,n) in set:
                    if b[m] != board[n]:
                        match = False
                        break
                        
                if match == True:
                    timeSymmetrizing += clock() - tStart
                    return (True, s)#got our match.
    
    timeSymmetrizing += clock() - tStart
    return (False, 0)#no match.

""" def symmetryCheckOne(b1,b2):
    isomorphs = \
        [[0,1,2,3,4,5,6,7,8],#isomorph 0. WLOG, we'll say b1 is in this format.
         [2,1,0,5,4,3,8,7,6],#1
         [0,3,6,1,4,7,2,5,8],#2
         [6,3,0,7,4,1,8,5,2],#3
         [6,7,8,3,4,5,0,1,2],#4
         [8,7,6,5,4,3,2,1,0],#5
         [2,5,8,1,4,7,0,3,6],#6
         [8,5,2,7,4,1,6,3,0]]#7

    possibilities = [0,1,1,1,1,1,1,1] #bitstring of isomorph types that b2 could be
    # 4 matches in all isomorphs
    if b1[4] != b2[4]:
        return (False, 0)
    # check corners first (indices 0,2,6,8)
    if b1[0] != b2[7]:
        possibilities[7] = 0
        possibilities[5] = 0
    if b1[2] == b[ """
        

def chooseMove(oldBoard, d, player, boards = [], a = float("-infinity"), b = float("infinity")): 
    # minimax depth-first recursive search 
    #   with symmetry checking & alpha-beta pruning
    
    # these are for data collection on the algo
    global statesEvaluated 
    global statesScored
    global statesSymmetrized
    global statesPruned
    
    if not boards:
        # boards keeps track of all evaluated boards
        # used for symmetry checking
        # boards are indexed by depth for efficiency
        boards = [[] for i in range(d+1)]
    
    # base condition: somebody won or no moves left
    if d<=0 or score(oldBoard, winCheck = 1) or not 0 in oldBoard: 
        statesScored[d] += 1
        return (score(oldBoard, d, terminal = True), -1)
    
    Move = -1 # this contains the best move; initialized as an invalid -1
    
    for i in range(9):# for each possible move on the board
        if not oldBoard[i]: # make sure nobody already moved there
            newBoard = oldBoard[:i] + [player] + oldBoard[i+1:] #apply move
            statesEvaluated[d] += 1
            
            
            skipd = False #symmetry checking may allow us to skip eval of this board
            if d >= 7:
                (sym, equivScore) = symmetryCheck(boards[d],newBoard)
                if sym: #we can skip eval - just use score from matching board
                    s = equivScore
                    skipd = True
                    statesSymmetrized[d] += 1
                    
            if not skipd: # we have to evaluate the move
                s = chooseMove(newBoard, d-1, -player, boards, a, b)[0]
            boards[d].append([newBoard,s]);
            
            
            if player == 1:
                if s>a:
                    a = s;
                    Move = i;
            else:
                if s<b:
                    b = s;
                    Move = i;
            if b <= a:
                statesPruned[d] += 1;
                break # PRUNE'D
    
    if player == 1: return (a,Move);
    else: return (b,Move);

def gameOver():
    r = input("GAME OVER! play again (y/n)? ")
    if r == "y":
        main()

def pName(p):# returns string version of player name
    if p == 1:
        return "x"
    elif p == -1:
        return "o"
    else:
        raise ValueError

def askForMove(board):#prompts human player to input move
    boardPrint(board, 1)
    i = input("Where would you like to move? ")
    if i.isdigit():
        i = int(i)
    else:
        print("Please enter a number on the board.")
        return askForMove(board)#retry
        
    if -1<i and i<9 and not board[i]:
        return i
    else: 
        print("sadface. you gotta gimme a number on the board that's not taken yet.")
        return askForMove(board)#retry

def askForAIPlayer():
    p = input("Which player gets AI (x/o/r for random)? ")
    
    if p == "x": AIplayer = 1 
    elif p == "o": AIplayer = -1
    elif p == "r": 
        random.seed()
        AIplayer = random.choice([-1,1])
    else: 
        print("unhappy face. you gotta answer the question with an x, o or r.")
        return askForAIPlayer()#retry
    
    return AIplayer

def main():
    AIplayer = askForAIPlayer()

    initBoard = [0,0,0,0,0,0,0,0,0]
    
    print("AIplayer is", pName(AIplayer), "\nlet's get started!")
    playMove(initBoard, 9, 1, AIplayer)

main()
