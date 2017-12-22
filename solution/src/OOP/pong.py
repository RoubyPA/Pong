#!/usr/bin/env python3

import sys
import pygame

class Racket(object):
    def __init__(self, y, speed):
        self.y = y
        self.speed = speed


    def behaviour(self):
        racket_coords = racket_coords.move(racket_speed)
        # Clip racket on court
        if racket_coords.left < 0:
            racket_coords.left = 0
        elif racket_coords.right >= width:
            racket_coords.right = width-1
        if racket_coords.top < 0:
            racket_coords.top = 0
        elif racket_coords.bottom >= height:
            racket_coords.bottom = height-1

       
class Ball(object):
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def bounce(self):
        ball_coords = ball_coords.move(ball_speed)

        if ball_coords.left < 0 or ball_coords.right >= width:
            ball_speed[0] = -ball_speed[0]
        if ball_coords.top < 0 or ball_coords.bottom >= height:
            ball_speed[1] = -ball_speed[1]

    def throw(self):
        ball_coords.left = 2*width/3
        ball_coords.top = height/2

        
class Score(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        
class Game(object):
    width = 800
    height = 600

    background_color = (229,228,240)
    
    ball_speed = [ -2, -2 ]
    racket_speed = [ 0, 0 ]

    ball = pygame.image.load("../../images/ball.png")
    ball_coords = ball.get_rect()

    racket = pygame.image.load("../../images/lightsaber_green.png")
    racket_coords = racket.get_rect()

    screen = pygame.display.set_mode( (width, height) )
    

    def __init__(self):
        pygame.init()
        
        def play(self):
            while True:
                for e in pygame.event.get():
                    # Check for exit
                    if e.type == pygame.QUIT:
                        sys.exit()

                    # Check for racket movements
                    elif e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_UP:
                            racket_speed[1] = -4
                            pass
                        elif e.key == pygame.K_DOWN:
                            racket_speed[1] = 4
                            pass

                    elif e.type == pygame.KEYUP:
                        if e.key == pygame.K_UP:
                            racket_speed[1] = 0
                            pass
                        elif e.key == pygame.K_DOWN:
                            racket_speed[1] = 0
                            pass


            self.draw()

            
        def draw(self):
            self.screen.fill(background_color)
            self.screen.blit(ball, ball_coords)
            self.screen.blit(racket, racket_coords)
            pygame.display.flip()
            pygame.time.delay(10)
