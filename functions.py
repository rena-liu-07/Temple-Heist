from pygame import *
from random import *
from datetime import date

width, height = 1000, 700
screen = display.set_mode((width, height))

RED = (255, 0, 0)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

X = 0
Y = 1
WIDTH = 60
HEIGHT = 60
ROCK = 0
WOOD = 1
METAL = 2
LEFT = 0
UP = 1
DOWN = 2
RIGHT = 3

## INITIALIZING MUSIC
mixer.init()

## MAKING LISTS OF POSITIONS

#making list of all the (top left) positions of all the wall blocks (blocks that border the path)
def getWallPos(twoDList, walls):
    for row in range(len(twoDList)): #looping through each element
        for col in range(len(twoDList[row])):
            if twoDList[row][col] != 0: #if the current block isn't a path block
                if col > 0:
                    if twoDList[row][col-1] == 0: #is a right wall
                        walls.append((col*60, row*60)) #adding current pos (scaled correctly) to list
                if col < len(twoDList[row]) - 1:
                    if twoDList[row][col+1] == 0: #is a left wall
                        walls.append((col*60, row*60))
                if row > 0:
                    if twoDList[row-1][col] == 0: #is a bottom wall
                        walls.append((col*60, row*60))
                if row <len(twoDList)-1:
                    if twoDList[row+1][col] == 0: #is a top wall
                        walls.append((col*60, row*60))

#randomly putting diamonds around the map, storing as list of positions of diamonds, picking from list of pos (tuples)
def getDiamondPos(choices, diamonds, num):
    for each in range(num): #for each diamond
        diamond = randrange(0, len(choices)) #choosing a random choice
        diamonds.append((choices[diamond])) #adding position to list
        del choices[diamond] #removing that position from choices since it's already used

#getting Rects of all the obstacles
def getObstacles(fires, snakes):
    newList = []    
    for each in fires: #for each fire, add Rect of fire into list of all obstaces
        newList.append(each)
    for each in snakes: #for each snake, do the same
        eachRect = Rect(int(each[0]), int(each[1]), WIDTH, HEIGHT) #Rect of each obstacle
        newList.append(eachRect)
    
    return newList

## CHECKING THINGS

#checking how many lives player has
def checkLives(lives):
    if lives <= 0:
        return "noLives"
    
#checking if the player exceeded the time
def checkTime(currTime, givenTime):
    if currTime >= givenTime: #if player took longer than given time
        return "noTime" #bring player to another page

#when player reaches the end, checks if they have enough diamonds to pass the level
def checkDiamonds(greens, needed, level, levelsOpen, currTime): 

    if greens < needed: #if they don't have enough green diamonds
        return levelsOpen, "noDiamonds" #bring player to another page
    
    #otherwise (enough diamonds)
    if level != 2: #if it's not the final level
        levelsOpen[level+1] = True #opening the next level
    
    changeRecords(currTime, level)
    return levelsOpen, "win" #bring player to win page


## IF PLAYER COLLIDED WITH SOMETHING

#if the player hit a snake or fire
def hitObstacle(player, obstacle, lives, isLosingLife):
    currPos = Rect(player[X], player[Y], WIDTH, HEIGHT) #Rect of player currently
    if currPos.collidelist(obstacle) != -1: #if player dying
        if isLosingLife == False: #if player wasn't already getting killed, it is now
            isLosingLife = True

            mixer.music.load("AUDIO/Lose_a_life.ogg") #load and play losing life audio
            mixer.music.play()

            lives -= 1 #subtract life
    else: #if not hittng anything 
        isLosingLife = False #not losing life anymore
    
    return isLosingLife, lives

#if player went over a diamond or chest
def hitTreasure(player, diamonds, closedChests, openedChests, greens, purples):
    currPos = (player[X], player[Y]) #getting players current position

    if currPos in diamonds: #if player is on a diamond
        purples += 1 #gained a diamond
        diamonds.remove(currPos) #diamond is no longer there to be collected

        mixer.music.load("AUDIO/Sparkles_for_diamonds.ogg") #load and play the sound for collecting diamonds
        mixer.music.play()
    
    if currPos in closedChests: #if player is on unopened chest
        greens += 1 #player will collect the green diamond inside

        closedChests.remove(currPos) #takes away chest from closedChests since it's no longer unopened
        openedChests.append(currPos) #there is now a opened chest at that possible, adding position to list

        mixer.music.load("AUDIO/Chest_unlock.ogg") #load and play the sound for opening chests
        mixer.music.play()

    return purples, greens

