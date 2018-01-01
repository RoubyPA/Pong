#!/usr/bin/env python3

import sys
import pygame

################################################################################
# Class Paddle
################################################################################
class Paddle(object):
    def __init__(self, y, max_speed):
        "init player paddle"
        self.y = y # not used
        self.max_speed = max_speed # not used
        self.paddle_speed = paddle_speed = [ 0, 0 ]
        self.image = pygame.image.load("../images/lightsaber_green.png")
        self.coords = self.image.get_rect()
        
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
    def __init__(self, x, y, vx, vy, radius, colour, image = 0):
        "Init ball object"
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.colour = colour
        self.paddle_coords = paddle_coords = [ 0, 0 ]

        # if image != 0:

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
    def __init__(self):
        self.width = 1500
        self.height = 600

        # Games parameters
        self.paddle_max_speed = 4

        # Ball parameters
        self.ball_gravity = 0
        self.ball_x = 300
        self.ball_y = 300
        self.ball_vx = 4 # velocity along the x axis
        self.ball_vy = 4
        self.ball_radius = 20
        self.ball_color = (0,0,0)

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
        self.ball = Ball(self.ball_x, self.ball_y, self.ball_vx, self.ball_vy, self.ball_radius, self.ball_color)
        self.score = Score()

    def draw(self):
        self.screen.fill(self.background_color)
        self.ball.draw(self.screen)
        self.ball.move()
        self.ball.bounce(self.width, self.height)
        self.ball.paddle_collision(self.player_1.get_coords())

        self.player_1.draw(self.width, self.height)
        self.screen.blit(self.player_1.image, self.player_1.get_coords())

        pygame.display.flip()

    def delay(self):
        pygame.time.delay(10)


    def event(self, event):
        # Check for exit
        if event.type == pygame.QUIT:
            sys.exit()
            
        # Check for paddle movements
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.player_1.move_paddle("up")
                pass
            elif event.key == pygame.K_DOWN:
                self.player_1.move_paddle("down")
                pass
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.player_1.move_paddle("stop")
                    pass
                elif event.key == pygame.K_DOWN:
                    self.player_1.move_paddle("stop")
                    pass
