from functions import *
from levels import *
from instructions import *
from story import *
from scores import *

## CREATING SCREEN
width, height = 1000, 700
screen = display.set_mode((width, height))
display.set_caption("Temple Heist")
mixer.init()

## LOADING IMAGES 
opening = [image.load("SCREENS/MENU/" + str(i) + ".png").convert_alpha() for i in range(1, 10)] #opening animation for the menu
startingPage = image.load("SCREENS/MENU/menu.png").convert_alpha() #menu after animation

backstory = image.load("SCREENS/MENU/backstory.png").convert_alpha() #when mouse is on backstory
highScore = image.load("SCREENS/MENU/high scores.png").convert_alpha() #when mouse is on highScore, etc
play = image.load("SCREENS/MENU/play.png").convert_alpha()
instruction = image.load("SCREENS/MENU/instructions.png").convert_alpha()

pages = [play, highScore, instruction, backstory] #list of the different pages
pageNames = ["map", "highScorePage", "instructions", "story"] #parallel list for their names

levelMaps = [image.load("SCREENS/MAP/" + str(i) + ".png").convert_alpha() for i in range(1, 4)] #map for the three levels
figure = image.load("SPRITES/STICKER/hover icon.png").convert_alpha() #icon of the man that moves on map

playButton = image.load("SCREENS/MAP/play button.png").convert_alpha() #image of the button player clicks to play level
homeButton = image.load("SPRITES/STICKER/home.png").convert_alpha() #image to bring player back to menu

## LOADING RESULT SCREENS/TRANSITION SCREENS
noDiamondsFrames = [image.load("SCREENS/NO DIAMONDS/" + str(i) + ".png").convert_alpha() for i in range(1, 16)]
levelCompleteFrames = [image.load("SCREENS/LEVEL COMPLETE/" + str(i) + ".png").convert_alpha() for i in range(1, 13)]
noLivesFrames = [image.load("SCREENS/NO LIVES/" + str(i) + ".png").convert_alpha() for i in range(1, 25)]
timeUpFrames = [image.load("SCREENS/TIME UP/" + str(i) + ".png").convert_alpha() for i in range(1, 33)]

## LOADING MUSIC
transitionSound = mixer.music.load("AUDIO/Transition.ogg")

## WIN SCREEN FONT
fontWin = font.SysFont("Arial", 50)

## VARIABLES 
myClock = time.Clock()

#MENU
buttons = [Rect(195, 315, 130, 50), Rect(110, 490, 345, 45), Rect(540, 315, 370, 45), Rect(600, 490, 290, 50)] #Rects for pageNames for menu

#MAP
#list of coordinates of the path that the figure runs along as it changed from level to level on the map
path = [(100, i) for i in range(200, 551, 10)] + [(i, 550) for i in range(100, 441, 10)] + [(440, i) for i in range(550, 311, -10)] + [(i, 310) for i in range(440, 251, -10)] + [(250, i) for i in range(310, 166, -10)] + [(i, 165) for i in range(250, 581, 10)] + [(580, i) for i in range(165, 546, 10)] + [(i, 545) for i in range(580, 786, 10)] + [(785, i) for i in range(545, 231, -10)]

#positon of Back to Menu button
homeRect = Rect(550, 90, 156, 42)

levelPos = 0 #current level (0, 1, or 2)
levelsOpen = [True, False, False] #which levels are unlocked
levelRects = [Rect(90, 169, 105, 105), Rect(425, 354, 105, 105), Rect(775, 199, 105, 105)] #where the level's X's are
levelIconPos = [(100, 200), (440, 390), (785, 230)] #where to blit the figure for standing on each level
figPos = [levelIconPos[levelPos]] #current position of the figure on the map


