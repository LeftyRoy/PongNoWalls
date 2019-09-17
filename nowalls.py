import pygame
import sys
from pygame.locals import *
from random import randint

WIDTH = 1200
HEIGHT = 600
TEXT_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)
FPS = 60
BALL_MIN_SPEED = 3
BALL_MAX_SPEED = 5
ROUND = 0
player_win = 0
computer_win = 0
player_score = 0
computer_score = 0
match_over = False


def wait_for_player_to_press_key():
    while True:
        global event
        for event in pygame.event.get():
            if event.type is QUIT:
                terminate()
            if event.type is KEYDOWN:
                if event.key is K_ESCAPE:  # Pressing ESC quits.
                    terminate()
                return


def draw_text(text, font, surface, x, y):
    text_obj = font.render(text, 1, TEXT_COLOR)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def terminate():
    pygame.quit()
    sys.exit()


# Set up PyGame and the window
pygame.init()
mainClock = pygame.time.Clock()
window_surface = pygame.display.set_mode((WIDTH, HEIGHT))
surface_rect = window_surface.get_rect()
pygame.display.set_caption('Pong No Walls')

# Set up the fonts.
title_font = pygame.font.SysFont(None, 80)
title_font2 = pygame.font.SysFont(None, 48)
title_font3 = pygame.font.SysFont(None, 16)
match_over_font = pygame.font.SysFont(None, 72)
score_font = pygame.font.SysFont(None, 50)

# Title Screen
window_surface.fill(BACKGROUND_COLOR)
draw_text('Pong No Walls', title_font, window_surface, (WIDTH / 3),
          (HEIGHT / 3))
draw_text('To win you must score at least 11 points and 2 more than the AI', title_font2, window_surface,
          (WIDTH / 3) - 250, (HEIGHT / 3) + 100)
draw_text('Press an arrow key to start', title_font2, window_surface,
          (WIDTH / 3) - 20, (HEIGHT / 3) + 200)
pygame.display.update()
wait_for_player_to_press_key()

# music
pygame.mixer.music.load("Sounds/theme.mp3")
pygame.mixer.music.play(0)
hit_sound = pygame.mixer.Sound('Sounds/hit.wav')
victory1 = pygame.mixer.Sound('Sounds/victory1.aiff')
victory2 = pygame.mixer.Sound('Sounds/victory2.wav')
failure1 = pygame.mixer.Sound('Sounds/failure1.wav')
failure2 = pygame.mixer.Sound('Sounds/failure2.wav')

# player paddle images
player_image = pygame.image.load('Images/knife.png')
player_rect = player_image.get_rect()

player_image2 = pygame.image.load('Images/knife.png')
player_image2 = pygame.transform.rotate(player_image2, 90)
player_rect2 = player_image2.get_rect()

player_image3 = pygame.transform.rotate(player_image2, 180)
player_image3 = pygame.transform.flip(player_image3, 1, 0)
player_rect3 = player_image3.get_rect()

# computer paddle images
computer_image = pygame.image.load('Images/knife.png')
computer_image = pygame.transform.flip(computer_image, 1, 0)
computer_rect = computer_image.get_rect()

computer_image2 = pygame.image.load('Images/knife.png')
computer_image2 = pygame.transform.rotate(computer_image2, 90)
computer_image2 = pygame.transform.flip(computer_image2, 1, 0)
computer_rect2 = computer_image2.get_rect()

computer_image3 = pygame.image.load('Images/knife.png')
computer_image3 = pygame.transform.rotate(computer_image3, 270)
computer_rect3 = computer_image3.get_rect()

# ball image
ball_image = pygame.image.load('Images/ball.png')
ball_image = pygame.image.load('Images/ball.png')
ball_rect = ball_image.get_rect()

# player directions
UP = False
DOWN = False
LEFT = False
RIGHT = False
STOPPED = False

# ball directions
UP_LEFT = 0
DOWN_LEFT = 1
UP_RIGHT = 2
DOWN_RIGHT = 3


# Player Paddle Classes

# Vertical
class PlayerPaddle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = player_image
        self.rect = player_rect
        self.speed = 8

        self.rect.centerx = window_surface.get_rect().right
        self.rect.centerx -= 50
        self.rect.centery = window_surface.get_rect().centery

    def move(self):
        if (UP is True) and (self.rect.y > 5):
            self.rect.y -= self.speed
        elif (DOWN is True) and (self.rect.bottom < HEIGHT - 5):
            self.rect.y += self.speed
        elif STOPPED is True:
            pass


