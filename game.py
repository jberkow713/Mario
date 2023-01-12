import pygame
from sys import exit
import copy
pygame.init()
# Globals
WIDTH=800
HEIGHT=400
Health = 100
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
        self.original = copy.deepcopy(x)
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

snails = [500,750]
for x in snails:
    Snail(x,5)

Game_Active = True
can_jump=True
T_0 = 0
while True:    
    if Game_Active==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if can_jump==True:
                if event.type == pygame.MOUSEBUTTONDOWN:            
                    # Jumping
                    player_rect.y -=100
                    can_jump = False
        
        screen.blit(sky, (0,0))
        screen.blit(ground,(0,300))
        Score = pygame.time.get_ticks()-T_0
        # Score  
        score_surface = test_font.render(f'Score:{Score//1000}',False, 'Black')
        score_rect_1 = score_surface.get_rect(center=(100, 25))
        pygame.draw.rect(screen, 'Pink', score_rect_1)
        screen.blit(score_surface, score_rect_1)
        # Health
        score_surface_2 = test_font.render(f'Health:{Health}',False, 'Black')
        score_rect_2 = score_surface_2.get_rect(center=(700, 25))
        pygame.draw.rect(screen, 'Pink', score_rect_2)
        screen.blit(score_surface_2, score_rect_2)        
        # Snail Movement
        for snail in Snails:
            snail.blit()
            snail.move()
            if player_rect.right<=WIDTH and snail.rect.right<=WIDTH:
                if player_rect.colliderect(snail.rect):
                    Health-=1
                    if Health <=0:
                        Game_Active=False                      
        # Player Movement
        if player_rect.bottom <300:
            player_rect.y +=5    
        if player_rect.bottom>=300:
            can_jump=True
            player_rect.bottom = 300   
        player_rect.left +=5    
        if player_rect.left>=WIDTH:
            player_rect.right = 0
        screen.blit(player, player_rect)
    #Game Over/Reset Screen 
    else:        
        screen.fill('Blue')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                T_0 =pygame.time.get_ticks()
                Game_Active=True
                Health=100
                player_rect.x = 80
                for snail in Snails:
                    snail.rect = snail.image.get_rect(bottomright=(snail.original,300))
                    snail.blit()                                        
    pygame.display.update()
    clock.tick(60)     