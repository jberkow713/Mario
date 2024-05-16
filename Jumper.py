import pygame
import random
from sys import exit
from pygame.locals import  *
import copy
pygame.init()

WIDTH=1000
HEIGHT=800
FLOOR=700
BG_Color = (64,124,200)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font('font.ttf',50)
pygame.display.set_caption('Jumper')
clock = pygame.time.Clock()
gaps = []
ground = []

class Ground:
    def __init__(self, start, end, y):
        self.start = start        
        self.end = end
        self.y = y 
        self.size = self.end-self.start 
        gaps.append([self.start,self.end, self.y])
        self.image = pygame.image.load('ground.png')
        self.image = pygame.transform.scale(self.image, (self.size,100))
        self.rect = self.image.get_rect(topleft=(self.start,self.y ))
        ground.append(self)

    def blit(self):
        screen.blit(self.image,self.rect)
class Player:
    # Character Movement, collision detection, etc.
    def __init__(self, x,y):
        self.x = x
        self.start_x = copy.deepcopy(self.x)
        self.y = y
        self.x_size = 75
        self.y_size = 75
        self.speed = 10
        self.can_jump=True
        self.image = pygame.image.load('mario.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (75,75))
        self.rect = self.image.get_rect(bottomleft=(self.x,self.y))
        self.lives = 5
        self.last_key = None
    
    def blit(self):
        screen.blit(self.image,self.rect)

    def move(self):
        if self.rect.y >HEIGHT:
            self.lives -=1            
            self.rect.x,self.rect.y = self.start_x,FLOOR-self.y_size 
            self.curr_gap = 0          
            
            if self.lives == 0:
                print('game over')
                pygame.quit()
                exit()
            return          
        
        count = 0
        for val in gaps:
            if self.last_key !='l':
                v0,v1,v2 = val[0],val[1],val[2]
            else:
                v0,v1,v2 = val[0]-self.x_size,val[1]-self.x_size,val[2]    
            if self.rect.x >= v0 and self.rect.x <=v1:
                if self.can_jump==False:
                    self.rect.y +=10
                    if self.rect.y>=val[2]-self.y_size:
                        self.can_jump=True
                        self.rect.y=val[2]-self.y_size 
                
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.rect.x -= self.speed
                    self.last_key = 'l'                    
                    if self.rect.x<0:                
                        self.rect.x = 0           
                    
                if keys[pygame.K_RIGHT]:
                    self.rect.x +=self.speed
                    self.last_key = 'r'
                    if self.rect.x>WIDTH:                
                        self.rect.x = -self.x_size

                if keys[pygame.K_RETURN] and self.can_jump==True:
                    self.rect.y-=300
                    self.can_jump=False
                return           
            else:
                count +=1
                
        if count ==len(gaps):            
            self.rect.y +=10
            if self.last_key == 'r':
                self.rect.x +=self.speed
            elif self.last_key == 'l':
                self.rect.x -=self.speed               
           
class Level:
    def __init__(self, grounds):        
        self.ground = grounds
        
    def blit(self):
        for ground in self.ground:
            ground.blit()
        

P = Player(0,500)
L = Level([Ground(0,300,P.y), Ground(500,800,600)])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill(BG_Color)
    # L.rebuild()
    L.blit()
    P.move()
    P.blit()
    
    pygame.display.update()
    clock.tick(60)    