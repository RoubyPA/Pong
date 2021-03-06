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


################################################################################
# Class Ball
################################################################################
class Ball(object):
    def __init__(self, radius, player):
        "Init ball object"
        self.throw()
        
        self.radius = radius
        self.player = player

        self.blue = (30,144,255)
        self.red = (178,34,34)

        if self.player == True:
            self.color = self.blue #blue
        else:
            self.color = self.red #red
        
    def move(self):
        "move the ball"
        self.x += self.vx
        self.y += self.vy        

    def bounce(self, width, height):
        "bounce the ball on the walls"
        if self.x - self.radius < 0 or self.x + self.radius >= width:
              self.vx = -self.vx
        if self.y - self.radius < 0 or self.y + self.radius >= height:
              self.vy = -self.vy

        if self.x - self.radius < 0 and self.color == self.blue:
            self.color = self.red
        elif self.x - self.radius < 0 and self.color == self.red:
            self.color = self.blue

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius, 0)

    def throw(self):
        self.x = 300
        self.y = 300
        self.vx = 4
        self.vy = 4

    def increase_speed(self):
        self.vx += 1
        self.vy += 1
        
################################################################################
# Class Item (bonus, malus, etc) + subclasses
################################################################################
class Item(object):
    "Item class, its was destined to be a superclass for bonus elements, see example below"
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
        self.player_1 = 0
        self.player_2 = 0

        self.font = pygame.font.Font(None, 25)
        
    def add_point_player_1(self):
        self.player_1 += 1

    def add_point_player_2(self):
        self.player_2 += 1
        
    def get_score_player_1 (self):
        return self.player_1

    def get_score_player_2 (self):
        return self.player_2

    def draw(self, screen):
        score = "Score: {}/{}".format(self.player_1, self.player_2)
        self.text = self.font.render(score, True, (128, 128, 128))
        self.screen = screen
        self.screen.blit(self.text, (700, 0))

        
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
        self.ball = Ball(ball_radius, server_mode)
        self.score = Score()
        
        # who am i ?
        if server_mode == True:
            self.curent_player = self.player_1
        else:
            self.curent_player = self.player_2

    def switch_player(self):
        if self.curent_player == self.player_1:
            self.curent_player = self.player_2
        else:
            self.curent_player = self.player_1
            
    def paddle_collision(self, paddle_coords):
        "detect paddle collision"
        if self.ball.x - self.ball.radius < 0:
            self.switch_player()
            
            if (self.ball.y - self.ball.radius < paddle_coords.bottom and
                self.ball.y + self.ball.radius > paddle_coords.top):
                return "touch"
            else:
                return "lost"

        return "nope"
    
    def draw(self):
        ret = "none"
        
        touch = self.paddle_collision(self.curent_player.get_coords()) 
        if touch == "lost":
            if self.curent_player == self.player_1:
                self.score.add_point_player_1()
                ret = "1 lost"
            else:
                self.score.add_point_player_2()
                ret = "2 lost"
            self.ball.throw()
            
        elif touch == "touch":
            self.ball.increase_speed()
            ret = "touch"

        self.screen.fill(self.background_color)
        self.ball.draw(self.screen)
        self.ball.move()
        self.ball.bounce(self.width, self.height)

        self.player_1.draw(self.width, self.height)
        self.screen.blit(self.player_1.image, self.player_1.get_coords())

        self.player_2.draw(self.width, self.height)
        self.screen.blit(self.player_2.image, self.player_2.get_coords())

        self.score.draw(self.screen)

        pygame.display.flip()

        return ret
        
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
