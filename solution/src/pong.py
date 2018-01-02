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
        self.paddle_speed = [ 0, 0 ]
        self.image = pygame.image.load("../images/racket.png")       
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



################################################################################
# Class Ball
################################################################################
class Ball(object):
    def __init__(self, x, y, vx, vy):
        "Init ball object"
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ball_speed = [ self.vx, self.vy ]

        self.image = pygame.image.load("../images/ball.png")
        #self.image = self.image.convert()
        #self.image.set_alpha(127)
        self.coords = self.image.get_rect()
    
    def move(self):
        "move the ball"
        self.coords = self.coords.move(self.ball_speed)
                
    def bounce(self, width, height):
        if self.coords.left < 0 or self.coords.right >= width:
            self.ball_speed[0] = -self.ball_speed[0]
        if self.coords.top < 0 or self.coords.bottom >= height:
            self.ball_speed[1] = -self.ball_speed[1]

    def paddle_collision(self, paddle_coords):
        "detect paddle collision"
        if self.coords.left <= 0:
            if self.coords.bottom <= paddle_coords.bottom and self.coords.top >= paddle_coords.top:
                print("touch!")
            else:
                print("lost!")

    def get_coords(self):
        return self.coords.move(self.ball_speed)
    
    def high_opacity(self, target):
        self.target = target
        self.x = self.get_coords()[0]
        self.y = self.get_coords()[1]
        self.temp = pygame.Surface((self.image.get_width(), self.image.get_height())).convert()
        self.temp.blit(self.target, (-self.x, -self.y))
        self.temp.blit(self.image, (0, 0))
        self.temp.set_alpha(255)
        self.target.blit(self.temp, self.get_coords())

    def low_opacity(self, target):
        self.target = target
        self.x = self.get_coords()[0]
        self.y = self.get_coords()[1]
        self.temp = pygame.Surface((self.image.get_width(), self.image.get_height())).convert()
        self.temp.blit(self.target, (-self.x, -self.y))
        self.temp.blit(self.image, (0, 0))
        self.temp.set_alpha(80)
        self.target.blit(self.temp, self.get_coords())
        

    
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
        ball_x = 300
        ball_y = 300
        ball_vx = 4 # velocity along the x axis
        ball_vy = 4
      
        # Background init
        self.bg_R = 229
        self.bg_V = 228
        self.bg_B = 240
        self.background_color = (self.bg_R, self.bg_V, self.bg_B)        

        # Init pygame lib
        pygame.init()
        self.screen = pygame.display.set_mode( (self.width, self.height) )

        # Init Games Objects
        self.player_1 = Paddle(self.height/2, paddle_max_speed)
        self.player_2 = Paddle(self.height/2, paddle_max_speed)
        self.ball = Ball(ball_x, ball_y, ball_vx, ball_vy)
        self.score = Score()

        if server_mode == True:
            self.curent_player = self.player_1
        else:
            self.curent_player = self.player_2
            
    
        
    def draw(self):
        self.screen.fill(self.background_color)

        self.ball.move()
        self.ball.bounce(self.width, self.height)

        self.ball.paddle_collision(self.player_1.get_coords())
        self.ball.paddle_collision(self.player_2.get_coords())

        self.player_1.draw(self.width, self.height)
        self.screen.blit(self.player_1.image, self.player_1.get_coords())

        self.player_2.draw(self.width, self.height)
        self.screen.blit(self.player_2.image, self.player_2.get_coords())        

        pygame.display.flip()


    def delay(self):
        pygame.time.delay(10)


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
