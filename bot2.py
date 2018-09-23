from AlbotOnline.Snake.SnakeGame import SnakeGame
import random
import time

game = SnakeGame() #Connects you to the Client
turn = 0
is_player_one = False

def getOkeyMoves(simBoard):
    playerMoves, enemyMoves = game.getPossibleMoves(simBoard)
    newPlayerMoves = playerMoves[:]
    newEnemyMoves = enemyMoves[:]

    for move in playerMoves:
        simBoard = game.simulateMove(board, move, random.choice(enemyMoves))
        if(game.evaluateBoard(simBoard) == 'enemyWon' or game.evaluateBoard(simBoard) == 'draw'):
            newPlayerMoves.remove(move)

    for move in enemyMoves:
        simBoard = game.simulateMove(board, random.choice(playerMoves), move)

        if(game.evaluateBoard(simBoard) == 'playerWon' or game.evaluateBoard(simBoard) == 'draw' ):
            newEnemyMoves.remove(move)

    # if återvändsgränd
    if not newPlayerMoves:
        #print("-----")
        newPlayerMoves.append('down')


    if not newEnemyMoves:
        #print("-----")
        newEnemyMoves.append('down')

    # print(newEnemyMoves)
    # print(newPlayerMoves)

    return newPlayerMoves, newEnemyMoves


def PlayFullGame(simBoard):
    while(game.evaluateBoard(simBoard) == "ongoing"):
        playerMoves, enemyMoves = getOkeyMoves(simBoard)
        simBoard = game.simulateMove(simBoard, random.choice(playerMoves), random.choice(enemyMoves))
    return game.evaluateBoard(simBoard)

def MakePredictions(board, playerMoves, enemyMoves, thinkTime, stats):
    for j, move in enumerate(playerMoves):
        won = 0
        for _ in (range(thinkTime)):
            result = PlayFullGame(game.simulateMove(board, move, random.choice(enemyMoves)))
            if result == 'playerWon':
                won = won + 1
        stats[j] = stats[j] + won

    return stats

#
while(game.awaitNextGameState() == "ongoing"):
    #print("-----------------------------")
    start_time = time.time()
    turn_time = 0

    turn = turn + 1
    board = game.currentBoard
    thinkTime = 30

    numberOfSims = 0




    #Simulate games <<-
    playerMoves, enemyMoves = getOkeyMoves(board)
    game.makeMove(playerMoves[0])

    stats = []
    for i in playerMoves:
        stats.append(0)

    # start_time = time.time()
    # stats = MakePredictions(board, playerMoves, enemyMoves, thinkTime, stats)
    # best_move = playerMoves[stats.index(max(stats))]
    # game.makeMove(best_move)
    # end_time = time.time()
    #
    # numberOfSims = (thinkTime * 3) ##

    #print(is_player_one)
    p = board.player
    if (p.x == 2 and p.y == 2):
        #print("True")
        is_player_one = True

    if(turn < 5):
        #print(turn)
        if(is_player_one):
            if(turn == 1):
                game.makeMove('down')
            elif(turn == 2):
                game.makeMove('right')
            elif(turn == 3):
                game.makeMove('down')
            elif(turn == 4):
                game.makeMove('right')
        else:
            if(turn == 1):
                game.makeMove('up')
            elif(turn == 2):
                game.makeMove('left')
            elif(turn == 3):
                game.makeMove('up')
            elif(turn == 4):
                game.makeMove('left')

    else:
        turn_time = time.time() - start_time
        while(turn_time < 2.7):
            #print(turn_time)
            #start_time = time.time()
            stats = MakePredictions(board, playerMoves[:], enemyMoves[:], int(1), stats)
            numberOfSims = numberOfSims + (3 * int(thinkTime/3))
            # print("Number of sims = ",numberOfSims)
            #print("Stats ", stats)
            best_move = playerMoves[stats.index(max(stats))]

            game.makeMove(best_move)
            #end_time = time.time()
            #print(end_time-start_time)
            turn_time = time.time() - start_time
