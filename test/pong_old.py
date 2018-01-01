#! /usr/bin/env python3

import sys
import pygame

################################################################################
# Racket                                                                       #
################################################################################
class Racket(object):
    def __init__(self, y, max_speed):
        self.y = y
        self.max_speed = max_speed
        self.racket = pygame.image.load("../images/racket.png")
        self.coords = self.racket.get_rect()

    def move(self, up):
        if up == True:
            self.speed = self.max_speed
        else:
            self.speed = -self.max_speed

    def get_speed(self):
        return self.speed

    def get_y(self):
        return self.y


################################################################################
# Ball                                                                         #
################################################################################
class Ball(object):
    def throw(self, width, height):
        self.coords.left = 2*width/3
        self.coords.top = height/2

    def __init__(self, speed, gravity):
        self.speed = speed
        
        self.gravity = gravity
        self.ball = pygame.image.load("../images/ball.png")
        self.coords = self.ball.get_rect()
        

################################################################################
# Score                                                                        #
################################################################################
class Score(object):
    def __init__(self):
        self.player_1 = 0
        self.player_2 = 0

    def add_point_player_1(self):
        self.player_1 += 1

    def add_point_player_2(self):
        self.player_2 += 1
        
    def get_score_player_1 (self):
        return self.player_1

    def get_score_player_2 (self):
        return self.player_2
    
################################################################################
# Game                                                                         #
################################################################################
class Game(object):
    def __init__(self):
        self.width = 800
        self.height = 600

        # Games paramèters
        self.racket_max_speed = 4
        self.ball_speed = 2
        self.ball_gravity = 0

        # Background init
        self.bg_R = 229
        self.bg_V = 228
        self.bg_B = 240
        self.background_color = (self.bg_R, self.bg_V, self.bg_B)

        # Init pygame lib
        pygame.init()
        self.screen = pygame.display.set_mode( (self.width, self.height) )

        # Init Games Objects
        self.player_1 = Racket(self.height/2, self.racket_max_speed)
        self.player_2 = Racket(self.height/2, self.racket_max_speed)
        self.ball = Ball(2, 0)
        self.score = Score()
    
    def throw_ball(self):
        self.ball.throw(self.width, self.height)

    def update_screen(self):
        self.screen.fill(self.background_color)
        self.screen.blit(self.player_1.racket, self.player_1.coords)
        self.screen.blit(self.player_2.racket, self.player_2.coords)
        self.screen.blit(self.ball.ball, self.ball.coords)
        pygame.display.flip()
        
    def delay(self):
        pygame.time.delay(10)
