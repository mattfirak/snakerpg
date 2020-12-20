import pygame
import time
import random

pygame.init()

clock = pygame.time.Clock()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)
blue = (0,0,255)

display_width = 800
display_height = 800

border_width = 40

snake_head_img = pygame.image.load('/home/matt/Python/snake/snake_head.png')
snake_body_img = pygame.image.load('/home/matt/Python/snake/snake_body.png')
snake_turn_img = pygame.image.load('/home/matt/Python/snake/snake_turn.png')
snake_tail_img = pygame.image.load('/home/matt/Python/snake/snake_tail.png')
apple_img = pygame.image.load('/home/matt/Python/snake/apple.png')

snake_block_size = snake_body_img.get_rect().size[0]
apple_block_size = apple_img.get_rect().size[0]

direction = "right"
snakeLength = 1

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.mouse.set_visible(1)
pygame.display.set_caption('Snake')
pygame.display.set_icon(apple_img)

small_font_size = int(display_width/32)
medium_font_size = int(display_width/16)
large_font_size = int(display_width/8)

def text_objects(text,color,size):
	if size == "small":
		font = pygame.font.SysFont(None, small_font_size)
		textSurface = font.render(text, True, color)
	if size == "medium":
		font = pygame.font.SysFont(None, medium_font_size)
		textSurface = font.render(text, True, color)
	if size == "large":
		font = pygame.font.SysFont(None, large_font_size)
	textSurface = font.render(text, True, color)
	return textSurface, textSurface.get_rect()

def message_to_screen(msg,color,y_displace=0,size="small"):
	textSurf, textRect = text_objects(msg,color,size)
	textRect.center = (display_width/2), (display_height/2) + y_displace
	gameDisplay.blit(textSurf, textRect)

def score(score):
	text = smallfont.render("score: "+str(score), True, black)
	gameDisplay.blit(text, [0,0])

def snake(snakeList):
	for index, XnYnD in enumerate(snakeList):
		#draw snake head
		if index == snakeLength - 1:
			if XnYnD[2] == "right":
				segment = pygame.transform.rotate(snake_head_img, 270)
			if XnYnD[2] == "left":
				segment = pygame.transform.rotate(snake_head_img, 90)
			if XnYnD[2] == "up":
				segment = snake_head_img
			if XnYnD[2] == "down":
				segment = pygame.transform.rotate(snake_head_img, 180)

		#draw snake tail
		elif index == 0:
			if snakeList[index + 1][2] == "right":
				segment = pygame.transform.rotate(snake_tail_img, 270)
			elif snakeList[index + 1][2] == "left":
				segment = pygame.transform.rotate(snake_tail_img, 90)
			elif snakeList[index + 1][2] == "up":
				segment = snake_tail_img
			elif snakeList[index + 1][2] == "down":
				segment = pygame.transform.rotate(snake_tail_img, 180)

		elif snakeLength > 2:
			if XnYnD[2] == "right":
				if snakeList[index + 1][2] == "up":
					segment = pygame.transform.rotate(snake_turn_img, 90)
				elif snakeList[index + 1][2] == "down":
					segment = pygame.transform.rotate(snake_turn_img, 180)
				else:
					segment = pygame.transform.rotate(snake_body_img, 90)
			elif XnYnD[2] == "left":
				if snakeList[index + 1][2] == "up":
					segment = snake_turn_img
				elif snakeList[index + 1][2] == "down":
					segment = pygame.transform.rotate(snake_turn_img, 270)
				else:
					segment = pygame.transform.rotate(snake_body_img, 90)
			elif XnYnD[2] == "up":
				if snakeList[index + 1][2] == "left":
					segment = pygame.transform.rotate(snake_turn_img, 180)
				elif snakeList[index + 1][2] == "right":
					segment = pygame.transform.rotate(snake_turn_img, 270)
				else:
					segment = snake_body_img
			elif XnYnD[2] == "down":
				if snakeList[index + 1][2] == "left":
					segment = pygame.transform.rotate(snake_turn_img, 90)
				elif snakeList[index + 1][2] == "right":
					segment = snake_turn_img
				else:
					segment = snake_body_img

		gameDisplay.blit(segment, (XnYnD[0], XnYnD[1]))

def randAppleGen():
	randAppleX = random.randrange(border_width, display_width - 2 * border_width - apple_block_size, apple_block_size)
	randAppleY = random.randrange(border_width, display_height - 2 * border_width - apple_block_size, apple_block_size)
	return randAppleX, randAppleY

def apple(randAppleX, randAppleY, apple_block_size):
	gameDisplay.blit(apple_img, (randAppleX, randAppleY))

def start_menu():
	intro = True
	while intro:
		gameDisplay.fill(white)
		message_to_screen("Snake RPG", black, -100, "large")
		message_to_screen("Press ENTER To Start Game", blue, 100, "medium")
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				intro = False
				gameExit = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					gameLoop()

		clock.tick(15)