def menu():
    timeCounter = 0 #counter for the opening animation
    frame = 0 #frame that the animation is on

    running = True

    while running:
        for evt in event.get():
            if evt.type == QUIT:
                running = False
            if evt.type == MOUSEBUTTONDOWN:
                for i in range(len(buttons)): #for each button on the menu (play, story, instructions, high scores)
                    if buttons[i].collidepoint(mx, my): #if user clicked on that button
                        
                        return pageNames[i] #bring player to that page by changing page variable (parallel lists of pageNames and buttons)

        mx, my = mouse.get_pos()

        timeCounter += 1 #chaning the counter for the animation

        if timeCounter % 5 == 0 and frame < 9: #if the animation hasn't ended and 5 iterations passed
            frame += 1 #move onto next frame
        
        if frame != 9: #if animation isn't done, blit the correct frame
            screen.blit(opening[frame], (0, 0))
        else: #if it is, blit the standard final page
            screen.blit(startingPage, (0, 0))

        for i in range(len(buttons)): #for each button
            if buttons[i].collidepoint(mx, my): #if the mouse is hovering over that button, blit the image that shows that button having diamonds next to it
                screen.blit(pages[i], (0, 0))
        
        myClock.tick(60)
        display.flip()

    return "exit" #if user closes this window, quit game

def mainMap(levelPos):

    mapCounter = 0 #counter for how fast the icon on the map moves
    figPos = levelIconPos[levelPos] #the starting position of the icon (at the current level X)
    newLevel = levelPos #starts off with no destination

    drawing = False #the figure is not moving
    running = True

    while running:
        for evt in event.get():
            if evt.type == QUIT:
                running = False
            if evt.type == MOUSEBUTTONDOWN:
                if drawing == False: #if the figure is not moving and the user clicked on one of other 2 levels
                    for i in range(3):
                        if levelRects[i].collidepoint(mx, my):
                            newLevel = i #new destination is now that level player clicked on
                
                if levelsOpen[levelPos] == True: #if the level the the player is currently on is unlocked (double checking)
                    playPos = Rect(760, 90, 129, 49) #position of the Play button
                    if playPos.collidepoint(mx, my): #if they click on Play button
                        mixer.music.play()
                        return levelPos, "lev" + str(levelPos+1) #bring them to that level
                
                if homeRect.collidepoint(mx, my):
                    return levelPos, "menu"
                
                

        mx, my = mouse.get_pos()

        #depending on how many levels there are, blit the map image that has that many X's unlocked
        if levelsOpen[2] == True:
            screen.blit(levelMaps[2], (0, 0))
        elif levelsOpen[1] == True:
            screen.blit(levelMaps[1], (0, 0))
        else:
            screen.blit(levelMaps[0], (0, 0))
        
        screen.blit(figure, figPos) #blit the figure at it's position

        #function for moving the figure from current level to new level, will animate the figure moving and change levelPos value
        mapCounter, levelPos, figPos, drawing= moveMapIcon(levelIconPos, levelPos, newLevel, mapCounter, path, levelsOpen, figPos, drawing)
        
        #blitting the Play button
        if levelsOpen[levelPos] == True:
            screen.blit(playButton, (760, 90))
        
        #blitting the Back to Menu button
        screen.blit(homeButton, homeRect)
        
        myClock.tick(60)
        display.flip()

    return levelPos, "menu" #if user exits, brings them back to the menu

page = "menu"

while page != "exit":
    if page == "menu":
        page = menu()
    if page == "map":
        levelPos, page = mainMap(levelPos) 
    if page == "story":
        page = story()
    if page == "instructions":
        page = instructions()
    if page == "highScorePage":
        page = highScores()
    if page == "lev1":
        levelsOpen, levelPos, page, greens, purples, neededPurples = level1(levelsOpen, 0)
    if page == "lev2":
        levelsOpen, levelPos, page, greens, purples, neededPurples = level2(levelsOpen, 1)
    if page == "lev3":
        levelsOpen, levelPos, page, greens, purples, neededPurples = finalLevel(levelsOpen, 2)
    if page == "noLives":
        levelPos, page = noLives(noLivesFrames, levelPos)
    if page == "noTime":
        levelPos, page = timeOver(timeUpFrames, levelPos)
    if page == "noDiamonds":
        levelPos, page = noDiamonds(noDiamondsFrames, levelPos)
    if page == "win":
        page = win(levelCompleteFrames, purples, greens, neededPurples, fontWin)
quit()
