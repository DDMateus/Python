import pygame, sys, random

def draw_floor(): #dois floors para parecer movement
    screen.blit(floor_surface,(floor_x_pos,600))
    screen.blit(floor_surface,(floor_x_pos + 576,600))
    
def create_pipe():
    random_pipe_pos = random.choice(pipe_height) #para variar o tamanho dos pipes no eixo dos y
    bottom_new_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos - 200 ))
    return bottom_new_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5  #moving pipes to the left
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes #return a new list of pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 700:
            screen.blit(pipe_surface, pipe)
        else: #virar o pipe de cima ao contrario, False = no eixo do x, True = eixo y
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    global can_score
    for pipe in pipes: #para trabalhar com todos os rectangulos inside the list
        if bird_rect.colliderect(pipe):#verificar se o bird esta a colidir com o pipe
            death_sound.play()
            can_score = True
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 600: #colisao do passaro com o top or bottom
            can_score = True
            return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery)) #center y do previous rectangulo

    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface,score_rect)
        
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (288, 500))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score #porque é um local variable temos que devolver

def pipe_score_check():
    global score, can_score
    
    if pipe_list: #se a listar tiver alguma coisa
        for pipe in pipe_list: #check cada pipe
            if 95 < pipe.centerx < 105 and can_score: #se o pipe estiver na posição do bird, intervalo é melhor
                score += 1
                score_sound.play()
                can_score = False
            if pipe.centerx < 0:
                can_score = True
            

pygame.init() #inicia o pygame
clock = pygame.time.Clock() #clock object para limitar o framerate
screen = pygame.display.set_mode((576, 700)) #surface - tupple or list with 2 pieces of information, lenght and height of the screen
game_font = pygame.font.Font('sprites/04B_19.ttf',30)

#game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True



bg_surface = pygame.image.load('sprites/background-day.png').convert() #converte a imagem em file mais facil de ler para o pygame 
bg_surface = pygame.transform.scale2x(bg_surface) #double the size delevering a new surface

floor_surface = pygame.image.load('sprites/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0 #dar a impressão de que o chão está a mexer


bird_downflap = (pygame.image.load('sprites/bluebird-downflap.png').convert_alpha())
bird_midflap = (pygame.image.load('sprites/bluebird-midflap.png').convert_alpha())
bird_upflap = (pygame.image.load('sprites/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100,350))

BIRDFLAP = pygame.USEREVENT + 1  #another user event
pygame.time.set_timer(BIRDFLAP,200)

#bird_surface = pygame.image.load('sprites/bluebird-midflap.png').convert_alpha()
#bird_surface = pygame.transform.scale2x(bird_surface) 
#bird_rect = bird_surface.get_rect(center = (100,350)) #puts a renctangular around the surface

pipe_surface = pygame.image.load('sprites/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = [] #vamos por aqui varios rectangulos através de um timer
SPAWNPIPE = pygame.USEREVENT #event triggered by timer para criar varios pipes
pygame.time.set_timer(SPAWNPIPE, 1200) #trigger 1200 ms = 1.2 sec.
pipe_height = [300,400,500] #tamanho random que os pipes podem ter


game_over_surface = (pygame.image.load('sprites/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center =(288, 300))

flap_sound = pygame.mixer.Sound('audio/wing.wav')
death_sound = pygame.mixer.Sound('audio/hit.wav')
score_sound = pygame.mixer.Sound('audio/point.wav')
score_sound_countdown = 100

while True: #infinite loop para correr o jogo  
    
    for event in pygame.event.get(): #pygame looks for all events happening: closing window, moving mouse etc
        if event.type == pygame.QUIT: #VAMOS PROCURAR o evento de fechar a janela
            pygame.quit() #fecha o jogo mas dá erro, while loop continua
            sys.exit() #fechar completamente o codigo
        if event.type == pygame.KEYDOWN: #ver se toca em alguma key
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0 #disable the efect of gravity se nao o bird cai sempre com o acumular de gravity
                bird_movement -= 8 # sobe no eixo y
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False: #continuar a jogar
                game_active = True #ao recomeçar o bird continua a bater no pipe e acumula pipes
                pipe_list.clear() #reset pipes
                bird_rect.center = (100,350) #reset bird position
                bird_movement = 0 #reset se não acumula e chega um momento e só cai
                score = 0
                
            if event.type == BIRDFLAP:
                if bird_index < 2: #para nao dar erro e sair do tamanho da lista
                    bird_index += 1
                else:
                    bird_index = 0

                bird_surface, bird_rect = bird_animation() #rectangulos tem que ter o mesmo tamanho que a imagem, ou dá erro

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe()) #store new_pipe (rectangulos) nesta lista



    screen.blit(bg_surface,(0,0)) #colocar a imagem de background definida fora do loop

    if game_active:
        #bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement #mexe no y, para o bird cair
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)


        #pipes
        pipe_list = move_pipes(pipe_list) #mover os pipes da lista
        draw_pipes(pipe_list)

        #score
        pipe_score_check()
        score_display('main_game')
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')

    #floor
    floor_x_pos -= 1 #move to the left leva menos -1
    draw_floor()
    if floor_x_pos <= -576: #se acabar o floor
        floor_x_pos = 0 #reset floor 

    
    pygame.display.update() #draw on the screen tudo o que está no while loop
    clock.tick(120) #game nao corre mais de 60 fps (frame per second) mas pode correr menos

