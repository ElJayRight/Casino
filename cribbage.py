from random import randrange
import pygame
from math import cos, sin, pi
class Window:
    def __init__(self,screen):
        #for selected cards
        self.selected = [0,0,0,0,0,0]

        self.crib = []
        self.button_locations = {
            'c1':(75,350,62,90),
            'c2':(150,350,62,90),
            'c3':(225,350,62,90),
            'c4':(300,350,62,90),
            'c5':(375,350,62,90),
            'c6':(450,350,62,90),
            'quit':(540,670,60,60)
        }

        self.screen = screen
        self.player_1_peg_spot = {}
        self.player_2_peg_spot = {}

        self.player_1_peg_index = 0
        self.player_2_peg_index = 0
        #creates pygame instance
        pygame.init()
        #fonts
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS',12)
        self.screen.fill((42, 161, 60))

        self.draw_board()
        pygame.draw.rect(self.screen,(255,0,0),(540,670,60,60))
        text_obj = self.font.render("QUIT",False,(255,255,255))
        self.screen.blit(text_obj,(570-text_obj.get_width()//2,700-text_obj.get_height()//2))
       
        pygame.display.update()
    def draw_board(self):
        #draws the board with pygame
        #also adds the location of the pegs to the peg_spot dictionary
        #right semicircle
        pygame.draw.circle(self.screen,(255,0,0),(475,625),75)
        pygame.draw.circle(self.screen,(0,255,0),(475,625),55)
        pygame.draw.rect(self.screen,(42, 161, 60),(400,550,75,150))
        pygame.draw.circle(self.screen,(42, 161, 60),(475,625),35)

        #left semicirlce
        pygame.draw.circle(self.screen,(255,0,0),(125,652.5),47.5)
        pygame.draw.circle(self.screen,(0,255,0),(125,652.5),27.5)
        pygame.draw.circle(self.screen,(42, 161, 60),(125,652.5),7.5)
        pygame.draw.rect(self.screen,(42, 161, 60),(125,600,50,100))
        #rows
        pygame.draw.rect(self.screen,(255,0,0),(125,550,350,20))
        pygame.draw.rect(self.screen,(0,255,0),(125,570,350,20))
        pygame.draw.rect(self.screen,(255,0,0),(125,605,350,20))
        pygame.draw.rect(self.screen,(0,255,0),(125,625,350,20))
        pygame.draw.rect(self.screen,(0,255,0),(125,660,350,20))
        pygame.draw.rect(self.screen,(255,0,0),(125,680,350,20))
        #pegs
        for i in range(35):
            self.player_1_peg_spot[i] = (135+i*10,560)
            self.player_2_peg_spot[i] = (135+i*10,580)
            pygame.draw.circle(self.screen,(0,0,0),(135+i*10,560),3)
            pygame.draw.circle(self.screen,(0,0,0),(135+i*10,580),3)

            self.player_1_peg_spot[i+80] = (130+i*10,615)
            self.player_2_peg_spot[i+80] = (130+i*10,635)

            pygame.draw.circle(self.screen,(0,0,0),(130+i*10,615),3)
            pygame.draw.circle(self.screen,(0,0,0),(130+i*10,635),3)
            #as it goes from right ot left
            self.player_2_peg_spot[75-i] = (135+i*10,670)
            self.player_1_peg_spot[75-i] = (135+i*10,690)

            pygame.draw.circle(self.screen,(0,0,0),(135+i*10,670),3)
            pygame.draw.circle(self.screen,(0,0,0),(135+i*10,690),3)
        
        for i in range(-2,3):
            #math magic for corners

            x_r = 475
            y_r = 625
            x_r+=65*cos((i*pi)/5)
            y_r+=65*sin((i*pi)/5)
            pygame.draw.circle(self.screen,(0,0,0),(x_r,y_r),3)

            x_g = 475
            y_g = 625
            x_g+=45*cos((i*pi)/5)
            y_g+=45*sin((i*pi)/5)
            pygame.draw.circle(self.screen,(0,0,0),(x_g,y_g),3)

            self.player_1_peg_spot[i+37] = (x_r,y_r)
            self.player_2_peg_spot[i+37] = (x_g,y_g)

            x_r = 125
            y_r = 652.5
            x_r-=37.5*cos((i*pi)/5)
            y_r+=37.5*sin((i*pi)/5)
            pygame.draw.circle(self.screen,(0,0,0),(x_r,y_r),3)

            x_g = 125
            y_g = 652.5
            x_g-=17.5*cos((i*pi)/5)
            y_g+=17.5*sin((i*pi)/5)
            pygame.draw.circle(self.screen,(0,0,0),(x_g,y_g),3)
            
            self.player_1_peg_spot[i+73] = (x_r,y_r)
            self.player_2_peg_spot[i+73] = (x_g,y_g)

        pygame.draw.circle(self.screen,(255,255,255),self.player_1_peg_spot[self.player_1_peg_index],3)
        pygame.draw.circle(self.screen,(255,255,255),self.player_2_peg_spot[self.player_2_peg_index],3)

        pygame.display.update()

    def keep(self,box):
        #shows the cards to be removed (keep sounds backwards but so be it)
        button_box= (170,460,260,40)
        value = (box[0])//75 -1
        if self.selected[value]:
            new_box =[box[0],box[1]-30,62,20]
            pygame.draw.rect(self.screen,(42, 161, 60),new_box)
            self.selected[value]=0
            try:
                #remove button location
                del self.button_locations['discard']
                #remove button GUI
                pygame.draw.rect(self.screen,(42, 161, 60),button_box)
                pygame.display.update()
            except:
                pass
        else:
            if self.selected.count(1)==2:
                pygame.display.update()
                return
            new_box =[box[0],box[1]-30,62,20]
            pygame.draw.rect(self.screen,(0,0,0),new_box)
            self.selected[value]=1
            if self.selected.count(1)==2:
                #draw button
                pygame.draw.rect(self.screen,(0,0,0),button_box)
                text_obj = self.font.render('Discard selected cards.',False,(255,255,255))
                self.screen.blit(text_obj,(button_box[0]+button_box[2]//2-text_obj.get_width()//2,
                button_box[1]+button_box[3]//2-text_obj.get_height()//2))
                #update button locations
                self.button_locations['discard']=button_box
                

            text_obj = self.font.render('Discard',False,(255,255,255))
            x = box[0]+31-text_obj.get_width()//2
            y = box[1]-30
            self.screen.blit(text_obj,(x,y))
        pygame.display.update()
    #this shouldnt be here
    def input(self,action):
        return
    def init_gameplay(self):
        
        return
    #adds a card to the pile
    def add_card(self,player,box):
        card = box[0]//75-1

        card = player.hand[card]
        self.pile.append(card)
        player.hand.remove(card)

        return
    #adds cards to the crib
    def add_to_crib(self,player, is_dealer =False):
        if is_dealer:
            #as the dealer just removes first two cards for simplicity
            for i in range(2):
                self.crib.append(player.hand[0])
                player.hand.remove(player.hand[0])
        remove = []
        #removes both cards and adds them to the crib
        for i,j in enumerate(self.selected):
            if j ==1:
                remove.append(i)
                self.crib.append(player.hand[i])  
        for i,j in enumerate(remove):
            player.hand.remove(player.hand[j-i])
        pygame.draw.rect(self.screen,(42, 161, 60),(170,460,260,40))
        
        self.selected = [0,0,0,0,0,0] #resets the cards selected.
    def text(self,string):
        #button
        pygame.draw.rect(self.screen,(0,0,0),(470,470,70,50))
        text_obj = self.font.render("Next",False,(255,255,255))
        self.screen.blit(text_obj,(490,485))
        #text
        text_obj = self.font.render(string,False,(255,255,255))
        self.screen.blit(text_obj,(150,480))

        pygame.display.update()
        #to wait for the player ot hit the next button
        while True:
            for event in pygame.event.get():
                #left click
                if event.type ==pygame.MOUSEBUTTONDOWN and event.button==1:
                    if event.pos[0] in range(490,560) and event.pos[1] in range(480,530):
                        pygame.draw.rect(self.screen,(42, 161, 60),(150,470,410,50))
                        pygame.display.update()
                        return

    def score(self,hand):
        #calculates the score of the hand
        cards = hand
        score_counter=0
        cards.append(self.pile[0]) #the top crib card is included
        suits,values = [],[]
        for i in cards:
            suits.append(i[1])
            values.append(i[2])
        values.sort()

        #runs of 3,4 or 5
        counter =0
        for i in range(len(values)-1):
            if values[i]+1 != values[i+1] or values[i] ==0:
                break
            else:
                counter +=1
        if counter ==2:
            self.text("run of 3")
            score_counter+=15
        elif counter==3:
            self.text("run of 4")
            score_counter+=16
        elif counter ==4:
            self.text("run of 5")
            score_counter+=17

        
        #same suit
        for i in suits:
            if suits.count(i)==5:
                self.text("ALL FIVE")
                score_counter+=25
                break
            elif suits.count(i)==4:
                self.text("Four cards of same suit")
                score_counter+=20
                break

        #2,3,4 of a kind   
        counted = []
        for i in values:
            if values.count(i)==4 and i not in counted:
                self.text("Four of a kind")
                score_counter+=12
                counted.append(i)
            if values.count(i)==3 and i not in counted:
                self.text("Three of a kind")
                score_counter+=6
                counted.append(i)
            if values.count(i)==2 and i not in counted:
                self.text("Two of a kind")
                score_counter+=2
                counted.append(i)

        #add to fifteen
        #hard code method
        for i,j in enumerate(values):
            if j>10:
                values[i]=10
        fifteen_counter = 0
        if values[4] !=0:
            two_cards = [values[0]+values[1],values[0]+values[2],values[0]+values[3],values[0]+values[4],
            values[1]+values[2],values[1]+values[3],values[1]+values[4],
            values[2]+values[3],values[2]+values[4],values[3]+values[4]]
            three_cards = [values[0]+values[1]+values[2],values[0]+values[1]+values[3],
            values[0]+values[1]+values[4],values[0]+values[2]+values[3],values[0]+values[2]+values[4],
            values[0]+values[3]+values[4],values[1]+values[2]+values[3],values[1]+values[2]+values[4],
            values[1]+values[3]+values[4],values[2]+values[3]+values[4]]
            four_cards = [values[1]+values[2]+values[3]+values[4],values[0]+values[2]+values[3]+values[4],
            values[0]+values[1]+values[3]+values[4], values[0]+values[1]+values[2]+values[4],
            values[0]+values[1]+values[2]+values[3]]
            five_cards = [values[0]+values[1]+values[2]+values[3]+values[4]]
            
        else:
            two_cards = [values[0]+values[1],values[0]+values[2],values[0]+values[3],
            values[1]+values[2],values[1]+values[3], values[2]+values[3]]
            three_cards = [values[0]+values[1]+values[2],values[0]+values[1]+values[3],
            values[0]+values[2]+values[3], values[1]+values[2]+values[3]]
            four_cards = [values[0]+values[1]+values[2]+values[3]]
            five_cards = 0

        for i in two_cards:
            if i ==15:
                fifteen_counter+=1
        for i in three_cards:
            if i ==15:
                fifteen_counter+=1
        for i in four_cards:
            if i==15:
                fifteen_counter+=1
        for i in five_cards:
            if i==15:
                fifteen_counter+=1
        if fifteen_counter != 0:
            if fifteen_counter==1:
                text = (str(fifteen_counter)+" group that adds up to 15")
            else:
                text = (str(fifteen_counter)+" groups that add up to 15")
            fifteen_counter*=2
            score_counter+=fifteen_counter
            self.text(text)
        cards.remove(self.pile[0])
        return score_counter

    def render(self,object=None): #Is this used?
        pygame.display.update()

    def count_crib(self):
        #counts the crib score
        from time import sleep
        font = pygame.font.SysFont('Comic Sans MS',24)
        text_obj = font.render("The Crib",False,(255,255,255))
        pygame.draw.rect(self.screen,(42, 161, 60),(50,50,550,400))
        self.screen.blit(text_obj,(300-text_obj.get_width(),290-text_obj.get_height()))
        for j,i in enumerate(self.crib):
            j+=1
            self.screen.blit(i[0], (75+j*75,300))
        pygame.display.update()
        sleep(1)
        self.crib.append([0,'NONE',0])
        self.score(self.crib)
class rules:
    def __init__(self,screen):
        pygame.init()
        self.font = pygame.font.SysFont('Comic Sans MS',12)
        self.screen = screen
        self.screen.fill((42, 161, 60))
        #Quit button
        pygame.draw.rect(self.screen,(255,0,0),(540,670,60,60))
        text_obj = self.font.render("QUIT",False,(255,255,255))
        self.screen.blit(text_obj,(570-text_obj.get_width()//2,700-text_obj.get_height()//2))


        #text
        text = ["You made it to the rules section.","Cribbage has many different parts.",
        "The first section is to select 2 cards to add to the cirb","After this the remaining four cards are used to from a pile of 31.",
        "The player and computer take turns placing one card at a time.",
        "From here points are awarded form the crib, starting hand and if the score 15 or 31 was reached.",
        "The first person to reach a score of 121 wins."]
        for j,i in enumerate(text):
            self.render_text(i,10,80+j*30)
        pygame.display.update()
        self.button_locations = {
            'quit':(540,670,60,60)
        }
    def render_text(self,string,x,y):
        text_obj = self.font.render(str(string),False,(0,0,0))
        self.screen.blit(text_obj,(x,y))