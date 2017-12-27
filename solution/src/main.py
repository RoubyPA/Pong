#! /usr/bin/env python3

import sys
import pygame
from pong import *

session = Game();
session.throw_ball();

while True:
    for e in pygame.event.get():
        # Check for exit
        if e.type == pygame.QUIT:
            sys.exit()

        session.update_screen()
        session.delay()