#if the player hit a barrier
def hitBarrier(player, barriersBreaking, barriers, barrierImages, hammering, hammeringImages):
    keys = key.get_pressed()
    breakPos = [(player[X], player[Y]-HEIGHT), (player[X], player[Y]+HEIGHT), (player[X]-WIDTH, player[Y]), (player[X]+WIDTH, player[Y])] #possible positions for the barrier to be

    woodRect = Rect(45, 535, 100, 100) #tool rects to click on tools
    rockRect = Rect(150, 535, 100, 100)
    metalRect = Rect(255, 535, 100, 100)

    mx, my = mouse.get_pos()

    for pos in breakPos: #for each possible block in breakPos
        #player presses 1 for rock, 2 for wood, and 3 for metal
        #for rock
        if (keys[K_1] or rockRect.collidepoint(mx, my)) and pos in barriers[ROCK]: #if player used tool and barrier is in range
            barriers[ROCK].remove(pos) #remove barrier from list of barriers since it's getting destroyed
            barriersBreaking = [pos, barrierImages[ROCK], 0] #current block being animated and destoryed is this one
            hammering = [hammeringImages[breakPos.index(pos)], 0.1] #add list of images of character hammering to be blitted later

            mixer.music.load("AUDIO/Break_barrier.ogg") #load and play barrier breaking sound
            mixer.music.play()

        #for wood
        if (keys[K_2] or woodRect.collidepoint(mx, my)) and pos in barriers[WOOD]:
            barriers[WOOD].remove(pos) 
            barriersBreaking = [pos, barrierImages[WOOD], 0] 
            hammering = [hammeringImages[breakPos.index(pos)], 0.1]

            mixer.music.load("AUDIO/Break_barrier.ogg") #load and play barrier breaking sound
            mixer.music.play()
        
        #for metal
        if (keys[K_3] or metalRect.collidepoint(mx, my)) and pos in barriers[METAL]:
            barriers[METAL].remove(pos) 
            barriersBreaking = [pos, barrierImages[METAL], 0]
            hammering = [hammeringImages[breakPos.index(pos)], 0.1]
            
            mixer.music.load("AUDIO/Break_barrier.ogg") #load and play barrier breaking sound
            mixer.music.play()

    return hammering, barriersBreaking


## MOVING MOVING OBJECTS

#moving player's position
def movePlayer(player, walls, barriers, counter):
    keys = key.get_pressed()

    #checks if keys are pressed and that it won't hit a wall or run off the page if player moves
    #for moving right
    if (keys[K_RIGHT] or keys[K_d]) and player[X] < 2340 and (player[X]+60, player[Y]) not in walls and (player[X]+60, player[Y]) not in barriers[0] and (player[X]+60, player[Y]) not in barriers[1] and (player[X]+60, player[Y]) not in barriers[2]: #"D" or "→"
        counter += 0.2 #adding small number to counter to slow down animation
        if counter > 2.6: #once count has been reached
            player[X] += WIDTH #actually moves the player's position
            counter = 0 #restarting counter
        player[2] = 4 #setting the direction of the character (1 for left, 2 for up, 3 for down, 4 for right)

    #for moving left
    if (keys[K_LEFT] or keys[K_a]) and player[X] > 0 and (player[X]-60, player[Y]) not in walls and (player[X]-60, player[Y]) not in barriers[0] and (player[X]-60, player[Y]) not in barriers[1] and (player[X]-60, player[Y]) not in barriers[2]: #"A" or "←"
        counter += 0.2
        if counter > 2.6: 
            player[X] -= WIDTH
            counter = 0
        player[2] = 1

    #for moving up
    if (keys[K_UP] or keys[K_w]) and player[Y] > 0 and (player[X], player[Y]-60) not in walls and (player[X], player[Y]-60) not in barriers[0] and (player[X], player[Y]-60) not in barriers[1] and (player[X], player[Y]-60) not in barriers[2]: #"W" or "↑"
        counter += 0.2
        if counter > 2.6: 
            player[Y] -= HEIGHT
            counter = 0
        player[2] = 2
    
    #for moving down
    if (keys[K_DOWN] or keys[K_s]) and player[X] < 2340 and (player[X], player[1]+60) not in walls and (player[X], player[1]+60) not in barriers[0] and (player[X], player[1]+60) not in barriers[1] and (player[X], player[1]+60) not in barriers[2]: #"S" or "↓"
        counter += 0.2
        if counter > 2.6: 
            player[Y] += HEIGHT
            counter = 0
        player[2] = 3

    return counter

