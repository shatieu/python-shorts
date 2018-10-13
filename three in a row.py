from random import randint
#import itertools
"""
put 3 circles in a row next to each other pc with simple strategy
"""

# till fn pc_better () 180 min
def game_three_in_row (game_plan_size = 10, player_starts = True, configuration = {"player_name" : "Ondra" , "empty_postition_char": " ", "used_postition_char" : "O"}):
    won = "nobody"
    whos_turn = ""
    taken = [-1 for i in range (game_plan_size)]
    turn=0
    player_turn = 0
    while won == "nobody":          
        whos_next = who_should_go (player_starts, turn)         #determins who's turn is it
        if whos_next == 1:                                      #player turn
            whos_turn= "player"
            player_turn = ask_player (configuration, taken, game_plan_size)
            if type(player_turn)== int:                         #in case player's input was correct
                taken[player_turn] = player_turn                #changes default value -1 of played index to the value of the index
            else:
                print(player_turn)                              #in case it wasn't ... see fn. ask_player ()
                turn += -1
        elif whos_next == 0:                                    #pc turn
            whos_turn = "pc"
            print ("computer turn")
            pc_turn = pc_better (game_plan_size, taken, player_starts, turn, player_turn)
            taken[pc_turn] = pc_turn
        turn += 1
        taken_for_print = ""
        for x in (taken):                                       #converts list of played to visual form
            if x == -1:
                taken_for_print += "#"+ str(configuration["empty_postition_char"]) +"#"
            else:
                taken_for_print += "#" + str(configuration["used_postition_char"]) +"#"
        top_row = []
        for y in range (game_plan_size):
            top_row.append(str((y+1) // 10))
        bot_row = []
        for y in range (game_plan_size):
            bot_row.append(str((y+1)-((y+1)//10)*10))
        print (" " + "  ".join(top_row) + " ")                  #prints identification numbers
        print (" " + "  ".join(bot_row)+" ")
        print ("#"*game_plan_size *3)                           #prints #######
        print (taken_for_print)                                 # prints visualisation of taken
        print ("#"*game_plan_size *3)
        won = anyone_won (taken, whos_turn)
        if won != "nobody":                                     #if there are 3 in a row
            print ("won by  " + str(whos_turn))
            
def ask_player (configuration, taken, game_plan_size):              #asks player for input and chcecks it
    pl_input = input (str(configuration["player_name"]) + " turn: type number")
    player_wants = 0
    try:
        player_wants = int(pl_input)-1
    except ValueError:                                              #in case there is something else than number
        return("You can not play that")
    if player_wants in taken or player_wants > game_plan_size or player_wants < 0:      #chcecks if it already has been played or if it is outside game plan
        return ("You can not play that")
        ask_player (configuration, taken, game_plan_size)
    else:
        return (player_wants)

def pcc_turn (game_plan_size, taken):                               #random pc turn
    x = -1
    while x in taken:
        x = randint(0, game_plan_size-1)
        if x in taken:
            pass
        else:
            return (x)
        


def anyone_won (taken, whos_turn):                                  #checks if there are 3 Os next to each other, must be at the end of cycle!
    winning_list =[]
    for x in taken:
        if x != -1:
            winning_list.append (x)
        else:
            winning_list [:] = []
        if len(winning_list) == 3:
            return (whos_turn)
    return ("nobody")        
    


def who_should_go (player_starts, turn):                            #determins who's turn it is... It didnt work when I had it inside the main function so I defined it as a function on it's own
    x = 0
    if player_starts == True:
        if turn % 2 == 0:
            x = 1
        else:
            x = 0
    elif player_starts == False:
        if turn % 2 == 0:
            x = 0
        else:
            x = 1
    return (x)


"""
following strategy pc_better wins if it can, doesn't play in such way that it would help the player if possible
on odd game plan size it starts in the middle and then copies symetrically players turn (as long as there isnt a winning move)(in case it starts the game)
this part took me another 180 min
"""
def pc_better (game_plan_size, taken, player_starts, turn, player_turn):
    x = winning_move (game_plan_size, taken, player_starts, turn, player_turn)          #if it can win wins + wins if it starts and game_plan_size is odd see fn. winning_move ()
    if type(x) == int:
        return x
    if game_plan_size % 2 == 1 and player_starts == False:                              # if no win move available and odd game plan size goes with odd game plan strategy
        return (odd_game_plan_size (game_plan_size, taken, player_starts, turn, player_turn))
    y = not_helping_move (game_plan_size, taken, player_starts, turn, player_turn)      #if possible plays in such way that it doesnt help player see fn. not_helping_move ()
    if type(y) == int:
        return y
    x = pcc_turn (game_plan_size, taken)                                                #if neither of the above is possible plays randomly see fn. pcc turn ()
    return x

def winning_move (game_plan_size, taken, player_starts, turn, player_turn):
    for i in range (1,len(taken)-1):
        if taken[i] == -1 and taken[i-1] != -1 and taken[i+1] != -1:                     #checks #O## ##O#
            return i
        elif taken[i-1] != -1 and taken[i] != -1 and taken[i+1] == -1:                   #checks #O##O## #
            return (i+1)
        elif taken[i-1] == -1 and taken[i] != -1 and taken[i+1] != -1:                   #checks # ##O##O# (nesscessary for position 0)
            return (i-1)
    return ("no_win_move")
        

def odd_game_plan_size (game_plan_size, taken, player_starts, turn, player_turn):        #odd game plan size strategy
    if turn == 0:                                                                #only if pc starts otherwise there is no definite winning strategy
        x = game_plan_size//2
        return (x)                    
    else:                                                                        #plays symmetricaly to what player played on his last move
        x = game_plan_size - (player_turn+1)
        return (x)

def not_helping_move (game_plan_size, taken, player_starts, turn, player_turn):
    if turn==0 and player_starts == False:                                              #start
        x = game_plan_size//2
        return (x)                                            
    elif taken[0] == -1 and taken[1] == -1 and taken[2] == -1:                          #if first three are free it is safe to play(and it does thus) first one  
        return (0)
    elif taken[len(taken)-1] == -1 and taken[len(taken)-3] == -1 and taken[len(taken)-2] == -1:     #if last three are free it is safe to play last one
        return (len(taken)-1)
    for y in range (2,len(taken)-2):
        if taken[y-2] == -1 and taken[y-1] == -1 and taken[y] == -1 and taken[y+1] == -1 and taken[y+2] == -1:      #if none of the above is true it is safe to play those fields which have two nearest neighbours to each side free
            return y
    return ("have_to_help")                                                             #if it cant play in such way that it wouldn't help

game_three_in_row()
