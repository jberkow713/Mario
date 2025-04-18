import pygame
import pygame.display
import random  

pygame.init()
pygame.font.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
BG_Colors = [(64,124,200), (255,255,255), (231,120,56)]
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

Speed_multiplier = 1
Enemies = []
Coins= []
Lasers = []
Objects = []

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

class Obj:
    def __init__(self, x,y,Type):
        self.x = x 
        self.y = y
        self.rect = pygame.Rect(0,0,40,40)
        self.rect.center = (x,y)
        self.type = Type
        self.color = random.choice([(255,0,0), (0,255,0), (0,0,255)])
        Objects.append(self)
    def blit(self):
        pygame.draw.rect(screen, self.color, self.rect)
        self.rect.y += 2
        font = pygame.font.SysFont("comicsans", 35, True)    
        text = font.render(self.type[0].upper(), 1, (255,255,255))
        x_sz = self.rect[2]/3 
        y_sz = self.rect[3]/3
        screen.blit(text, (self.rect.x+x_sz,self.rect.y+y_sz)) 
        if self.rect.y >SCREEN_HEIGHT:
            Objects.remove(self)

class Player:
    def __init__(self, x,y):
        self.index = 0
        self.color = self.find_idx()
        self.rect = pygame.Rect(0,0,40,40)
        self.rect.center = (x,y)
        self.x = x 
        self.y = y
        self.speed = 5
        self.health = 100
        self.Score = 0
        self.hit_reset = 0
        self.Laser_reset = 0
        self.can_hit = True
        self.can_shoot = True
        self.coins = 0
        self.total_coins = 0
        self.dir = None
        self.laser_type = 'normal'
        self.coin = pygame.mixer.Sound('coin_s.mp3')
        self.coin.set_volume(0.3)  
        create_enemies(random.randint(5,10))
    
    def find_idx(self):
        return BG_Colors[self.index % len(BG_Colors)] 

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
    
    def display_player(self):
        font = pygame.font.SysFont("comicsans", 35, True)    
        text = font.render('P', 1, (255,255,255))
        x_sz = self.rect[2]/3 
        y_sz = self.rect[3]/3
        screen.blit(text, (self.rect.x+x_sz,self.rect.y+y_sz)) 

    def display_health(self):
        font = pygame.font.SysFont("comicsans", 40, True)    
        text = font.render(f'Health: {self.health}', 1, (255,0,0)) 
        screen.blit(text, (800, 0))
    
    def display_coins(self):
        font = pygame.font.SysFont("comicsans", 40, True)    
        text = font.render(f'Coins: {self.coins}', 1, (255,0,0)) 
        screen.blit(text, (0, 0))
    
    def display_score(self):
        font = pygame.font.SysFont("comicsans", 40, True)
          
        text = font.render(f'Score: {self.Score}', 1, (255,0,0)) 
        screen.blit(text, (400, 0))    
        
    def blit(self):
        pygame.draw.rect(screen, (255,0,0), self.rect)
        self.display_coins()
        self.display_health()
        self.display_score()
        self.display_player()
    
    def shoot_laser(self):
        self.can_shoot = False
        mid = self.rect[2] / 2 
        if self.dir == None:
            Laser((self.x+mid,self.y),10,'u',self.laser_type,self )
        else:
            mid_down = self.rect[3]/2
            if self.dir == 'l':                 
                Laser((self.rect.x,self.rect.y+mid_down),10,self.dir,self.laser_type,self  )
            if self.dir == 'r':
                Laser((self.rect.x+self.rect[2],self.rect.y+mid_down),10,self.dir,self.laser_type,self  )

            if self.dir =='d':
                Laser((self.rect.x + mid,self.rect.y + self.rect[3]),10,self.dir,self.laser_type,self  )
            if self.dir == 'u':
                Laser((self.rect.x + mid, self.rect.y), 10, self.dir,self.laser_type,self  )

    def move(self):
        if self.total_coins == 10:
            self.index +=1
            self.color = self.find_idx() 
            global Speed_multiplier
            Speed_multiplier +=.1
            create_enemies(random.randint(5,15))
            self.total_coins=0
        
        if self.can_hit == False:
            self.clock_reset()
        
        if self.can_shoot == False:
            self.laser_reset()
        for o in Objects:
            if p.rect.colliderect(o.rect):
                Objects.remove(o)
                self.laser_type = o.type 

        for c in Coins:
            if p.rect.colliderect(c.rect):
                Coins.remove(c)
                self.Score +=1
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
    def __init__(self,pos,speed,dir,typ,player):
        if typ == 'normal':
            if dir == 'u' or dir == 'd':
                POS = 6,25
            else:                
                POS = 25,6
        elif typ == 'large':
            if dir == 'u' or dir == 'd':
                POS = 18,50
            else:                
                POS = 50,18
        elif typ =='super':
            if dir == 'u' or dir == 'd':
                POS = 36,75
            else:                
                POS = 75,36
        elif typ == 'giant':
            if dir == 'u' or dir == 'd':
                POS = 50,100
            else:                
                POS = 100,50
        self.player = player 
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
                self.player.Score +=1
                self.explosion.play()
                if self in Lasers:
                    Lasers.remove(self)
        for o in Objects:
            if self.rect.colliderect(o.rect):
                Objects.remove(o)
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
laser_types = ['large','super','normal','giant'] 

while Run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or p.health<=0:
            Run=False 
    screen.fill(p.color)
    if Coins == []:
        create_coins(2)
    p.move()
    p.blit()
    if len(Enemies)>0:
        if random.randint(0,100)>95 and len(Objects)==0:
            Obj(random.randint(40,SCREEN_WIDTH-40),40,random.choice(laser_types))

    for o in Objects:
        o.blit()
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