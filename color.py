import os
import copy
from itertools import repeat

from random import choice

x=0
y=0
player=0
size=1
roots=[]
letters=[]
move=None
board=[]


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
    


class root:
    score=1
    a=None
    b=None
    
    def __init__(this,player,a,b):
        board[a][b].player=player
        board[a][b].letter=player
        this.a=a
        this.b=b

    def tally(this,num):
        this.score+=num
    
class tile:
    player=-1;
    letter=None;
    
    def __init__(this):
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


def unused(board):
    inused = [ board[root.a][root.b].letter for root in roots if board[root.a][root.b].letter in letters]
    return list(set(letters) - set(inused))


def makeboard():
    global board

    board = [[tile() for i in repeat(None,y)] for i in repeat(None,x)]

    startingPoints()

def switchLetters(board, a, b):
    total=0
        
    if b  > 0:                  
        test=board[a][b].compare(board[a][b-1])
        if test == -1:
            total+=board[a][b-1].setPlayer(board[a][b].player)
            total+=switchLetters(board,a,b-1)
        elif test == 1:
            board[a][b-1].setLetter(board[a][b].letter)
            total+=switchLetters(board,a,b-1)

    if  y > b + 1:              
        test=board[a][b].compare(board[a][b+1])
        if test == -1:
            total+=board[a][b+1].setPlayer(board[a][b].player)
            total+=switchLetters(board,a,b+1)
        elif test == 1:
            board[a][b+1].setLetter(board[a][b].letter)
            total+=switchLetters(board,a,b+1)


    if a  > 0:                  
        test=board[a][b].compare(board[a-1][b])
        if test == -1:
            total+=board[a-1][b].setPlayer(board[a][b].player)
            total+=switchLetters(board,a-1,b)
        elif test == 1:
            board[a-1][b].setLetter(board[a][b].letter)
            total+=switchLetters(board,a-1,b)

    if  x > a + 1 :             
        test=board[a][b].compare(board[a+1][b])
        if test == -1:
            total+=board[a+1][b].setPlayer(board[a][b].player)
            total+=switchLetters(board,a+1,b)
        elif test == 1:
            board[a+1][b].setLetter(board[a][b].letter)
            total+=switchLetters(board,a+1,b)

    return total


def startingPoints():
    global roots
    if(size==2):
        roots=[root(1,x/2,0),root(2,x/2,y-1)]
        return
    
    if(size==3):
        roots=[root(1,0,0), root(2,x-1,y-1), root(3,x/2,y/2)]
        return
    
    if(size==4):
        roots=[root(1,x/2,0), root(2,x-1,y/2), root(3,x/2,y-1), root(4,0,y/2)]
        return
    
    if(size==5):
        roots=[root(1,x/2,0), root(2,x-1,y/2), root(3,x/2,y-1), root(4,0,y/2), root(5,x/2,y/2)]
        return

def finish(board):
    for x in board:
        for y in x:
            if y.player==-1:
                return False
    return True
                


def minimax(board,currentplayer,initialplayer,depth,alpha,beta,top=False):
    global move
    if depth==0 or finish(board):
        return 0
    
    if currentplayer==initialplayer:
        for letter in unused(board):
            newboard= copy.deepcopy(board)
            val = play(newboard,roots[currentplayer].a,roots[currentplayer].b,letter) \
            + minimax(newboard,turn(currentplayer),initialplayer,depth-1,alpha,beta)
            alpha=max(alpha,val)
            if beta<=alpha:
                break
            if val==alpha and top:
                move=letter
            
        return alpha
    else:
        for letter in unused(board):
            newboard= copy.deepcopy(board)
            val = play(newboard,roots[currentplayer].a,roots[currentplayer].b,letter) \
            + minimax(newboard,turn(currentplayer),initialplayer,depth-1,alpha,beta)
            beta=min(beta,val)
            if beta<=alpha:
                break
        return beta
        
# clearScreen taken from "http://stackoverflow.com/questions/517970/how-to-clear-python-interpreter-console"
def clearscreen():
    os.system(['clear','cls'][os.name == 'nt'])


def drawboard():
    for x in board:
        _print("\n ")
        for y in x:
            if(y.player!=-1 and type(y.letter) is str):
                _print(y.letter.upper())
            else: _print(y.letter)
    print        
    

def score():
    clearscreen()
    for root in roots:
        _print("PLAYER:")
        _print(board[root.a][root.b].player)
        _print("SCORE:")
        _print(root.score)
        _print("LETTER:")
        _print(board[root.a][root.b].letter)
        print
    print
    drawboard()

def read(setup=False):
    global y
    global x
    global letters
    global size
    global move
    global roots
    
    if not setup:
        _print("\nYou are Player:")
        _print(player+1)
        _print("Using")
        try:
            _print(board[roots[player].a][roots[player].b].letter.upper())
        except AttributeError:
            _print(board[roots[player].a][roots[player].b].letter)
        _print("\nEnter a Letter in set:")
        temp=unused(board)
        _print(temp)
        print
        while(not move in temp):
            move =  getch()
            if move == chr(3) or move == chr(4):
                raise Exception("I Know Python - BYE!") 
    else:
        while True:
            try:
                size += int(raw_input("Enter 1, 2, 3 or 4 for Number of AI opponents\n"))
                if size<2: size=2
                if size>5: size=5
                break
            except ValueError:
                print "Error: Please enter a number\n"
                
        while True:
            try:
                y = int(raw_input("Enter a Number for the heigth of board \n"))
                if y<size:y=size
                break
            except ValueError:
                print "Error: Please enter a number\n"
        while True:
            try:
                x = int(raw_input("Enter a Number for the width of board \n"))
                if x<size:x=size
                break
            except ValueError:
                print "Error: Please enter a number\n"
        
        while True:
            try:
                temp=int(raw_input("Enter a Number for size of alphabet\n"))
                if temp<2+size: temp = 2+size
                if temp>26: temp = 26
                letters = list(map(chr, range(97, 98+temp)))
                break
            except ValueError:
                print "Error: Please enter a number"
        
def turn(player):
    global size
    return (player+1)%size

def play(board,a,b,move):
    board[a][b].setLetter(move)
    return switchLetters(board,roots[player].a,roots[player].b)
    
def main(console=True):
    global player
    
    read(console)
    makeboard()
    while(not finish(board)):
        score()
        
        if player == 1: read()
        else: minimax(board,player, player,8,-x*y , x*y,True)

        roots[player].tally(play(board,roots[player].a,roots[player].b,move))
        player= turn(player)
    score()
        
            
def config():
    #added to set up variable from gui safely
    pass

if __name__ == "__main__":
    main()
