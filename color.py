import os
import copy
from random import choice

x=0
y=0
player=0
size=1
roots=[]
letters=[]
current=0
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
    tile=None
    score=0
    a=None
    b=None
    
    def __init__(this,player,a,b):
        this.tile=board[a][b]
        this.tile.player=player
        this.tile.letter=player
        this.a=a
        this.b=b

    def tally(this,num):
        score+=num
    
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


def unused(roots):       
    def inuse(letter,roots):
        for root in roots:
            if(root.tile.letter==letter):
                return []
        return letter
                      
    unused=[]
    for letter in letters:
        unused+=inuse(letter,roots)
    return unused


def makeboard():
    global board
    board = [[] for i in range(x)]
    for entry in board:
        entry.extend([tile() for i in range(y)])
    for column in board:
        for index in column:
            index=tile()
            
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
        roots+=[root(1,x/2,0),root(2,x/2,y-1)]
        return
    
    if(size==3):
        roots+=[root(1,0,0), root(2,x-1,y-1), root(3,x/2,y/2)]
        return
    
    if(size==4):
        roots+=[root(1,x/2,0), root(2,x-1,y/2), root(3,x/2,y-1), root(4,x,y/2)]
        return
    

def finish(board):
    for x in board:
        for y in x:
            if y.player==-1:
                return False
    return True
                



def minimax(board,player, me ,depth,roots,top=False):
    global move
    if depth==0 or finish(board):
        return 0
    
    usuable=letterSet(board)
    if player%me==me:
        bestValue=-x*y
        for letter in usuable:
            newboard= copy.deepcopy(board)
            val = move(newboard,letter,roots[player/totalplayers]) + minimax(newboard,player+1,me,depth-1,roots)
            if top:
                move=letter
            bestValue=max(bestValue,val)
        return bestValue
    else:
        bestValue=x*y
        for letter in usuable:
            newboard= copy.deepcopy(board)
            val = move(newboard,letter,roots[player/totalplayers]) + minimax(newboard,player+1,me,depth-1,roots)
            bestValue=min(bestValue,val)
        return bestValue
        
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

def score():
    for root in roots:
        _print("Player ")
        _print(root.tile.player)
        _print(" Score is ")
        _print(root.score)
        print


def read(setup=False):
    global y
    global x
    global letters
    global size
    global move
    global roots
    
    if not setup:
        _print("\nEnter a Letter\n")
        while(not move in unused(roots)):
            move =  getch()
            if move == chr(27):
                raise Exception("ESC pressed.- crash exiting") 
    else:
        while True:
            try:
                size += int(raw_input("Enter 1, 2 or 3 for Number for the number of AI opponents\n"))
                if size<2: size=2
                if size>4: size=4
                break
            except ValueError:
                print "Error: Please enter a number\n"
                
        while True:
            try:
                y = int(raw_input("Enter a Number for the heigth of board \n"))
                if y<3:y=3
                break
            except ValueError:
                print "Error: Please enter a number\n"
        while True:
            try:
                x = int(raw_input("Enter a Number for the width of board \n"))
                if x<3:x=3
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
        
def main():
    clearscreen()
    read(True)
    makeboard()
    while(not finish(board)):
        clearscreen()
        score()
        drawboard()
        if player == 0: read()
        else: minimax(board,player, player,8,roots,True)
        
        roots[player].tile.setLetter(move)
        roots[player].score=switchLetters(board,roots[player].a,roots[player].b)
    
    #_print final scores and draw final board    
        
            

if __name__ == "__main__":
    main()