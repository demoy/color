from color import ColorGame


def main(console=True):
    color = ColorGame()
    
    color.read(console)
    color.makeboard()
    while(not color.finish(color.board)):
        color.score()
        color.drawboard()
        if color.player == 1: color.read()
        else: color.minimax(color.board, color.player, color.player,8,True)
        color.roots[color.player].tally(color.play(color.board,color.roots[color.player].a,color.roots[color.player].b,color.move))
        color.player= color.turn(color.player)
    #_print final scores and draw final board    
        
            
def config():
    #added to set up variable from gui safely
    pass

if __name__ == "__main__":
    main()
