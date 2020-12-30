'''
Snake Rpygame
Created by Matt Firak
2020
'''

import random
import math
import sys
import pygame
import checkbox

pygame.init()

clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)
blue = (0, 0, 255)

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800

BORDER_WIDTH = 40

snake_head_img = pygame.image.load("/home/matt/Python/snake/snake_head.png")
snake_body_img = pygame.image.load("/home/matt/Python/snake/snake_body.png")
snake_turn_img = pygame.image.load("/home/matt/Python/snake/snake_turn.png")
snake_tail_img = pygame.image.load("/home/matt/Python/snake/snake_tail.png")
apple_img = pygame.image.load("/home/matt/Python/snake/apple.png")

SNAKE_BLOCK_SIZE = snake_body_img.get_rect().size[0]
APPLE_BLOCK_SIZE = apple_img.get_rect().size[0]

DIRECTION = "right"
SNAKE_LENGTH = 1

gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.mouse.set_visible(1)
pygame.display.set_caption("Snake")
pygame.display.set_icon(apple_img)

chkbox1 = checkbox.Checkbox(gameDisplay, 200, 200, red, "Time Warp", black, black, 22, black, (50,1))

def text_objects(text, color, size):
    '''take a text string, color and size variable and ouputs a text objects'''
    if size == "small":
        font = pygame.font.Font("EightBitDragon.ttf", int(DISPLAY_WIDTH / 64))
        text_surface = font.render(text, True, color)
    if size == "medium":
        font = pygame.font.Font("EightBitDragon.ttf", int(DISPLAY_WIDTH / 32))
        text_surface = font.render(text, True, color)
    if size == "large":
        font = pygame.font.Font("EightBitDragon.ttf", int(DISPLAY_WIDTH / 16))
        text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

def message_to_screen(msg, color, left, top, size="small"):
    '''uses text objects and centers them on the screen'''
    text_surf, text_rect = text_objects(msg, color, size)
    text_rect.left = left
    text_rect.top = top
    gameDisplay.blit(text_surf, text_rect)

def message_to_center(msg, color, y_displace=0, size="small"):
    '''uses text objects and centers them on the screen'''
    text_surf, text_rect = text_objects(msg, color, size)
    text_rect.center = (DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 2) + y_displace
    gameDisplay.blit(text_surf, text_rect)

def score(num):
    '''displays score'''
    message_to_screen(
            "SCORE: " + str(num-1),
            white,
            BORDER_WIDTH,
            15
        )

def exp_bar(experience_points):
    '''displays experience bar'''
    exp_bar_width = 204
    exp_points_width = experience_points % 200
    player_level = math.ceil((experience_points+1)/200)
    # displays level
    message_to_screen(
            "LEVEL " + str(player_level),
            white,
            DISPLAY_WIDTH - BORDER_WIDTH - exp_bar_width - 60,
            13
        )
    # draw experience bar
    pygame.draw.rect(
            gameDisplay,
            white,
            (
                # left
                DISPLAY_WIDTH - BORDER_WIDTH - exp_bar_width,
                # top
                15,
                # width
                exp_bar_width,
                # height
                BORDER_WIDTH - 30,
            ),
        )
    # draw experience points
    pygame.draw.rect(
            gameDisplay,
            blue,
            (
                DISPLAY_WIDTH - BORDER_WIDTH - exp_bar_width + 2,
                17,
                exp_points_width,
                BORDER_WIDTH - 34,
            ),
        )

def snake(snake_list):
    '''draws the snake'''
    # creates an index of each segment and loops
    for index, x_y_d in enumerate(snake_list):
        # define snake head
        if index == SNAKE_LENGTH - 1:
            if x_y_d[2] == "right":
                segment = pygame.transform.rotate(snake_head_img, 270)
            if x_y_d[2] == "left":
                segment = pygame.transform.rotate(snake_head_img, 90)
            if x_y_d[2] == "up":
                segment = snake_head_img
            if x_y_d[2] == "down":
                segment = pygame.transform.rotate(snake_head_img, 180)
        # define snake tail
        elif index == 0:
            if snake_list[index + 1][2] == "right":
                segment = pygame.transform.rotate(snake_tail_img, 270)
            elif snake_list[index + 1][2] == "left":
                segment = pygame.transform.rotate(snake_tail_img, 90)
            elif snake_list[index + 1][2] == "up":
                segment = snake_tail_img
            elif snake_list[index + 1][2] == "down":
                segment = pygame.transform.rotate(snake_tail_img, 180)
        # define snake body
        elif SNAKE_LENGTH > 2:
            if x_y_d[2] == "right":
                if snake_list[index + 1][2] == "up":
                    segment = pygame.transform.rotate(snake_turn_img, 90)
                elif snake_list[index + 1][2] == "down":
                    segment = pygame.transform.rotate(snake_turn_img, 180)
                else:
                    segment = pygame.transform.rotate(snake_body_img, 90)
            elif x_y_d[2] == "left":
                if snake_list[index + 1][2] == "up":
                    segment = snake_turn_img
                elif snake_list[index + 1][2] == "down":
                    segment = pygame.transform.rotate(snake_turn_img, 270)
                else:
                    segment = pygame.transform.rotate(snake_body_img, 90)
            elif x_y_d[2] == "up":
                if snake_list[index + 1][2] == "left":
                    segment = pygame.transform.rotate(snake_turn_img, 180)
                elif snake_list[index + 1][2] == "right":
                    segment = pygame.transform.rotate(snake_turn_img, 270)
                else:
                    segment = snake_body_img
            elif x_y_d[2] == "down":
                if snake_list[index + 1][2] == "left":
                    segment = pygame.transform.rotate(snake_turn_img, 90)
                elif snake_list[index + 1][2] == "right":
                    segment = snake_turn_img
                else:
                    segment = snake_body_img
        # draw segment
        gameDisplay.blit(segment, (x_y_d[0], x_y_d[1]))

