import math
import os
import pygame
import random
import sys

pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
DARK_GREEN = (54, 114, 75)
YELLOW = (255, 255, 0)
IMPROVE = 5
FPS = 60
V = 1200
CLOCK = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
block_sprites = pygame.sprite.Group()
ball_sprite = pygame.sprite.Group()
plat_sprite = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('arkanoid', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


orange_block = load_image('orange.png')
red_block = load_image('red.png')
blue_block = load_image('blue.png')
purple_block = load_image('purple.png')
platform = load_image('platform.png', WHITE)
ball = load_image('ball.png', BLACK)


class Block(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__(all_sprites)
        self.image = color
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.add(block_sprites)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = platform
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 10
        self.add(plat_sprite)

    def move(self, plat_x):
        self.rect.x = plat_x


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, ball_rect, radius=12):
        super().__init__(all_sprites)
        self.radius = radius
        self.ball_rect = ball_rect
        self.image = ball
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.center = (x + radius, y + radius)
        self.side = math.sqrt(2) * radius / 2
        self.top = self.center[1] + self.side
        self.right = self.center[0] - self.side
        self.bottom = self.center[1] - self.side
        self.left = self.center[0] + self.side
        self.vy = 4
        self.vx = -4

    def update(self, *args, **kwargs):
        self.rect = self.rect.move(self.vx, self.vy)
        plat = pygame.sprite.spritecollideany(self, plat_sprite)
        if plat and self.bottom <= plat.rect.y and self.vy > 0:
            self.vy = -self.vy
            self.plusW()
        spr = pygame.sprite.spritecollideany(self, block_sprites)
        if spr:
            self.colliding(spr)
            spr.kill()
        if self.rect.x < 0 or self.rect.x + 24 > width:
            self.vx = -self.vx
        if self.rect.y < 0:
            self.vy = -self.vy
        if self.rect.y > height:
            print("IT'S A PITY, BUT YOU LOSE")
            exit()

    def plusW(self):
        global IMPROVE
        global V
        if IMPROVE == 0:
            if abs(self.vx) < 7:
                if self.vx > 0:
                    self.vx += 1
                else:
                    self.vx -= 1
                if self.vy > 0:
                    self.vy += 1
                else:
                    self.vy -= 1
                V += 100
            IMPROVE = 3
        else:
            IMPROVE -= 1

    def colliding(self, spr):
        if self.bottom <= spr.rect.y and self.vy > 0:
            self.vy = -self.vy
        elif self.top >= spr.rect.y + 30 and self.vy < 0:
            self.vy = -self.vy
        elif self.right >= spr.rect.x and self.vx < 0:
            self.vx = -self.vx
        elif self.left <= spr.rect.x + 60 and self.vx > 0:
            self.vx = -self.vx

def generate_level(number):
    color_list = [orange_block, red_block, blue_block, purple_block]
    if number == 1:
        for col in range(5):
            color = random.choice(color_list)
            for row in range(10):
                Block(color, row * 80 + 5, col * 40 + 5)
    elif number == 2:
        for col in range(5):
            for row in range(10):
                color = random.choice(color_list)
                Block(color, row * 80 + 5, col * 40 + 5)
    elif number == 3:
        for row in range(10):
            color = random.choice(color_list)
            for col in range(5):
                Block(color, row * 80 + 5, col * 40 + 5)
    elif number == 4:
        for row in range(10):
            color = random.choice(color_list)
            for col in range(random.randint(4, 6)):
                Block(color, row * 80 + 5, col * 40 + 5)
    elif number == 5:
        for row in range(10):
            for col in range(random.randint(4, 6)):
                color = random.choice(color_list)
                Block(color, row * 80 + 5, col * 40 + 5)

def main():
    running = True
    plat_x = 300
    plat_y = 540
    ball_rect = 17
    ball_x = random.randrange(ball_rect, width - ball_rect)
    ball_y = 300
    # генерация уровня
    generate_level(random.randint(1, 5))
    background = load_image('background.jpg')
    plat = Platform(plat_x, plat_y)
    Ball(ball_x, ball_y, ball_rect)
    while running:
        pygame.display.set_caption('THE BEST ARKANOID')
        screen.fill(BLACK)
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and plat_x > 0:
            plat_x -= 10
        if key[pygame.K_RIGHT] and plat_x + 180 < width:
            plat_x += 10
        all_sprites.draw(screen)
        all_sprites.update()
        plat.move(plat_x)
        if not len(block_sprites):
            print('YOU WIN!!!')
            exit()
        CLOCK.tick(FPS)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
