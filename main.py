import pygame
from random import randrange as rnd

from Ball import Ball
from Block import Block
from Paddle import Paddle

WIDTH, HEIGHT = 1200, 800
fps = 60

# paddle settings
PADDLE_W = 150
PADDLE_H = 20
PADDLE_SPEED = 15

paddle = Paddle(WIDTH // 2 - PADDLE_W // 2, HEIGHT - PADDLE_H - 10, PADDLE_W, PADDLE_H, PADDLE_SPEED, pygame.Color('darkorange'))

# ball settings
BALL_RADIUS = 10
BALL_SPEED = 8

ball = Ball(BALL_RADIUS, BALL_SPEED, WIDTH // 2 - BALL_RADIUS // 2, HEIGHT // 2, pygame.Color('white'))

BLOCKS_MARGIN_TOP = 70
BLOCKS_MARGIN_LEFT = 10

BLOCK_DISTANCE_X = 10
BLOCK_DISTANCE_Y = 10

BLOCK_WIDTH = 50
BLOCK_HEIGHT = 20

# blocks settings
block_list = [Block(BLOCKS_MARGIN_LEFT + (BLOCK_WIDTH + BLOCK_DISTANCE_X) * i,
                          BLOCKS_MARGIN_TOP + (BLOCK_HEIGHT + BLOCK_DISTANCE_Y) * j,
                          BLOCK_WIDTH, BLOCK_HEIGHT, pygame.Color('lightblue'))
              for i in range(20) for j in range(8)]

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
# background image
img = pygame.image.load('background.png')
img = pygame.transform.scale(img, (WIDTH, HEIGHT))

#ending config
font_end = pygame.font.SysFont('Arial', 66, bold=True)


def detect_collision(dx, dy, ball, hitShape):
    if dx > 0:
        delta_x = ball.shape.right - hitShape.left
    else:
        delta_x = hitShape.right - ball.shape.left
    if dy > 0:
        delta_y = ball.shape.bottom - hitShape.top
    else:
        delta_y = hitShape.bottom - ball.shape.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy

def handlePaddleControl():
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.shape.left > 0:
        paddle.moveLeft()
    if key[pygame.K_RIGHT] and paddle.shape.right < WIDTH:
        paddle.moveRight()

def close_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

def handleEndGame():
    # win, game over
    if ball.shape.bottom > HEIGHT:
        render_end = font_end.render('GAME OVER', 1, pygame.Color('orange'))
        sc.blit(render_end, (WIDTH // 2 - 200, HEIGHT // 3))
        pygame.display.flip()
        close_game()
    elif not len(block_list):
        render_end = font_end.render('YOU WIN!!!', 1, pygame.Color('orange'))
        sc.blit(render_end, (WIDTH // 2 - 200, HEIGHT // 3))
        pygame.display.flip()
        close_game()

def drawBackground():
    sc.blit(img, (0, 0))

def drawObjects():
    [pygame.draw.rect(sc, block.color, block.shape) for block in block_list]

    paddleImg = pygame.image.load('platform.png')
    paddleImg = pygame.transform.scale(paddleImg, (paddle.width, paddle.height))
    sc.blit(paddleImg, paddle.shape)

    pygame.draw.circle(sc, ball.color, ball.shape.center, ball.radius)

def handleBallMovement():
    ball.move()

    # collision left right
    if ball.shape.centerx < ball.radius or ball.shape.centerx > WIDTH - ball.radius:
        ball.dx = -ball.dx
    # collision top
    if ball.shape.centery < ball.radius:
        ball.dy = -ball.dy
    # collision paddle
    if ball.shape.colliderect(paddle.shape) and ball.dy > 0:
        ball.dx, ball.dy = detect_collision(ball.dx, ball.dy, ball, paddle.shape)

    # collision blocks
    hit_index = ball.shape.collidelist([block.shape for block in block_list])
    if hit_index != -1:
        hit_block = block_list.pop(hit_index)
        ball.dx, ball.dy = detect_collision(ball.dx, ball.dy, ball, hit_block.shape)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    drawBackground()

    drawObjects()

    handleBallMovement()

    handlePaddleControl()

    handleEndGame()

    # update screen
    pygame.display.flip()
    clock.tick(fps)