from pygame import *
from functions import *

width, height = 1000, 700
screen = display.set_mode((width, height))
display.set_caption("Temple Heist")

## IMPORTING IMAGES
back = image.load("SPRITES/STICKER/backblack.png").convert_alpha() #back button for flipping pages
next = image.load("SPRITES/STICKER/nextblack.png").convert_alpha() #next button
home = image.load("SPRITES/STICKER/home.png").convert_alpha() #home button that shows up on the last page

level1Scores = image.load("LEVELS/image1.png").convert_alpha() #backgrounds for the records
level2Scores = image.load("LEVELS/image2.png").convert_alpha()
level3Scores = image.load("LEVELS/image3.png").convert_alpha()
backgrounds = [level1Scores, level2Scores, level3Scores]

## Rects for the three buttons
homeRect = Rect(775, 80, 156, 42)
backRect = Rect(50, 600, 51, 51)
nextRect = Rect(900, 600, 51, 51)

## FONT
font.init()
arialRecords = font.SysFont("Arial", 30)

def highScores():
    ## lists to store records for blitting
    recordList1 = []
    recordList2 = []
    recordList3 = []
    allLists = [recordList1, recordList2, recordList3]

    #reading and getting all scores
    listLevel1 = open("RECORDS/record1.txt", "r")
    listLevel2 = open("RECORDS/record2.txt", "r")
    listLevel3 = open("RECORDS/record3.txt", "r")

    textLevel1 = listLevel1.readlines()
    textLevel2 = listLevel2.readlines()
    textLevel3 = listLevel3.readlines()
    texts = [textLevel1, textLevel2, textLevel3]

    listLevel1.close()
    listLevel2.close()
    listLevel3.close()
    
    for list in range(3): #for each of the three levels
        if len(texts[list]) < 10: #if there's less than ten scores, for loop range is len of scores
            for line in range(len(texts[list])): #for each score
                theTime, theDate = texts[list][line].split() #split time and date
                score = arialRecords.render(f"{theTime}       {theDate}", True, (139, 69, 19)) #space it out and render it
                allLists[list].append(score) #add it to the list of texts that will be blitted
        else: #otherwise if there's more than ten
            for line in range(10): #only do the first ten scores
                theTime, theDate = texts[list][line].split()
                score = arialRecords.render(f"{theTime}       {theDate}", True, (139, 69, 19))
                allLists[list].append(score)
    
    running = True
    pageNum = 0 #current page player is one

    while running:
        for evt in event.get():
            if evt.type == QUIT:
                running = False
            if evt.type == MOUSEBUTTONDOWN:
                if backRect.collidepoint(mx, my) and pageNum > 0: #if there is a page to go back to
                    pageNum -= 1
                if nextRect.collidepoint(mx, my) and pageNum < 2: #page to go forward to
                    pageNum += 1 
                if homeRect.collidepoint(mx, my):#back to menu
                    return "menu"
                        
        mx, my = mouse.get_pos()

        screen.blit(backgrounds[pageNum], (0, 0)) #blit background of current page

        for score in range(len(allLists[pageNum])): #for each of top 10 records
            screen.blit(allLists[pageNum][score], (380, 180+ score*42)) #blit the record in a list

        ## BLITTING THE BUTTONS

        screen.blit(back, backRect)
        screen.blit(next, nextRect)
        screen.blit(home, homeRect)


        display.flip()
                
    return "menu"