import pygame
import random
from sys import exit
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

class Player:
    def __init__(self, x):
        self.x = x
        self.y = 700
        self.image = pygame.image.load('player_walk_1.png').convert_alpha()
        self.rect = self.image.get_rect(bottomright=(self.x,self.y))
        self.speed = 5
        self.can_jump=True
    def move(self):
        if self.can_jump==False:
            self.y +=5
            if self.y>=700:
                self.y = 700
                self.can_jump=True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -=self.speed
        if keys[pygame.K_RIGHT]:
            self.x +=self.speed
        if keys[pygame.K_RETURN] and self.can_jump==True:
            self.y-= 250
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
        self.image = pygame.transform.scale(self.image, (100, 75))
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
for _ in range(5):
    Meteor()
P = Player(100)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill(BG_Color)
    screen.blit(ground,(0,700))    
    for meteor in Meteors:
        meteor.move()
        meteor.blit()    
    P.move()
    P.blit()    
    pygame.display.update()
    clock.tick(60)