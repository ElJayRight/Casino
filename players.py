import pygame
from random import randint
class player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.bal = 0
        self.bet = 0
    def add_bet(self,value):
        self.bet +=value
    def update_balance(self,win):
        self.bal +=self.bet*win
    def wipe(self):
        self.hand = []
        self.bet = 0
    def add_card(self,deck):
        self.hand.append(deck.deck[randint(0, len(deck.deck)-2)])
    def score_blackjack(self):
        #logic of blackjack scoring
        score = 0
        ace_counter = 0
        for i in self.hand:
            if i[2] ==1:
                ace_counter+=1
                score+=1
            elif i[2] >10:
                score+=10
            else:
                score+=i[2]
        for i in range(ace_counter):
            if score+10 >21:
                pass
            else:
                score+=10
        return score


class Sprite_Sheet:
    #loads the deck image as a sprite file.
    def __init__(self,img,rows, cols):
        self.image = pygame.image.load(img)
        #scales the image reletavie to itself.
        self.image = pygame.transform.scale(self.image,(self.image.get_width()//2,self.image.get_height()//2))
        self.rows = rows
        self.cols =cols
        #used for offsets
        self.row_width = self.image.get_height()/rows 
        self.cols_width = self.image.get_width()/cols
        self.images()
    #Gets each image and adds the image to an array.
    def images(self):
        self.sprites = []
        for j in range(self.rows):
            j*=self.row_width
            for i in range(self.cols):
                #blits the section onto a new surface (like snipping tool)
                rect = pygame.Rect((i*self.cols_width,j,self.cols_width,self.row_width)) 
                #should read my comments they might help
                image = pygame.Surface(rect.size).convert()
                image.blit(self.image,(0,0),rect)

                self.sprites.append(image)

class Deck:
    #builds the deck form the sprite sheet.
    def __init__(self,picture):
        images = Sprite_Sheet(picture,4,13)
        self.images = images.sprites
        self.deck = self.Create_deck()
    def Create_deck(self):
        deck = {}
        for i in range(len(self.images)):
            score = i
            suit = ["Clubs","Spades","Hearts","Diamonds"][score//13]
            score = score %13
            deck[i] = [self.images[i],suit,score+1]

        image = pygame.image.load("back_of_card.png")
        image = pygame.transform.scale(image, (self.images[i].get_width(),self.images[i].get_height()))
        deck["BACK"] = image
        return deck