#--coding:utf8--

import pygame
import random
from settings import *


shoot_img = pygame.image.load(SHOOT_IMG)
player_rect = []
player_rect.append(pygame.Rect(0, 99, 102, 126))        # 玩家精灵图片区域
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126))     # 玩家爆炸精灵图片区域
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))

class Player(pygame.sprite.Sprite):
    def __init__(self, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []

        for i in range(len(player_rect)):
            self.image.append(shoot_img.subsurface(player_rect[i]).convert_alpha())
        self.rect = player_rect[0]                      # 初始化图片所在的矩形
        self.rect.topleft = init_pos                    # 初始化矩形的左上角坐标
        self.speed = 8                                  # 初始化玩家速度，这里是一个确定的值
        self.bullets = pygame.sprite.Group()            # 玩家飞机所发射的子弹的集合
        self.img_index = 0                              # 玩家精灵图片索引
        self.is_hit = False                             # 玩家是否被击中

        self.frequence = 15

    def shoot(self):
        if not self.is_hit and self.frequence == 15:
            bullet = Bullet(self.rect.midtop)
            self.bullets.add(bullet)

        for bullet in self.bullets:
            bullet.move()
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)

    def show(self, screen):
        if not self.is_hit:
            screen.blit(self.image[self.img_index], self.rect)
            # 更换图片索引使飞机有动画效果
            self.frequence -= 1
            if self.frequence < 0:
                self.frequence = 15
            self.img_index = self.frequence / 8

            self.bullets.draw(screen)

    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed 

    def moveDown(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed


bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_image = shoot_img.subsurface(bullet_rect)
  
class Bullet(pygame.sprite.Sprite):
    def __init__(self, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed

# 定义敌机对象使用的surface相关参数
enemy_rect = pygame.Rect(534, 612, 57, 43)
enemy_img = shoot_img.subsurface(enemy_rect)
enemy_down_imgs = []
enemy_down_imgs.append(shoot_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy_down_imgs.append(shoot_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy_down_imgs.append(shoot_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy_down_imgs.append(shoot_img.subsurface(pygame.Rect(930, 697, 57, 43)))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.down_imgs = enemy_down_imgs
        self.speed = 2
        self.down_index = 0

    def move(self):
        self.rect.top += self.speed

class EnemyCollection(object):
    def __init__(self):
        self.frequence = 0
        self.enemies = pygame.sprite.Group()

    def add_enemy(self):
        if self.frequence % 50 == 0:
            enemy_pos = [random.randint(0, SCREEN_WIDTH - enemy_rect.width), 0]
            enemy = Enemy( enemy_pos)
            self.enemies.add(enemy)
        self.frequence += 1
        if self.frequence >= 100:
            self.frequence = 0

    def move(self):
        for enemy in self.enemies:
            enemy.move()
            if enemy.rect.top < 0:
                self.enemies.remove(enemy)
        

    def show(self, screen):
        self.add_enemy()
        self.move()
        self.enemies.draw(screen)

class EnemyDownCollection(object):
    def __init__(self):
        self.enemies = pygame.sprite.Group()

    def add(self, enemies):
        for enemy in enemies:
            self.enemies.add(enemy)

    def show(self, screen):
        for enemy in self.enemies:
            if enemy.down_index > 7:
                self.enemies.remove(enemy)
                continue
            screen.blit(enemy.down_imgs[enemy.down_index / 2], enemy.rect)
            enemy.down_index += 1

