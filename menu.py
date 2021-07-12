import pygame
import blackjack, poker, cribbage
import players,login

from time import sleep
from random import randint

class Window:
    def __init__(self,x,y,name,bal):
        self.width = x
        self.height = y
        #Creates the player and dealer object
        self.player = players.player(name)
        self.player.bal = int(bal)
        self.dealer = players.player('Dealer')

        #creates pygame instance
        pygame.init()

        #fonts
        pygame.font.init()

        self.screen = pygame.display.set_mode((x,y))
        self.screen.fill((255,255,255))

        #calls the menu so it can be rendered
        self.active_screen = Menu(self.screen,self.player)
        #updates button locations (this is uniform everytime.)
        self.game_buttons = self.active_screen.button_locations

        pygame.display.update() #need this to render the changes to the screen

    def input(self,action):
        #action is a tuple of mouse position (x,y)
        x = action[0]
        y = action[1]

        #will check if a button is pressed from the active screen.
        for value in self.game_buttons:
            box = self.game_buttons[value]
            if x in range(box[0]-box[2],box[0]+box[2]) and y in range(box[1]-box[3],box[1]+box[3]):
                #change game
                if value in ['blackjack','Blackjack_rules','Cribbage',
                'Cribbage_rules','Poker','Poker_rules']:
                    self.change_game(value)
                #bet stage in blackjack
                if 'bet' in value:
                    self.player.bet+=int(value.split()[1])
                    pygame.draw.circle(self.screen,(205, 217, 41),(300,540),25)
                    pygame.draw.circle(self.screen,(42, 161, 60),(300,540),22)
                    self.render_text(self.player.bet, 300, 540)
                #pick a card in cribbage
                if 'c' in value and len(value)==2:
                    self.active_screen.keep(box)
                    self.game_buttons = self.active_screen.button_locations
                #redraw cards in cribbage.
                def cribbage_redraw():
                    pygame.draw.rect(self.screen,(42, 161, 60),(0,50,600,120))
                    pygame.draw.rect(self.screen,(42, 161, 60),(0,340,600,150))
                    #use of enumerate throughout is so I don't have to create an itterator.
                    for j,i in enumerate(self.player.hand):
                        j+=1
                        self.render(i[0], j*75,350)
                    for j,i in enumerate(self.dealer.hand):
                        j+=1
                        self.render(self.deck.deck['BACK'], j*75, 50)
                    pygame.display.update()
                #adds card to the pile and follow the cribbage logic.
                if 'a' in value and len(value)==2:
                    self.active_screen.add_card(self.player,box)
                    self.render(self.active_screen.pile[-1][0], 420, 210)
                    value = 0
                    #deals with face cards having the wrong value.
                    for i in range(len(self.active_screen.pile)):
                        if self.active_screen.pile[i][2]>10:
                            value +=10
                        else:
                            value += self.active_screen.pile[i][2]

                    #end of pile conditions
                    if value ==31:
                        self.active_screen.player_1_peg_index+=2
                        self.active_screen.draw_board()
                    elif value>31:
                        self.active_screen.player_2_peg_index+=1
                        self.active_screen.draw_board()
                        
                        self.active_screen.pile = [self.active_screen.pile[-1]]
                        value = self.active_screen.pile[0][2]
                        if value>10: 
                            value =10

                    #displays the total to the user because they like to see what they are doing.
                    pygame.draw.rect(self.screen,(42, 161, 60),(410,300,100,30))
                    text_obj = self.active_screen.font.render("Total: "+str(value),False,(0,0,0))
                    self.screen.blit(text_obj,(410+text_obj.get_width()//2,300+text_obj.get_height()//2))


                    
                    cribbage_redraw()

                    #computer turn display
                    pygame.draw.rect(self.screen,(42, 161, 60),(100,250,200,30))
                    font = pygame.font.SysFont('Comic Sans MS',18)
                    text_obj = font.render("Computer's Turn",False,(0,0,0))
                    self.screen.blit(text_obj,(300-text_obj.get_width(),250))
                    pygame.display.update()

                    del self.game_buttons["a"+str(len(self.game_buttons)-1)]

                    sleep(randint(200,400)/100)

                    self.active_screen.add_card(self.dealer,[75])
                    self.render(self.active_screen.pile[-1][0], 420, 210) 

                    #same logic as above and should be a function
                    value = 0
                    for i in range(len(self.active_screen.pile)):
                        if self.active_screen.pile[i][2]>10:
                            value +=10
                        else:
                            value += self.active_screen.pile[i][2]
                    if value ==31:

                        self.active_screen.player_2_peg_index+=2
                        self.active_screen.draw_board()
                        
                    elif value>31:

                        self.active_screen.player_1_peg_index+=1
                        self.active_screen.draw_board()

                        self.active_screen.pile = [self.active_screen.pile[-1]]
                        value = self.active_screen.pile[0][2]
                        if value>10: value =10
                    pygame.draw.rect(self.screen,(42, 161, 60),(410,300,100,30))
                    text_obj = self.active_screen.font.render("total: "+str(value),False,(0,0,0))
                    self.screen.blit(text_obj,(410+text_obj.get_width()//2,300+text_obj.get_height()//2))

                    cribbage_redraw()

                    #win condition for the game
                    if len(self.player.hand)==0:
                        self.active_screen.count_crib()
                        if self.active_screen.player_1_peg_index>=121 or self.active_screen.player_2_peg_index>=121:
                            pygame.draw.rect(self.screen,(42,161,60),(0,50,600,400))
                            if self.active_screen.player_1_peg_index>=121:
                                text = "The Player Wins!"
                            else:
                                text = "The Computer Wins."
                            text_obj = self.active_screen.font.render(text,False,(0,0,0))
                            self.screen.blit(text_obj,(300-text_obj.get_width()//2,300))
                            pygame.display.update()
                            sleep(3)
                            #resets the screen back to the start
                            self.active_screen = Menu(self.screen,self.player)
                            self.game_buttons = self.active_screen.button_locations
                        else:
                            #resets the screen to the start of cribbage
                            self.Cribbage_start()
                    else:
                        #player turn display
                        pygame.draw.rect(self.screen,(42, 161, 60),(100,250,200,30))
                        font = pygame.font.SysFont('Comic Sans MS',18)
                        text_obj = font.render("Player's Turn",False,(0,0,0))
                        self.screen.blit(text_obj,(300-text_obj.get_width(),250))
                        pygame.display.update()
                #redrawing cards for poker.
                if 'p_r'==value:
                    self.active_screen.redraw_cards(self.player,self.deck)
                    for j,i in enumerate(self.player.hand):
                        j+=1
                        self.render(i[0], 50+j*75,400)
                    score = poker.scoring(self.player.hand)
                    #the output will be words that were displayed to the screen so they need to be converted to numbers.
                    #computers like numbers
                    bet_conversion = {"Royal flush":40, "Straight Flush":20,
                    "Four of a kind":21, "Full house":15, "Flush":20, "Straight":10, 
                    "Three of a kind": 3, "Two pairs":6, "A pair":1.5, "":0}
                    self.active_screen.player.bet*=bet_conversion[score]

                    self.active_screen.end(score)
                    self.game_buttons = {'quit':(540,670,60,60)}
                    return
                #the play button in blackjack
                if 'Play'==value:
                    #player init
                    self.player.add_card(self.deck)
                    self.player.add_card(self.deck)
                    for j,i in enumerate(self.player.hand):
                        j+=1
                        self.render(i[0], 240+j*15,370+j*15)
                    self.active_screen = blackjack.main(self.screen)
                    #gets the score of the hand.
                    score = self.player.score_blackjack()

                    pygame.draw.rect(self.screen,(42, 161, 60),(250,570,140,30))
                    self.render_text(("Score: "+str(score)),300,580)
                    self.game_buttons = self.active_screen.button_locations

                    #dealer init
                    self.dealer.add_card(self.deck)
                    for j,i in enumerate(self.dealer.hand):
                        j+=1
                        self.render(i[0], 240+j*15,70+j*15)

                    pygame.display.update()

                if 'discard'==value:
                    #deals with cards that are added to the crib in cribbage.
                    self.active_screen.add_to_crib(self.player)
                    self.active_screen.add_to_crib(self.dealer,True)
                    pygame.draw.rect(self.screen,(42, 161, 60),(0,320,600,150))
                    cribbage_redraw()
                    #crib
                    self.render(self.deck.deck['BACK'], 500, 210)
                    pygame.draw.rect(self.screen, (0,0,0), (500,180,62,20))
                    text_obj = self.active_screen.font.render(str("Crib"),False,(255,255,255))
                    self.screen.blit(text_obj,(531-text_obj.get_width()//2,190-text_obj.get_height()//2))
                    pygame.display.update()

                    #pile
                    self.active_screen.pile = []
                    self.active_screen.pile.append(self.deck.deck[randint(0, len(self.deck.deck)-2)])
                    self.render(self.active_screen.pile[-1][0], 420, 210)

                    pygame.draw.rect(self.screen, (0,0,0), (420,180,62,20))
                    text_obj = self.active_screen.font.render(str("Pile"),False,(255,255,255))
                    self.screen.blit(text_obj,(451-text_obj.get_width()//2,190-text_obj.get_height()//2))
                    
                    #user display
                    font = pygame.font.SysFont('Comic Sans MS',18)
                    text_obj = font.render("Counting the player's hand.",False,(0,0,0))
                    self.screen.blit(text_obj,(300-text_obj.get_width(),250))

                    pygame.display.update()
                    self.active_screen.player_1_peg_index+=self.active_screen.score(self.player.hand)

                    pygame.draw.rect(self.screen,(42,161,60),(0,250,400,30))
                    text_obj = font.render("Counting the computer's hand.",False,(0,0,0))
                    self.screen.blit(text_obj,(300-text_obj.get_width(),250))
                    pygame.display.update()

                    self.active_screen.player_2_peg_index+=self.active_screen.score(self.dealer.hand)
                    pygame.draw.rect(self.screen,(42,161,60),(0,250,400,30))

                    self.active_screen.draw_board()
                    #update the game buttons becaues there are now 4 cards
                    self.game_buttons = {
                        'a1':(75,350,62,90),
                        'a2':(150,350,62,90),
                        'a3':(225,350,62,90),
                        'a4':(300,350,62,90),
                        'quit':(540,670,60,60)
                    }
                    #player turn display
                    pygame.draw.rect(self.screen,(42, 161, 60),(100,250,200,30))
                    font = pygame.font.SysFont('Comic Sans MS',18)
                    text_obj = font.render("Player's Turn",False,(0,0,0))
                    self.screen.blit(text_obj,(300-text_obj.get_width(),250))
                    pygame.display.update()
                #The section for quitting a game.
                if 'quit'==value:
                    #Calls the main screen and quits the game
                    self.active_screen = Menu(self.screen,self.player)
                    self.game_buttons = self.active_screen.button_locations
                
                #dealer logic for blackjack
                def dealer_hit():
                    score = self.dealer.score_blackjack()
                    pygame.draw.rect(self.screen,(42, 161, 60),(250,40,140,30))
                    self.render_text(("Score: "+str(score)),300,50)
                    if len(self.dealer.hand) ==5 or score>16:
                        return False
                    else:
                        self.dealer.add_card(self.deck)
                        self.render(self.dealer.hand[len(self.dealer.hand)-1][0], 
                        240+len(self.dealer.hand)*15,70+len(self.dealer.hand)*15)
                        return True
                #adds a card to the players hand
                if 'hit'==value:
                    self.player.add_card(self.deck)
                    self.render(self.player.hand[len(self.player.hand)-1][0], 
                    240+len(self.player.hand)*15,370+len(self.player.hand)*15)

                    score = self.player.score_blackjack()
                    pygame.draw.rect(self.screen,(42, 161, 60),(250,570,140,30))
                    self.render_text(("Score: "+str(score)),300,580)
                    #checks for end conditions
                    if len(self.player.hand) ==5 or score>21:
                        while dealer_hit():
                            dealer_hit()
                        self.active_screen.scoring(self.player,self.dealer.score_blackjack())
                        self.game_buttons = self.active_screen.button_locations

                if 'pass'==value:
                    while dealer_hit():
                        dealer_hit()
                    self.active_screen.scoring(self.player,self.dealer.score_blackjack())
                    self.game_buttons = self.active_screen.button_locations

                #hit and pass combined and the bet is also doubbled.
                if 'double_down'==value:
                    self.player.add_card(self.deck)
                    self.render(self.player.hand[len(self.player.hand)-1][0], 
                    240+len(self.player.hand)*15,370+len(self.player.hand)*15)
                    while dealer_hit():
                        dealer_hit()
                    self.active_screen.scoring(self.player,self.dealer.score_blackjack())
                    self.game_buttons = self.active_screen.button_locations
                return
    #handles rendering text on the screen because pygame wont do it in one line.
    def render_text(self,string,x,y):
        text_obj = self.active_screen.chip_font.render(str(string),False,(0,0,0))
        self.screen.blit(text_obj,(x-text_obj.get_width()//2,y-text_obj.get_height()//2))
        pygame.display.update()
        return
    #renders an object on the screen and is useless
    def render(self,object,x,y):
        self.screen.blit(object, (x,y))
        pygame.display.update()

    #this is used for two different reasons
    #to start cribbage and to wipe the screen for a new hand.
    def Cribbage_start(self):
        #need a try loop because the attributes aren't there on the first time.
        try:
            p1 = self.active_screen.player_1_peg_index
            p2 = self.active_screen.player_2_peg_index
        except:
            pass

        self.active_screen = cribbage.Window(self.screen)
        try:
            self.active_screen.player_2_peg_index = p2
            self.active_screen.player_1_peg_index = p1

            self.active_screen.draw_board()
        except:
            pass
        
        #gets cards for the users and renders them to the screen.
        for i in range(6):
            self.dealer.add_card(self.deck)
            self.player.add_card(self.deck)
        for j,i in enumerate(self.player.hand):
            j+=1
            self.render(self.deck.deck['BACK'], j*75, 50)
            self.render(i[0], j*75,350)
        #updates button locations
        self.game_buttons = self.active_screen.button_locations
    #change games by wiping the player data and updating the active screen and button locations
    def change_game(self,game):
        if game == 'blackjack':
            self.player.wipe()
            self.dealer.wipe()
            self.active_screen = blackjack.start(self.screen,self.player)
            self.deck = players.Deck("deck.png")
        elif game =="Blackjack_rules":
            self.active_screen = blackjack.rules(self.screen)
        elif game =='Poker':
            self.player.wipe()
            self.active_screen = poker.start(self.screen,self.player)
            self.deck = players.Deck("deck.png")
            for i in range(5):
                self.player.add_card(self.deck)
            for j,i in enumerate(self.player.hand):
                j+=1
                self.render(i[0], 50+j*75,400)
        elif game =="Cribbage":
            self.player.wipe()
            self.dealer.wipe()
            self.deck = players.Deck("deck.png")
            self.Cribbage_start()
        elif game =='Cribbage_rules':
            self.active_screen = cribbage.rules(self.screen)
        elif game =="Poker_rules":
            self.active_screen = poker.rules(self.screen)
        self.game_buttons = self.active_screen.button_locations

#The main screen.
class Menu:
    def __init__(self,screen,player):
        self.player = player
        #the button format is uniform throughout the whole suite.
        self.button_locations = {
            "blackjack":(250,90,100,50),
            "Blackjack_rules":(250,150,100,30),
            "Cribbage":(250,240,100,50),
            "Cribbage_rules":(250,300,100,30),
            "Poker":(250,390,100,50),
            "Poker_rules":(250,450,100,30)
        }
        #draws the GUI to the screen
        self.screen = screen
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS',12)

        self.screen.fill((255,255,255))
        self.button(250,90,100,50,(0,255,255),"Blackjack")
        self.button(250,150,100,30,(0,255,255),"Rules")

        self.button(250,240,100,50,(0,255,255),"Cribbage")
        self.button(250,300,100,30,(0,255,255),"Rules")

        self.button(250,390,100,50,(0,255,255),"Poker")
        self.button(250,450,100,30,(0,255,255),"Rules")

        #User pannel
        text_obj = self.font.render("Welcome: "+self.player.name,False,(0,0,0))
        self.screen.blit(text_obj,(570-text_obj.get_width(),30))
        text_obj = self.font.render("Balance: "+str(self.player.bal),False,(0,0,0))
        self.screen.blit(text_obj,(570-text_obj.get_width(),60))
        pygame.display.update()
    #draws the buttons
    def button(self,x,y,width,height,colour,text):
        pygame.draw.rect(self.screen,colour,(x,y,width,height))
        text_obj = self.font.render(text,False,(0,0,0))
        self.screen.blit(text_obj,(x-text_obj.get_width()/2+width/2,y-text_obj.get_height()/2+height/2))

def main():

    name,bal = login.main()
    win = Window(600,750,name,bal)
    #main pygame loop
    while True:
        for event in pygame.event.get():
            #if the player wants to quit the game.
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()
            #left click
            if event.type ==pygame.MOUSEBUTTONDOWN and event.button==1:
                win.input(event.pos)
main() #to run the program