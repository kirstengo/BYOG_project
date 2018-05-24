import pygame, sys, time, random

WIN_H = 670
WIN_W = 1200
fps = 60
paddle_height = 5
paddle_width = 150
pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (119, 157, 255)
RED = (255, 64, 34)
PURPLE = (184, 120, 255)
YELLOW = (255, 243, 17)
ORANGE = (255, 166, 33)
GREEN = (65, 255, 85)
screen = pygame.display.set_mode((WIN_W, WIN_H), pygame.SRCALPHA)
play = intro = outro = True
BLOCK_WIDTH = 50
BLOCK_HEIGHT = 30
BLOCK_X = 20
TOP = 100

BLOCK_COUNTER = 36
LIVES = 5

# Classes

class Text():
    def __init__(self, size, text, x, y):
        self.font = pygame.font.Font(None, size)
        self.image = self.font.render(text, 1, BLACK)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)


class Score(pygame.sprite.Sprite):
    def __init__(self, type, size, color, position):
       pygame.sprite.Sprite.__init__(self)
       self.type = type
       self.color = color
       self.position = position
       self.font = pygame.font.Font(None, size)

    def update(self):
       if self.type == "blocks":
           text = "Blocks Left: " + str(BLOCK_COUNTER)
       else:
           text = "Lives: " + str(LIVES)

       self.image = self.font.render(str(text), 1, self.color)
       self.rect = self.image.get_rect()
       self.rect.move_ip(self.position[0] - self.rect.width / 2, self.position[1])


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.color = random.randint(1, 7)
        self.image = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT)).convert()
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.image.fill(self.update())

    def update(self):
        if self.color == 1:
            return YELLOW
        elif self.color == 2:
            return RED
        elif self.color == 3:
            return BLUE
        elif self.color == 4:
            return BLACK
        elif self.color == 5:
            return PURPLE
        elif self.color == 6:
            return ORANGE
        elif self.color == 7:
            return GREEN


class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 5
        self.image = pygame.Surface((paddle_width, paddle_height)).convert()
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if key[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIN_W:
            self.rect.right = WIN_W


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.speed = [5, 5]
        self.height = 10
        self.width = 10
        self.image = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def collide_walls(self):
        if self.rect.top <= 50:
            self.speed = (self.speed[0], -self.speed[1])
        if self.rect.right >= WIN_W - self.rect.width:
            self.speed = (-self.speed[0], self.speed[1])
        if self.rect.left <= 0:
            self.speed = (-self.speed[0], self.speed[1])

    def reset(self, paddle):
        global LIVES
        if self.rect.top > WIN_H - self.rect.height:
            self.rect.x = WIN_W/2
            self.rect.y = 400
            paddle.rect.x = 540
            paddle.rect.y = 600
            LIVES -= 1
            time.sleep(1.5)
            self.rect.move(self.speed)

    def collide_objects(self, paddle_group, block_group):
        global BLOCK_COUNTER
        paddle_collisions = pygame.sprite.spritecollide(self, paddle_group, False)
        for b in paddle_collisions:
            self.speed = (self.speed[0], -self.speed[1])

        block_collisions = pygame.sprite.spritecollide(self, block_group, True)
        for p in block_collisions:
            self.speed = (self.speed[0], -self.speed[1])
            BLOCK_COUNTER -= 1


def check_wins():
    global BLOCK_COUNTER, play, outro, LIVES
    if BLOCK_COUNTER == 0 or LIVES == 0:
        play = False
        outro = True


def create_blocks(block_group):
    global BLOCK_X
    for row in range(12):
        block = Block(BLOCK_X, TOP)
        block_2 = Block(BLOCK_X, (TOP + 50))
        block_3 = Block(BLOCK_X, (TOP + 100))
        block_group.add(block, block_2, block_3)
        BLOCK_X += 100


def main():
    # Initialize variables
    global outro, intro, play, BLOCK_X, BLOCK_COUNTER, LIVES
    clock = pygame.time.Clock()
    top_buffer = 50

    # Create Game Objects
    ball = Ball(WIN_W/2, 400)
    paddle = Paddle(540, 600)
    title = Text(100, "Breakout Remake", 300, 250)
    subtitle = Text(50, "--Click here--", 475, WIN_H / 1.8)
    you_win = Text(100, "You win!", 450, 250)
    again = Text(50, "--Click to Restart--", 475, WIN_H / 1.8)
    game_over = Text(100, "Game Over!", 450, 250)
    horizontal = pygame.Surface((WIN_H + 600, 1)).convert()
    blocks_left = Score("blocks", 40, BLACK, (WIN_W / 5 + 50, 10))
    lives = Score("lives", 40, BLACK, ((WIN_W / 2 + 300), 10))

    # Create Groups
    paddle_group = pygame.sprite.Group()
    paddle_group.add(paddle)
    block_group = pygame.sprite.Group()
    score_group = pygame.sprite.Group()
    score_group.add(blocks_left, lives)


    # Create blocks
    create_blocks(block_group)

    while True:
    # Intro Loop
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                    intro = False

                screen.fill(WHITE)
                screen.blit(title.image, title.rect)
                if pygame.time.get_ticks() % 1000 < 500:
                    screen.blit(subtitle.image, subtitle.rect)
                clock.tick(fps)
                pygame.display.flip()

    # Game Loop
        while play:
            # Checks if window exit button pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Keypresses
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            # Update Groups
            paddle_group.update()
            ball.collide_walls()
            ball.reset(paddle)
            ball.collide_objects(paddle_group, block_group)
            block_group.update()
            score_group.update()
            check_wins()
            # Print Groups
            screen.fill(WHITE)
            score_group.draw(screen)
            paddle_group.draw(screen)
            screen.blit(ball.image, ball.rect)
            block_group.draw(screen)
            screen.blit(horizontal, (0, top_buffer))
            ball.rect = ball.rect.move(ball.speed)
            # Limits frames per iteration of while loop
            clock.tick(fps)
            # Writes to main surface
            pygame.display.flip()

        while outro:
            screen.fill(WHITE)
            if BLOCK_COUNTER == 0:
                screen.blit(you_win.image, you_win.rect)
                if pygame.time.get_ticks() % 1000 < 500:
                    screen.blit(again.image, again.rect)

            if LIVES == 0:
                screen.blit(game_over.image, game_over.rect)
                if pygame.time.get_ticks() % 1000 < 500:
                    screen.blit(again.image, again.rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                    outro = False
                    intro = True
                    play = True
                    paddle.rect.move(540, 600)
                    ball.rect.move(WIN_W/2, 400)
                    BLOCK_COUNTER = 36
                    BLOCK_X = 20
                    LIVES = 5
                    create_blocks(block_group)

            clock.tick(fps)
            pygame.display.flip()

if __name__ == "__main__":
    main()
