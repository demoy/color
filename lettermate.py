from time import sleep 
from copy import deepcopy
from itertools import repeat
from random import choice
import os

class setting:
    width=0
    height=0
    current=0
    size=1
    roots=()
    letters=[]
    move=None
    board=[0,[]]
    
    def __init__(this,width,height,current,size,roots,letters,move,board):
        this.width=width
        this.height=height
        this.current=current
        this.size=size
        this.roots=roots
        this.letters=letters
        this.move=move
        this.board=board
    
    def getroot(this):
        return this.roots[this.current]
        
    def advance(this):
        myroot=this.getroot()
        score=play(this,this.board,myroot.Xdex,myroot.Ydex,this.move)
        myroot.tally(score)
        this.current= turn(this,this.current)
    
    
    
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

class root:
    label=-1
    score=1
    Xdex=-1
    Ydex=-1
    
    def __init__(this,game,label,Player,Xdex,Ydex):
        this.label=label
        game.board[1][Xdex][Ydex].Player=Player
        game.board[1][Xdex][Ydex].letter=Player
        this.Xdex=Xdex
        this.Ydex=Ydex

    def tally(this,num):
        this.score+=num
    
class tile:
    Player=-1;
    letter=None;
    
    def __init__(this,game):
        this.letter=choice(game.letters)

    def setPlayer(this,Player):
        this.Player=Player
        return 1
    
    def setLetter(this,letter):
        this.letter=letter

    def compare(this,tile):
        if(this.letter == tile.letter and this.Player == tile.Player):
            return 0

        elif this.letter == tile.letter :
            return -1

        elif this.Player == tile.Player :
            return 1

        return 0


def unused(game,board):
    inused = [ board[1][root.Xdex][root.Ydex].letter for root in game.roots]
    return list(set(game.letters) - set(inused))


def makeboard(game):
    game.board = [game.width*game.height-game.size,[[tile(game) for i in repeat(None,game.height)] for i in repeat(None,game.width)]]
    startingPoints(game)

def switchLetters(game,board, Xdex, Ydex):
    total=0
        
    if Ydex > 0:                  
        test=board[1][Xdex][Ydex].compare(board[1][Xdex][Ydex-1])
        if test == -1:
            total+=board[1][Xdex][Ydex-1].setPlayer(board[1][Xdex][Ydex].Player)
            total+=switchLetters(game,board,Xdex,Ydex-1)
        elif test == 1:
            board[1][Xdex][Ydex-1].setLetter(board[1][Xdex][Ydex].letter)
            total+=switchLetters(game,board,Xdex,Ydex-1)

    if  game.height > Ydex + 1:              
        test=board[1][Xdex][Ydex].compare(board[1][Xdex][Ydex+1])
        if test == -1:
            total+=board[1][Xdex][Ydex+1].setPlayer(board[1][Xdex][Ydex].Player)
            total+=switchLetters(game,board,Xdex,Ydex+1)
        elif test == 1:
            board[1][Xdex][Ydex+1].setLetter(board[1][Xdex][Ydex].letter)
            total+=switchLetters(game,board,Xdex,Ydex+1)


    if Xdex > 0:                  
        test=board[1][Xdex][Ydex].compare(board[1][Xdex-1][Ydex])
        if test == -1:
            total+=board[1][Xdex-1][Ydex].setPlayer(board[1][Xdex][Ydex].Player)
            total+=switchLetters(game,board,Xdex-1,Ydex)
        elif test == 1:
            board[1][Xdex-1][Ydex].setLetter(board[1][Xdex][Ydex].letter)
            total+=switchLetters(game,board,Xdex-1,Ydex)

    if  game.width > Xdex + 1 :             
        test=board[1][Xdex][Ydex].compare(board[1][Xdex+1][Ydex])
        if test == -1:
            total+=board[1][Xdex+1][Ydex].setPlayer(board[1][Xdex][Ydex].Player)
            total+=switchLetters(game,board,Xdex+1,Ydex)
        elif test == 1:
            board[1][Xdex+1][Ydex].setLetter(board[1][Xdex][Ydex].letter)
            total+=switchLetters(game,board,Xdex+1,Ydex)
    return total


def startingPoints(game):
    if(game.size==2):
        game.roots=(root(game,1,'1',game.width/2,0),root(game,2,'2',game.width/2,game.height-1))
        return
    
    if(game.size==3):
        game.roots=(root(game,1,'1',0,0), root(game,2,'2',game.width-1,game.height-1), \
        root(game,3,'3',game.width/2,game.height/2))
        return
    
    if(game.size==4):
        game.roots=(root(game,1,'1',game.width/2,0), root(game,2,'2',game.width-1,game.height/2), \
        root(game,3,'3',game.width/2,game.height-1), root(game,4,'4',0,game.height/2))
        return
    
    if(game.size==5):
        game.roots=(root(game,1,'1',game.width/2,0), root(game,2,'2',game.width-1,game.height/2), \
        root(game,3,'3',game.width/2,game.height-1), root(game,4,'4',0,game.height/2), \
        root(game,5,'5',game.width/2,game.height/2))
        return