#moving the snackes (snakes -> snakes positions, snakeRanges -> snakes paths)
def moveSnakes(snakes, snakeRanges):
    for snake in range(len(snakes)): #for (num of) each snake
        index = snakes[snake][3] #index of which way (vert/hor, X/Y) snake is going (0 for hor, 1 for vert)

        #if snake went too far past
        if snakes[snake][index]  >= snakeRanges[snake][1]:
            snakes[snake][2] = -3 #setting direction to be backwards/-3
            snakes[snake][index] = snakeRanges[snake][1] - 1 #changing pos so that snake won't get stuck forever at the end, starts it back on it's way
        
        #if it went too far back
        if snakes[snake][index] <= snakeRanges[snake][0]:
            snakes[snake][2] = 3 #setting to forward/3
            snakes[snake][index] = snakeRanges[snake][0] + 1
        
        #adding movement/step to actual positon of snake
        snakes[snake][index] += snakes[snake][2]

#moving the boss snake to follow the player once they're in range
def moveBossSnake(player, bossSnake, station, range):
    playerRect = Rect(player[X], player[Y], WIDTH, HEIGHT)

    #moving the boss to chase after player
    if playerRect.colliderect(range): #if player in range
        if bossSnake[X] < player[X]: #if boss to the left, move it right
            bossSnake[X] += 2
            bossSnake[2] = 4 #changing the direction of the boss snake (1 -> left, 2 -> up, 3 -> down, 4 -> right)
        if bossSnake[X] > player[X]: #if boss to the right, move left
            bossSnake[X] -= 2
            bossSnake[2] = 1
        if bossSnake[Y] < player[Y]: #if boss up, move down
            bossSnake[Y] += 2
            bossSnake[2] = 3
        if bossSnake[Y] > player[Y]: #if boss down, move up
            bossSnake[Y] -= 2
            bossSnake[2] = 2
    
    #returning boss back to station
    if bossSnake != station: #otherwise if player isn't in range, but boss isn't in his default position, he has to return to default pos
      if bossSnake[X] < station[X]:
        bossSnake[X] += 1
        bossSnake[2] = 4
      if bossSnake[X] > station[X]:
        bossSnake[X] -= 1
        bossSnake[2] = 1
      if bossSnake[Y] < station[Y]:
        bossSnake[Y] += 1
        bossSnake[2] = 3
      if bossSnake[Y] > station[Y]:
        bossSnake[Y] -= 1
        bossSnake[2] = 2

#changing the length of the fires
def moveFire(fires, counter):
    for fire in range(len(fires)): #for each fire
        counter[fire] += 1 #adding a counter to slow down animation
        length = fires[fire][2] / 60 #length of fire currently

        if counter[fire] % 25 == 0:
            if length == 3: #if fire is 3 blocks long, it has to start at no blocks long again
                fires[fire][2] = 0 #no length = no fire
            
            else: #keep adding more blocks
                fires[fire][2] += WIDTH

