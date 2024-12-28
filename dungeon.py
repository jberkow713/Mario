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
        buffer = self.rect[2]/2                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.rect.center[0]>buffer:
                self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            if self.rect.center[0] +buffer<SCREEN_WIDTH:
                self.rect.x +=self.speed
        if keys[pygame.K_UP]:
            if self.rect.center[1]>buffer:
                self.rect.y -=self.speed
        if keys[pygame.K_DOWN]:
            if self.rect.center[1]+buffer < SCREEN_HEIGHT:
                self.rect.y +=self.speed                                 

p = Player(200,200)

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