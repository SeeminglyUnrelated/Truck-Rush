import pygame, random
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

class Player(pygame.sprite.Sprite):
	def __init__(self, player):
		super(Player, self).__init__()
		self.player = player
		self.surf = pygame.image.load(f"images/car{player}.png").convert_alpha()
		self.y = 450
		self.rect = self.surf.get_rect(center = (lanes[2], 444))
		self.lane = 2 if player == 2 else 1
		self.dead = False
		self.score = 0

	def update(self, pressed_keys):
		global move_ticker
		if pressed_keys[K_RIGHT]:
			if move_ticker == 0:
				move_ticker = sensitivity
				self.lane = self.lane + 1 if self.lane < 2 else self.lane
				self.rect = self.surf.get_rect(center = (lanes[self.lane], self.y))
		elif pressed_keys[K_LEFT]:
			if move_ticker == 0:
				move_ticker = sensitivity
				self.lane = self.lane - 1 if self.lane > 0 else self.lane
				self.rect = self.surf.get_rect(center = (lanes[self.lane], self.y))

class EnemyCar(pygame.sprite.Sprite):
	def __init__(self, lane):
		super(EnemyCar, self).__init__()
		self.surf = pygame.image.load(f"images/enemy_{random.randint(1, 2)}.png").convert_alpha()
		self.lane = lane#random.randint(0, 2)
		self.rect = self.surf.get_rect(center = (lanes[self.lane], -150))
		self.speed = random.randint(4, 6)

	def update(self):
		self.rect.move_ip(0, self.speed)
		if self.rect.bottom > SCREEN_HEIGHT + 150:
			carCount[self.lane] -= 1
			player.score += 1
			self.kill()

pygame.init()
pygame.mixer.init()


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Truck Rush")

clock = pygame.time.Clock()

background = pygame.image.load("images/bg.png")

lanes = [112, 200, 293]
carCount = [0, 0, 0]
move_ticker = 0
sensitivity = 15

def play_state(playerNum, clock):
	global lanes, move_ticker, carCount, player

	font = pygame.font.Font("fonts/ARCADECLASSIC.ttf", 60)
	running = True
	player = Player(2)
	start = True
	playerPos = SCREEN_HEIGHT
	bg1Pos = 0
	bg2Pos = -600
	crash = pygame.mixer.Sound("Music/crash_sound.wav")

	enemies = pygame.sprite.Group()
	ADDENEMY = pygame.USEREVENT + 2
	pygame.time.set_timer(ADDENEMY, random.randint(900, 1050))

	while running:
		screen.fill((0, 150, 0))
		screen.blit(background, (0, bg1Pos))
		screen.blit(background, (0, bg2Pos))
		screen.blit(font.render(str(player.score), False, (0,0,0)), (10, 500))
		#if background.
		bg1Pos += 3
		bg2Pos += 3
		if bg1Pos > 600:
			bg1Pos = -600
		if bg2Pos > 600:
			bg2Pos = -600

		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					running = False
			elif event.type == QUIT:
				running = False

			elif event.type == ADDENEMY:
				lanePos = random.randint(0, 2)
				carCount[lanePos] += 1
				if carCount[lanePos] > 2:
					carCount[lanePos] -= 1
				else:
					new_Enemy = EnemyCar(lanePos)
					enemies.add(new_Enemy)

		if start:
			screen.blit(player.surf, (lanes[2]-44, playerPos))
			playerPos -= 4
			if playerPos < 400:
				start = False
		else:
			for enemy in enemies:
				screen.blit(enemy.surf, enemy.rect)

			screen.blit(player.surf, player.rect)
			pressed_keys = pygame.key.get_pressed()
			player.update(pressed_keys)
			enemies.update()

		if move_ticker > 0:
			move_ticker -= 1

		if pygame.sprite.spritecollideany(player, enemies):
			player.kill()
			carCount = [0, 0, 0]
			running = False

		pygame.display.flip()
		clock.tick(60)
	pygame.mixer.music.pause()
	crash.play()

	idle_state(clock)

def idle_state(clock):
    # Set up music
	pygame.mixer.music.load("Music/Main Menu.wav")
	pygame.mixer.music.play(loops=-1)
 
	global SCREEN_WIDTH
	quit = False
	running = True

	font = pygame.font.Font("fonts/ARCADECLASSIC.ttf", 70)

	text = font.render(' Truck Rush ', False, (0,0,0), (255, 30, 30))
	textRect = text.get_rect()
	textRect.center = (SCREEN_WIDTH / 2, 100)

	while running:
		screen.fill((255, 255, 255))
		screen.blit(background, (0,0))
		screen.blit(text, textRect)
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					quit = True
					running = False
				elif event.key == K_SPACE:
					running = False
			elif event.type == QUIT:
				quit = True
				running = False
		pygame.display.flip()
		clock.tick(60)
	if not quit:
		play_state(1, clock)
	pygame.mixer.music.stop()

idle_state(clock)