#moving the figure on the map to the different levels
def moveMapIcon(levelIconPos, currLevel, newLevel, counter, path, unlockedLevels, figurePos, currDrawing):
    if currLevel != newLevel: #if figure isn't at the new level yet
        counter += 0.75 #counter to make animation happen slower
        currDrawing = True #now is currently drawing
    
    else: #if figure doesn't need to go to another level
        figurePos = levelIconPos[currLevel] #changing the figure pos to make sure it's exactly where it should be
        counter = 0 #resets it to let it sit there until its needed again
        currDrawing = False #no longer in the process of moving
    
    #checking which path to follow
    if currLevel == 0 and newLevel == 1 and unlockedLevels[1]:
        figurePos = path[int(counter)] #going through the list until right destination is reached
        if (440, 410) == figurePos: #if the figure reached the new level
            currLevel = 1 #update current level to the new level

    elif currLevel == 0 and newLevel == 2 and unlockedLevels[2]:
        figurePos = path[int(counter)] #going until the end of the path
        if (785, 235) == figurePos:
            currLevel = 2

    elif currLevel == 1 and newLevel == 0 and unlockedLevels[0]:
        figurePos = path[86-int(counter)] #starting from the middle, going backwards
        if (100, 200) == figurePos:
            currLevel = 0

    elif currLevel == 1 and newLevel == 2 and unlockedLevels[2]:
        figurePos = path[85 + int(counter)] #starting from the middle, going to the end
        if (785, 235) == figurePos:
            currLevel = 2

    elif currLevel == 2 and newLevel == 0 and unlockedLevels[0]:
        figurePos = path[254-int(counter)] #starting from the end, going to the beginning
        if (100, 200) == figurePos:
            currLevel = 0

    elif currLevel == 2 and newLevel == 1 and unlockedLevels[1]:
        figurePos = path[254-int(counter)] #starting from the end, stopping at the middle
        if (440, 410) == figurePos:
            currLevel = 1
    
    return counter, currLevel, figurePos, currDrawing

#changing the barrier breaking animation frame
def moveBarrier(barrierBreaking):
    if len(barrierBreaking) != 0:
        barrierBreaking[2] += 0.25 #adding to move the animation

        if barrierBreaking[2] >= 6: #if blitted all the images
            barrierBreaking = [] #not breaking anymore, remove from list entirely
    
    return barrierBreaking


## CHANGING THINGS (TIME, VOLUME, SCORES)

#changing the timer in each level
def changeTime(time, counter):
    counter += 1 #changing the counter 60 times every second

    if counter % 60 == 0:
        time += 1 #adding 1 every so many times so it adds 1 to seconds every second

    return time, counter

#updating highscores with new recordTime + date pair
def changeRecords(newTime, currLevel):
    file = open("RECORDS/record" + str(currLevel+1) + ".txt", "r") #getting all the previous records
    times = file.readlines() #each time + date pair is put as a string in list called times
    file.close()

    withDates = {} #making a dictionary
    for i in range(len(times)): #for each time + date pair
        unconvertedTime, dates = times[i].split() #splitting the pair into time and date
        minutes, seconds = unconvertedTime.split(":") #splitting time into minutes and seconds to convert to float num
        convertedTime = int(minutes)*60 + int(seconds) #getting time in num of secs
        withDates[convertedTime] = str(dates) #adding to the dictionary
        times[i] = convertedTime #changing times[i] to an int instead of time + date pair (string)

    today = date.today() #getting the current date
    withDates[newTime] = str(today.year) + "-" + str(today.month) + "-" + str(today.day) #adding the time and date into the dictionary
    times.append(newTime) #adding time into the list of times-only
    times.sort() #sorting the list of times

    newTimes = open("RECORDS/record" + str(currLevel+1) + ".txt", "w") #rewriting in the text file
    for time in times: #for each time
        minutes = int(time)//60 #getting the num of minutes
        seconds = int(time)%60 #converting decimal into the num of seconds
        if seconds < 10: #if seconds is one digit (to add the number 0 infront)
            newTimes.write(f"{minutes}:0{seconds} {withDates[time]}\n") #remake the time + date pair (seperated by a space)
        else:
            newTimes.write(f"{minutes}:{seconds} {withDates[time]}\n") #remake the time + date pair (seperated by a space)
    
    newTimes.close()

#muting or unmuting the volume
def changeVolume(mute, evt):
    volumeRect = Rect(890, 575, 50, 50) #the button/where the icon is displayed
    mx, my = mouse.get_pos()

    if evt.type == MOUSEBUTTONDOWN and volumeRect.collidepoint(mx, my): #if player clicked on the mute button
        if mute == True: #if it was muted, unmute it
            mute = False
            mixer.music.set_volume(1)
        else: #otherwise mute it
            mute = True
            mixer.music.set_volume(0)
    
    return mute


## DRAWING FUNCTIONS

