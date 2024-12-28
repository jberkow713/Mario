import pygame
import pygame.display 

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_Color = (64,124,200)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Dungeon Crawler')

class Player:
    def __init__(self, x,y):
        self.rect = pygame.Rect(0,0,40,40)
        self.rect.center = (x,y)
        self.x = x 
        self.y = y
        self.speed = 5
    def blit(self):
        pygame.draw.rect(screen, (255,0,0), self.rect)
    def move(self):
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
            if spot>0:
                self.rect.y -=self.speed
            else:
                self.rect.top = 0   
        if keys[pygame.K_DOWN]:
            spot = self.rect.bottom + self.speed
            if spot < SCREEN_HEIGHT:
                self.rect.y +=self.speed
            else:
                self.rect.bottom = SCREEN_HEIGHT                                     

p = Player(207,207)

run = True 
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False 
    screen.fill(BG_Color)
    p.move()
    p.blit()
    pygame.display.update()
    clock.tick(60)    

pygame.quit()    