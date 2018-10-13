from random import randint
"""
Python versin 3.4.2
Ondrej Urbanovsky Engeto task for python kurz submission
General comments:
Simulates cows and bulls game.
Evaluation of the palyer requires to create statistics.txt file, where all finished attempts are stored
Whole programe is executable via calling main() function, but does not execute itself, see end
One can determine how many digits does the secret number contain via changing parameter guessing pins of main(guessing_pins)
guessing pins is game size (how many digits does player have to guess)
"""

def main(guessing_pins = 4):
    secret = []                                     #list of digits which player is trying to guess
    _list = [0,1,2,3,4,5,6,7,8,9]
    turn = 1
    for i in range (guessing_pins):                 #generates n digit (no digits are equal)secret number that player is trying to guess
        ran_num = randint (0,len(_list)-1)          #where n is guessing_pins parameter, default 4
        picked = _list[ran_num]
        secret.append(picked)
        _list.remove(picked)
    print ("Hi there!")
    print ("I've generated a random {} digit number for you.".format(guessing_pins))
    print ("Let's play bulls and cows game.")
    
    logic (guessing_pins, secret, _list, turn)
    
    
def logic (guessing_pins, secret, _list, turn):                         #asks for input and checks how many digits of the guess are cows/bulls calls input checking function
    bulls = 0
    cows = 0
    input_num = input ("Enter a number with length {} with each digit different:  ".format(guessing_pins))
    is_input_correct = check_input (guessing_pins, input_num, secret, _list, turn)
    if is_input_correct == True:                                        #how many cows/bulls is computed only if input is correct
        inputed_list = change_input(input_num)
        for x in range (len(inputed_list)):
            if inputed_list[x] in secret and inputed_list[x] != secret[x]:
                cows += 1
            elif inputed_list[x] == secret [x]:
                bulls += 1
    print ("{} bulls, {} cows".format(bulls,cows))
    is_over(guessing_pins, bulls, secret, _list, turn )                 #determines whether the player won or not
            
    
def is_over (guessing_pins, bulls, secret, _list, turn):                #determines whether the game is over or not, 
    if bulls == guessing_pins:
        make_statistics(guessing_pins, turn)
        player_score = evaluate_player(guessing_pins, turn)
        print("Correct, you've guessed the right number in {} guesses!".format(turn))
        print (player_score)
        ask_restart(guessing_pins, turn)
    else:                                                               # if not calls for logic() for another guess
        turn += 1
        logic (guessing_pins, secret, _list, turn)
        
def evaluate_player(guessing_pins, turn):                               #when game is won reads statistics.txt and determines how good player is
    pins_count = {}
    pins_total = {}
    with open("statistics.txt", "r") as data:
        for line in data:                                               #stores data in dictionaries (expected input (guessing_pins, turns when the game was won))
            line = line.rstrip()
            line = line.split(',')
            if line[0] in pins_count:
                pins_count[line[0]] += 1
            else:
                pins_count[line[0]] = 1
            if line[0] in pins_total:
                pins_total[line[0]] += int(line[1])
            else:
                pins_total[line[0]] = int(line[1])
    if str(guessing_pins) in pins_total:
        average = pins_total[str(guessing_pins)]/pins_count[str(guessing_pins)]     #counts average for that many digits and tells how player stands
        if turn > average:
            return ("That's bellow average")
        else:
            return ("That's above average")
    else:
        return ("You are the first one to play so you are the best as well as the worst!")
        
  
    
def make_statistics (guessing_pins, turn):                                  #if there isnt => creates statistics.txt  
    statistics = open("statistics.txt", "a")                                #in which is stored "guessing_pins,turn\n" after game is won e.g. "4,8\n"
    statistics.write("{},{}\n".format(guessing_pins, turn))
    statistics.close
    

def ask_restart(guessing_pins, turn):                                       #after game is completed asks whether the player want to repeat the game
    again = input ("Do you want to go again? Input Y / N")                  #expected input e.g.: Y
    if again == "Y":
        main()
    elif again == "N":                                                      #if not quits program
        print("Bye!")
        quit()
    else:                                                                   #in case of incorrect input => asks again
        print("I don't know what you want to do")
        ask_restart(guessing_pins, turn)

def check_input (guessing_pins, input_num, secret, _list, turn):            #checks inputted number
    if input_num.isnumeric():                                               #Is number?
        if len(list(input_num)) == guessing_pins:                           #rigt size?
            input_list = list(input_num)                                    
            if len(set(input_list)) == len(input_list):                     #no digits repeat?
                return (True)
            else:
                print ("Sorry digits must be different!")
                logic (guessing_pins, secret, _list, turn)
        elif len(list(input_num)) != guessing_pins:
            print ("Try again, incorrect size of your guess.")
            logic (guessing_pins, secret, _list, turn)
    else:
        print ("not an integer try again")
        logic (guessing_pins, secret, _list, turn)

def change_input(input_num):                                                #makes of string digit representation list of digits
    input_list = list(input_num)
    for i in range (len(input_list)):
        input_list[i] = int(input_list[i])
    return (input_list)

#To make this program auto-execute upon F5 uncomment following comment
    
#main()
    
