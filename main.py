import pygame
from sys import exit
from random import randint
pygame.init()
def score_display():
    current_time=int(pygame.time.get_ticks()/1000)-start_time
    score_surf=test_font.render(f'Score:{current_time}',False,(255,64,64))
    score_rect=score_surf.get_rect(center=(400,80))
    screen.blit(score_surf,score_rect)
    return current_time
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for a in obstacle_list:
            a.x-=5
            if a.bottom==400:
                screen.blit(snail_surf,a)
            else:
                screen.blit(fly_surf, a)
        obstacle_list=[obstacle for obstacle in obstacle_list if obstacle.x>-100]
        return obstacle_list
    else:
        return []

def collisions(player,obstacles):
    if obstacles:
        for b in obstacles:
            if player.colliderect(b):
                return False

    return True


def player_animation():
    jump_sound=pygame.mixer.Sound('audio_jump.mp3')
    jump_sound.set_volume(0.1)
    global player_surf,player_index
    if player_rect.bottom<400:
        player_surf=player_jump
        jump_sound.play()

    else:
        player_index+=0.1
        if player_index>=2:player_index=0
        player_surf=player_walk[int(player_index)]

start_time=0
screen=pygame.display.set_mode((800,600))
pygame.display.set_caption('Runner')
clock=pygame.time.Clock()
test_font=pygame.font.Font(None,50)
sky_surf=pygame.image.load('desert.png').convert()
road_surf=pygame.image.load('road.png').convert()
text_surf=test_font.render('Snail Runner',False,(64,0,0))
text_rect=text_surf.get_rect(center=(400,80))
message_surf=test_font.render('Press Space to Play',False,(64,87,28))
message_rect=message_surf.get_rect(center=(400,300))

snail_frame1=pygame.image.load('snail_1.png').convert_alpha()
snail_frame2=pygame.image.load('snail_2.png').convert_alpha()
snail_frames=[snail_frame1,snail_frame2]
snail_index=0
snail_surf=snail_frames[snail_index]

fly_frame1=pygame.image.load('fly_1.png').convert_alpha()
fly_frame2=pygame.image.load('fly_2.png').convert_alpha()
fly_frames=[fly_frame1,fly_frame2]
fly_index=0
fly_surf=fly_frames[fly_index]

player_walk_1=pygame.image.load('player_walk_1.png').convert_alpha()
player_walk_2=pygame.image.load('player_walk_2.png').convert_alpha()
player_walk=[player_walk_1,player_walk_2]
player_index=0
player_jump=pygame.image.load('player_jump.png').convert_alpha()

player_surf=player_walk[player_index]
player_rect=player_surf.get_rect(midbottom=(300,400))
player_gravity=0
game_active=False
score=0
#timer
obstacle_timer=pygame.USEREVENT+1
pygame.time.set_timer(obstacle_timer,1500)
obstacle_rect_list=[]

snail_animation_timer=pygame.USEREVENT+2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer=pygame.USEREVENT+3
pygame.time.set_timer(fly_animation_timer,200)


while True:

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type==pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    if player_rect.bottom == 420:
                        player_gravity=-30
            if event.type==pygame.KEYDOWN:
               if event.key==pygame.K_SPACE:
                   if player_rect.bottom==420:
                        player_gravity=-30

        elif(event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE):
            game_active=True

            start_time=int(pygame.time.get_ticks()/1000)
        if game_active:
            if event.type==obstacle_timer :
                if randint(0,2):
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright=(randint(900,1100),400)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900,1100),300)))

            if event.type==snail_animation_timer:
                if snail_index==0:snail_index=1
                else:snail_index=0
                snail_surf=snail_frames[snail_index]
            if event.type==fly_animation_timer:
                if fly_index==0:fly_index=1
                else:fly_index=0
                fly_surf=fly_frames[fly_index]

    if game_active:
        score = score_display()

        screen.blit(sky_surf,(0,0))
        screen.blit(road_surf,(0,350))

        # screen.blit(snail_surface, snail_rect)
        # pygame.draw.rect(screen,(20,25,63),score_rect)
        # pygame.draw.rect(screen,(20,25,63),score_rect,20)
        # screen.blit(score_surface, score_rect)

        obstacle_rect_list=obstacle_movement(obstacle_rect_list)
        player_gravity+=1.1
        player_rect.y+=player_gravity
        if player_rect.bottom>=420:
            player_rect.bottom=420
        player_animation()
        screen.blit(player_surf,player_rect)

        score_display()
            # mouse_pos=pygame.mouse.get_pos()
            # if player_rect.collidepoint(mouse_pos):
            #     print(pygame.mouse.get_pressed())
        game_active = collisions(player_rect, obstacle_rect_list)


    else:
        obstacle_rect_list.clear()
        screen.fill((0,0,64))
        screen.blit(text_surf,text_rect)

        if score==0:
            screen.blit(message_surf,message_rect)

        else:
            score_message = test_font.render(f"score:{score}", False, (64, 87, 28))
            score_message_rect = score_message.get_rect(center=(400, 300))
            screen.blit(score_message,score_message_rect)




    pygame.display.update()
    clock.tick(60)