import pygame
import pygame.display
import random  

pygame.init()
pygame.font.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
BG_Color = (64,124,200)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

Enemies = []
Coins= []
Lasers = []

Player = None

def create_coins(num):
    for _ in range(num):
        Coin(random.randint(25,SCREEN_WIDTH), random.randint(25,SCREEN_HEIGHT))
    return     
class Player:
    def __init__(self, x,y):
        self.rect = pygame.Rect(0,0,40,40)
        self.rect.center = (x,y)
        self.x = x 
        self.y = y
        self.speed = 5
        self.health = 100
        self.hit_reset = 0
        self.can_hit = True 
     
    def clock_reset(self):
        self.hit_reset+=1
        if self.hit_reset == 15:
            self.can_hit = True
            self.hit_reset = 0
    def display_health(self):
        font = pygame.font.SysFont("comicsans", 40, True)    
        text = font.render(f'Health: {self.health}', 1, (255,0,0)) 
        screen.blit(text, (750, 0))
    
    def blit(self):
        pygame.draw.rect(screen, (255,0,0), self.rect)
    
    def move(self):
        if self.can_hit == False:
            self.clock_reset()

        for c in Coins:
            if p.rect.colliderect(c.rect):
                Coins.remove(c)
                self.health +=10

        for e in Enemies:
            if p.rect.colliderect(e.rect):
                if self.can_hit == True:
                    self.health -=20
                    print(self.health)
                    self.can_hit = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            spot = self.rect.left - self.speed
            if spot>0:
                self.rect.x -= self.speed
            else:
                self.rect.left = 0
        if keys[pygame.K_RIGHT]:
            spot = self.rect.right + self.speed
            if spot<SCREEN_WIDTH:
                self.rect.x +=self.speed
            else:
                self.rect.right = SCREEN_WIDTH
        if keys[pygame.K_UP]:
            spot = self.rect.top - self.speed
            if spot>25:
                self.rect.y -=self.speed
            else:
                self.rect.top = 25   
        if keys[pygame.K_DOWN]:
            spot = self.rect.bottom + self.speed
            if spot < SCREEN_HEIGHT:
                self.rect.y +=self.speed
            else:
                self.rect.bottom = SCREEN_HEIGHT                                     
class Coin:
    def __init__(self, x,y):
        self.x = x 
        self.y =y 
        self.image = pygame.image.load('COIN.png')
        self.image = pygame.transform.scale(self.image, (25,25))
        self.rect = self.image.get_rect(bottomleft=(self.x,self.y))
        Coins.append(self)

    def blit(self):
        screen.blit(self.image,self.rect)    
class Enemy:
    def __init__(self, x,y):
        self.rect = pygame.Rect(0,0,25,25)
        self.rect.center = (x,y)
        self.x = x 
        self.y = y
        self.speed = random.randint(4,7)
        self.dirs = ['u','d','l','r']
        self.colors = [(255,0,0), (0,255,0), (0,0,255)]
        self.color = random.choice(self.colors)
        self.dir = random.choice(self.dirs)
        Enemies.append(self)
        
    def blit(self):
        pygame.draw.rect(screen, self.color, self.rect)
    
    def move(self):
        # dir changes
        other = random.choice([x for x in self.dirs if x!=self.dir])
        for e in Enemies:
            if e!= self:
                if self.rect.colliderect(e.rect):
                    self.dir = other
                    
        if random.randint(0,100)>98:
            self.dir = random.choice(self.dirs)
            self.speed = random.randint(2,4)
        if self.dir == 'u':
            spot = self.rect.top - self.speed
            if spot>25:
                self.rect.y -=self.speed
            else:
                self.rect.top = 25
                self.dir = 'd'
        if self.dir == 'd':
            spot = self.rect.bottom + self.speed
            if spot < SCREEN_HEIGHT:
                self.rect.y +=self.speed
            else:
                self.rect.bottom = SCREEN_HEIGHT
                self.dir = 'u'
        if self.dir == 'r':
            spot = self.rect.right + self.speed
            if spot<SCREEN_WIDTH:
                self.rect.x +=self.speed
            else:
                self.rect.right = SCREEN_WIDTH
                self.dir = 'l'
        if self.dir == 'l':
            spot = self.rect.left - self.speed
            if spot>0:
                self.rect.x -= self.speed
            else:
                self.rect.left = 0
                self.dir = 'r'

p = Player(207,207)


for _ in range(10):
    e = Enemy(random.randint(25,SCREEN_HEIGHT), random.randint(25,SCREEN_WIDTH))

run = True 
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False 
    screen.fill(BG_Color)
    if Coins == []:
        create_coins(2)
    
    p.move()
    p.blit()
    p.display_health()
    
    for coin in Coins:
        coin.blit()

    for E in Enemies:
        E.move()
        E.blit()
        
    pygame.display.update()
    clock.tick(60)    

pygame.quit()    