import pygame
from sys import exit
from random import randint, choice

#score
def display_score(): 
    current_score = int(pygame.time.get_ticks()/1000) - start_time
    score = pixel_font.render(f'Score: {current_score}' ,False,(64,64,64))
    score_pos = score.get_rect(center = (400,50))
    win.blit(score,score_pos)
    return current_score

#obstacle movment
def obstacle_movement(obstacle_list):
	if obstacle_list:
		for obstacle_rect in obstacle_list:
			obstacle_rect.x -= 5

			if obstacle_rect.bottom == 300: win.blit(snail,obstacle_rect)
			else: win.blit(fly,obstacle_rect)

		obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

		return obstacle_list
	else: return []

#collisions
def collisions(player,obstacles):
	if obstacles:
		for obstacle_rect in obstacles:
			if player.colliderect(obstacle_rect): return False
	return True      

#player animation
def player_animation():
    global player, player_index
    if player_pos.bottom < 300:
        player = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):player_index = 0
        player = player_walk[int(player_index)]

pygame.init()

#window
win = pygame.display.set_mode((800, 400))
pygame.display.set_caption('First game')

#fonts
pixel_font = pygame.font.Font('font/Pixeltype.ttf', 50)


#import
sky = pygame.image.load('graphics/Sky.png')
ground = pygame.image.load('graphics/ground.png')
snail = pygame.image.load('graphics/snail/snail1.png')
player_walk1 = pygame.image.load('graphics/Player/player_walk_1.png')
player_walk2 = pygame.image.load('graphics/Player/player_walk_2.png')
player_jump = pygame.image.load('graphics/Player/jump.png')
stand_player = pygame.transform.scale2x(pygame.image.load('graphics/Player/player_stand.png'))
fly = pygame.image.load('graphics/Fly/Fly1.png')

#render
text = pixel_font.render('My Game',False,(111,196,169))
game_name = pixel_font.render('Pixel Runner',False,(111,196,169))
game_score = pixel_font.render('Press Space To Run',False,(111,196,169))

#vars
score = 0
start_time=0
game_active = False
clock = pygame.time.Clock()
obstacle_list = []
#player vars
player_gravity = 0
player_walk = [player_walk1,player_walk2]
player_index = 0
player = player_walk[player_index]

#get rect
player_pos = player.get_rect(midbottom = (80,300))
game_name_pos = game_name.get_rect(center = (400,60))
game_score_pos = game_score.get_rect(center = (400,340))
stand_player_pos = stand_player.get_rect(center = (400,200))


#timer
timer = pygame.USEREVENT + 1
pygame.time.set_timer(timer,1500)

#game loop
while True:
    #event loop
    for event in pygame.event.get():
        #exit button
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        #activesljhlas
        if game_active:
            
            #jump with mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_pos.bottom >= 300:
                    player_gravity = -20
            
            #jump with space button
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_pos.bottom >= 300:
                    player_gravity = -20
        
        #to rematch the game
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/1000)

        if event.type == timer and game_active:
            if randint(0,2):
                obstacle_list.append(snail.get_rect(bottomright = (randint(900,1100),300)))
            else:
                obstacle_list.append(fly.get_rect(bottomright = (randint(900,1100),210)))
    #active
    if game_active:
        win.blit(sky,(0,0))
        win.blit(ground,(0,300))

        score = display_score()

        #player
        player_gravity += 1
        player_pos.y += player_gravity
        if player_pos.bottom >= 300: player_pos.bottom = 300
        player_animation()
        win.blit(player,player_pos)
        
        

        #obstacle movement
        obstacle_list = obstacle_movement(obstacle_list)

        game_active = collisions(player_pos,obstacle_list)

    #main screen
    else:
        win.fill((94,129,162))
        win.blit(stand_player,stand_player_pos)
        obstacle_list.clear()
        player_pos.midbottom = (80,300)
        player_gravity = 0
        score_message = pixel_font.render(f'your score: {score}',False,(111,196,169))
        score_message_pos= score_message.get_rect(center = (400,330))
        
        win.blit(game_name,game_name_pos)
        
        if score == 0: win.blit(game_score, game_score_pos)
        else: win.blit(score_message,score_message_pos)
    
    pygame.display.update()
    clock.tick(60)