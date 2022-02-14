import pygame
import random

class Doctor(pygame.sprite.Sprite):

    def __init__(self,pos):
        super().__init__()
        self.image = pygame.image.load("doctor.png")
        self.image = pygame.transform.smoothscale(self.image,(15,15))

        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.speed = pygame.math.Vector2(0,5)
        self.speed.rotate_ip(random.randint(0,360))

    def update(self):
        self.rect.move_ip(self.speed)
        screen_info = pygame.display.Info()
        width,height = screen_info.current_w,screen_info.current_h

        if self.rect.left < 0:
            self.rect.left = 0
            self.speed[0] *= -1

        if self.rect.top < 0:
            self.rect.top = 0
            self.speed[1] *= -1

        if self.rect.right > width:
            self.rect.right = width
            self.speed[0] *= -1

        if self.rect.bottom > height:
            self.rect.bottom = height
            self.speed[1] *= -1
