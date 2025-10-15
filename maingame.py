import pygame
from player import Player
from platform_sprite import Platform


pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode(
                                (SCREEN_WIDTH, SCREEN_HEIGHT),
                                 pygame.RESIZABLE)
pygame.display.set_caption("The Scrap Collector")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

player = Player(50, SCREEN_HEIGHT - 32)


all_sprites = pygame.sprite.Group()
all_sprites.add(player)

clock = pygame.time.Clock()


platform_list = pygame.sprite.Group()

level = [
    [0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40],
    [200, SCREEN_HEIGHT - 150, 150, 20],
    [500, SCREEN_HEIGHT - 250, 180, 20],
    [180, SCREEN_HEIGHT - 350, 100, 20],
]


for plat_data in level:
    platform = Platform(plat_data[0], plat_data[1], plat_data[2], plat_data[3])
    platform_list.add(platform)
    all_sprites.add(platform)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.go_left()
            if event.key == pygame.K_RIGHT:
                player.go_right()
            if event.key == pygame.K_SPACE:
                player.jump(platform_list)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.change_x < 0:
                player.stop()
            if event.key == pygame.K_RIGHT and player.change_x > 0:
                player.stop()

    all_sprites.update(platform_list)

    screen.fill(BLACK)
    all_sprites.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
