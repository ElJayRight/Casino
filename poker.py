from time import sleep
import pygame
from random import randint
class start:
    def __init__(self,screen,player):
        pygame.init()
        self.player = player
        self.selected = [0,0,0,0,0]
        self.font = pygame.font.SysFont('Comic Sans MS',12)
        self.screen = screen
        self.screen.fill((42, 161, 60))

        self.bets()

        #Quit button
        pygame.draw.rect(self.screen,(255,0,0),(540,670,60,60))
        text_obj = self.font.render("QUIT",False,(255,255,255))
        self.screen.blit(text_obj,(570-text_obj.get_width()//2,700-text_obj.get_height()//2))
        self.button_locations = {
            'c1':(125,400,62,90),
            'c2':(200,400,62,90),
            'c3':(275,400,62,90),
            'c4':(350,400,62,90),
            'c5':(425,400,62,90),
            'p_r':(145,520,325,50),
            'quit':(540,670,60,60)
        }
        
        self.redraw()
        self.winnings()
        pygame.display.update()
    def bets(self):

        font = pygame.font.SysFont('Comic Sans MS',18)
        text_obj = font.render("Bet amount:",False,(0,0,0))
        self.screen.blit(text_obj,(250,370))

        error_font = pygame.font.SysFont('Comic Sans MS',12)
        text_obj = error_font.render("Press enter to continue",False,(0,0,0))
        self.screen.blit(text_obj,(250,450))
        
        def update(text,font):
            pygame.draw.rect(self.screen,(42, 161, 60),(250,400,100,50))
            pygame.draw.rect(self.screen,(0,0,0),(250,400,100,50),1)
            text_obj = font.render(text,False,(0,0,0))
            self.screen.blit(text_obj,(260,410))
            pygame.display.update()

        pygame.draw.rect(self.screen,(0,0,0),(250,400,100,50),1)
        pygame.display.update()
        text = ''

        while True:
            for event in pygame.event.get():
                #if the player wants to quit the game.
                if event.type==pygame.QUIT:
                    pygame.quit()
                    exit()
                #left click
                if event.type ==pygame.MOUSEBUTTONDOWN and event.button==1:
                    pass
                if event.type ==pygame.KEYDOWN:
                    try:
                        if event.key ==8:
                            text = text[:-1]
                            update(text,font)
                        elif event.key ==13:
                            
                            if int(text) <=self.player.bal:
                                pygame.draw.rect(self.screen,(42, 161, 60),(200,300,200,200))
                                self.player.bet = int(text)
                                self.player.bal -=self.player.bet
                                return
                            else:
                                text = ''
                                update(text,font)
                                text_obj = error_font.render("The bet is to big.",False,(0,0,0))
                                self.screen.blit(text_obj,(250,470))
                                pygame.display.update()
                                sleep(2)
                                pygame.draw.rect(self.screen,(42, 161, 60),(250,470,100,20))
                                pygame.display.update()

                        elif event.key in range(48,58):
                            text+=chr(event.key)
                            update(text,font)
                    except Exception as e:
                        pass
    def keep(self,box):
        #selected cards to keep
        value = (box[0]-50)//75 -1
        if self.selected[value]:
            new_box =[box[0],box[1]-30,62,20]
            pygame.draw.rect(self.screen,(42, 161, 60),new_box)
            self.selected[value]=0
        else:
            new_box =[box[0],box[1]-30,62,20]
            pygame.draw.rect(self.screen,(0,0,0),new_box)
            self.selected[value]=1
            
            text_obj = self.font.render('hold',False,(255,255,255))
            x = box[0]+31-text_obj.get_width()//2
            y = box[1]-30
            self.screen.blit(text_obj,(x,y))
        pygame.display.update()

    def redraw(self):
        #tells the user that they can redraw the cards
        pygame.draw.rect(self.screen,(0,0,0),(145,520,325,50))
        text_obj = self.font.render('REDRAW',False,(255,255,255))
        x = 145+(325/2) - text_obj.get_width()//2
        y = 520+(50/2) - text_obj.get_height()//2
        self.screen.blit(text_obj,(x,y))

    def redraw_cards(self,player,deck):
        #redraws cards that are not selected
        for j,i in enumerate(self.selected):
            if i==0:
                player.hand[j] = deck.deck[randint(0, len(deck.deck)-1)]

    def winnings(self,bet=None):
        #Shows the users bet and the value.
        pygame.draw.rect(self.screen,(0,0,0),(0,640,100,50))
        text_obj = self.font.render('User\'s bet',False,(255,255,255))
        x = 0+(100/2) - text_obj.get_width()//2
        y = 640+(50/2) - text_obj.get_height()//2
        self.screen.blit(text_obj,(x,y))

        pygame.draw.rect(self.screen,(0,0,0),(0,690,100,40))
        text_obj = self.font.render(str(self.player.bet),False,(255,255,255))
        x = 0+(100/2) - text_obj.get_width()//2
        y = 690+(50/2) - text_obj.get_height()//2
        self.screen.blit(text_obj,(x,y))
        return
    def end(self,result):
        #shows the result of the game
        pygame.draw.rect(self.screen,(42, 161, 60),(125,370,400,20))
        pygame.draw.rect(self.screen,(0,0,0),(145,520,325,50))
        text_obj = self.font.render(result,False,(255,255,255))
        x = 145+(325/2) - text_obj.get_width()//2
        y = 520+(50/2) - text_obj.get_height()//2
        self.screen.blit(text_obj,(x,y))
        pygame.display.update()

        results = []
        self.player.bal +=self.player.bet
        file = open("database.txt",'r')
        for line in file:
            if line.split()[0]==self.player.name:
                line = line.split()
                line[2] = str(self.player.bal)
                line = ' '.join(line)
            results.append(line)
        file.close()

        file = open('database.txt','w')
        for j,i in enumerate(results):
            if j ==len(results)-1:
                file.write(i)
            else:
                file.write(i+'\n')
        file.close()

        return

#User display for the rules.
class rules:
    def __init__(self,screen):
        pygame.init()
        self.selected = [0,0,0,0,0]
        self.font = pygame.font.SysFont('Comic Sans MS',12)
        self.screen = screen
        self.screen.fill((42, 161, 60))
        #Quit button
        pygame.draw.rect(self.screen,(255,0,0),(540,670,60,60))
        text_obj = self.font.render("QUIT",False,(255,255,255))
        self.screen.blit(text_obj,(570-text_obj.get_width()//2,700-text_obj.get_height()//2))
        image = pygame.image.load('scoringsheet.jpg')
        image = pygame.transform.scale(image,(image.get_width()//2,image.get_height()//2))
        self.screen.blit(image,(100,220))


        #text
        text = ["You made it to the rules section.","You start by being delt five cards.",
        "You can choose as many cards to hold as you want by clicking on them",
        "Then you hit play and it will redraw the cards that have not been selected.",
        "The hand will then be compaired against a scoring sheet and winnings will be handed out."]
        for j,i in enumerate(text):
            self.render_text(i,10,80+j*30)
        pygame.display.update()
        self.button_locations = {
            'quit':(540,670,60,60)
        }
    def render_text(self,string,x,y):
        text_obj = self.font.render(str(string),False,(0,0,0))
        self.screen.blit(text_obj,(x,y))

def scoring(hand):
    #Two of a kind
    values = []
    suits = []
    for i in hand:
        suits.append(i[1])
        if i[2] ==1:
            values.append(14)
        else:
            values.append(i[2])
    pairs = []

    Results_of_pairs = {2:0,3:0,4:0}
    for i in values:
        if i not in pairs:
            if values.count(i)==4:
                pairs.append(i)
                Results_of_pairs[4]+=1
            elif values.count(i)==3:
                pairs.append(i)
                Results_of_pairs[3]+=1
            elif values.count(i) ==2:
                pairs.append(i)
                Results_of_pairs[2]+=1
    #straight
    counter =0
    values.sort()
    for i in range(len(values)-1):
        if values[i]+1 != values[i+1]:
            break
        else:
            counter +=1
            
    if suits.count(suits[0])==5:
        if 14 in values and counter ==4:
            return "Royal flush"
        elif counter ==4:
            return "Straight Flush"
    if Results_of_pairs[4]:
        return "Four of a kind"
    if Results_of_pairs[3] and Results_of_pairs[2]:
        return "Full house"
    if suits.count(suits[0])==5:
        return "Flush"
    if counter ==4:
        return "Straight"
    if Results_of_pairs[3]:
        return "Three of a kind"
    if Results_of_pairs[2] ==2:
        return "Two pairs"
    if Results_of_pairs[2]:
        return "A pair"
    return ""