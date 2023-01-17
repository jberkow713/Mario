import pygame
import random
from sys import exit
from pygame.locals import  *
pygame.init()

WIDTH=800
HEIGHT=800
FLOOR = 700
BG_Color = (64,124,200)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
ground = pygame.image.load('ground.png').convert()
font = pygame.font.Font('font.ttf',50)
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
Meteors = []
Rectangles= []
Coins = []

class Player:
    # Character Movement, collision detection, etc.
    def __init__(self, x):
        self.x = x
        self.y = FLOOR
        self.image = pygame.image.load('player_walk_1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (75,75))
        self.rect = self.image.get_rect(bottomright=(self.x,self.y))
        self.speed = 5
        self.floor = None
        self.can_jump=True
        self.JUMP = 400
        self.x_size = 75
        self.y_size = 75
        self.gravity = 10
        self.map = Map(8)
        self.map.build()
    def coin_check(self):
        for coin in Coins:
            if pygame.Rect.colliderect(self.rect,coin.rect)==1:
                Coins.remove(coin)
    def move(self):
        if self.can_jump==True and self.floor!=None:
            count = 0
            temp = self.image.get_rect(bottomright=(self.x,self.y+self.gravity))
            for r in Rectangles:
                if pygame.Rect.colliderect(temp, r.rect)==0:
                    count+=1
            if count==len(Rectangles):
                self.y+=self.gravity
                if self.y !=FLOOR:
                    self.floor = self.y
                    self.can_jump=False
                if self.y>=FLOOR:                    
                    self.y = FLOOR
                    self.floor=None
                    self.can_jump=True
                    
        if self.can_jump==False:            
            current = self.y + self.gravity
            for r in Rectangles:
                temp = self.image.get_rect(bottomright=(self.x, current))                                    
                if pygame.Rect.colliderect(temp, r.rect)==1:
                    self.floor = self.y = r.y
                    self.can_jump=True
                    return
            self.y =current
            if self.y>=FLOOR:
                self.y = FLOOR
                self.can_jump=True                
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            collide=False
            current = self.x - self.speed            
            temp = self.image.get_rect(bottomright=(current,self.y))
            for r in Rectangles:                            
                if collide==True:
                    break
                if r.x < current - self.x_size: 
                    if pygame.Rect.colliderect(temp, r.rect)==1:                    
                        self.x = r.x + r.width + self.x_size
                        collide=True                        
            if collide==False:
                self.x = current            
            if self.x<=0:
                Rectangles.clear()
                Coins.clear()
                self.map.build()
                self.x = WIDTH+self.x_size
            self.coin_check()                                            
                                                                   
        if keys[pygame.K_RIGHT]:            
            collide=False
            current = self.x + self.speed            
            temp = self.image.get_rect(bottomright=(current,self.y))
            for r in Rectangles:
                if collide==True:
                    break                            
                if r.x > self.x-self.x_size:
                    if pygame.Rect.colliderect(temp, r.rect)==1:
                        self.x = r.x
                        collide=True
            if collide==False:
                self.x = current
            if self.rect.left>=WIDTH:
                Rectangles.clear()
                Coins.clear()
                self.map.build()
                self.x = 0
            self.coin_check()                                  
                
        if keys[pygame.K_RETURN] and self.can_jump==True:
            L = []
            for r in Rectangles:
                # blocks above you when you're not on the floor
                if self.floor != None:
                    if self.x >r.x and self.x-self.x_size< r.x + r.width:
                        if r.y <self.floor:
                            L.append(r)
                elif self.floor==None:
                    # blocks above you when on the floor
                    if self.x >r.x and self.x-self.x_size< r.x + r.width:
                        L.append(r)           
                                  
            Lowest = 0
            for r in L:
                if r.y>=Lowest:
                    Lowest = r.y 
            for r in L:
                if r.y == Lowest:                                        
                    if r.y +r.height >= self.y - self.JUMP:
                        self.y = r.y + r.height+self.y_size 
                        self.can_jump=False
                        # Blocked by the bottom of the block in your way
                        return  
            # Can make full jump            
            self.y -= self.JUMP
            self.can_jump=False
            self.coin_check()
            if self.y<=-300:
                Rectangles.clear()
                Coins.clear()
                self.map.build()
                self.y = FLOOR
            return        
                     
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

class Coin:
    def __init__(self,x,y,width,height):
        self.x = x 
        self.y = y
        self.width=width
        self.height=height
        self.image = pygame.image.load('COIN.png').convert_alpha()
        
        self.image.set_colorkey(BG_Color)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(midbottom=(self.x,self.y))        
        self.colors = ['red', 'blue', 'green']
        Coins.append(self)
    def blit(self):
        screen.blit(self.image,self.rect)

class Map:
    def __init__(self, count):
        self.count = count
        self.x_locs = [50*x for x in range(2,13,2)]
        self.y_locs = [50*y for y in range(2,12,2)]
        self.colors = ['red', 'blue', 'green', 'orange']
        
    def build(self):
        # TODO
        # Smarter mapping function for better level creation
        tiles = []
        for _ in range(self.count):
            used = False
            while used==False:
                x_loc = self.x_locs[random.randint(0,len(self.x_locs)-1)]
                y_loc = self.y_locs[random.randint(0,len(self.y_locs)-1)]
                loc = x_loc,y_loc
                if loc not in tiles:
                    tiles.append(loc)
                    used=True
        for x in tiles:
            RECT(self.colors[random.randint(0,len(self.colors)-1)], x[0], x[1], 100,100)            
        for X in Rectangles:
            count = 0
            for other in Rectangles:
                if other.x == X.x:
                    if X.y -X.height==other.y:
                        count+=1
            if count ==0:
                chance = random.randint(0,3)
                if chance==3:
                    Coin(X.x+50,X.y, 50,50)            

#TODO Count counter display, meteor health display, more enemies 

for _ in range(5):
    Meteor()
P = Player(100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill(BG_Color)
    screen.blit(ground,(0,FLOOR))    
    for r in Rectangles:
        r.blit()
    for c in Coins:
        c.blit()    
    for meteor in Meteors:
        meteor.move()
        meteor.blit()    
    P.move()
    P.blit()

    pygame.display.update()
    clock.tick(60)