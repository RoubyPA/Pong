#!/usr/bin/env python3

import sys
import pygame

################################################################################
# Class Paddle
################################################################################
class Paddle(object):
    def __init__(self, y, max_speed):
        "init player paddle"
        self.y = y
        self.max_speed = max_speed
        self.image = pygame.image.load("images/lightsaber_green.png")
        self.coords = self.image.get_rect()

    def move(self, up):
        "Move paddle up if up == True or down"
        if up == True:
            self.speed = speed
        else:
            self.speed = -speed

    def get_speed(self):
        "get self.speed"
        return self.speed

    def get_y(self):
        "get self.y"
        return self.y


################################################################################
# Class Ball
################################################################################
class Ball(object):
    def throw(self):
        self.coords.left = 2*self.width/3
        self.coords.top = self.height/2

    def __init__(self, speed=1, gravity=1):
        self.width = 1
        self.height = 1
        self.speed = speed
        self.gravity = gravity
        self.image = pygame.image.load("images/ball.png")
        self.coords = self.image.get_rect()
        self.throw()
        
    def bounce(self):
        ball_coords = ball_coords.move(ball_speed)

        if ball_coords.left < 0 or ball_coords.right >= width:
            ball_speed[0] = -ball_speed[0]
        if ball_coords.top < 0 or ball_coords.bottom >= height:
            ball_speed[1] = -ball_speed[1]


################################################################################
# Class Score
################################################################################
class Score(object):
    def __init__(self):
        self.player_1 = 0
        self.player_2 = 0

    def add_player1(self):
        self.player_1 += 1

    def add_player2(self):
        self.player_2 += 1
        
        
################################################################################
# Class Game
################################################################################
class Game(object):
    def __init__(self):
        self.width = 800
        self.height = 600

        # Games parameters
        self.paddle_max_speed = 4
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
        self.player_1 = Paddle(self.height/2, self.paddle_max_speed)
        self.player_2 = Paddle(self.height/2, self.paddle_max_speed)
        self.ball = Ball()
        self.score = Score()
    
    def draw(self):
        self.screen.fill(self.background_color)
        self.screen.blit(self.ball, self.ball.coords)
        self.screen.blit(self.player_1, self.player_1.coords)
        self.screen.blit(self.player_2, self.player_2.coords)
        pygame.display.flip()
        pygame.time.delay(10)

        
    def play(self):
        while True:
            for e in pygame.event.get():
                # Check for exit
                if e.type == pygame.QUIT:
                    sys.exit()
                    
                # Check for paddle movements
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP:
                        paddle_speed[1] = -4
                        pass
                    elif e.key == pygame.K_DOWN:
                        paddle_speed[1] = 4
                        pass

                elif e.type == pygame.KEYUP:
                    if e.key == pygame.K_UP:
                        paddle_speed[1] = 0
                        pass
                    elif e.key == pygame.K_DOWN:
                        paddle_speed[1] = 0
                        pass

            self.draw()
            
toto = Game().play()
