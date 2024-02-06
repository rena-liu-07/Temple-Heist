from pygame import *

width, height = 1000, 700
screen = display.set_mode((width, height))
display.set_caption("Temple Heist")

X = 0
Y = 1

## IMPORTING IMAGES
storyImages = [image.load("SCREENS/STORY/" + str(i) + ".png").convert_alpha() for i in range(1, 6)]
back = image.load("SPRITES/STICKER/back.png").convert_alpha() #back button for flipping pages
next = image.load("SPRITES/STICKER/next.png").convert_alpha() #next button
home = image.load("SPRITES/STICKER/home.png").convert_alpha() #home button that shows up on the last page

## Rects for the three buttons
homeRect = Rect(765, 616, 156, 42)
backRect = Rect(50, 600, 51, 51)
nextRect = Rect(900, 600, 51, 51)

def story():
    pageNum = 0
    running = True

    while running:
        for evt in event.get():
            if evt.type == QUIT:
                running = False
            if evt.type == MOUSEBUTTONDOWN:
                if pageNum == 4 and homeRect.collidepoint(mx, my): #if player hit home, go back to menu
                    return "menu"
                if backRect.collidepoint(mx, my) and pageNum > 0: #flip back a page if possible
                    pageNum -= 1 
                if nextRect.collidepoint(mx, my) and pageNum < 4: #flip forward a page if possible
                    pageNum += 1
                        
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()

        screen.blit(storyImages[pageNum], (0, 0)) #blitting the story page

        if pageNum == 4: #if it's the last page, blit home button and back button
            screen.blit(home, (homeRect[X], homeRect[Y])) 
            screen.blit(back, (backRect[X], backRect[Y]))
        else:
            screen.blit(back, (backRect[X], backRect[Y])) #otherwise blit back and forward rect
            screen.blit(next, (nextRect[X], nextRect[Y]))

        display.flip()
                
    return "menu"
