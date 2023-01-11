import pygame
from sys import exit
pygame.init()

WIDTH=800
HEIGHT=400

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Runner')

clock = pygame.time.Clock()
sky = pygame.image.load('Sky.png').convert()
ground = pygame.image.load('ground.png').convert()
# snail = pygame.image.load('snail1.png').convert_alpha()
player = pygame.image.load('player_walk_1.png').convert_alpha()

player_rect = player.get_rect(midbottom=(80,300))
# snail_rect = snail.get_rect(bottomright=(725,300))
test_font = pygame.font.Font('font.ttf',50)
text_surface = test_font.render('My game', False, 'Blue')
contact_flag=False
Lives = 50
Snails = []

class Snail:
    def __init__(self, x,speed):
        self.x = x
        self.speed = speed
        self.image = pygame.image.load('snail1.png').convert_alpha()
        self.rect = self.image.get_rect(bottomright=(self.x,300))
        Snails.append(self)
    def blit(self):
        screen.blit(self.image,self.rect)    
    def move(self):
        self.rect.x -= self.speed
        if self.rect.right <=0:
            self.rect.left = WIDTH 

snails = [350,700]
for s in snails:
    Snail(s,5)
    
while True:    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.blit(sky, (0,0))
    screen.blit(ground,(0,300))
    screen.blit(text_surface,(300,50))
    screen.blit(player, player_rect)
    
    for snail in Snails:
        snail.blit()
        snail.move()
        
    if contact_flag==True:
        if event.type == pygame.MOUSEBUTTONUP:
            player_rect.bottom +=50
            contact_flag=False
        
    player_rect.left +=5
    if player_rect.left>=WIDTH:
        player_rect.right = 0    
    
    for snail in Snails:
        if player_rect.right<=WIDTH and snail.rect.right<=WIDTH:
            if player_rect.colliderect(snail.rect):
                Lives -=1

    if Lives ==0:
        print('you lose')
        exit()    
    # if player_rect.collidepoint(mouse_pos):

    mouse_pos = pygame.mouse.get_pos()
    if contact_flag==False:

        if event.type == pygame.MOUSEBUTTONDOWN:        
            player_rect.bottom-=50
            contact_flag=True
            
    

    pygame.display.update()
    clock.tick(60)