def gameLoop():

	global direction
	global snakeLength

	#game start countdown
	countdown = ["3", "2", "1"]
	for x in countdown:
		gameDisplay.fill(white)
		message_to_screen(x, black, 0, "large")
		pygame.display.update()
		time.sleep(1)

	FPS = 10

	time_warp = 2
	time_warp_activate = False
	#enable to abllow time warp ability
	time_warp_ability = False

	collision_count = 0
	#increment to allow collisions without game over
	collisions_allowed = 0

	#enable to allow edge warp
	edge_warp = False

	gameExit = False
	gameOver = False
	gamePause = False

	lead_x = display_width/2
	lead_y = display_height/2
	lead_x_change = snake_block_size
	lead_y_change = 0

	snakeLength = 1
	direction = "right"

	snakeList = []

	randAppleX, randAppleY = randAppleGen()

	badSpawnCheck = True

	#gameplay loop
	while not gameExit:

		#pause screen loop
		while gamePause == True:
			gameDisplay.fill(white)
			message_to_screen("Game Paused", blue, -50, "large")
			message_to_screen("Press any key to continue", blue, 50, "medium")
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
						gamePause = False
				elif event.type == pygame.QUIT:
						gamePause = False
						gameExit = True

		#game over screen loop
		while gameOver == True:
			gameDisplay.fill(white)
			message_to_screen("Game Over!", red, -50, "large")
			message_to_screen("Press C to play again or Q to quit", blue, 50, "small")
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameExit = True
					gameOver = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						gameExit = True
						gameOver = False
					elif event.key == pygame.K_c:
						gameLoop()

		#gameplay event handler
		for event in pygame.event.get():
			#press x to quit
			if event.type == pygame.QUIT:
				gameExit = True
			if event.type == pygame.KEYDOWN:
				#press escape key to quit
				if event.key == pygame.K_ESCAPE:
					gamePause = True
				#move snake
				elif event.key == pygame.K_LEFT and snakeList[snakeLength - 1][2] != "right":
					lead_x_change = -snake_block_size
					lead_y_change = 0
					direction = "left"
				elif event.key == pygame.K_RIGHT and snakeList[snakeLength - 1][2] != "left":
					lead_x_change = snake_block_size
					lead_y_change = 0
					direction = "right"
				elif event.key == pygame.K_UP and snakeList[snakeLength - 1][2] != "down":
					lead_y_change = -snake_block_size
					lead_x_change = 0
					direction = "up"
				elif event.key == pygame.K_DOWN and snakeList[snakeLength - 1][2] != "up":
					lead_y_change = snake_block_size
					lead_x_change = 0
					direction = "down"
				#press space to slow time
				elif event.key == pygame.K_SPACE and time_warp_ability == True:
					FPS = FPS / time_warp
					time_warp_activate = True
			#release space to return to normal time
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE and time_warp_activate == True:
					FPS = FPS * time_warp

		#get new snake head coordinates
		lead_x += lead_x_change
		lead_y += lead_y_change

		#boundry check
		if lead_x >= display_width - border_width or lead_x < 0 + border_width or lead_y >= display_height - border_width or lead_y < 0 + border_width:
			if edge_warp == True:
				if lead_x >= display_width - border_width:
					lead_x = 0
				elif lead_x < 0 + border_width:
					lead_x = display_width - snake_block_size
				elif lead_y >= display_height - border_width:
					lead_y = 0
				elif lead_y < 0 + border_width:
					lead_y = display_height - snake_block_size
			else:
				gameOver = True

		#collision check
		for eachSegment in snakeList:
			for eachSegment2 in snakeList:
				if eachSegment[0] == eachSegment2[0] and eachSegment[1] == eachSegment2[1]:
					collision_count += 1
					if collision_count > snakeLength + 1 + collisions_allowed:
						gameOver = True

		collision_count = 0

		#eat apple check
		if lead_x + snake_block_size > randAppleX and lead_x < randAppleX + apple_block_size and lead_y + snake_block_size > randAppleY and lead_y < randAppleY + apple_block_size:
			#check if apple spawns on snake
			while badSpawnCheck == True:
				badSpawnCheck = False
				#get new apple coordinates
				randAppleX, randAppleY = randAppleGen()
				for eachSegment in snakeList:
					if eachSegment[1] == randAppleX and eachSegment[2] == randAppleY:
						badSpawnCheck = True

			#reset while loop
			badSpawnCheck = True
			#add a snake segment
			snakeLength += 1

		#adding snake head potion to snake list
		snakeHead = []
		snakeHead.append(lead_x)
		snakeHead.append(lead_y)
		snakeHead.append(direction)
		snakeList.append(snakeHead)

		#cut snake to length
		if len(snakeList) > snakeLength:
			del snakeList[0]
			
		#draw screen
		gameDisplay.fill(black)
		pygame.draw.rect(gameDisplay, white, (border_width, border_width, display_width - 2 * border_width, display_height - 2 * border_width))
		apple(randAppleX, randAppleY, apple_block_size)
		snake(snakeList)
		score(snakeLength)
		pygame.display.update()

		#define FPS
		clock.tick(FPS)

	#quit the game and exit pygame
	pygame.quit()
	quit()

#start the main game loop
start_menu()