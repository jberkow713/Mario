import pygame
import random
from sys import exit
from pygame.locals import  *
pygame.init()

WIDTH=800
HEIGHT=800
BG_Color = (64,124,200)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
ground = pygame.image.load('ground.png').convert()
font = pygame.font.Font('font.ttf',50)
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
Meteors = []
Rectangles= []

class Player:
    def __init__(self, x):
        self.x = x
        self.y = 700
        self.image = pygame.image.load('player_walk_1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (75,75))
        self.rect = self.image.get_rect(bottomright=(self.x,self.y))
        self.speed = 5
        self.floor = None
        self.can_jump=True

    def move(self):
        if self.can_jump==True and self.floor!=None:
            count = 0
            temp = self.image.get_rect(bottomright=(self.x,self.y+10))
            for r in Rectangles:
                if pygame.Rect.colliderect(temp, r.rect)==0:
                    count+=1
            if count==len(Rectangles):
                self.y+=10
                if self.y>=700:
                    self.y = 700
                    self.floor=None
        if self.can_jump==False:            
            current = self.y + 10
            for r in Rectangles:
                temp = self.image.get_rect(bottomright=(self.x, current))
                if pygame.Rect.colliderect(temp, r.rect)==1:
                    self.floor = self.y = r.y
                    self.can_jump=True
                    return
            self.y +=10
            if self.y>=700:
                self.y = 700
                self.can_jump=True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            current = self.x - self.speed
            count = 0
            for r in Rectangles:                            
                temp = self.image.get_rect(bottomright=(current,self.y))
                if pygame.Rect.colliderect(temp, r.rect)==0:
                    count+=1
            if count ==len(Rectangles):
                self.x =current                   
                                                                   
        if keys[pygame.K_RIGHT]:            
            current = self.x + self.speed
            count = 0
            for r in Rectangles:                            
                temp = self.image.get_rect(bottomright=(current,self.y))
                if pygame.Rect.colliderect(temp, r.rect)==0:
                    count+=1
            if count ==len(Rectangles):
                self.x =current                          
                
        if keys[pygame.K_RETURN] and self.can_jump==True:
            L = []
            for r in Rectangles:
                if self.floor ==None:

                    if self.x >r.x and self.x-75< r.x + r.width:
                        L.append(r)
                else:
                   if self.x >r.x and self.x-75< r.x + r.width:
                        if r.y <self.floor:
                            L.append(r)         
            
            Lowest = 0
            for r in L:
                if r.y>=Lowest:
                    Lowest = r.y 
            for r in L:
                if r.y == Lowest:
                    if self.y >r.y:                        
                        if r.y +r.height >= self.y - 300:
                            self.y = r.y + r.height+75 
                            self.can_jump=False
                            return  
            self.y -= 300
            self.can_jump=False        
        if self.rect.left>=WIDTH:
            self.x = 0
        elif self.rect.right<0:
            self.x = 850
        self.rect = self.image.get_rect(bottomright=(self.x,self.y))

    def blit(self):
        screen.blit(self.image,self.rect)                  

class Meteor:
    def __init__(self):
        self.x = random.randint(50,750)
        self.y = 0
        self.speed = 5
        self.image = pygame.image.load('Meteor.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (75, 50))
        self.rect = self.image.get_rect(midtop=(self.x,self.y))
        Meteors.append(self)          
    def blit(self):
        screen.blit(self.image,self.rect)        
    def move(self):
        self.rect.y += self.speed
        if self.rect.top >=HEIGHT:
            self.rect.bottom = 0
            rework=False
            while rework==False:
                x = random.randint(50,750)
                for m in Meteors:
                    if m.rect.x!=x:
                        self.rect.x = x
                        rework=True
                        break                    

class RECT:
    def __init__(self,color,x,y, width,height):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height   
        self.rect = Rect(x, y, width, height)
        Rectangles.append(self)        
    def blit(self):
        pygame.draw.rect(screen, self.color,self.rect)    

for _ in range(5):
    Meteor()
P = Player(100)
RECT('blue', 150,600,100,100)
RECT('red',250,500,100,100)
RECT('green',350,400,100,100)
RECT('blue', 450,300,100,100)
RECT('red',450,400,100,100)
RECT('green',650,500,100,100)
RECT('blue', 150,300,100,100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill(BG_Color)
    screen.blit(ground,(0,700))    
    for r in Rectangles:
        r.blit()
    for meteor in Meteors:
        meteor.move()
        meteor.blit()    
    P.move()
    P.blit()

    pygame.display.update()
    clock.tick(60)