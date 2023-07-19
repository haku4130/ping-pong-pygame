from sys import exit
import pygame
import time

pygame.init()

FRAME_RATE = 60

screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('ping-pong')
clock = pygame.time.Clock()

pixel_font = pygame.font.Font('04B_30__.TTF', 30)

ball_surf = pygame.Surface((10, 10)).convert_alpha()
ball_rect = ball_surf.get_rect(center=(400, 200))
player_surf = pygame.Surface((20, 100)).convert_alpha()
player_rect = player_surf.get_rect(center=(100, 200))
opponent_surf = pygame.Surface((20, 100)).convert_alpha()
opponent_rect = opponent_surf.get_rect(center=(700, 200))

controls_text_surf = pixel_font.render('Control with UP and DOWN arrows', False, 'Black').convert_alpha()
controls_text_rect = controls_text_surf.get_rect(center=(400, 50))
start_text_surf = pixel_font.render('Press any button to start', False, 'Black').convert_alpha()
start_text_rect = start_text_surf.get_rect(center=(400, 200))

background = pygame.Color("White")

ball_speed_x = 7
ball_speed_y = 3
game_active = False
was_played = False
score = 0
scored_time = time.time()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if not game_active:
            if event.type == pygame.KEYDOWN:
                game_active = True
                ball_rect.center = (400, 200)
                player_rect.center = (100, 200)
                opponent_rect.center = (700, 200)
                ball_speed_x = 7
                ball_speed_y = 3
                score = 0

    ball_rect.x += ball_speed_x
    ball_rect.y += ball_speed_y

    if game_active:
        was_played = True
        if ball_rect.right >= screen_width or ball_rect.left <= 0:
            game_active = False
        if ball_rect.bottom >= screen_height or ball_rect.top <= 0:
            ball_speed_y = -ball_speed_y

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_rect.y -= 5
        if keys[pygame.K_DOWN]:
            player_rect.y += 5

        if player_rect.bottom >= screen_height:
            player_rect.bottom = screen_height
        if player_rect.top <= 0:
            player_rect.top = 0
        if opponent_rect.bottom >= screen_height:
            opponent_rect.bottom = screen_height
        if opponent_rect.top <= 0:
            opponent_rect.top = 0

        if ball_speed_x > 0:
            if ball_rect.top < opponent_rect.centery:
                opponent_rect.y -= 5
            if ball_rect.bottom > opponent_rect.centery:
                opponent_rect.y += 5

        if player_rect.colliderect(ball_rect):
            if player_rect.left <= ball_rect.centerx <= player_rect.right and player_rect.top <= ball_rect.centery\
                    <= player_rect.bottom:
                # Мяч попал внутрь платформы игрока
                ball_speed_y = -ball_speed_y
            else:
                current_time = time.time()
                if current_time - scored_time > 1:
                    score += 1
                    scored_time = current_time
                scored_time = time.time()
                ball_speed_x = -ball_speed_x
        if opponent_rect.colliderect(ball_rect):
            ball_speed_x = -ball_speed_x

        score_text_surf = pixel_font.render(f'Score: {score}', False, 'Grey')
        score_text_rect = score_text_surf.get_rect(center=(400, 350))

        screen.fill(background)
        screen.blit(score_text_surf, score_text_rect)
        screen.blit(ball_surf, ball_rect)
        screen.blit(player_surf, player_rect)
        screen.blit(opponent_surf, opponent_rect)
    else:
        screen.fill(background)

        if was_played:
            score_text_surf = pixel_font.render(f'You lose, final score: {score}', False, (255, 89, 103))
            score_text_rect = score_text_surf.get_rect(center=(400, 350))
            screen.blit(score_text_surf, score_text_rect)

        screen.blit(controls_text_surf, controls_text_rect)
        screen.blit(start_text_surf, start_text_rect)

    pygame.display.update()
    clock.tick(FRAME_RATE)
