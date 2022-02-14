import pygame
import random

class Virus(pygame.sprite.Sprite):

    def __init__(self,pos,split_time):
        super().__init__()
        self.image = pygame.image.load("virus.png")
        self.image = pygame.transform.smoothscale(self.image,(15,15))

        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.speed = pygame.math.Vector2(0,5)
        self.speed.rotate_ip(random.randint(0,360))
        self.split_time = split_time

        self.timer = 0


    def update(self):
        self.timer += 1

        self.rect.move_ip(self.speed)
        screen_info = pygame.display.Info()
        width,height = screen_info.current_w,screen_info.current_h

        if self.rect.left < 0:
            self.rect.left = 0
            self.speed[0] *= -1

        if self.rect.right > width:
            self.rect.right = width
            self.speed[0] *= -1

        if self.rect.top < 0:
            self.rect.top = 0
            self.speed[1] *= -1

        if self.rect.bottom > height:
            self.rect.bottom = height
            self.speed[1] *= -1


        if self.timer % self.split_time == 0:
            new_virus = Virus(self.rect.center,self.split_time)
            self.groups()[0].add(new_virus)