# initAI role to return the best possible move
def initAI(game):
    unset=unused(game,game.board) # return all the current player can move  make
    alpha=-game.board[0] # the initial alpha value is the negative total points remaining on board
    root=game.getroot() 
    for letter in unset:
        testboard= deepcopy(game.board) # creating a copy of board allows to expand the possibility without the the need to revert changes
        val = play(game,testboard,root.Xdex,root.Ydex, letter)
        #if (val==0): #we avoid optimizing the initial search to cover niche situation where ai was no good move so it \
        #    continue # hinders its opponent
        val +=minimax(game,testboard,turn(game,game.current),game.current,0,8,alpha,game.board[0])# the initial heuristic is 0 since we know nothing about the board
        #the initial depth is  but could be increased greatly since we currently add a 1 second delay since the ai moves in millisecond
        if (alpha<=val):
            alpha = val 
            game.move = letter # set the move with the hightest value
    return

def minimax(game, board, Cplayer,Iplayer,depth,heuristic,alpha,beta):
    if depth == 0 or board[0] == 0:
        return heuristic # the heuristic is the player score so far minus their opponents scores so far  

    if Cplayer == Iplayer: # Cplayer is the current player, Iplayer is the initial player  
        testboard= deepcopy(board)
        for letter in unused(game,board):
            tally = play(testboard,game.roots[Cplayer].Xdex,game.roots[Cplayer].Ydex,letter)
            if (tally==0):
                continue # if a move has no effect don't consider taking it and \
                #don't replace the testboard since no changes were made

            alpha=max(alpha,minimax(game,testboard,turn(game,Cplayer),Iplayer,depth-1,heuristic+tally,alpha,beta))
            if beta <= alpha:
                break
            testboard= deepcopy(board)

        return alpha
    else:
        bestValue = board[0]
        testboard= deepcopy(board)
        for letter in unused(game,board):
            tally = play(testboard,game.roots[Cplayer].Xdex,game.roots[Cplayer].Ydex,letter)
            if (val==0):
                continue
            beta = min(beta,minimax(game,testboard,turn(game,Cplayer),Iplayer,depth-1,heuristic-tally,alpha,beta))
            testboard= deepcopy(board)

        return beta


def drawboard(game,prompt=False):
    temp=chr(27) + "[2J"
    for root in game.roots:
        temp+=" Player: " + str(root.label) +" SCORE: " +\
        str(root.score) +" LETTER: " +\
        game.board[1][root.Xdex][root.Ydex].letter +"\n"
    temp+="\n"    
    for column in game.board[1]:
        temp+="\t"
        for tile in column:
            temp+=" "
            if(tile.Player!=-1):
                temp+=tile.letter.upper()
            else: temp+=tile.letter
        temp+="\n"
    if(prompt):
        root=game.getroot()
        temp+=" You are Player: " + str(root.label) +" Using " \
        +game.board[1][root.Xdex][root.Ydex].letter.upper() \
        +"\n Enter a Letter in set: "
        lst=unused(game,game.board)
        temp+=str(lst)
        print(temp)
        while(not game.move in temp):
            game.move =  getch()
            if game.move == chr(3) or game.move == chr(4):
                raise Exception("I Know Python - crashing!") 
    else:
        print(temp)
    
def read(game):
    root=game.getroot()
    string=" You are Player: " + str(root.label) +" Using " \
    +game.board[1][root.Xdex][root.Ydex].letter.upper() \
    +"\n Enter a Letter in set: "
    temp=unused(game,game.board)
    string+=str(temp)
    print(string)
    
    while(not game.move in temp):
        game.move =  getch()
        if game.move == chr(3) or game.move == chr(4):
            raise Exception("I Know Python - crashing!") 
    
        
def turn(game,player):
    return (player+1)%game.size

def play(game,board,Xdex,Ydex,move):
    board[1][Xdex][Ydex].setLetter(move)
    temp=switchLetters(game,board,Xdex,Ydex)
    board[0]-=temp
    return temp
    
def main():
    game=config()
    makeboard(game)
    while(game.board[0]):
        drawboard(game)
        
        if game.current == 0: read(game)
        else: 
            initAI(game)
            sleep(1)
        game.advance()
    drawboard(game)
        
            
def config(arg=[]):
        height=0
        width=0
        letters=[]
        size=1
        move=None
        roots=()

        
        if len(arg)==8:
            return setting(arg[0],arg[1],arg[2],arg[3],arg[4],arg[5],arg[6],arg[7])
            
        while True:
            try:
                size += int(raw_input(" Enter 1, 2, 3 or 4 for Number of AI opponents\n  "))
                if size<2: size=2
                if size>5: size=5
                break
            except ValueError:
                print " Error: Please enter a number\n"
                
        while True:
            try:
                height = int(raw_input(" Enter dimension of board \n  "))
                if height<size:height=size
                width=height
                break
            except ValueError:
                print " Error: Please enter a number\n"
        while True:
            try:
                temp=int(raw_input(" Enter a Number for size of alphabet\n  "))
                if temp<2+size: temp = 2+size
                if temp>10: temp = 10
                letters = list(map(chr, range(97, 98+temp)))
                break
            except ValueError:
                print " Error: Please enter a number"
        return setting(width,height,0,size,(),letters,move,[0,[]])

if __name__ == "__main__":
    main()
