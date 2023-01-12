import pygame
from sys import exit
pygame.init()

WIDTH=800
HEIGHT=400
Score = 0
Health = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Runner')

clock = pygame.time.Clock()
sky = pygame.image.load('Sky.png').convert()
ground = pygame.image.load('ground.png').convert()
test_font = pygame.font.Font('font.ttf',50)
player = pygame.image.load('player_walk_1.png').convert_alpha()
player_rect = player.get_rect(midbottom=(80,300))
# Enemy Storage
Snails = []

class Snail:
    def __init__(self, x,speed):
        self.x = x
        self.speed = speed
        self.image = pygame.image.load('snail1.png').convert_alpha()
        self.rect = self.image.get_rect(bottomright=(self.x,300))
        Snails.append(self)
        self.span = (self.rect.left,self.rect.right)
        self.size = self.rect.right-self.rect.left
    
    def blit(self):
        screen.blit(self.image,self.rect)    
    
    def move(self):
        self.rect.x -= self.speed
        if self.rect.right <=0:
            self.rect.left = WIDTH

snails = [500]
for x in snails:
    Snail(x,5)

can_jump=True
while True:    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if can_jump==True:
            if event.type == pygame.MOUSEBUTTONDOWN:            
                # Jumping
                player_rect.y -=80
                can_jump = False
    
    screen.blit(sky, (0,0))
    screen.blit(ground,(0,300))    
    score_surface = test_font.render(f'Health Left {Health}',False, 'Black')
    score_rect = score_surface.get_rect(center=(WIDTH/2, 50))
    pygame.draw.rect(screen, 'Pink', score_rect)
    screen.blit(score_surface, score_rect)    
    
    # Snails
    for snail in Snails:
        snail.blit()
        snail.move()
        if player_rect.right<=WIDTH and snail.rect.right<=WIDTH:
            if player_rect.colliderect(snail.rect):
                Health-=1
                if Health <=0:
                    print('Game Over')
                    exit()                       
    # Player
    if player_rect.bottom <300:
        player_rect.y +=3    
    if player_rect.bottom>=300:
        can_jump=True
        player_rect.bottom = 300   
    player_rect.left +=5    
    if player_rect.left>=WIDTH:
        player_rect.right = 0
    screen.blit(player, player_rect) 
    
    pygame.display.update()
    clock.tick(60)