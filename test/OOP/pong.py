#!/usr/bin/env python3

import sys
import pygame

class Racket(object):
    def __init__(self, y, speed):
        self.y = y
        self.speed = speed
        self.racket_coords = racket_coords.move(racket_speed)
        
    def behaviour(self):
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
    def __init__(self, x=0, y=0, speed=[0,0]):
        self.x = x
        self.y = y
        self.speed = speed
        self.ball_coords = ball_coords.move(ball_speed)

    def bounce(self):
        if ball_coords.left < 0 or ball_coords.right >= width:
            ball_speed[0] = -ball_speed[0]
        if ball_coords.top < 0 or ball_coords.bottom >= height:
            ball_speed[1] = -ball_speed[1]

    def throw(self):
        self.ball_coords.left = 2*self.width/3
        self.ball_coords.top = self.height/2

        
class Score(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        
class Game(object):
    def __init__(self):
        self.width = 800
        self.height = 600
        self.background_color = (229,228,240)
        self.ball_speed = [ -2, -2 ]
        self.racket_speed = [ 0, 0 ]
        self.ball = pygame.image.load("../../images/ball.png")
        self.ball_coords = self.ball.get_rect()
        self.racket = pygame.image.load("../../images/lightsaber_green.png")
        self.racket_coords = self.racket.get_rect()
        self.screen = pygame.display.set_mode( (self.width, self.height) )
        
        pygame.init()

        Ball().throw()

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

            Ball().bounce()
            self.draw()
            
            
    def draw(self):
        self.screen.fill(background_color)
        self.screen.blit(ball, ball_coords)
        self.screen.blit(racket, racket_coords)
        pygame.display.flip()
        pygame.time.delay(10)


# if __name__ == "__main__":
#     Game().play()
