#!/usr/bin/python

import pygame

pygame.init()

width = 320
height = 240
size = (width, height)
screen = pygame.display.set_mode(flags=pygame.FULLSCREEN | pygame.DOUBLEBUF)
# screen = pygame.display.set_mode()

black = (0, 0, 0)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == 113: # q to quit
                running = False

    screen.fill(black)
    pygame.display.flip()
