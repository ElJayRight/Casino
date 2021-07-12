import pygame,hashlib
from time import sleep
class Window:
    def __init__(self,x,y):
        self.width = x
        self.height = y
        #creates pygame instance
        pygame.init()

        #fonts
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS',18)
        self.screen = pygame.display.set_mode((x,y))
        self.screen.fill((255,255,255))

        self.font_buttons = pygame.font.SysFont('Comic Sans MS',14)
        
        self.Login()
        self.enter_text()
    def make_user(self):
        self.active = 0
        self.box_locations = []
        #Username
        self.username = ''
        text_obj = self.font.render("Username: ",False,(0,0,0))
        self.screen.blit(text_obj,(140-text_obj.get_width()/2,130))

        x = 140+text_obj.get_width()/2
        self.box_locations.append((x,130,170,25))
        pygame.draw.rect(self.screen,(0,0,0),(x,130,170,25),1)

        #Password
        self.password = ''
        text_obj = self.font.render("Password: ",False,(0,0,0))
        self.screen.blit(text_obj,(140-text_obj.get_width()/2,170))

        self.box_locations.append((x,170,170,25))

        pygame.draw.rect(self.screen,(0,0,0),(x,170,170,25),1)
        
        #Confirm password
        self.confirm_password = ''
        text_obj = self.font.render("Confirm Password: ",False,(0,0,0))
        self.screen.blit(text_obj,(text_obj.get_width()/2-50,210))

        self.box_locations.append((x,210,170,25))

        pygame.draw.rect(self.screen,(0,0,0),(x,210,170,25),1)

        #buttons
        self.button_locations = {}
        
        #Login
        location = (90,380,120,60)
        self.button_locations['Back'] = location
        pygame.draw.rect(self.screen,(0,255,255),location)
        
        text_obj = self.font_buttons.render("Back",False,(0,0,0))
        self.screen.blit(text_obj,(150-text_obj.get_width()/2,410-text_obj.get_height()/2))

        #New User
        location = (290,380,120,60)
        self.button_locations['Create'] = location
        pygame.draw.rect(self.screen,(0,255,255),location)
        
        text_obj = self.font_buttons.render("Create",False,(0,0,0))
        self.screen.blit(text_obj,(350-text_obj.get_width()/2,410-text_obj.get_height()/2))
        pygame.display.update()

    def Login(self):
        #GUI
        self.active= 0 #0 for username 1 for password
        self.box_locations = []
        self.confirm_password = ''
        #Username
        self.username = ''
        text_obj = self.font.render("Username: ",False,(0,0,0))
        self.screen.blit(text_obj,(140-text_obj.get_width()/2,130))

        x = 140+text_obj.get_width()/2
        self.box_locations.append((x,130,170,25))
        pygame.draw.rect(self.screen,(0,0,0),(x,130,170,25),1)

        #Password
        self.password = ''
        text_obj = self.font.render("Password: ",False,(0,0,0))
        self.screen.blit(text_obj,(140-text_obj.get_width()/2,170))

        self.box_locations.append((x,170,170,25))

        pygame.draw.rect(self.screen,(0,0,0),(x,170,170,25),1)
        pygame.draw.rect(self.screen,(255,255,255),(0,210,400,30))
        #buttons
        self.button_locations = {}
        
        #Login
        location = (90,380,120,60)
        self.button_locations['login'] = location
        pygame.draw.rect(self.screen,(0,255,255),location)
        
        text_obj = self.font_buttons.render("Login",False,(0,0,0))
        self.screen.blit(text_obj,(150-text_obj.get_width()/2,410-text_obj.get_height()/2))

        #New User
        location = (290,380,120,60)
        self.button_locations['new user'] = location
        pygame.draw.rect(self.screen,(0,255,255),location)
        
        text_obj = self.font_buttons.render("Create New User",False,(0,0,0))
        self.screen.blit(text_obj,(350-text_obj.get_width()/2,410-text_obj.get_height()/2))
        pygame.display.update()
    def update_text(self):
        self.creds_font = pygame.font.SysFont('Comic Sans MS',12)
        text = [self.username,self.password,self.confirm_password]
        for i in range(len(self.box_locations)):
            pygame.draw.rect(self.screen,(255,255,255),self.box_locations[i])
            pygame.draw.rect(self.screen,(0,0,0),self.box_locations[i],1)

            text_obj = self.creds_font.render(text[i],False,(0,0,0))
            x,y = self.box_locations[i][0],self.box_locations[i][1]
            self.screen.blit(text_obj,(x+5,y))
        pygame.display.update()

    def enter_text(self,change = None):
        #draws the green box
        green_box = {
            '0':(360,137,10,10),
            '1':(360,177,10,10)
        }
        if self.active==2:
            green_box['2'] = (360,217,10,10)
        location = green_box[str(self.active)]
        #wiping previous display
        pygame.draw.rect(self.screen,(255,255,255),(360,137,10,10))
        pygame.draw.rect(self.screen,(255,255,255),(360,177,10,10))
        pygame.draw.rect(self.screen,(255,255,255),(360,217,10,10))

        #drawing new box
        pygame.draw.rect(self.screen,(0,255,0),location)
        #handle text
        if self.active==0:
            if change ==8:
                self.username = self.username[:-1]
            elif change !=None:
                self.username+=change
        elif self.active ==1:
            if change ==8:
                self.password = self.password[:-1]
            elif change !=None:
                self.password+=change
        else:
            if change==8:
                self.confirm_password = self.confirm_password[:-1]
            elif change !=None:
                self.confirm_password+=change
        self.update_text()
        pygame.display.update()
    def create_user(self):
        if self.password==self.confirm_password and self.password!='':
            file = open("database.txt","a")         
            file.write('\n'+self.username+' '+hashlib.sha256(bytes(self.password,'utf-8')).hexdigest()+' 500')
            self.error("New User Created.")
        else:
            self.error("There was an error please try again.")
            self.active=0
            self.password = ''
            self.username = ''
            self.confirm_password = ''
            self.enter_text()
        return
    def error(self,text):
        text_obj = self.font.render(text,False,(255,0,0))
        self.screen.blit(text_obj,(250-text_obj.get_width()/2,250))
        pygame.display.update()
        sleep(3)
        pygame.draw.rect(self.screen,(255,255,255),(250-text_obj.get_width()/2,250,400,30))
        pygame.display.update()
        self.active=0
        self.password = ''
        self.username = ''
        self.confirm_password = ''
        self.enter_text()
    def input(self,action):
        x,y = action
        for action in self.button_locations:
            location = self.button_locations[action]
            if x in range(location[0],location[0]+location[2]) and y in range(location[1],location[1]+location[3]):
                if action =='login':
                    result = self.login()
                    return result
                elif action =='new user':
                    self.make_user()
                    self.enter_text()
                    return 0
                elif action =='Back':
                    self.Login()
                    self.enter_text()
                    return 0
                elif action == 'Create':
                    self.create_user()
        return 0
    def login(self):
        with open("database.txt","r") as file:
            for line in file:
                line = line.split()
                if line[0] ==self.username:
                    hashed_value = hashlib.sha256(bytes(self.password,'utf-8'))
                    if line[1] ==hashed_value.hexdigest():
                        return line[0], line[2]
                    else:
                        self.error("Username or password found")
                    return 0
            self.error("Username or password not found")
            return 0
def main():
    win = Window(500,500)
    result = 0
    while True:
        for event in pygame.event.get():
            #if the player wants to quit the game.
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()
            #left click
            if event.type ==pygame.MOUSEBUTTONDOWN and event.button==1:
                result = win.input(event.pos)

            if event.type ==pygame.KEYDOWN:
                try:
                    if event.key ==8:
                        win.enter_text(8)
                    elif event.key ==9:
                        win.active = (win.active+1)%len(win.box_locations)
                        win.enter_text()
                    elif event.key ==13:
                        result =win.login()
                    else:
                        letter = chr(event.key)
                        win.enter_text(letter)
                except Exception as e:
                    pass
        if result !=0:
            return result
if __name__ =='__main__':
    print(main())