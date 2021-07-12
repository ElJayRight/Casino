from time import sleep
import pygame
class start:
    def __init__(self,screen,player):
        self.player = player
        #creates pygame instance
        pygame.init()

        #fonts
        pygame.font.init()
        self.chip_font = pygame.font.SysFont('Comic Sans MS',12)
        self.screen = screen
        self.screen.fill((42, 161, 60))
        self.bets()
        #dealer area
        pygame.draw.circle(self.screen,(205, 217, 41),(300,130),50)
        pygame.draw.circle(self.screen,(42, 161, 60),(300,130),43)


        #player area
        pygame.draw.circle(self.screen,(205, 217, 41),(300,430),50)
        pygame.draw.circle(self.screen,(42, 161, 60),(300,430),43)

        pygame.draw.circle(self.screen,(205, 217, 41),(300,540),25)
        pygame.draw.circle(self.screen,(42, 161, 60),(300,540),22)
        self.draw_circle(280,630,25,20,(44,111,212),(0,0,0),"Play")
        #buttons
        self.button_locations = {
            'Play':(280,630,25,25)
        }
        
        
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
    #pygame does not like to make circles with text easy
    def draw_circle(self,x,y,R,r,colour,f_colour,text = False):
        pygame.draw.circle(self.screen,(205, 217, 41),(x,y),R)
        pygame.draw.circle(self.screen,colour,(x,y),r)
        if text:
            text_obj = self.chip_font.render(text,False,f_colour)
            self.screen.blit(text_obj,(x-text_obj.get_width()//2,y-text_obj.get_height()//2))

class main:
    def __init__(self,screen):
        self.screen = screen
        #displays icons on the screen
        self.chip_font = pygame.font.SysFont('Comic Sans MS',12)
        self.draw_circle(200,630,25,20,(44, 111, 212),(0,0,0),"Hit")
        self.draw_circle(280,630,25,20,(113, 40, 191),(0,0,0),"Pass")
        self.draw_circle(360,630,25,20,(50, 160, 219),(0,0,0),"Double down")
        
        pygame.draw.rect(self.screen,(42,161,60),(400,520,150,100))
        #updates buttons
        self.button_locations = {
        'hit':(200,630,25,25),
        'pass':(280,630,25,25),
        'double_down':(360,630,25,25)
        }
        pygame.display.update()

    def draw_circle(self,x,y,R,r,colour,f_colour,text = False):
        pygame.draw.circle(self.screen,(205, 217, 41),(x,y),R)
        pygame.draw.circle(self.screen,colour,(x,y),r)
        if text:
            text_obj = self.chip_font.render(text,False,f_colour)
            self.screen.blit(text_obj,(x-text_obj.get_width()//2,y-text_obj.get_height()//2))

    def scoring(self,player,dealer_score):
        self.chip_font1 = pygame.font.SysFont('Comic Sans MS',14)

        def render_text(string,x=300,y=280):
            text_obj = self.chip_font1.render(str(string),False,(0,0,0))
            self.screen.blit(text_obj,(x-text_obj.get_width()//2,y-text_obj.get_height()//2))
        #gets the score of the players hand
        player_score = player.score_blackjack()
        
        #Finds the winning hand and computes bets
        if player_score>21 or (dealer_score<21 and dealer_score>player_score):
            render_text("You lost")
            player.bal -=player.bet
            output = "Remaining balance: "+str(player.bal)
        elif dealer_score==player_score:
            render_text('It was a tie')
            output = "Remaining balance: "+str(player.bal)
        else:
            render_text("You won")
            player.bal +=player.bet
            output = "Remaining balance: "+str(player.bal)
        render_text(output,300,280+24)

        results = []
        file = open("database.txt",'r')
        for line in file:
            if line.split()[0]==player.name:
                line = line.split()
                line[2] = str(player.bal)
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
        self.button_locations = {
            'quit':(540,670,60,60)
        }
        pygame.draw.rect(self.screen,(255,0,0),(540,670,60,60))
        text_obj = self.chip_font.render("QUIT",False,(255,255,255))
        self.screen.blit(text_obj,(570-text_obj.get_width()//2,700-text_obj.get_height()//2))
        pygame.display.update()
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
        text = ["You made it to the rules section.","The goal of the game is to:"," - Beat the dealer by being closer to 21.",
        " - You can not exceed 21."]
        for j,i in enumerate(text):
            self.render_text(i,10,80+j*30)
        pygame.display.update()
        self.button_locations = {
            'quit':(540,670,60,60)
        }
    def render_text(self,string,x,y):
        text_obj = self.font.render(str(string),False,(0,0,0))
        self.screen.blit(text_obj,(x,y))