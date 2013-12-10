#--coding:utf8--

import pygame
from pygame.locals import *
from sys import exit

from settings import *
from roles import Player

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_CAPTION)
background = pygame.image.load(BACKGROUND_IMG).convert()

player_pos = [200, 600]
player = Player(player_pos)

clock = pygame.time.Clock()

def main():
    done = False
    while done == False:
        clock.tick(60)

        screen.fill(0)
        screen.blit(background, (0, 0))

        player.show(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # 监听键盘事件
        key_pressed = pygame.key.get_pressed()
        # 若玩家被击中，则无效
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.moveRight()


if __name__ == '__main__':
    main()