#determining where top left corner of map (and everything else) will be blitted
def getBlittingPos(player, mapWidth, mapHeight):
    #if player is against left side section of the map (no horizontal movement)
    if player[X] < 500 - WIDTH/2:
        if player[Y] < 250 - HEIGHT/2: #if player is against upper side section (no vertical movement)
            blittingPosX = 0
            blittingPosY = 0
        elif player[Y] > 1550 - HEIGHT/2: #against bottom side section (no veritcal movement)
            blittingPosX = 0
            blittingPosY = 700-mapHeight
        else: #anywhere in between (vertical movement)
            blittingPosX = 0
            blittingPosY = 250-HEIGHT/2-player[Y]
    
    #if player is against right side section of the map (no horizontal movement)
    elif player[X] > mapWidth - 500 - WIDTH/2:
        if player[Y] < 250 - HEIGHT/2: #if player is against top side section (no vertical movement)
            blittingPosX = 1000 - mapWidth
            blittingPosY = 0
        elif player[Y] > mapHeight-250 - HEIGHT/2: #against bottom side section (no vertical movement)
            blittingPosX = 1000 - mapWidth
            blittingPosY = 700 - mapHeight
        else: #anywhere in between (vertical movement)
            blittingPosX = 1000 - mapWidth
            blittingPosY = 250-HEIGHT/2-player[Y]

    #else if player is in centre area of map(horizontal and vertical movement)
    else:
        if player[Y] < 250 - HEIGHT/2: #if player is against top side section (no vertical movement)
            blittingPosX = 500-WIDTH/2-player[X]
            blittingPosY = 0
        elif player[Y] > mapHeight-250 - HEIGHT/2: #against bottom side section (no vertical movement)
            blittingPosX = 500-WIDTH/2-player[X]
            blittingPosY = 700 - mapHeight
        else: #anywhere in between (vertical movement)
            blittingPosX = 500-WIDTH/2-player[X]
            blittingPosY = 250-HEIGHT/2-player[Y]
    
    return blittingPosX, blittingPosY

#drawing the game itself
def drawScene(blittingPosX, blittingPosY, map, player, walkingImages, hammering, barrierBreaking, snakes, snakeWalkingImages, diamonds, diamondImage, openChests, openChestImage, closedChests, closedChestImage, fires, fireImages, burningImages, barriers, barrierImages, walking, hammerUp):
    #blitting the map
    screen.blit(map, (blittingPosX, blittingPosY))
    
    #blitting snakes
    for snake in snakes:
        if snake[2] == -3: #if snake is going backwards, either blitting left or up
            if snake[3] == 0: #if moving horizontally
                snake[4] = 1 #now going left
            else:
                snake[4] = 3 #otherwise going up
        else: #if snake is going forwards
            if snake[3] == 0: #if snake is moving horizontally
                snake[4] = 0 #now going right
            else:
                snake[4] = 2 #else, going down

        screen.blit(snakeWalkingImages[snake[4]], (blittingPosX+snake[X], blittingPosY+snake[Y]))

    #blitting diamonds
    for diamond in diamonds:
        screen.blit(diamondImage, (blittingPosX+diamond[X], blittingPosY+diamond[Y]))
    
    #blitting chests
    for chest in openChests:
        screen.blit(openChestImage, (blittingPosX+chest[X], blittingPosY+chest[Y]+25))
    
    for chest in closedChests:
        screen.blit(closedChestImage, (blittingPosX+chest[X], blittingPosY+chest[Y]))
    
    #blitting barriers
    for i in range(3): #looping through the three types of barriers
        barrierPos = barriers[i]
        typeImages = barrierImages[i]

        for barrier in range(len(barriers[i])):
            screen.blit(typeImages[0], (blittingPosX+barrierPos[barrier][X], blittingPosY+barrierPos[barrier][Y]))

    #blitting fires
    for fire in fires:
        length = int(int(fire[2])/WIDTH) #getting length of fire (how many blocks)

        if length > 0: #if there is fire coming out
            screen.blit(fireImages[length-1], (blittingPosX+fire[X], blittingPosY+fire[Y]))

    
    #blitting barrier being broken
    if barrierBreaking != []:
        barrierBreakingPos = barrierBreaking[0] #getting the position and the kind of barrier that's being broken
        barrierBreakingType = barrierBreaking[1]

        screen.blit(barrierBreakingType[int(barrierBreaking[2])], (blittingPosX+barrierBreakingPos[X], blittingPosY+barrierBreakingPos[Y]))


    #blitting character
    #if character is in fire aka burning
    if Rect(player[X], player[Y], WIDTH, HEIGHT).collidelist(fires) != -1:
        frames = [burningImages, 0] #frames to play through are the burning sprites
        walking = False #character is not walking
    
    elif hammering != []: #if player is hitting
        frames = hammering #frames to play through are hitting frames
        walking = False #not walking
    
    if walking == False and frames[1] >= len(frames[0]): #once all animation frames of hitting or burning have played
        walking = True #player starts walking again
        hammering = [] #player is not hammering anymore
    
    if walking:
        if player[2] == 1: #if direction is left
            frames = [walkingImages[0], 0.2] #animating the walkLeft frames, playing through the frames forwards
        if player[2] == 2: #if direction is up
            frames = [walkingImages[1], 0.2]
        if player[2] == 3: #if direction is down
            frames = [walkingImages[1], -0.2] #playing through walkVert frames backwards to crawl down
        if player[2] == 4: #if direction is right
            frames = [walkingImages[2], 0.2]

    keys = key.get_pressed()

    #if player is walking and pressing on keys
    if walking:
        if keys[K_a] or keys[K_s] or keys[K_w] or keys[K_d] or keys[K_LEFT] or keys[K_UP] or keys[K_RIGHT] or keys[K_DOWN]:
            player[3] += frames[1]
            
    else: #otherwise frames should player automatically
        player[3] += frames[1]

    #if the animation went through all the frames, start over again
    if player[3] >= len(frames[0]) or -1*player[3] >= len(frames[0]): 
        if walking == False:
            walking = True
            hammering = []

        player[3] = 0

    #special case, hitting up (image is longer so needs to be blitted higher)
    if frames[0] == hammerUp:
        screen.blit(frames[0][int(player[3])], (blittingPosX+player[X], blittingPosY+player[Y]-54)) #blit it 54 pixels higher
    else:
        screen.blit(frames[0][int(player[3])], (blittingPosX+player[X], blittingPosY+player[Y]))

    return hammering
    
