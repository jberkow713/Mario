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
    def __init__(self, start, size):
        self.start = start        
        self.size=size
        gaps.append((self.start,self.start+self.size))
        self.image = pygame.image.load('ground.png')
        self.image = pygame.transform.scale(self.image, (self.size,100))
        self.rect = self.image.get_rect(topleft=(self.start,700))
        ground.append(self)

    def blit(self):
        screen.blit(self.image,self.rect)
class Player:
    # Character Movement, collision detection, etc.
    def __init__(self, x):
        self.x = x
        self.y = FLOOR
        self.x_size = 75
        self.y_size = 75
        self.speed = 5
        self.can_jump=True
        self.image = pygame.image.load('mario.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (75,75))
        self.rect = self.image.get_rect(bottomleft=(self.x,self.y))
    
    def blit(self):
        screen.blit(self.image,self.rect)
    def move(self):

        if self.rect.y >HEIGHT:
            print('game over')
            pygame.quit()
            exit()

        for start,end in gaps:            
            if self.rect.x <start or self.rect.x>end:                
                self.rect.y +=10

        if self.can_jump==False:
            self.rect.y +=10
            if self.rect.y>=625:
                self.can_jump=True
                self.rect.y=625 
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            if self.rect.x<0:                
                self.rect.x = 0           
            
        if keys[pygame.K_RIGHT]:
            self.rect.x +=self.speed
            if self.rect.x>WIDTH:                
                self.rect.x = -self.x_size

        if keys[pygame.K_RETURN] and self.can_jump==True:
            self.rect.y-=300
            self.can_jump=False
            return
class Level:
    def __init__(self,player_x, g_size):
        self.player = Player(player_x)
        self.ground = Ground(0,g_size)
        print(gaps)
    def blit(self):
        self.ground.blit()
        self.player.move()
        self.player.blit()
    def rebuild(self):
        # Advanced build function insert here
        if self.player.rect.x>WIDTH-self.player.x_size:
            size = random.randint(800,1000)            
            self.ground = Ground(0,size)
            self.player.rect.x = 0    

L = Level(0,600)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill(BG_Color)
    L.rebuild()
    L.blit()
    
    pygame.display.update()
    clock.tick(60)    