# Horizontal
# Top
class PlayerPaddle2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = player_image2
        self.rect = player_rect2
        self.speed = 8

        self.rect.top = window_surface.get_rect().right
        self.rect.x += 1000
        self.rect.y = window_surface.get_rect().y + 20

    def move(self):
        if (RIGHT is True) and (self.rect.x < WIDTH - 100):
            self.rect.x += self.speed
        elif (LEFT is True) and (self.rect.x > 600):
            self.rect.x -= self.speed
        elif STOPPED is True:
            pass


# Bottom
class PlayerPaddle3(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = player_image3
        self.rect = player_rect3
        self.speed = 8

        self.rect.bottom = window_surface.get_rect().right
        self.rect.x += 1000
        self.rect.y = window_surface.get_rect().y + 555

    def move(self):
        if (RIGHT is True) and (self.rect.x < WIDTH - 100):
            self.rect.x += self.speed
        elif (LEFT is True) and (self.rect.x > 600):
            self.rect.x -= self.speed
        elif STOPPED is True:
            pass


# Computer Paddle Classes

# Vertical
class ComputerPaddle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = computer_image
        self.rect = computer_rect
        self.speed = 2.5

        self.rect.centerx = window_surface.get_rect().left
        self.rect.centerx += 50
        self.rect.centery = window_surface.get_rect().centery

    def update(self, ball_b):
        if ball_rect.top < self.rect.top:
            self.rect.centery -= self.speed
        elif ball.rect.bottom > self.rect.bottom:
            self.rect.centery += self.speed

        self.rect.center = (self.rect.centerx, self.rect.centery)


# Horizontal
# Top
class ComputerPaddle2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = computer_image2
        self.rect = computer_rect2
        self.speed = 2.5

        self.rect.top = window_surface.get_rect().left
        self.rect.x += 10
        self.rect.y = window_surface.get_rect().y + 20

    def update(self, ball_b):
        if ball_rect.right > self.rect.right and self.rect.right < 600:
            self.rect.right += self.speed
        elif ball.rect.left < self.rect.left:
            self.rect.left -= self.speed

        self.rect.center = (self.rect.centerx, self.rect.centery)


# Bottom
class ComputerPaddle3(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = computer_image3
        self.rect = computer_rect3
        self.speed = 2.5

        self.rect.bottom = window_surface.get_rect().left
        self.rect.x += 10
        self.rect.y = window_surface.get_rect().y + 555

    def update(self, ball_b):
        if ball_rect.right > self.rect.right and self.rect.right < 600:
            self.rect.right += self.speed
        elif ball.rect.left < self.rect.left:
            self.rect.left -= self.speed

        self.rect.center = (self.rect.centerx, self.rect.centery)


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = ball_image
        self.rect = ball_rect
        self.rect.centerx = surface_rect.centerx
        self.rect.centery = surface_rect.centery
        self.direction = randint(0, 3)
        self.speed = randint(BALL_MIN_SPEED, BALL_MAX_SPEED)

    def move(self):
        if self.direction is UP_LEFT:
            self.rect.x -= self.speed
            self.rect.y -= self.speed
        elif self.direction is UP_RIGHT:
            self.rect.x += self.speed
            self.rect.y -= self.speed
        elif self.direction is DOWN_LEFT:
            self.rect.x -= self.speed
            self.rect.y += self.speed
        elif self.direction is DOWN_RIGHT:
            self.rect.x += self.speed
            self.rect.y += self.speed

    def reset(self):
        if self.rect.y < 0 or self.rect.y > HEIGHT:
            self.rect.centerx = surface_rect.centerx
            self.rect.centery = surface_rect.centery
            self.speed = randint(BALL_MIN_SPEED, BALL_MAX_SPEED)
            self.direction = randint(0, 3)
        if self.rect.x < 0 or self.rect.x > WIDTH:
            self.rect.centerx = surface_rect.centerx
            self.rect.centery = surface_rect.centery
            self.speed = randint(BALL_MIN_SPEED, BALL_MAX_SPEED)
            self.direction = randint(0, 3)


paddle_p = PlayerPaddle()
paddle_p2 = PlayerPaddle2()
paddle_p3 = PlayerPaddle3()
paddle_c = ComputerPaddle()
paddle_c2 = ComputerPaddle2()
paddle_c3 = ComputerPaddle3()
ball = Ball()

sprites = pygame.sprite.Group(paddle_p, paddle_p2, paddle_p3, paddle_c, paddle_c2, paddle_c3, ball)


def hit():
    if pygame.sprite.collide_circle(ball, paddle_p):
        if ball.direction is UP_RIGHT:
            ball.direction = UP_LEFT
        elif ball.direction is DOWN_RIGHT:
            ball.direction = DOWN_LEFT
        hit_sound.play()
    elif pygame.sprite.collide_circle(ball, paddle_p2):
        if ball.direction is UP_RIGHT:
            ball.direction = DOWN_RIGHT
        elif ball.direction is UP_LEFT:
            ball.direction = DOWN_LEFT
        hit_sound.play()
    elif pygame.sprite.collide_circle(ball, paddle_p3):
        if ball.direction is DOWN_RIGHT:
            ball.direction = UP_RIGHT
        elif ball.direction is DOWN_LEFT:
            ball.direction = UP_LEFT
        hit_sound.play()
    elif pygame.sprite.collide_circle(ball, paddle_c):
        if ball.direction is UP_LEFT:
            ball.direction = UP_RIGHT
        elif ball.direction is DOWN_LEFT:
            ball.direction = DOWN_RIGHT
        hit_sound.play()
    elif pygame.sprite.collide_circle(ball, paddle_c2):
        if ball.direction is UP_LEFT:
            ball.direction = DOWN_LEFT
        elif ball.direction is UP_RIGHT:
            ball.direction = DOWN_RIGHT
        hit_sound.play()
    elif pygame.sprite.collide_circle(ball, paddle_c3):
        if ball.direction is DOWN_LEFT:
            ball.direction = UP_LEFT
        elif ball.direction is DOWN_RIGHT:
            ball.direction = UP_RIGHT
        hit_sound.play()


while True:

    mainClock.tick(FPS)

    if ball.rect.x > WIDTH:
        ball.centerx = surface_rect.centerx
        ball.centery = surface_rect.centery
        ball.direction = randint(0, 1)
    elif ball.rect.x < 0:
        ball.centerx = surface_rect.centerx
        ball.centery = surface_rect.centery
        ball.direction - randint(2, 3)

    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()

        # Player movement
        if event.type == KEYDOWN:
            if event.key == K_UP:
                UP = True
                DOWN = False
                STOPPED = False
            if event.key == K_DOWN:
                UP = False
                DOWN = True
                STOPPED = False
            if event.key == K_RIGHT:
                RIGHT = True
                LEFT = False
                STOPPED = False
            if event.key == K_LEFT:
                LEFT = True
                RIGHT = False
                STOPPED = False
        elif event.type == KEYUP:
            if event.key == K_DOWN or event.key == K_UP:
                STOPPED = True
                DOWN = False
                UP = False
            elif event.key == K_LEFT or event.key == K_RIGHT:
                STOPPED = True
                LEFT = False
                RIGHT = False

    # Scoreboard
    scoreboard = score_font.render("AI:   " + str(computer_score) + "   |   "
                                   + "YOU:   " + str(player_score), True, TEXT_COLOR, BACKGROUND_COLOR)
    scoreboard_rect = scoreboard.get_rect()
    scoreboard_rect.centerx = surface_rect.centerx
    scoreboard_rect.x += 24
    scoreboard_rect.y = 50

    window_surface.fill(BACKGROUND_COLOR)

    # Net
    net = surface_rect.centerx
    net_rect0 = pygame.Rect(net, 0, 7, 7)
    net_rect1 = pygame.Rect(net, 60, 7, 7)
    net_rect2 = pygame.Rect(net, 120, 7, 7)
    net_rect3 = pygame.Rect(net, 180, 7, 7)
    net_rect4 = pygame.Rect(net, 240, 7, 7)
    net_rect5 = pygame.Rect(net, 300, 7, 7)
    net_rect6 = pygame.Rect(net, 360, 7, 7)
    net_rect7 = pygame.Rect(net, 420, 7, 7)
    net_rect8 = pygame.Rect(net, 480, 7, 7)
    net_rect9 = pygame.Rect(net, 540, 7, 7)
    net_rect10 = pygame.Rect(net, 595, 7, 7)

    pygame.draw.rect(window_surface, TEXT_COLOR, (net_rect0.left, net_rect0.top, net_rect0.width, net_rect0.height))
    pygame.draw.rect(window_surface, TEXT_COLOR, (net_rect1.left, net_rect1.top, net_rect1.width, net_rect1.height))
    pygame.draw.rect(window_surface, TEXT_COLOR, (net_rect2.left, net_rect2.top, net_rect2.width, net_rect2.height))
    pygame.draw.rect(window_surface, TEXT_COLOR, (net_rect3.left, net_rect3.top, net_rect3.width, net_rect3.height))
    pygame.draw.rect(window_surface, TEXT_COLOR, (net_rect4.left, net_rect4.top, net_rect4.width, net_rect4.height))
    pygame.draw.rect(window_surface, TEXT_COLOR, (net_rect5.left, net_rect5.top, net_rect5.width, net_rect5.height))
    pygame.draw.rect(window_surface, TEXT_COLOR, (net_rect6.left, net_rect6.top, net_rect6.width, net_rect6.height))
    pygame.draw.rect(window_surface, TEXT_COLOR, (net_rect7.left, net_rect7.top, net_rect7.width, net_rect7.height))
    pygame.draw.rect(window_surface, TEXT_COLOR, (net_rect8.left, net_rect8.top, net_rect8.width, net_rect8.height))
    pygame.draw.rect(window_surface, TEXT_COLOR, (net_rect9.left, net_rect9.top, net_rect9.width, net_rect9.height))
    pygame.draw.rect(window_surface, TEXT_COLOR, (net_rect10.left, net_rect10.top, net_rect10.width, net_rect10.height))

    sprites.draw(window_surface)

    PlayerPaddle.move(paddle_p)
    PlayerPaddle2.move(paddle_p2)
    PlayerPaddle3.move(paddle_p3)
    ComputerPaddle.update(paddle_c, ball)
    ComputerPaddle2.update(paddle_c2, ball)
    ComputerPaddle3.update(paddle_c3, ball)
    ball.move()
    hit()
    ball.reset()

    if ball.rect.x >= 1198 or (ball.rect.y <= 3 and ball.rect.x >= 600) or (ball.rect.y >= 597 and ball.rect.x >= 600):
        computer_score += 1
    elif ball.rect.x <= 4 or (ball.rect.y <= 3 and ball.rect.x < 600) or (ball.rect.y >= 597 and ball.rect.x < 600):
        player_score += 1

    window_surface.blit(scoreboard, scoreboard_rect)
    pygame.display.update()

    # win/lose conditions
    if ROUND <= 5 or player_win != 3 or computer_win != 3:
        if player_score > computer_score + 2 and player_score >= 11:
            victory1.play()
            player_score = 0
            computer_score = 0
            player_win += 1
            if player_win == 3:
                match_over = match_over_font.render("PLAYER WINS", True, TEXT_COLOR, BACKGROUND_COLOR)
                match_over_rect = match_over.get_rect()
                match_over_rect.centerx = surface_rect.centerx
                match_over_rect.centery = surface_rect.centery - 50

                window_surface.blit(match_over, match_over_rect)

                pygame.mixer_music.stop()
                victory2.play()
                pygame.display.update()
                pygame.time.wait(5000)
                match_over = True
            else:
                ROUND += 1

        elif computer_score > player_score + 2 and computer_score >= 11:
            pygame.mixer_music.pause()
            failure1.play()
            player_score = 0
            computer_score = 0
            computer_win += 1
            if computer_win == 3:
                match_over = match_over_font.render("COMPUTER WINS YOU LOSE", True, TEXT_COLOR, BACKGROUND_COLOR)
                match_over_rect = match_over.get_rect()
                match_over_rect.centerx = surface_rect.centerx
                match_over_rect.centery = surface_rect.centery - 50

                window_surface.blit(match_over, match_over_rect)

                pygame.mixer_music.stop()
                failure2.play()
                pygame.display.update()
                pygame.time.wait(5000)
                match_over = True
            else:
                ROUND += 1

        if match_over is True:
            window_surface.fill(BACKGROUND_COLOR)
            draw_text('Pong No Walls', title_font, window_surface, (WIDTH / 3),
                    (HEIGHT / 3))
            draw_text('Play again?', title_font2, window_surface,
                  (WIDTH / 3) - 20, (HEIGHT / 3) + 100)
            pygame.display.update()
            wait_for_player_to_press_key()
