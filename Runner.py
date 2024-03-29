import pygame
import random
from sys import exit
from pygame.locals import  *
import copy
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
Items = []
Enemies = []
Level = 0

class Player:
    # Character Movement, collision detection, etc.
    def __init__(self, x):
        self.x = x
        self.y = FLOOR
        self.x_size = 75
        self.y_size = 75
        self.image = pygame.image.load('toadette.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (75,75))
        self.rect = self.image.get_rect(bottomright=(self.x,self.y))        
        self.speed = 5
        self.floor = None
        self.can_jump=True
        self.JUMP = 400        
        self.gravity = 10
        self.map = Map(15)
        self.map.build()
        self.coins = 0
        self.health = 100
        self.direction = 'right'
        self.weapon = Weapon()
        self.defeated = []
        self.jump_range=None        
    
    def add_enemies(self):
        Enemies.clear()

        e = [(x*200)-self.x for x in range(2,6)]
        for i in range(4):
            x = e[i] 
            Snail(x,self)  

    def Item_check(self,jump=False):
        if jump==True:
            for item in Items:
                for y in range(self.jump_range[0],self.jump_range[1],25):
                    
                    self.rect = self.image.get_rect(bottomright=(self.x,y))
                    if pygame.Rect.colliderect(self.rect, item.rect)==1:                        
                        
                        if item.type=='Heart':
                            self.health +=10
                        elif item.type=='Coin':
                            self.coins +=1
                        Items.remove(item)
                        break
            return            
        elif jump==False:
            for item in Items:
                if pygame.Rect.colliderect(self.rect,item.rect)==1:
                    Items.remove(item)
                    if item.type=='Heart':
                        self.health +=10
                    elif item.type=='Coin':
                        self.coins +=1    

    def move(self):
        if self.can_jump==True and self.floor!=None:
            count = 0
            temp = self.image.get_rect(bottomright=(self.x,self.y+self.gravity))
            for r in Rectangles:
                if pygame.Rect.colliderect(temp, r.rect)==0:
                    count+=1
            if count==len(Rectangles):
                self.y+=self.gravity
                self.Item_check()
                if self.y !=FLOOR:
                    self.floor = self.y
                    # self.can_jump=False
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
                    self.Item_check()
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
                Items.clear()
                self.map.build()
                self.add_enemies()
                self.x = WIDTH+self.x_size
            self.direction = 'left'    
            self.Item_check()                                          
                                                                   
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
                Items.clear()
                self.map.build()
                self.add_enemies()
                self.x = 0
            self.direction='right'    
            self.Item_check()                               
               
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
                        self.jump_range = (r.y+r.height+self.y_size,self.y)            
                        self.Item_check(jump=True)
                        self.y = r.y + r.height+self.y_size 
                        self.can_jump=False
                        # Blocked by the bottom of the block in your way
                        return  
            # Can make full jump
            self.jump_range = (self.y-self.JUMP,self.y)            
            self.Item_check(jump=True)
            self.y -= self.JUMP
            self.can_jump=False
            
            if self.y<=-300:
                Rectangles.clear()
                Items.clear()
                self.map.build()
                self.add_enemies()
                self.health +=20
                global Level 
                Level +=1
                self.y = FLOOR
            return                       
            
        if keys[pygame.K_SPACE]:            
            if self.direction=='right':
                self.weapon.blit('right',self.x+self.x_size-15,self.y+15)
            else:
                self.weapon.blit('left',self.x-self.x_size+15, self.y+15)                
            for block in Rectangles:
                if self.weapon.sword_rect_offset.colliderect(block.rect):
                    Rectangles.remove(block)
            for enemy in Enemies:
                if self.weapon.sword_rect.colliderect(enemy.rect):
                    enemy.health-=1
                    if enemy.health<1:
                        Enemies.remove(enemy)
                        c = random.randint(0,5)                        
                        if c==0:
                            Item(enemy.x,700,'Coin')
                        elif c==1:                            
                            Item(enemy.x,700,'Heart')
                         
                    if self.direction == 'right':
                        enemy.rect.x +=150
                    elif self.direction =='left':
                        enemy.rect.x -=150                                     
                    enemy.blit()                   
        self.rect = self.image.get_rect(bottomright=(self.x,self.y)) 

    def blit(self):
        screen.blit(self.image,self.rect)             

class Weapon:
    def __init__(self):
        self.left = pygame.image.load('Sword_Left.jpg').convert_alpha()
        self.left = pygame.transform.scale(self.left, (75,75))
        self.left.set_colorkey('white')
        self.right = pygame.image.load('Sword_Right.png').convert_alpha()
        self.right = pygame.transform.scale(self.right, (75,75))
        self.sword_rect = None
        self.sword_rect_offset = None
        # self.right.set_colorkey('white')
    def blit(self, direction,x,y):
        if direction == 'left':
            sword_rect = self.left.get_rect(bottomright=(x,y))
            offset = self.left.get_rect(bottomright=(x,y-37))
            screen.blit(self.left, sword_rect)
        else:
            sword_rect = self.right.get_rect(bottomright=(x,y))
            offset = self.right.get_rect(bottomright=(x,y-37))
            screen.blit(self.right,sword_rect)
        self.sword_rect = sword_rect
        self.sword_rect_offset = offset
        
        return
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

class Item:
    def __init__(self,x,y,type):
        self.x = x 
        self.y = y
        self.type = type
        self.type_dict = {'Heart':'Heart.png', 'Coin':'COIN.png'}
        self.create_image()
        self.rect = self.image.get_rect(midbottom=(self.x,self.y))        
        self.colors = ['red', 'blue', 'green']
        Items.append(self)
    def blit(self):
        screen.blit(self.image,self.rect)
    def create_image(self):
        self.image = pygame.image.load(self.type_dict[self.type])
        self.image = pygame.transform.scale(self.image, (50, 50))

class Map:
    def __init__(self, count):
        self.count = count
        self.x_locs = [50*x for x in range(2,13,2)]
        self.y_locs = [50*y for y in range(2,11,2)]
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
                if chance==2:
                    Item(X.x+50,X.y,'Coin')
                elif chance==3:
                    Item(X.x+50,X.y,'Heart')            
class Snail:
    def __init__(self, x, Player):
        self.x = x
        self.original = copy.deepcopy(x)
        self.speed = 2 + Level//5
        self.image = pygame.image.load('snail1.png').convert_alpha()
        self.rect = self.image.get_rect(bottomright=(self.x,700))
        Enemies.append(self)
        self.Player = Player
        self.health = 4
    def blit(self):
        screen.blit(self.image,self.rect)        
    def move(self):
        if self.Player.y ==700:
            if self.rect.x >= self.Player.x:
                self.rect.x -= self.speed
                if self.rect.right <=0:
                    self.rect.left = WIDTH
                self.x = self.rect.x
            elif self.rect.x <=self.Player.x:
                self.rect.x +=self.speed 
                if self.rect.left >=WIDTH:
                    self.rect.right = 0
                self.x = self.rect.x
        else:
            self.rect.x -=self.speed 
            if self.rect.right <=0:
                self.rect.left = WIDTH
            self.x = self.rect.x
                                
        if self.Player.rect.right<=WIDTH and self.rect.right<=WIDTH:
            if self.Player.rect.colliderect(self.rect):
                self.Player.health-=1
                if self.Player.health <=0:
                    print('Game Over')
                    exit()
P = Player(100)
snails = [200,400,600,750]
for x in snails:
    Snail(x,P)
#TODO Count counter display, health display, more enemies 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill(BG_Color)
    screen.blit(ground,(0,FLOOR))    
    for r in Rectangles:
        r.blit()
    for i in Items:
        i.blit()
    for snail in Enemies:
        snail.blit()
        snail.move()        
    P.move()
    P.blit()
    
    score_surface_1 = font.render(f'Health:{P.health}',False, 'Black')
    score_rect_1 = score_surface_1.get_rect(center=(75, 25))
    screen.blit(score_surface_1, score_rect_1)
    score_surface_2 = font.render(f'Level:{Level}',False, 'Black')
    score_rect_2 = score_surface_2.get_rect(center=(400, 25))
    screen.blit(score_surface_2, score_rect_2)
    score_surface_3 = font.render(f'Coins:{P.coins}',False, 'Black')
    score_rect_3 = score_surface_3.get_rect(center=(700, 25))
    screen.blit(score_surface_3, score_rect_3)
    pygame.display.update()
    clock.tick(60)