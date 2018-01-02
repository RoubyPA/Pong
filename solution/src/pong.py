#!/usr/bin/env python3

import sys
import pygame

################################################################################
# Class Paddle
################################################################################
class Paddle(object):
    def __init__(self, max_speed, player):
        "init player paddle"
        self.player = player
        self.max_speed = max_speed # not used
        self.paddle_speed = [ 0, 0 ]

        if player == 1:
            self.image = pygame.image.load("../images/racket_b.png")
        else:
            self.image = pygame.image.load("../images/racket_r.png")
        self.coords = self.image.get_rect()

        self.state = "stop"
        
    def move_paddle(self, direction):
        "Move paddle up if direction == up"
        self.direction = direction
        if self.direction == "up":
            self.paddle_speed[1] = -5
        elif self.direction == "down":
            self.paddle_speed[1] = 5
        else:
            self.paddle_speed[1] = 0
                
    def draw(self, width, height):
        self.coords = self.coords.move(self.paddle_speed)
    
        if self.coords.left < 0:
            self.coords.left = 0
        elif self.coords.right >= width:
            self.coords.right = width-1
        if self.coords.top < 0:
            self.coords.top = 0
        elif self.coords.bottom >= height:
            self.coords.bottom = height-1

    def get_coords(self):
        return self.coords.move(self.paddle_speed)
            
    def get_speed(self):
        "get self.speed"
        return self.speed

    def get_y(self):
        "get self.y"
        return self.get_y

    def rect(self):
        "to use or to remove in the future"
        # Rect(left, top, width, height)
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)   
        

################################################################################
# Class Ball
################################################################################
class Ball(object):
    def __init__(self, x, y, vx, vy, radius, player):
        "Init ball object"
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.player = player

        self.blue = (30,144,255)
        self.red = (178,34,34)

        if self.player == True:
            self.colour = self.blue #blue
        else:
            self.colour = self.red #red
        
        # self.paddle_coords = paddle_coords = [ 0, 0 ]

    def move(self):
        "move the ball"
        self.x += self.vx
        self.y += self.vy

    def rect(self):
        "to use or to remove in the future"
        # Rect(left, top, width, height)
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)
                
    def bounce(self, width, height):
        "bounce the ball on the walls"
        if self.x - self.radius < 0 or self.x + self.radius >= width:
              self.vx = -self.vx
        if self.y - self.radius < 0 or self.y + self.radius >= height:
              self.vy = -self.vy

        if self.x - self.radius < 0 and self.colour == self.blue:
            self.colour = self.red
        elif self.x - self.radius < 0 and self.colour == self.red:
            self.colour = self.blue

    def paddle_collision(self, paddle_coords):
        "detect paddle collision"
        if self.x - self.radius < 0:
            if self.y - self.radius < paddle_coords.bottom and self.y + self.radius > paddle_coords.top:
                print("touch!")
            else:
                print("lost!")

    def draw(self, surface):
        pygame.draw.circle(surface, self.colour, (self.x, self.y), self.radius, 0)

    def throw(self):
        "Use random, this method should be in Game"
                
        
################################################################################
# Class Item (bonus, malus, etc) + subclasses
################################################################################
class Item(object):
    "Item class, will serve as a superclass for bonus elements, see example below"
    def __init__(self, x, y, vx, vy, ):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        
# class RMS(Item):
#     "Will replace or place RMS face on ball, or send a RMS face to the oponent, don't know"

# class BillGates(Item):
#     "This one is clearly a malus, add a 'hahaha' sound to it"

# class SteveBalmer(Item):
#     "A malus too"

# class Torvalds(Item):
# class JWZ(Item):
# class Doom(Item):
# class KungFurry(Item):
        
################################################################################
# Class Score
################################################################################
class Score(object):
    def __init__(self):
        "todo: write a graphical module that go on top of the elements"
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
# Class Game
################################################################################
class Game(object):
    def __init__(self, server_mode):
        self.width = 800
        self.height = 600

        # Games parameters
        paddle_max_speed = 4

        # Ball parameters
        ball_gravity = 0
        ball_x = 300
        ball_y = 300
        ball_vx = 4 # velocity along the x axis
        ball_vy = 4
        ball_radius = 20
        ball_color = (0,0,0)

        # Background init
        self.bg_R = 229
        self.bg_V = 228
        self.bg_B = 240
        self.background_color = (self.bg_R, self.bg_V, self.bg_B)        

        # Init pygame lib
        pygame.init()
        self.screen = pygame.display.set_mode( (self.width, self.height) )

        # Init Games Objects
        self.player_1 = Paddle(paddle_max_speed, 1)
        self.player_2 = Paddle(paddle_max_speed, 2)
        self.ball = Ball(ball_x, ball_y, ball_vx, ball_vy, ball_radius, server_mode)
        self.score = Score()

        # who am i ?
        if server_mode == True:
            self.curent_player = self.player_1
            self.me = self.player_1
        else:
            self.curent_player = self.player_2
            self.me = self.player_2
            
    def draw(self):
        self.screen.fill(self.background_color)
        self.ball.draw(self.screen)
        self.ball.move()
        self.ball.bounce(self.width, self.height)
        self.ball.paddle_collision(self.player_1.get_coords())

        self.player_1.draw(self.width, self.height)
        self.screen.blit(self.player_1.image, self.player_1.get_coords())

        self.player_2.draw(self.width, self.height)
        self.screen.blit(self.player_2.image, self.player_2.get_coords())

        pygame.display.flip()

    def delay(self, timer):
        timer = timer*1000
        
        if timer < 0:
            timer = 0
        elif timer > 10:
            timer = 10
        
        pygame.time.delay(10-int(timer))


    def event(self, event):
        # Check for exit
        if event.type == pygame.QUIT:
            sys.exit(1)
            
        # Check for paddle movements
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.player_1.move_paddle("up")
                return "up"
            elif event.key == pygame.K_DOWN:
                self.player_1.move_paddle("down")
                return "down"
            

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.player_1.move_paddle("stop")
                return "stop"
            elif event.key == pygame.K_DOWN:
                self.player_1.move_paddle("stop")
                return "stop"

        return "nope"