def rand_apple_gen():
    '''generates random apple location'''
    rand_apple_x = random.randrange(
        BORDER_WIDTH,
        DISPLAY_WIDTH - 2 * BORDER_WIDTH - APPLE_BLOCK_SIZE,
        APPLE_BLOCK_SIZE,
    )
    rand_apple_y = random.randrange(
        BORDER_WIDTH,
        DISPLAY_HEIGHT - 2 * BORDER_WIDTH - APPLE_BLOCK_SIZE,
        APPLE_BLOCK_SIZE,
    )
    return rand_apple_x, rand_apple_y

def apple(rand_apple_x, rand_apple_y):
    '''draws apple'''
    gameDisplay.blit(apple_img, (rand_apple_x, rand_apple_y))

def start_menu():
    '''title screen with event handler'''
    intro = True
    while intro:
        gameDisplay.fill(white)
        message_to_center("Snake RPG", black, -100, "large")
        message_to_center("Press ENTER To Start Game", blue, 100, "medium")
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()

        clock.tick(15)

def pause():
    '''paused game loop'''
    paused = True
    while paused:
        gameDisplay.fill(white)
        message_to_center("Game Paused", blue, -50, "large")
        message_to_center("Press any key to continue", blue, 50, "medium")
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                paused = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def skill_tree():
    '''skill tree menu'''
    paused = True
    
    while paused:
        pygame.draw.rect(gameDisplay, white, (BORDER_WIDTH, BORDER_WIDTH, DISPLAY_WIDTH - (2 * BORDER_WIDTH), DISPLAY_HEIGHT - (2 * BORDER_WIDTH)))
        message_to_center("Skill Tree", blue, -300, "large")
        message_to_center("Press ESC To Resume", blue, 300, "medium")

        for event in pygame.event.get():
            chkbox1.update_checkbox(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        chkbox1.render_checkbox()
        pygame.display.update()

def game_loop():
    '''main gameplay loop'''

    global DIRECTION
    global SNAKE_LENGTH

    # game start countdown
    # countdown = ["3", "2", "1"]
    # for num in countdown:
    #     gameDisplay.fill(white)
    #     message_to_center(num, black, 0, "large")
    #     pygame.display.update()
    #     time.sleep(1)

    fps = 10

    time_warp = 2
    time_warp_activate = False
    # enable to abllow time warp ability
    time_warp_ability = True

    collision_count = 0
    # increment to allow collisions without game over
    collisions_allowed = 1

    # enable to allow edge warp
    edge_warp = True

    game_exit = False
    game_over = False

    lead_x = DISPLAY_WIDTH / 2
    lead_y = DISPLAY_HEIGHT / 2
    lead_x_change = SNAKE_BLOCK_SIZE
    lead_y_change = 0

    experience_points = 0

    SNAKE_LENGTH = 1
    DIRECTION = "right"

    snake_list = []

    rand_apple_x, rand_apple_y = rand_apple_gen()

    bad_spawn_check = True

    # gameplay loop
    while not game_exit:
        # game over screen loop
        while game_over is True:
            gameDisplay.fill(white)
            message_to_center("Game Over!", red, -50, "large")
            message_to_center("Press C to play again or Q to quit", blue, 50, "medium")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_exit = True
                        game_over = False
                    elif event.key == pygame.K_c:
                        game_loop()

        # gameplay event handler
        for event in pygame.event.get():
            # press x to quit
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                # press escape key to pause
                if event.key == pygame.K_ESCAPE:
                    pause()
                # press 'S' to open skill tree menu
                elif event.key == pygame.K_s:
                    skill_tree()
                # move snake
                elif (
                    event.key == pygame.K_LEFT
                    and snake_list[SNAKE_LENGTH - 1][2] != "right"
                ):
                    lead_x_change = -SNAKE_BLOCK_SIZE
                    lead_y_change = 0
                    DIRECTION = "left"
                elif (
                    event.key == pygame.K_RIGHT
                    and snake_list[SNAKE_LENGTH - 1][2] != "left"
                ):
                    lead_x_change = SNAKE_BLOCK_SIZE
                    lead_y_change = 0
                    DIRECTION = "right"
                elif (
                    event.key == pygame.K_UP and snake_list[SNAKE_LENGTH - 1][2] != "down"
                ):
                    lead_y_change = -SNAKE_BLOCK_SIZE
                    lead_x_change = 0
                    DIRECTION = "up"
                elif (
                    event.key == pygame.K_DOWN and snake_list[SNAKE_LENGTH - 1][2] != "up"
                ):
                    lead_y_change = SNAKE_BLOCK_SIZE
                    lead_x_change = 0
                    DIRECTION = "down"
                # press space to slow time
                elif event.key == pygame.K_SPACE and time_warp_ability is True:
                    fps = fps / time_warp
                    time_warp_activate = True
            # release space to return to normal time
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and time_warp_activate is True:
                    fps = fps * time_warp

        # get new snake head coordinates
        lead_x += lead_x_change
        lead_y += lead_y_change

        # boundry check
        if (
            lead_x >= DISPLAY_WIDTH - BORDER_WIDTH
            or lead_x < 0 + BORDER_WIDTH
            or lead_y >= DISPLAY_HEIGHT - BORDER_WIDTH
            or lead_y < 0 + BORDER_WIDTH
        ):
            if edge_warp is True:
                if lead_x >= DISPLAY_WIDTH - BORDER_WIDTH:
                    lead_x = BORDER_WIDTH
                elif lead_x < 0 + BORDER_WIDTH:
                    lead_x = DISPLAY_WIDTH - SNAKE_BLOCK_SIZE - BORDER_WIDTH
                elif lead_y >= DISPLAY_HEIGHT - BORDER_WIDTH:
                    lead_y = BORDER_WIDTH
                elif lead_y < 0 + BORDER_WIDTH:
                    lead_y = DISPLAY_HEIGHT - SNAKE_BLOCK_SIZE - BORDER_WIDTH
            else:
                game_over = True

        # collision check
        for each_segment in snake_list:
            for each_segment_2 in snake_list:
                if (
                    each_segment[0] == each_segment_2[0]
                    and each_segment[1] == each_segment_2[1]
                ):
                    collision_count += 1
                    if collision_count > SNAKE_LENGTH + 1 + collisions_allowed:
                        game_over = True

        collision_count = 0

        # eat apple check
        if (
            lead_x + SNAKE_BLOCK_SIZE > rand_apple_x
            and lead_x < rand_apple_x + APPLE_BLOCK_SIZE
            and lead_y + SNAKE_BLOCK_SIZE > rand_apple_y
            and lead_y < rand_apple_y + APPLE_BLOCK_SIZE
        ):
            # check if apple spawns on snake
            while bad_spawn_check is True:
                bad_spawn_check = False
                # get new apple coordinates
                rand_apple_x, rand_apple_y = rand_apple_gen()
                for each_segment in snake_list:
                    if each_segment[1] == rand_apple_x and each_segment[2] == rand_apple_y:
                        bad_spawn_check = True

            # reset while loop
            bad_spawn_check = True
            # add a snake segment
            SNAKE_LENGTH += 1
            # gain experience points
            experience_points += 25

        # adding snake head potion to snake list
        snake_head = []
        snake_head.append(lead_x)
        snake_head.append(lead_y)
        snake_head.append(DIRECTION)
        snake_list.append(snake_head)

        # cut snake to length
        if len(snake_list) > SNAKE_LENGTH:
            del snake_list[0]

        # draw screen
        gameDisplay.fill(black)
        pygame.draw.rect(
            gameDisplay,
            white,
            (
                BORDER_WIDTH,
                BORDER_WIDTH,
                DISPLAY_WIDTH - 2 * BORDER_WIDTH,
                DISPLAY_HEIGHT - 2 * BORDER_WIDTH,
            ),
        )
        apple(rand_apple_x, rand_apple_y)
        snake(snake_list)
        score(SNAKE_LENGTH)
        exp_bar(experience_points)
        pygame.display.update()

        # define fps
        clock.tick(fps)

    # quit the game and exit pygame
    pygame.quit()
    quit()

# start the main game loop
start_menu()
