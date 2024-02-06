from pygame import *
from random import *
from datetime import date

width, height = 1000, 700
screen = display.set_mode((width, height))
display.set_caption("Temple Heist")
X = 0
Y = 1

## IMPORTNG IMAGES
background = image.load("SCREENS/instructions.png").convert_alpha() #instructions pic

home = image.load("SPRITES/STICKER/home.png").convert_alpha() #home button for menu
homeRect = Rect(765, 616, 156, 42) 

def instructions():
    running = True

    while running:
        for evt in event.get():
            if evt.type == QUIT:
                running = False
            if evt.type == MOUSEBUTTONDOWN:
                if homeRect.collidepoint(mx, my):
                    return "menu"
                        
        mx, my = mouse.get_pos()
        
        screen.blit(background, (0, 0))
        screen.blit(home, (homeRect[X], homeRect[Y]))


        display.flip()
                
    return "menu"
