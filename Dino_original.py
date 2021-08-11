import pygame
from sys import exit
import random
from itertools import cycle


def Obstacles(obstacles_list):      
    if obstacles_list:                             #list with something inside
        for obstacle in obstacles_list:
            obstacle.x -= game_speed
            
            if obstacle.y < 429: #large_cactus.y > small_cactus.y
                SCREEN.blit(LARGE_SURFACE, obstacle)
            else:
                SCREEN.blit(SMALL_SURFACE, obstacle)
            
        obstacles_list = [obstacle for obstacle in OBSTACLE_LIST if obstacle.x > -100]
        
        return obstacles_list
    else:
        return []
    
def collisions(player, obstacle_list):
    if obstacle_list:                             #list with something inside
        for obstacle in obstacle_list:
            if player.colliderect(obstacle):      #test if two rectangles overlap
                return True

pygame.init()
pygame.display.set_caption("Dino") #function will change the name on the window.
clock = pygame.time.Clock() #create an object (Clock object) to help track time

#Game variable
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
game_speed = 20
gravity = 0
score = 0
game_font = pygame.font.Font('freesansbold.ttf', 20)  #create a new Font object from a file/object
menu_font = pygame.font.Font('freesansbold.ttf', 60)
game_active = True

#screen display
SCREEN = pygame.display.set_mode((1100,600)) #creates a new surface object that represents the game display

#Dino  (returns us a Surface with the image data)
RUN_1 = pygame.image.load('Dino/DinoRun1.png').convert_alpha()
RUN_2 = pygame.image.load('Dino/DinoRun2.png').convert_alpha()
RUN = [RUN_1, RUN_2]
RUN_INDEX = 0
RUN_SURFACE = RUN[RUN_INDEX] #init game with index 0 = RUN_1
RUN_RECT = RUN_SURFACE.get_rect(midbottom = (80,515))

JUMP = pygame.image.load('Dino/DinoJump.png').convert_alpha()


#Obstacles
LARGE_CACTUS_1 = pygame.image.load('Dino/LargeCactus1.png').convert_alpha()
LARGE_CACTUS_2 = pygame.image.load('Dino/LargeCactus2.png').convert_alpha()
LARGE_CACTUS_3 = pygame.image.load('Dino/LargeCactus3.png').convert_alpha()

LARGE_CACTUS = [LARGE_CACTUS_1, LARGE_CACTUS_2, LARGE_CACTUS_3]
LARGE_SURFACE = LARGE_CACTUS[random.randint(0,2)]

SMALL_CACTUS_1 = pygame.image.load('Dino/SmallCactus1.png').convert_alpha()
SMALL_CACTUS_2 = pygame.image.load('Dino/SmallCactus2.png').convert_alpha()
SMALL_CACTUS_3 = pygame.image.load('Dino/SmallCactus3.png').convert_alpha()

SMALL_CACTUS = [SMALL_CACTUS_1, SMALL_CACTUS_2, SMALL_CACTUS_3]
SMALL_SURFACE = SMALL_CACTUS[random.randint(0,2)] #init game with index 0 = RUN_1

OBSTACLE_LIST = []

#Background
TRACK = pygame.image.load('Dino/Track.png').convert_alpha()
TRACK_x_pos = 0
TRACK_y_pos = 500

#Timer event
obstacle_timer = pygame.USEREVENT + 0   #custom events to increase the level of control and flexibility we have over our game.
pygame.time.set_timer(obstacle_timer, 1200) #event repeated periodically after the specified time interval.
#time should be add to not notice changes of images in game

while True:
       
    #game events
    for event in pygame.event.get(): #none = eventlist
        if event.type == pygame.QUIT:
            pygame.quit
            exit()
        
        if game_active:
            if RUN_RECT.bottom == 515: #jump available when the dinosaur is on the ground
                   if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                           gravity = -20
                           
            if event.type == obstacle_timer:
                if random.randint(0,2):
                        LARGE_SURFACE = LARGE_CACTUS[random.randint(0,2)]
                        OBSTACLE_LIST.append(LARGE_SURFACE.get_rect(midbottom = (random.randrange(1200,1400),515)))
                else:
                        SMALL_SURFACE = SMALL_CACTUS[random.randint(0,2)]
                        OBSTACLE_LIST.append(SMALL_SURFACE.get_rect(midbottom = (random.randrange(1200,1400),515)))            
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                OBSTACLE_LIST = []
                score = 0
                 
    if game_active: 
        #Animation background
        TRACK_x_pos -= game_speed
        if TRACK_x_pos <= -TRACK.get_width():
           TRACK_x_pos = 0
           
        #background draw
        SCREEN.fill(WHITE)
        SCREEN.blit(TRACK, (TRACK_x_pos,TRACK_y_pos))
        SCREEN.blit(TRACK, (TRACK.get_width() + TRACK_x_pos,TRACK_y_pos))
        
        #player
        gravity += 1
        RUN_RECT.y += gravity
        if RUN_RECT.bottom >= 515: #player cant go pass the floor (due to gravity)
            RUN_RECT.bottom = 515
            
        #player animations
        if RUN_RECT.bottom < 515:
            RUN_SURFACE = JUMP
        else:
            RUN_INDEX += 0.1
            if RUN_INDEX >= len(RUN):
                RUN_INDEX = 0
            RUN_SURFACE = RUN[int(RUN_INDEX)]
        
        #obstacle
        OBSTACLE_LIST = Obstacles(OBSTACLE_LIST)
        
        if collisions(RUN_RECT, OBSTACLE_LIST):
            game_active = False
        
            
        #player draw
        SCREEN.blit(RUN_SURFACE, RUN_RECT)
        
        #score
        score += 1
        if score % 100 == 0:
            game_speed += 1
        game_text = game_font.render(f'Score: {score}', True, BLACK)
        SCREEN.blit(game_text, (900, 50))  
    
    else: 
        #menu
        SCREEN.fill(WHITE)
        menu_text = menu_font.render('DINO', True, BLACK)
        SCREEN.blit(menu_text, menu_text.get_rect(center = (550, 100)))
        JUMP_MENU = pygame.transform.scale2x(pygame.image.load('Dino/DinoJump.png').convert_alpha())
        SCREEN.blit(JUMP_MENU, JUMP_MENU.get_rect(center = (550, 300)))
        on_text_surface = game_font.render('PRESS SPACE TO START', True, BLACK)
        SCREEN.blit(on_text_surface, on_text_surface.get_rect(center = (550, 500)))
    
    clock.tick(60) #(frames per second).
    pygame.display.update() #Update portions of the screen for software displays
            

