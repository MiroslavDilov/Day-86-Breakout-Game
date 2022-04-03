import pygame

pygame.init()

window = pygame.display.set_mode((800,600))
pygame.display.set_caption("Breakout")

pygame.display.set_icon(pygame.image.load("images/ball.png"))

clock = pygame.time.Clock()

running = True


class Paddle:
    def __init__(self):
        self.x = 400
        self.y = 500
        self.width = 80
        self.height = 20
        self.paddle_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.paddle_rect.center = (self.x, self.y)

    def draw_paddle(self):
        self.paddle_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.paddle_rect.center = (self.x, self.y)
        pygame.draw.rect(window, (135, 67, 86), self.paddle_rect)

    def move_paddle(self, key):
        if key == pygame.K_LEFT and self.paddle_rect.left >= 0:
            self.x -= 2
        elif key == pygame.K_RIGHT and self.paddle_rect.right <= 800:
            self.x += 2

    def get_center(self):
        return self.paddle_rect.center


class Ball:
    def __init__(self):
        self.img = pygame.image.load("images/ball.png")
        self.ball_rect = self.img.get_rect()
        self.started = False
        self.x_move = 1
        self.y_move = -1

    def draw_ball(self, pad_center):
        pad_x = pad_center[0]
        pad_y = pad_center[1]
        if not self.started:
            self.ball_rect.center = pad_x, pad_y - 25
        else:
            self.calc_collision()
        window.blit(self.img, self.ball_rect)

    def calc_collision(self):
        self.ball_rect.center = self.ball_rect.center[0] + self.x_move, self.ball_rect.center[1] + self.y_move
        if self.ball_rect.right >= 800:
            self.x_move = -1
        elif self.ball_rect.left <= 0:
            self.x_move = 1
        elif self.ball_rect.top <= 0:
            self.y_move = 1
        elif self.ball_rect.bottom >= 600:
            self.y_move = -1

    def detect_paddle_collision(self, paddle_rect):
        if self.ball_rect.colliderect(paddle_rect) and ball.ball_rect.center[1] < paddle_rect.center[1]:
            self.y_move = -1

    def start(self):
        self.started = True

    def brick_collide(self, brick_rect):
        if self.ball_rect.top <= brick_rect.bottom:
            if self.ball_rect.right >= brick_rect.left and self.ball_rect.center[1] > brick_rect.center[1]:
                self.x_move = -1
            self.y_move = 1



class Brick():
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 20)

    def draw_brick(self):
        pygame.draw.rect(window, (246, 137, 137), self.rect)

    def detect_collision(self, ball_rect):
        return self.rect.colliderect(ball_rect)


def generate_bricks(rows):
    array = []

    x = 50
    y = 50
    for i in range(rows):
        for j in range(13):
            brick = Brick(x, y)
            array.append(brick)
            x += 55
        x = 50
        y += 30

    return array


bricks = generate_bricks(5)
paddle = Paddle()
ball = Ball()
while running:
    clock.tick(200)
    pygame.key.set_repeat(3)
    window.fill((246, 231, 216))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                paddle.move_paddle(event.key)
            if event.key == pygame.K_SPACE:
                ball.start()

    for brick in bricks:
        brick.draw_brick()

        if brick.detect_collision(ball.ball_rect):
            bricks.remove(brick)
            ball.brick_collide(brick.rect)

    ball.detect_paddle_collision(paddle.paddle_rect)
    ball.draw_ball(paddle.get_center())
    paddle.draw_paddle()
    pygame.display.flip()


