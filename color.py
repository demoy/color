import os
import copy
from itertools import repeat

from random import choice

# _Getch class taken from "http://code.activestate.com/recipes/134892/"
class Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = Getch().__call__

def _print(item):
    print(item),
    #sys.stdout.flush()
    #sys.stdout.write(item)



class Root:
    score=1
    a=None
    b=None

    def __init__(this, board, player,a,b):
        board[a][b].player=player
        board[a][b].letter=player
        this.a=a
        this.b=b

    def tally(this,num):
        this.score+=num

class tile:
    player=-1;
    letter=None;

    def __init__(this, letters):
        this.letter=choice(letters)

    def setPlayer(this,player):
        this.player=player
        return 1

    def setLetter(this,letter):
        this.letter=letter

    def compare(this,tile):
        if(this.letter == tile.letter and this.player == tile.player):
            return 0

        elif this.letter == tile.letter :
            return -1

        elif this.player == tile.player :
            return 1

        return 0

class ColorGame():
    x=0
    y=0
    player=0
    size=1
    roots=[]
    letters=[]
    move=None
    board=[]


    def unused(this, board):
        inused = [board[root.a][root.b].letter for root in this.roots if board[root.a][root.b].letter in this.letters]
        return list(set(this.letters) - set(inused))


    def makeboard(this):
        this.board = [[tile(this.letters) for i in repeat(None,this.y)] for i in repeat(None,this.x)]
        this.startingPoints()

    def switchLetters(this, board, a, b):
        total=0

        if b  > 0:
            test=board[a][b].compare(board[a][b-1])
            if test == -1:
                total+=board[a][b-1].setPlayer(board[a][b].player)
                total+=this.switchLetters(board,a,b-1)
            elif test == 1:
                board[a][b-1].setLetter(board[a][b].letter)
                total+=this.switchLetters(board,a,b-1)

        if  this.y > b + 1:
            test=board[a][b].compare(board[a][b+1])
            if test == -1:
                total+=board[a][b+1].setPlayer(board[a][b].player)
                total+=this.switchLetters(board,a,b+1)
            elif test == 1:
                board[a][b+1].setLetter(board[a][b].letter)
                total+=this.switchLetters(board,a,b+1)


        if a  > 0:
            test=board[a][b].compare(board[a-1][b])
            if test == -1:
                total+=board[a-1][b].setPlayer(board[a][b].player)
                total+=this.switchLetters(board,a-1,b)
            elif test == 1:
                board[a-1][b].setLetter(board[a][b].letter)
                total+=this.switchLetters(board,a-1,b)

        if  this.x > a + 1 :
            test=board[a][b].compare(board[a+1][b])
            if test == -1:
                total+=board[a+1][b].setPlayer(board[a][b].player)
                total+=this.switchLetters(board,a+1,b)
            elif test == 1:
                board[a+1][b].setLetter(board[a][b].letter)
                total+=this.switchLetters(board,a+1,b)

        return total


    def startingPoints(this):
        if(this.size==2):
            this.roots=[Root(this.board, 1,this.x/2,0),Root(this.board, 2,this.x/2,this.y-1)]
            return

        if(this.size==3):
            this.roots=[Root(this.board, 1,0,0), Root(this.board, 2,this.x-1,this.y-1), Root(this.board, 3,this.x/2,this.y/2)]
            return

        if(this.size==4):
            this.roots=[Root(this.board, 1,this.x/2,0), Root(this.board, 2,this.x-1,this.y/2), Root(this.board, 3,this.x/2,this.y-1), Root(this.board, 4,0,this.y/2)]
            return

        if(this.size==5):
            this.roots=[Root(this.board, 1,this.x/2,0), Root(this.board, 2,this.x-1,this.y/2), Root(this.board, 3,this.x/2,this.y-1), Root(this.board, 4,0,this.y/2), Root(this.board, 5,this.x/2,this.y/2)]
            return

    def finish(this, board):
        for x in board:
            for y in x:
                if y.player==-1:
                    return False
        return True




    def minimax(this, board,currentplayer,initialplayer,depth,top=False):
        if depth==0 or this.finish(board):
            return 0

        if currentplayer==initialplayer:
            bestValue=-this.x*this.y
            for letter in this.unused(board):
                newboard= copy.deepcopy(board)
                val = this.play(newboard,this.roots[currentplayer].a,this.roots[currentplayer].b,letter) + this.minimax(newboard,this.turn(currentplayer),initialplayer,depth-1)

                bestValue=max(bestValue,val)
                if val==bestValue and top:
                    this.move=letter

            return bestValue
        else:
            bestValue=this.x*this.y
            for letter in this.unused(board):
                newboard= copy.deepcopy(board)
                val = this.play(newboard,this.roots[currentplayer].a,this.roots[currentplayer].b,letter) + this.minimax(newboard,this.turn(currentplayer),initialplayer,depth-1)
                bestValue=min(bestValue,val)
            return bestValue

    # clearScreen taken from "http://stackoverflow.com/questions/517970/how-to-clear-python-interpreter-console"
    def clearscreen(this):
        os.system(['clear','cls'][os.name == 'nt'])


    def drawboard(this):
        for x in this.board:
            _print("\n ")
            for y in x:
                if(y.player!=-1 and type(y.letter) is str):
                    _print(y.letter.upper())
                else: _print(y.letter)
        print


    def score(this):
        this.clearscreen()
        for root in this.roots:
            _print("PLAYER:")
            _print(this.board[root.a][root.b].player)
            _print("SCORE:")
            _print(root.score)
            _print("LETTER:")
            _print(this.board[root.a][root.b].letter)
            print
        print
        this.drawboard()

    def read(this, setup=False):

        if not setup:
            _print("\nYou are Player:")
            _print(this.player+1)
            _print("Using")
            try:
                _print(this.board[this.roots[this.player].a][this.roots[this.player].b].letter.upper())
            except AttributeError:
                _print(this.board[this.roots[this.player].a][this.roots[this.player].b].letter)
            _print("\nEnter a Letter in set:")
            _print(this.unused(this.board))
            print
            while(not this.move in this.unused(this.board)):
                this.move =  getch()
                if this.move == chr(3) or this.move == chr(4):
                    raise Exception("I Know Python - BYE!")
        else:
            while True:
                try:
                    this.size += int(raw_input("Enter 1, 2, 3 or 4 for Number of AI opponents\n"))
                    if this.size<2: this.size=2
                    if this.size>5: this.size=5
                    break
                except ValueError:
                    print "Error: Please enter a number\n"

            while True:
                try:
                    this.y = int(raw_input("Enter a Number for the heigth of board \n"))
                    if this.y<this.size:this.y=this.size
                    break
                except ValueError:
                    print "Error: Please enter a number\n"
            while True:
                try:
                    this.x = int(raw_input("Enter a Number for the width of board \n"))
                    if this.x<this.size:x=this.size
                    break
                except ValueError:
                    print "Error: Please enter a number\n"

            while True:
                try:
                    temp=int(raw_input("Enter a Number for size of alphabet\n"))
                    if temp<2+this.size: temp = 2+this.size
                    if temp>26: temp = 26
                    this.letters = list(map(chr, range(97, 98+temp)))
                    break
                except ValueError:
                    print "Error: Please enter a number"

    def turn(this, player):
        return (player+1)%this.size

    def play(this, board,a,b,move):
        board[a][b].setLetter(move)
        return this.switchLetters(board,this.roots[this.player].a,this.roots[this.player].b)

