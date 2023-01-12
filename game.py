import pygame
from sys import exit
pygame.init()

WIDTH=800
HEIGHT=400
Score = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Runner')

clock = pygame.time.Clock()
sky = pygame.image.load('Sky.png').convert()
ground = pygame.image.load('ground.png').convert()

test_font = pygame.font.Font('font.ttf',50)
score_surface = test_font.render(f'My Game',False, 'Black')
score_rect = score_surface.get_rect(center=(WIDTH/2, 50))

player = pygame.image.load('player_walk_1.png').convert_alpha()
player_rect = player.get_rect(midbottom=(80,300))

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
        self.span = (self.rect.left,self.rect.right)
        self.size = self.rect.right-self.rect.left
    def blit(self):
        screen.blit(self.image,self.rect)    
    def move(self):
        self.rect.x -= self.speed
        if self.rect.right <=0:
            self.rect.left = WIDTH

snails = [500]
for s in snails:
    Snail(s,5)

start_x = None
end_x = None
jumped_snail = None 

while True:    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.blit(sky, (0,0))
    screen.blit(ground,(0,300))
    pygame.draw.rect(screen, 'Pink', score_rect)
    screen.blit(score_surface, score_rect)
    
    screen.blit(player, player_rect)
    
    for snail in Snails:
        snail.blit()
        snail.move()
        
    if contact_flag==True:
        if event.type == pygame.MOUSEBUTTONUP:
            player_rect.bottom +=50
            end_x = player_rect.left
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
            start_x = player_rect.right
            player_rect.bottom-=50
            contact_flag=True 

    pygame.display.update()
    clock.tick(60)