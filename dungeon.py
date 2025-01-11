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

Speed_multiplier = 1
Enemies = []
Coins= []
Lasers = []

def create_coins(num):
    for _ in range(num):
        Coin(random.randint(50,SCREEN_WIDTH-50), random.randint(50,SCREEN_HEIGHT-50))
    return

def create_enemies(num):
    Enemies.clear()
    for _ in range(num):
        speed = random.randint(4,7)*Speed_multiplier
        size = random.randint(25,50)
        Enemy((size,size),random.randint(int(size*1.5),int(SCREEN_HEIGHT-(1.5*size))), random.randint(size,SCREEN_WIDTH-size), speed)
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
        self.Laser_reset = 0
        self.can_hit = True
        self.can_shoot = True
        self.coins = 0
        self.total_coins = 0
        self.dir = None
        self.coin = pygame.mixer.Sound('coin_s.mp3')
        self.coin.set_volume(0.3)  
        create_enemies(random.randint(5,10))
            
    def clock_reset(self):
        self.hit_reset+=1
        if self.hit_reset == 15:
            self.can_hit = True
            self.hit_reset = 0
    
    def laser_reset(self):
        self.Laser_reset+=1
        if self.Laser_reset == 25:
            self.can_shoot = True
            self.Laser_reset = 0        
    
    def display_health(self):
        font = pygame.font.SysFont("comicsans", 40, True)    
        text = font.render(f'Health: {self.health}', 1, (255,0,0)) 
        screen.blit(text, (750, 0))
    
    def display_coins(self):
        font = pygame.font.SysFont("comicsans", 40, True)    
        text = font.render(f'Coins: {self.coins}', 1, (255,0,0)) 
        screen.blit(text, (250, 0))
    
    def blit(self):
        self.display_coins()
        self.display_health()
        pygame.draw.rect(screen, (255,0,0), self.rect)
    
    def shoot_laser(self):
        self.can_shoot = False
        mid = self.rect[2] / 2 
        if self.dir == None:
            Laser((self.x+mid,self.y),5,'u')
        else:
            mid_down = self.rect[3]/2
            if self.dir == 'l':                 
                Laser((self.rect.x,self.rect.y+mid_down),5,self.dir)
            if self.dir == 'r':
                Laser((self.rect.x+self.rect[2],self.rect.y+mid_down),5,self.dir)

            if self.dir =='d':
                Laser((self.rect.x + mid,self.rect.y + self.rect[3]),5,self.dir)
            if self.dir == 'u':
                Laser((self.rect.x + mid, self.rect.y), 5, self.dir)

    def move(self):
        if self.total_coins == 10:
            global Speed_multiplier
            Speed_multiplier +=.1
            create_enemies(random.randint(5,15))
            self.total_coins=0
        
        if self.can_hit == False:
            self.clock_reset()
        
        if self.can_shoot == False:
            self.laser_reset()
        
        for c in Coins:
            if p.rect.colliderect(c.rect):
                Coins.remove(c)
                self.coins +=1
                self.total_coins +=1
                self.health +=10
                self.coin.play()

        for e in Enemies:
            if p.rect.colliderect(e.rect):
                if self.can_hit == True:
                    self.health -=10
                    self.health = max(0,self.health)
                    self.can_hit = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            spot = self.rect.left - self.speed
            if spot>0:
                self.rect.x -= self.speed
            else:
                self.rect.left = 0
            self.dir = 'l'    
        if keys[pygame.K_RIGHT]:
            spot = self.rect.right + self.speed
            if spot<SCREEN_WIDTH:
                self.rect.x +=self.speed
            else:
                self.rect.right = SCREEN_WIDTH
            self.dir = 'r'       
        if keys[pygame.K_UP]:
            spot = self.rect.top - self.speed
            if spot>25:
                self.rect.y -=self.speed
            else:
                self.rect.top = 25
            self.dir = 'u'         
        if keys[pygame.K_DOWN]:
            spot = self.rect.bottom + self.speed
            if spot < SCREEN_HEIGHT:
                self.rect.y +=self.speed
            else:
                self.rect.bottom = SCREEN_HEIGHT
            self.dir = 'd'
        if keys[pygame.K_SPACE]:
            if self.can_shoot==True:
                self.shoot_laser()                                               
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

class Laser():
    def __init__(self,pos,speed,dir):
        if dir == 'u' or dir == 'd':
            POS = 6,25
        else:
            POS = 25,6    
        self.rect = pygame.Rect(0,0,POS[0],POS[1])
        self.rect.center = pos
        self.colors = [(255,0,0), (0,255,0), (0,0,255)]
        self.color = random.choice(self.colors)
        self.speed = speed
        self.dir = dir
        self.laser = pygame.mixer.Sound('audio_laser.wav')
        self.laser.set_volume(0.3)
        self.explosion = pygame.mixer.Sound('explosion.wav')
        self.explosion.set_volume(0.3)  
        Lasers.append(self)
        self.laser.play()
    
    def blit(self):
        pygame.draw.rect(screen, self.color, self.rect)
    
    def move(self):
        if self.dir == 'u':
            self.rect.y -= self.speed
        if self.dir == 'd':
            self.rect.y +=self.speed 
        if self.dir == 'r':
            self.rect.x +=self.speed 
        if self.dir == 'l':
            self.rect.x -=self.speed 

        if self.rect.y <0 or self.rect.y > SCREEN_HEIGHT \
            or self.rect.x <0 or self.rect.x > SCREEN_WIDTH:
            if self in Lasers:
                Lasers.remove(self)

        for e in Enemies:
            if self.rect.colliderect(e.rect):
                Enemies.remove(e)
                self.explosion.play()
                if self in Lasers:
                    Lasers.remove(self)
class Enemy:
    def __init__(self, size,x,y,speed):
        self.rect = pygame.Rect(0,0,size[0],size[1])
        self.rect.center = (x,y)
        self.x = x 
        self.y = y
        self.speed = speed
        self.dirs = ['u','d','l','r']
        self.colors = [(240,0,255), (0,255,0), (0,0,255)]
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
        if self.dir == 'u':
            spot = self.rect.top - self.speed
            if spot>25:
                self.rect.y -=self.speed 
            else:
                self.rect.top = self.rect[3]
                self.dir = 'd'
        if self.dir == 'd':
            spot = self.rect.bottom + self.speed
            if spot < SCREEN_HEIGHT:
                self.rect.y +=self.speed
            else:
                self.rect.bottom = SCREEN_HEIGHT-self.rect[3]
                self.dir = 'u'
        if self.dir == 'r':
            spot = self.rect.right + self.speed
            if spot<SCREEN_WIDTH:
                self.rect.x +=self.speed
            else:
                self.rect.right = SCREEN_WIDTH-self.rect[2]
                self.dir = 'l'
        if self.dir == 'l':
            spot = self.rect.left - self.speed
            if spot>0:
                self.rect.x -= self.speed
            else:
                self.rect.left = self.rect[2]
                self.dir = 'r'

p = Player(207,207)
Run = True 

while Run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or p.health<=0:
            Run=False 
    screen.fill(BG_Color)
    if Coins == []:
        create_coins(2)
    p.move()
    p.blit()
    
    for l in Lasers:
        l.move()
        l.blit()
    for coin in Coins:
        coin.blit()
    for E in Enemies:
        E.move()
        E.blit()
     
    pygame.display.update()
    clock.tick(60)    

pygame.quit()    