from AlbotOnline.Snake.SnakeGame import SnakeGame
import random

game = SnakeGame() #Connects you to the Client
while(game.awaitNextGameState() == "ongoing"):
    board = game.currentBoard
    board.printBoard("Current Board")

    playerMoves, enemyMoves = game.getPossibleMoves(board)
    game.makeMove(random.choice(playerMoves))