#drawing the toolbar + timer
def drawToolbar(toolbar, hearts, purple, green, lives, mute, volumeOn, volumeOff, timerBlock, timer, fontTools, fontTimer):
    screen.blit(toolbar, (0, 500)) #draw toolbar
  
    heartPos = [(601, 554), (688, 554), (770, 554)] #positions of the hearts on the toolbar
    heartPos = heartPos[:lives] #how many hearts are filled
    for i in range(lives): #for each heart that is filled
        screen.blit(hearts, heartPos[i]) #blit colored heart at that position

    purpleNum = fontTools.render(str(purple), True, WHITE) #number of purple diamonds rendered as text
    greenNum = fontTools.render(str(green), True, WHITE) #number of green diamonds rendered as text

    screen.blit(purpleNum, (450, 605)) #blit the two numbers next to their corresponding diamonds
    screen.blit(greenNum, (550, 605))

    if mute == True: #if volume is muted
        screen.blit(volumeOff, (890, 575)) #display muted icon
    else:
        screen.blit(volumeOn, (890, 575)) #otherwise display sound on icon

    volume = Rect(890, 575, 50, 50) #the button player clicks to change mute or unmute
    tools = [Rect(45, 530, 100, 115), Rect(150, 530, 100, 115), Rect(255, 530, 100, 115)] #Rects of the three hammers

    mx, my = mouse.get_pos()

    for tool in tools: #if mouse hovers over the hammers, blits a rectangle border over tool player is hovering over
        if tool.collidepoint(mx, my):
            draw.rect(screen, (139, 69, 19), tool, 2)
    
    if volume.collidepoint(mx, my): #same for volume button
        draw.rect(screen, (139, 69, 19), volume, 2)

    screen.blit(timerBlock, (423, 0)) #background image for the timer
    
    if timer%60 < 10:
        timerString = str(timer//60) + ":0" + str(timer%60)
    else:
        timerString = str(timer//60) + ":" + str(timer%60)
    time = fontTimer.render(timerString, True, (139, 69, 19)) #making the time rendered words
    screen.blit(time, (466, 12)) #blitting the time
    