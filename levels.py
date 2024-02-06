from pygame import *
from functions import *

width, height = 1000, 700
screen = display.set_mode((width, height))
display.set_caption("Temple Heist")

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

myClock = time.Clock()

## IMPORTING IMAGES
#SCREENS
timeUp = [image.load("SCREENS/TIME UP/" + str(i) + ".png").convert_alpha() for i in range(1, 33)] #the images for animation for time up
noLives = [image.load("SCREENS/NO LIVES/" + str(i) + ".png").convert_alpha() for i in range(1, 25)] #images for animation for 3 lives gone
win = [image.load("SCREENS/LEVEL COMPLETE/" + str(i) + ".png").convert_alpha() for i in range(1, 13)] #for level complete animation
noDiamonds = [image.load("SCREENS/NO DIAMONDS/" + str(i) + ".png").convert_alpha() for i in range(1, 16)] #for not enough diamonds

#BARRIER ANIMATION
rockList = [image.load("SPRITES/STICKER/ROCK/rock" + str(i)+".png").convert_alpha() for i in range(1, 7)] #animation for breaking rocks
woodList = [image.load("SPRITES/STICKER/WOOD/wood"+str(i)+".png").convert_alpha() for i in range(1, 7)] 
metalList = [image.load("SPRITES/STICKER/METAL/metal"+str(i)+".png").convert_alpha() for i in range(1, 7)]
barrierImages = [rockList, woodList, metalList]

#ICONS
openChestImage = image.load("SPRITES/STICKER/openchest.png").convert_alpha() #icon for opened chest
closedChestImage = image.load("SPRITES/STICKER/chest.png").convert_alpha() #icon for closed chest

green = image.load("SPRITES/STICKER/green.png").convert_alpha() #icon for green diamonds
purple = image.load("SPRITES/STICKER/purple.png").convert_alpha()

woodHammer = image.load("SPRITES/STICKER/woodhammer.png").convert_alpha() #icon for wood hammer (toolbar)
rockHammer = image.load("SPRITES/STICKER/rockhammer.png").convert_alpha()
metalHammer = image.load("SPRITES/STICKER/metalhammer.png").convert_alpha()

heart = image.load("SPRITES/STICKER/heart.png").convert_alpha() #heart icon for lives on toolbar 
greyHeart = image.load("SPRITES/STICKER/dead heart.png").convert_alpha() #greyed out/ lost lives on toolbar

volumeOn = image.load("SPRITES/STICKER/volumeon.png").convert_alpha() #button to click to unmute
volumeOff = image.load("SPRITES/STICKER/mute.png").convert_alpha() #to mute

#TOOLBAR
toolbar = image.load("SCREENS/toolbar.png").convert_alpha() #toolbar image on bottom of screen during game
timerBlock = image.load("SCREENS/timer.png") #timer at the top of the screen

#making fonts
font.init()
fontTimer = font.SysFont("Arial", 40)
fontToolbar = font.SysFont("Arial", 15)

#FIRE ANIMATION
fireImages = [image.load("SPRITES/BURN/fireright" + str(i)+".png").convert_alpha() for i in range(1, 4)] #fire shooting to the right

burnedPlayer = [image.load("SPRITES/BURN/burn.png").convert_alpha()] #player on fire

#WALKING ANIMATION
walkingLeft = [image.load("SPRITES/WALKING/LEFT/walking" + str(i) + ".png").convert_alpha() for i in range(1, 5)] #character walking to the left
walkingRight = [image.load("SPRITES/WALKING/RIGHT/walking" + str(i) + ".png").convert_alpha() for i in range(1, 5)] #character walking to the right
walkingVert = [image.load("SPRITES/WALKING/VERT/walking" + str(i) + ".png").convert_alpha() for i in range(1, 7)] #character walking up/down
walkingImages = [walkingLeft, walkingVert, walkingRight]

#HAMMERING ANNIMATION
hammerUp = [image.load("SPRITES/HAMMER UP/hitup" + str(i) + ".png").convert_alpha() for i in range(1, 6)]
hammerDown = [image.load("SPRITES/HAMMER DOWN/hammerdown" + str(i) + ".png").convert_alpha() for i in range(1, 5)]
hammerLeft = [image.load("SPRITES/HAMMER SIDEWAYS/hammerleft" + str(i) + ".png").convert_alpha() for i in range(1, 4)]
hammerRight = [image.load("SPRITES/HAMMER SIDEWAYS/hammerright" + str(i) + ".png").convert_alpha() for i in range(1, 4)]
hammeringImages = [hammerUp, hammerDown, hammerLeft, hammerRight]

#MAPS
level1Map = image.load("LEVELS/1.png").convert_alpha()
level2Map = image.load("LEVELS/2.png").convert_alpha()
level3Map = image.load("LEVELS/3.png").convert_alpha()

#BLUE SNAKES
snakeWalkDown = image.load("SPRITES/BLUE SNAKE/walkdown.png").convert_alpha()
snakeWalkLeft = image.load("SPRITES/BLUE SNAKE/walkleft.png").convert_alpha()
snakeWalkRight = image.load("SPRITES/BLUE SNAKE/walkright.png").convert_alpha()
snakeWalkUp = image.load("SPRITES/BLUE SNAKE/walkup.png").convert_alpha()
snakesWalkingImages = [snakeWalkRight, snakeWalkLeft, snakeWalkDown, snakeWalkUp]

#RED SNAKES (boss)
bossWalkDown = image.load("SPRITES/RED SNAKE/walkdown.png").convert_alpha()
bossWalkLeft = image.load("SPRITES/RED SNAKE/walkleft.png").convert_alpha()
bossWalkRight = image.load("SPRITES/RED SNAKE/walkright.png").convert_alpha()
bossWalkUp = image.load("SPRITES/RED SNAKE/walkup.png").convert_alpha()
bossSnakeImages = [bossWalkLeft, bossWalkUp, bossWalkDown, bossWalkRight]

## INITIALIZE SOUND
mixer.init()

def level1(levelsOpen, levelPos):
   #map of the level, used for making walls
   map = [[1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2, 2],
   [1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 2, 1, 2, 2, 2, 1, 2],
   [1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 1, 2, 2, 2, 1, 2, 1, 1, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1],
   [1, 2, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 2, 2, 1, 1, 1, 2, 2],
   [1, 2, 1, 1, 2, 1, 2, 2, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 1, 2, 1, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 1, 2, 2, 2, 1, 1],
   [1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 0, 0, 0, 2, 1, 1, 1, 2, 1, 2, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1],
   [1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 1, 0, 0, 0, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2],
   [2, 2, 1, 2, 2, 1, 1, 2, 1, 2, 1, 2, 2, 0, 0, 0, 2, 1, 2, 2, 1, 1, 2, 2, 2, 2, 1, 2, 1, 1, 1, 1, 1, 2, 2, 1, 2, 2, 2, 2],
   [1, 2, 2, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 0, 0, 0, 1, 1, 2, 2, 2, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 1, 2, 2],
   [1, 2, 1, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 0, 0, 0, 1, 1, 2, 2, 1, 1, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1, 2, 1, 2],
   [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 1, 2, 1, 1],
   [1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 0, 0, 0, 0, 0, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1],
   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 0, 0, 0, 1, 2, 0, 2, 0, 0, 0, 0, 2, 2, 1, 1],
   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 2, 2, 2, 1, 2, 2, 2, 1, 1, 2, 0, 0, 0, 2, 2, 1, 1, 0, 0, 0, 0, 2, 1, 2, 1],
   [1, 2, 1, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 0, 0, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 2, 1, 2, 0, 0, 0, 0, 2, 1, 2, 2],
   [2, 2, 2, 2, 1, 2, 2, 1, 1, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 1, 0, 0, 0, 2, 1, 1, 1, 0, 0, 0, 0, 2, 2, 1, 2],
   [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 2, 1, 0, 0, 0, 1, 2, 2, 1, 0, 0, 0, 0, 1, 2, 2, 2],
   [1, 2, 2, 1, 2, 1, 2, 2, 1, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 1, 0, 0, 0, 1, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 1],
   [2, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 2, 0, 0, 0, 0, 1, 2, 2, 1],
   [1, 1, 1, 2, 2, 2, 1, 2, 2, 1, 1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 0, 0, 0, 0, 1, 2, 1, 1],
   [1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 0, 0, 0, 0, 1, 2, 2, 1],
   [2, 1, 2, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 2, 2, 0, 0, 0, 0, 2, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0],
   [1, 2, 1, 2, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 2, 0, 0, 0, 0, 2, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0],
   [1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 2, 1, 1, 1, 2, 1, 0, 0, 0, 0, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0],
   [2, 1, 1, 1, 1, 2, 2, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 2, 2, 1, 2, 1, 2, 2, 2, 1, 1],
   [1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 2, 2, 1, 1, 2, 1, 2, 2, 2, 2],
   [2, 1, 2, 1, 2, 1, 1, 1, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 1, 1, 1, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 1],
   [1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 1, 1, 2, 1, 1, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 1, 2],
   [1, 2, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2],
   [2, 2, 2, 2, 2, 1, 1, 2, 2, 1, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2]]

   walls = []
   getWallPos(map, walls) #making the walls based on the map ^

   rocks = [(600, 600), (600, 660), (600, 720), (600, 780), (1440, 1260), (1500, 1260), (1560, 1260), (1620, 1260)] #positions of all the rock, wood, and metal barriers
   wood = [(660, 600), (720, 600), (780, 600), (840, 600), (1920, 660), (2220, 1260), (2220, 1320), (2220, 1380)]
   metal = [(2040, 660), (2040, 720), (2100, 720), (1200, 1080), (1200, 1140), (1200, 1200)]
   barriers = [rocks, wood, metal] #compiling into one list for easier use

   #list of all the possible choices or diamonds to be randomly placed on
   diamondChoices = [(780, 300), (840, 300), (780, 360), (840, 360), (900, 360), (780, 480), (840, 480), 
                  (900, 480), (1500, 480), (1560, 480), (1620, 480), (1680, 480), (1740, 480), (1800, 480), 
                  (1860, 480), (1920, 480), (780, 540), (840, 540), (900, 540), (1500, 540), (1560, 540), 
                  (1620, 540), (1680, 540), (1740, 540), (1800, 540), (1860, 540), (1920, 540), (1500, 600), 
                  (1560, 600), (1620, 600), (1680, 600), (1740, 600), (1800, 600), (1860, 600), (1920, 600), 
                  (660, 660), (720, 660), (780, 660), (840, 660), (1500, 660), (1560, 660), (1620, 660), (1680, 660), 
                  (1740, 660), (1800, 660), (1860, 660), (1980, 660), (0, 720), (60, 720), (120, 720), (180, 720), 
                  (240, 720), (300, 720), (360, 720), (420, 720), (480, 720), (540, 720), (660, 720), (720, 720), 
                  (780, 720), (840, 720), (1500, 720), (1560, 720), (1620, 720), (1920, 720), (1980, 720), (0, 780), 
                  (60, 780), (120, 780), (180, 780), (240, 780), (300, 780), (360, 780), (420, 780), (480, 780), 
                  (540, 780), (780, 780), (840, 780), (1920, 780), (1980, 780), (2040, 780), (2100, 780), (780, 840), 
                  (840, 840), (1500, 840), (1560, 840), (1620, 840), (780, 900), (840, 900), (900, 900), (960, 900), 
                  (1020, 900), (1080, 900), (1140, 900), (1500, 900), (1560, 900), (1620, 900), (1920, 900), (1980, 900), 
                  (2040, 900), (2100, 900), (1500, 960), (1560, 960), (1620, 960), (1920, 960), (1980, 960), (2040, 960), 
                  (2100, 960), (780, 1020), (840, 1020), (900, 1020), (960, 1020), (1020, 1020), (1080, 1020), (1140, 1020), 
                  (1920, 1020), (1980, 1020), (2040, 1020), (2100, 1020), (780, 1080), (840, 1080), (900, 1080), (960, 1080), 
                  (1020, 1080), (1080, 1080), (1140, 1080), (1260, 1080), (1320, 1080), (1380, 1080), (1440, 1080), (1500, 1080), 
                  (1560, 1080), (1620, 1080), (1920, 1080), (1980, 1080), (2040, 1080), (2100, 1080), (780, 1140), (840, 1140), 
                  (900, 1140), (960, 1140), (1020, 1140), (1080, 1140), (1140, 1140), (1260, 1140), (1320, 1140), (1380, 1140), 
                  (1440, 1140), (1500, 1140), (1560, 1140), (1620, 1140), (1920, 1140), (1980, 1140), (2040, 1140), (2100, 1140), 
                  (1140, 1200), (1260, 1200), (1320, 1200), (1380, 1200), (1440, 1200), (1500, 1200), (1560, 1200), (1620, 1200), 
                  (1920, 1200), (1920, 1260), (1980, 1260), (2040, 1260), (2100, 1260), (2160, 1260), (2280, 1260), (1440, 1320), 
                  (1500, 1320), (1560, 1320), (1620, 1320), (2040, 1320), (2100, 1320), (2160, 1320), (2280, 1320), (1440, 1380), 
                  (1560, 1380), (1620, 1380), (2040, 1380), (2100, 1380), (2160, 1380), (2280, 1380),]

   diamonds = []
   getDiamondPos(diamondChoices, diamonds, 10) #randomly placing the diamonds
   greens = 0 #num of green diamonds
   purples = 0 #num of purple diamonds

   closedChest = [(900, 300), (2100, 660), (1800, 720), (1500, 1380)] #chests that havent been opened
   openChest = [] #used for storing chests that have been opened

   fires = [Rect(1500, 1020, 60, 60), Rect(1920, 1200, 60, 60)] #Rects of fire blasts
   fireCounter = [0, 0] #counter for each fire blast animation

   snakes = [[780, 420, 1, 0, 0], [1500, 780, 1, 0, 0], [1740, 480, 1, 1, 2], [1920, 840, 1, 0, 0], [780, 960, 1, 0, 0]] #information for all the snakes
   snakeRanges = [(780, 900), (1500, 1620), (480, 660), (1920, 2100), (780, 1140)] #starting and ending position for each snake

   givenTime = 105 #how many seconds for that level
   timer = 0 #clock 
   timerCounter = 0 #counter variable for the clock

   exitBlocks = [(2340, 1260), (2340, 1320), (2340, 1380)] #blocks that player has to reach to end level

   lives = 3 #player starts with all 3 lives
   isLosingLife = False #player is not currently losing a life
   mute = False #if the volume is muted or not
   walking = True #if the player is walking, as opposed to burning or hammering

      #x  y direction frame
   player = [0, 720, 4, 0]
   movePlayerCount = 0 #counter to slow down animation time for character

   barriersBreaking = [] #list that will contain the blocks that are being destroyed (for animating)
   hammering = [] #list for storing information for character hammering blocks animation

   running = True

   while running:
      for evt in event.get():
            if evt.type == QUIT:
               running = False
            #checking if user presses mute button, changing mute variable if user did
            mute = changeVolume(mute, evt)

      ## MOVING MOVING PARTS
      movePlayerCount = movePlayer(player, walls, barriers, movePlayerCount) #moving the player
      moveSnakes(snakes, snakeRanges) 
      moveFire(fires, fireCounter) 
      barriersBreaking = moveBarrier(barriersBreaking)

      ## CHANGING THINGS 
      timer, timerCounter = changeTime(timer, timerCounter)

      ## CHECKING IF PLAYER HIT THINGS
      allObstacles = getObstacles(fires, snakes)
     
      isLosingLife, lives = hitObstacle(player, allObstacles, lives, isLosingLife) #hit any obstacle
      purples, greens = hitTreasure(player, diamonds, closedChest, openChest, greens, purples)
      hammering, barriersBreaking = hitBarrier(player, barriersBreaking, barriers, barrierImages, hammering, hammeringImages)

      ## DRAWING EVERYTHING
      blittingPosX, blittingPosY = getBlittingPos(player, 2400, 1800)
      hammering = drawScene(blittingPosX, blittingPosY, level1Map, player, walkingImages, hammering, barriersBreaking, snakes, snakesWalkingImages, diamonds, purple, openChest, openChestImage, closedChest, closedChestImage, fires, fireImages, burnedPlayer, barriers, barrierImages, walking, hammerUp)
      drawToolbar(toolbar, heart, purples, greens, lives, mute, volumeOn, volumeOff, timerBlock, timer, fontToolbar, fontTimer)

      #updating, get one green diamond in each chest so num of green diamonds = num of opened chest
      greens = len(openChest)

      ## CHECKING CURRENT SITUATION
      page = checkLives(lives) #check if player has one or more lives
      if page != None: #if they don't
         mixer.music.load("AUDIO/Transition.ogg") #switching between pages
         mixer.music.play()
         return levelsOpen, levelPos, page, greens, purples, 10#bring them to the No Lives page

      page = checkTime(timer, givenTime) #same thing but for No Time
      if page != None:
         mixer.music.load("AUDIO/Transition.ogg") #switching between pages
         mixer.music.play()
         return levelsOpen, levelPos, page, greens, purples, 10

      #if the player reached the end of the level
      if (player[X], player[Y]) in exitBlocks:
         levelsOpen, page = checkDiamonds(greens, 4, levelPos, levelsOpen, timer) #checks they have enough diamonds to complete the level
         mixer.music.load("AUDIO/Transition.ogg") #switching between pages
         mixer.music.play()
         return levelsOpen, levelPos, page, greens, purples, 10

      myClock.tick(60)

      display.flip()

   return levelsOpen, levelPos, "map", greens, purples, 10


def level2(levelsOpen, levelPos):

    #map of the level, used for making walls
   map = [[1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 2, 2, 1, 2, 1, 2, 1, 1, 2, 2, 2, 1], 
          [2, 2, 1, 2, 2, 2, 2, 1, 2, 1, 1, 1, 2, 2, 1, 2, 2, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 2, 1, 2, 2, 2, 1, 1, 2], 
          [1, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1], 
          [1, 2, 2, 1, 1, 1, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 2, 1, 1, 2], 
          [1, 1, 1, 2, 2, 1, 1, 2, 2, 1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2], 
          [1, 2, 2, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2], 
          [2, 2, 2, 2, 2, 2, 1, 1, 2, 1, 2, 2, 1, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 0, 0, 1, 2, 1, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 1], 
          [1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 2, 1, 2], 
          [2, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0], 
          [2, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 2, 2, 1, 1, 2, 2, 0, 0, 0, 0, 0, 0], 
          [1, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0], 
          [1, 1, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 2, 2, 1, 2, 1, 2, 0, 0, 0, 0, 0, 0], 
          [2, 1, 2, 2, 2, 1, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1], 
          [2, 1, 1, 2, 2, 2, 1, 2, 2, 1, 1, 1, 2, 1, 2, 2, 2, 2, 2, 2, 1, 2, 0, 0, 0, 0, 0, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1], 
          [2, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 2, 0, 0, 0, 0, 0, 1, 2, 2, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2], 
          [2, 2, 1, 2, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 2, 1, 2, 2, 2, 1, 2, 0, 0, 0, 0, 0, 2, 2, 2, 1, 2, 2, 2, 1, 1, 1, 1, 1, 2], 
          [1, 2, 2, 1, 1, 2, 2, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 2, 1, 2, 2, 1, 2], 
          [2, 1, 1, 2, 2, 1, 1, 1, 2, 2, 1, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1, 1, 1, 1, 1, 2], 
          [1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 2, 1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1, 1, 2, 1, 2, 2], 
          [1, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 2, 2, 1, 1, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 2, 2, 1, 2, 1, 1], 
          [2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 2, 2, 1, 1, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 2, 2, 2, 1, 2, 1, 2, 2], 
          [1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 1, 2, 1, 2, 0, 0, 0, 0, 0, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 1, 2, 1], 
          [1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 2, 2, 2, 1, 0, 0, 0, 0, 0, 1, 1, 2, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1], 
          [1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1], 
          [2, 2, 2, 1, 1, 2, 2, 1, 2, 2, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 1, 2, 2], 
          [1, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 0, 0, 0, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 2, 1, 2, 2, 2, 1, 2], 
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 2, 2, 1, 2, 1, 1, 1, 2, 2], 
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 1, 2], 
          [2, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 2, 2, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1], 
          [1, 2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 2, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 2, 1, 2, 1, 2, 2, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 2]]

   walls = []
   getWallPos(map, walls) #making the walls based on the map ^

   rocks = [(1260, 540), (1260, 660), (1620, 960), (1620, 1020), (1620, 1080), (1620, 1140)] #positions of all the rock, wood, and metal barriers
   wood = [(1380, 420), (1440, 420), (1320, 720), (1380, 720), (1440, 720), (1500, 1020), (1560, 1020)]
   metal = [(1260, 480), (840, 600), (1260, 600), (840, 660), (720, 1560), (720, 1620)]
   barriers = [rocks, wood, metal] #compiling into one list for easier use

   #list of all the possible choices or diamonds to be randomly placed on
   diamondChoices = [(1380, 240), (1440, 240), (1500, 240), (1560, 240), (1620, 240), (1680, 240), (1740, 240), (1800, 240), (1860, 240), 
                     (1920, 240), (1980, 240), (2040, 240), (2100, 240), (2160, 240), (1440, 300), (1500, 300), (1560, 300), (1620, 300), 
                     (1680, 300), (1740, 300), (1800, 300), (1860, 300), (1920, 300), (1980, 300), (2040, 300), (2100, 300), (2160, 300), 
                     (1380, 360), (1440, 360), (1860, 360), (1920, 360), (1980, 360), (2040, 360), (2100, 360), (2160, 360), (1860, 420), 
                     (1920, 420), (2040, 420), (2100, 420), (2160, 420), (900, 480), (960, 480), (1080, 480), (1200, 480), (1320, 480), 
                     (1380, 480), (1440, 480), (2100, 480), (2160, 480), (2220, 480), (2280, 480), (900, 540), (960, 540), (1020, 540), 
                     (1080, 540), (1140, 540), (1200, 540), (1320, 540), (1380, 540), (1440, 540), (2040, 540), (2100, 540), (2160, 540), 
                     (2220, 540), (2280, 540), (480, 600), (540, 600), (600, 600), (660, 600), (720, 600), (780, 600), (900, 600), (960, 600), 
                     (1020, 600), (1080, 600), (1140, 600), (1200, 600), (1320, 600), (1380, 600), (1440, 600), (2040, 600), (2100, 600), 
                     (2160, 600), (2220, 600), (2280, 600), (420, 660), (480, 660), (540, 660), (600, 660), (660, 660), (720, 660), (780, 660), 
                     (900, 660), (960, 660), (1020, 660), (1080, 660), (1140, 660), (1200, 660), (1320, 660), (1380, 660), (1440, 660), (2040, 660), 
                     (2100, 660), (2160, 660), (2220, 660), (2280, 660), (1500, 720), (1560, 720), (1320, 780), (1380, 780), (1440, 780), (1500, 780), 
                     (1560, 780), (1320, 840), (1380, 840), (1440, 840), (1500, 840), (1560, 840), (1320, 900), (1380, 900), (1440, 900), (1500, 900), 
                     (1560, 900), (1320, 960), (1380, 960), (1440, 960), (1500, 960), (1560, 960), (1680, 960), (1740, 960), (1800, 960), (1380, 1020), 
                     (1440, 1020), (1680, 1020), (1740, 1020), (1800, 1020), (1320, 1080), (1380, 1080), (1440, 1080), (1500, 1080), (1560, 1080), 
                     (1680, 1080), (1740, 1080), (1800, 1080), (1320, 1140), (1380, 1140), (1440, 1140), (1500, 1140), (1560, 1140), (1680, 1140), 
                     (1740, 1140), (780, 1200), (840, 1200), (900, 1200), (960, 1200), (1380, 1200), (1440, 1200), (1500, 1200), (1560, 1200), (780, 1260), 
                     (840, 1260), (900, 1260), (960, 1260), (1020, 1260), (1320, 1260), (1380, 1260), (1440, 1260), (1500, 1260), (1560, 1260), 
                     (840, 1320), (900, 1320), (960, 1320), (1020, 1320), (1320, 1320), (1380, 1320), (1440, 1320), (1500, 1320), (1560, 1320), (780, 1380), 
                     (840, 1380), (900, 1380), (960, 1380), (1020, 1380), (1080, 1380), (1140, 1380), (1200, 1380), (1260, 1380), (1320, 1380), (1380, 1380), 
                     (1440, 1380), (1500, 1380), (1560, 1380), (840, 1440), (900, 1440), (960, 1440), (1020, 1440), (1080, 1440), (1140, 1440), (1200, 1440), 
                     (1260, 1440), (1320, 1440), (1380, 1440), (1440, 1440), (1500, 1440), (1560, 1440), (780, 1500), (840, 1500), (900, 1500), (0, 1560), 
                     (60, 1560), (120, 1560), (180, 1560), (240, 1560), (300, 1560), (360, 1560), (420, 1560), (480, 1560), (540, 1560), (600, 1560), (660, 1560), 
                     (780, 1560), (840, 1560), (900, 1560), (0, 1620), (60, 1620), (120, 1620), (180, 1620), (240, 1620), (300, 1620), (360, 1620), (420, 1620), 
                     (480, 1620), (540, 1620), (600, 1620), (660, 1620), (780, 1620), (840, 1620), (900, 1620)]
   
   diamonds = []
   getDiamondPos(diamondChoices, diamonds, 10) #randomly placing the diamonds
   greens = 0 #num of green diamonds
   purples = 0 #num of purple diamonds

   closedChest = [(1980, 420), (420, 600), (1800, 1140), (1020, 1200)] #chests that havent been opened
   openChest = [] #used for storing chests that have been opened

   fires = [Rect(2040, 480, 60, 60), Rect(1320, 1020, 60, 60), Rect(780, 1320, 60, 60)] #Rects of fire blasts
   fireCounter = [0, 0, 0] #counter for each fire blast animation

   snakes = [[1380, 300, 1, 0, 0], [1020, 480, 1, 1, 2], [1140, 480, 1, 1, 2], [1320, 1200, 1, 0, 0], [780, 1440, 1, 0, 0]] #information for all the snakes
   snakeRanges = [(1380, 2160), (480, 660), (480, 660), (1320, 1560), (780, 1560)] #starting and ending position for each snake

   givenTime = 120 #how many seconds for that level
   timer = 0 #clock 
   timerCounter = 0 #counter variable for the clock

   exitBlocks = [(2340, 480), (2340, 540), (2340, 600), (2340, 660)] #blocks that player has to reach to end level

   lives = 3 #player starts with all 3 lives
   isLosingLife = False #player is not currently losing a life
   mute = False #if the volume is muted or not
   walking = True #if the player is walking, as opposed to burning or hammering

      #x  y direction frame
   player = [0, 1560, 4, 0]
   movePlayerCount = 0 #counter to slow down animation time for character

   barriersBreaking = [] #list that will contain the blocks that are being destroyed (for animating)
   hammering = [] #list for storing information for character hammering blocks animation

   running = True

   while running:
      for evt in event.get():
            if evt.type == QUIT:
               running = False
            #checking if user presses mute button, changing mute variable if user did
            mute = changeVolume(mute, evt)

      ## MOVING MOVING PARTS
      movePlayerCount = movePlayer(player, walls, barriers, movePlayerCount) #moving the player
      moveSnakes(snakes, snakeRanges) 
      moveFire(fires, fireCounter) 
      barriersBreaking = moveBarrier(barriersBreaking)

      ## CHANGING THINGS 
      timer, timerCounter = changeTime(timer, timerCounter)

      ## CHECKING IF PLAYER HIT THINGS
      allObstacles = getObstacles(fires, snakes)
     
      isLosingLife, lives = hitObstacle(player, allObstacles, lives, isLosingLife) #hit any obstacle
      purples, greens = hitTreasure(player, diamonds, closedChest, openChest, greens, purples)
      hammering, barriersBreaking = hitBarrier(player, barriersBreaking, barriers, barrierImages, hammering, hammeringImages)

      ## DRAWING EVERYTHING
      blittingPosX, blittingPosY = getBlittingPos(player, 2400, 2040)
      hammering = drawScene(blittingPosX, blittingPosY, level2Map, player, walkingImages, hammering, barriersBreaking, snakes, snakesWalkingImages, diamonds, purple, openChest, openChestImage, closedChest, closedChestImage, fires, fireImages, burnedPlayer, barriers, barrierImages, walking, hammerUp)
      drawToolbar(toolbar, heart, purples, greens, lives, mute, volumeOn, volumeOff, timerBlock, timer, fontToolbar, fontTimer)

      #updating, get one green diamond in each chest so num of green diamonds = num of opened chest
      greens = len(openChest)

      ## CHECKING CURRENT SITUATION
      page = checkLives(lives) #check if player has one or more lives
      if page != None: #if they don't
         return levelsOpen, levelPos, page, greens, purples, 10 #bring them to the No Lives page

      page = checkTime(timer, givenTime) #same thing but for No Time
      if page != None:
         return levelsOpen, levelPos, page, greens, purples, 10

      #if the player reached the end of the level
      if (player[X], player[Y]) in exitBlocks:
         levelsOpen, page = checkDiamonds(greens, 4, levelPos, levelsOpen, timer) #checks they have enough diamonds to complete the level
         return levelsOpen, levelPos, page, greens, purples, 10

      myClock.tick(60)
      
      display.flip()

   return levelsOpen, levelPos, "map", greens, purples, 10


def finalLevel(levelsOpen, levelPos):

    #map of the level, used for making walls
   map = [[1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 2, 2, 2, 1, 1, 2, 1, 2, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, 2, 2, 2, 1, 0, 0, 2], 
          [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 1, 0, 0, 2], 
          [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 1, 1, 0, 0, 1], 
          [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 2, 1, 0, 0, 1], 
          [1, 2, 0, 0, 0, 2, 1, 1, 2, 1, 0, 0, 0, 2, 2, 2, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 1, 1, 2, 0, 0, 2], 
          [2, 1, 0, 0, 0, 1, 1, 1, 1, 2, 0, 0, 0, 2, 1, 2, 1, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 2, 1, 1, 0, 0, 1], 
          [1, 1, 0, 0, 0, 2, 1, 1, 1, 1, 0, 0, 0, 2, 2, 1, 2, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 2, 2, 1, 0, 0, 1], 
          [1, 2, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 2, 2, 1, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 2, 1, 0, 0, 2], 
          [0, 0, 0, 0, 0, 1, 2, 1, 2, 1, 0, 0, 0, 2, 1, 1, 2, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 2, 1, 2, 0, 0, 2], 
          [0, 0, 0, 0, 0, 2, 1, 2, 1, 2, 0, 0, 0, 1, 1, 1, 2, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 1, 1, 0, 0, 1], 
          [0, 0, 0, 0, 0, 2, 1, 1, 1, 2, 0, 0, 0, 1, 2, 1, 2, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 1, 0, 0, 2], 
          [0, 0, 0, 0, 0, 1, 2, 2, 2, 1, 0, 0, 0, 1, 1, 1, 2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 2, 1, 1, 0, 0, 2], 
          [0, 0, 0, 0, 0, 2, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1], 
          [0, 0, 0, 0, 0, 2, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 1], 
          [0, 0, 0, 0, 0, 1, 2, 1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 2], 
          [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 2], 
          [2, 2, 2, 0, 0, 2, 2, 2, 2, 1, 0, 0, 2, 2, 2, 1, 2, 0, 0, 0, 1, 2, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 1], 
          [1, 1, 2, 0, 0, 1, 1, 1, 1, 2, 0, 0, 2, 2, 2, 2, 1, 0, 0, 0, 2, 2, 2, 1, 2, 2, 1, 1, 2, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 1], 
          [2, 2, 2, 0, 0, 1, 1, 1, 1, 2, 0, 0, 1, 2, 1, 1, 2, 0, 0, 0, 2, 2, 1, 2, 1, 1, 1, 2, 1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 1], 
          [2, 1, 2, 0, 0, 0, 0, 0, 2, 1, 0, 0, 1, 2, 2, 1, 1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
          [2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1, 2, 2, 2, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1], 
          [2, 2, 1, 0, 0, 0, 0, 0, 2, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 1], 
          [2, 1, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1, 2, 0, 0, 0, 1, 0, 0, 0, 1, 1, 2, 1, 2, 2, 2, 1, 2, 2, 1, 1, 1, 2, 1, 1, 0, 0, 0, 1], 
          [2, 2, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 1, 1, 2, 1, 0, 0, 0, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 1], 
          [1, 2, 0, 0, 0, 0, 0, 0, 2, 2, 1, 2, 1, 1, 1, 2, 1, 0, 0, 0, 2, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 0, 0, 0, 2], 
          [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 1, 2, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 2, 2, 2, 2, 1, 2, 0, 0, 0, 2], 
          [1, 1, 2, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 1, 2, 2, 2, 1, 1, 2, 0, 0, 0, 1], 
          [2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1], 
          [2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 1, 2, 2, 2, 1, 2, 1, 1, 1, 1, 2, 2, 1, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 1, 1], 
          [1, 2, 2, 1, 1, 2, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 1, 1, 1, 1, 2, 2, 2, 1, 2, 1, 2, 1, 2, 2, 2, 2, 1, 1]]

   walls = []
   getWallPos(map, walls) #making the walls based on the map ^

   rocks = [(600, 960), (660, 960), (1020, 960), (1080, 960), (1140, 960), (2220, 960), (2280, 960), (180, 1380), (180, 1440)]
   wood = [(2220, 360), (2280, 360), (2220, 420), (2280, 420), (960, 720), (1020, 720), (1080, 720), (1080, 780), (1080, 840), (1080, 900), (180, 960), (240, 960)]
   metal =[(420, 60), (480, 60), (420, 120), (480, 120), (480, 180), (540, 180), (1320, 240), (1380, 240), (1440, 240), (1500, 240), (1560, 240), (1620, 240), (1620, 300), 
           (1620, 360), (1620, 420), (1680, 420), (1740, 420), (1800, 420), (1620, 480), (1620, 540), (1620, 600), (1620, 660), (1620, 720), (960, 1200), (960, 1260)]
   barriers = [rocks, wood, metal] #compiling into one list for easier use

   #list of all the possible choices or diamonds to be randomly placed on
   diamondChoices = [(120, 60), (180, 60), (240, 60), (300, 60), (360, 60), (540, 60), (600, 60), (660, 60), (720, 60), (1020, 60), (1080, 60), (1140, 60), (1200, 60), 
                     (1260, 60), (1320, 60), (1380, 60), (1440, 60), (1500, 60), (1560, 60), (1620, 60), (1680, 60), (1740, 60), (1800, 60), (2220, 60), (2280, 60), 
                     (120, 120), (180, 120), (240, 120), (300, 120), (360, 120), (540, 120), (600, 120), (660, 120), (720, 120), (1020, 120), (1080, 120), (1140, 120), 
                     (1200, 120), (1260, 120), (1320, 120), (1380, 120), (1440, 120), (1500, 120), (1560, 120), (1620, 120), (1680, 120), (1740, 120), (1800, 120), 
                     (2220, 120), (2280, 120), (120, 180), (180, 180), (240, 180), (300, 180), (360, 180), (420, 180), (600, 180), (660, 180), (720, 180), (1020, 180), 
                     (1080, 180), (1140, 180), (1200, 180), (1260, 180), (1320, 180), (1380, 180), (1440, 180), (1500, 180), (1560, 180), (1620, 180), (1680, 180), 
                     (1740, 180), (1800, 180), (2220, 180), (2280, 180), (180, 240), (240, 240), (600, 240), (660, 240), (720, 240), (1080, 240), (1680, 240), (1740, 240), 
                     (1800, 240), (2220, 240), (2280, 240), (120, 300), (180, 300), (240, 300), (600, 300), (660, 300), (720, 300), (1020, 300), (1080, 300), (1140, 300), 
                     (1320, 300), (1380, 300), (1440, 300), (1500, 300), (1560, 300), (1680, 300), (1740, 300), (1800, 300), (2220, 300), (2280, 300), (120, 360), (180, 360), 
                     (240, 360), (600, 360), (660, 360), (720, 360), (1020, 360), (1080, 360), (1140, 360), (1320, 360), (1380, 360), (1440, 360), (1500, 360), (1560, 360), 
                     (1680, 360), (1740, 360), (1800, 360), (120, 420), (180, 420), (240, 420), (600, 420), (660, 420), (720, 420), (1080, 420), (1140, 420), (1380, 420), 
                     (1440, 420), (1500, 420), (60, 480), (180, 480), (240, 480), (600, 480), (660, 480), (720, 480), (1020, 480), (1080, 480), (1140, 480), (1320, 480), 
                     (1380, 480), (1440, 480), (1500, 480), (1560, 480), (1680, 480), (1740, 480), (1800, 480), (2220, 480), (2280, 480), (60, 540), (120, 540), (180, 540), 
                     (240, 540), (660, 540), (720, 540), (1020, 540), (1080, 540), (1140, 540), (1320, 540), (1380, 540), (1440, 540), (1500, 540), (1560, 540), (1680, 540), 
                     (1740, 540), (1800, 540), (2220, 540), (2280, 540), (60, 600), (120, 600), (180, 600), (240, 600), (600, 600), (660, 600), (720, 600), (1020, 600), 
                     (1080, 600), (1140, 600), (1320, 600), (1440, 600), (1500, 600), (1560, 600), (1680, 600), (1740, 600), (1800, 600), (2220, 600), (2280, 600), (60, 660), 
                     (120, 660), (180, 660), (240, 660), (600, 660), (660, 660), (720, 660), (1020, 660), (1080, 660), (1140, 660), (1320, 660), (1380, 660), (1440, 660), 
                     (1500, 660), (1680, 660), (1740, 660), (1800, 660), (2220, 660), (2280, 660), (60, 720), (120, 720), (180, 720), (240, 720), (660, 720), (720, 720), 
                     (780, 720), (900, 720), (1140, 720), (1680, 720), (1740, 720), (1800, 720), (1860, 720), (1920, 720), (1980, 720), (2040, 720), (2220, 720), (2280, 720), 
                     (60, 780), (120, 780), (180, 780), (240, 780), (600, 780), (660, 780), (720, 780), (780, 780), (840, 780), (900, 780), (960, 780), (1020, 780), (1140, 780), 
                     (1320, 780), (1380, 780), (1440, 780), (1500, 780), (1560, 780), (1620, 780), (1680, 780), (1740, 780), (1800, 780), (1920, 780), (1980, 780), (2040, 780), 
                     (2220, 780), (2280, 780), (60, 840), (120, 840), (180, 840), (240, 840), (600, 840), (660, 840), (720, 840), (780, 840), (840, 840), (900, 840), (960, 840), 
                     (1020, 840), (1140, 840), (1320, 840), (1380, 840), (1440, 840), (1500, 840), (1560, 840), (1620, 840), (1680, 840), (1740, 840), (1980, 840), (2220, 840), 
                     (2280, 840), (60, 900), (180, 900), (240, 900), (600, 900), (660, 900), (720, 900), (780, 900), (840, 900), (900, 900), (960, 900), (1020, 900), (1140, 900), 
                     (1620, 900), (1680, 900), (1740, 900), (1800, 900), (1860, 900), (1980, 900), (2040, 900), (2220, 900), (2280, 900), (1740, 960), (1800, 960), (1860, 960), 
                     (1980, 960), (2040, 960), (180, 1020), (240, 1020), (600, 1020), (660, 1020), (1080, 1020), (1140, 1020), (1740, 1020), (1800, 1020), (1980, 1020), 
                     (2040, 1020), (2220, 1020), (2280, 1020), (180, 1080), (240, 1080), (600, 1080), (660, 1080), (1080, 1080), (1140, 1080), (1740, 1080), (1800, 1080), 
                     (1920, 1080), (1980, 1080), (2040, 1080), (2220, 1080), (2280, 1080), (180, 1140), (240, 1140), (360, 1140), (600, 1140), (660, 1140), (1020, 1140), 
                     (1080, 1140), (1140, 1140), (1740, 1140), (1800, 1140), (1860, 1140), (1920, 1140), (1980, 1140), (2100, 1140), (2160, 1140), (2220, 1140), (2280, 1140), 
                     (180, 1200), (240, 1200), (300, 1200), (360, 1200), (420, 1200), (600, 1200), (660, 1200), (780, 1200), (840, 1200), (900, 1200), (1020, 1200), (1080, 1200), 
                     (1140, 1200), (1740, 1200), (1800, 1200), (1980, 1200), (2040, 1200), (2100, 1200), (2160, 1200), (2220, 1200), (2280, 1200), (180, 1260), (240, 1260), 
                     (300, 1260), (360, 1260), (420, 1260), (600, 1260), (660, 1260), (780, 1260), (840, 1260), (900, 1260), (1020, 1260), (1080, 1260), (1740, 1260), (1800, 1260), 
                     (1980, 1260), (2040, 1260), (2100, 1260), (2220, 1260), (2280, 1260), (120, 1320), (180, 1320), (240, 1320), (300, 1320), (360, 1320), (420, 1320), (840, 1320), 
                     (900, 1320), (1020, 1320), (1080, 1320), (1140, 1320), (2160, 1320), (2220, 1320), (2280, 1320), (120, 1380), (240, 1380), (300, 1380), (360, 1380), (420, 1380), 
                     (1020, 1380), (1080, 1380), (1140, 1380), (2160, 1380), (2220, 1380), (2280, 1380), (240, 1440), (360, 1440), (420, 1440), (1080, 1440), (1140, 1440), 
                     (2160, 1440), (2220, 1440), (2280, 1440), (2160, 1500), (2220, 1500), (2280, 1500), (2160, 1560), (2220, 1560)]
   
   diamonds = []
   getDiamondPos(diamondChoices, diamonds, 20) #randomly placing the diamonds
   greens = 0 #num of green diamonds
   purples = 0 #num of purple diamonds

   closedChest = [(1380, 600), (420, 1140), (1140, 1260), (780, 1320), (120, 1440), (2280, 1560)] #chests that havent been opened
   openChest = [] #used for storing chests that have been opened

   fires = [Rect(120, 240, 60, 60), Rect(1020, 420, 60, 60), Rect(1320, 420, 60, 60), Rect(600, 540, 60, 60), Rect(1020, 1020, 60, 60)] #Rects of fire blasts
   fireCounter = [0, 0, 0, 0, 0] #counter for each fire blast animation

   snakes = [[1020, 240, 1, 0, 0], [1560, 420, 1, 1, 2], [120, 480, 1, 1, 2], [600, 720, 1, 0, 0], [1020, 1080, 1, 1, 2], [300, 1140, 1, 1, 2]] #information for all the snakes
   snakeRanges = [(1020, 1140), (420, 660), (480, 900), (600, 840), (1080, 1440), (1140, 1440)] #starting and ending position for each snake

   bossSnake = [1920, 1020, 1] #position of boss snake
   bossSnakeStation = (1920, 1020) #the default station that it'll return to once player isn't in range
   bossSnakeRange = Rect(1740, 900, 360, 180) #range

   givenTime = 180 #how many seconds for that level
   timer = 0 #clock 
   timerCounter = 0 #counter variable for the clock

   exitBlocks = [(2220, 0), (2280, 0)] #blocks that player has to reach to end level

   lives = 3 #player starts with all 3 lives
   isLosingLife = False #player is not currently losing a life
   mute = False #if the volume is muted or not
   walking = True #if the player is walking, as opposed to burning or hammering

      #x  y direction frame
   player = [0, 480, 4, 0]
   movePlayerCount = 0 #counter to slow down animation time for character

   barriersBreaking = [] #list that will contain the blocks that are being destroyed (for animating)
   hammering = [] #list for storing information for character hammering blocks animation

   running = True

   while running:
      for evt in event.get():
            if evt.type == QUIT:
               running = False
            #checking if user presses mute button, changing mute variable if user did
            mute = changeVolume(mute, evt)

      ## MOVING MOVING PARTS
      movePlayerCount = movePlayer(player, walls, barriers, movePlayerCount) #moving the player
      moveSnakes(snakes, snakeRanges) 
      moveFire(fires, fireCounter) 
      barriersBreaking = moveBarrier(barriersBreaking)
      moveBossSnake(player, bossSnake, bossSnakeStation, bossSnakeRange)
      
      ## CHANGING THINGS 
      timer, timerCounter = changeTime(timer, timerCounter)
     
      ## CHECKING IF PLAYER HIT THINGS
      allObstacles = getObstacles(fires, snakes)
      allObstacles += [Rect(bossSnake[X], bossSnake[Y], WIDTH, HEIGHT)] #adding boss snake to obstacles that would cost a life

      isLosingLife, lives = hitObstacle(player, allObstacles, lives, isLosingLife) #hit any obstacle
      purples, greens = hitTreasure(player, diamonds, closedChest, openChest, greens, purples)
      hammering, barriersBreaking = hitBarrier(player, barriersBreaking, barriers, barrierImages, hammering, hammeringImages)

      ## DRAWING EVERYTHING
      blittingPosX, blittingPosY = getBlittingPos(player, 2400, 2040)
      hammering = drawScene(blittingPosX, blittingPosY, level3Map, player, walkingImages, hammering, barriersBreaking, snakes, snakesWalkingImages, diamonds, purple, openChest, openChestImage, closedChest, closedChestImage, fires, fireImages, burnedPlayer, barriers, barrierImages, walking, hammerUp)

      #drawing boss snake
      screen.blit(bossSnakeImages[bossSnake[2]-1], (blittingPosX+bossSnake[X], blittingPosY+bossSnake[Y]))

      drawToolbar(toolbar, heart, purples, greens, lives, mute, volumeOn, volumeOff, timerBlock, timer, fontToolbar, fontTimer)

      #updating, get one green diamond in each chest so num of green diamonds = num of opened chest
      greens = len(openChest)

      ## CHECKING CURRENT SITUATION
      page = checkLives(lives) #check if player has one or more lives
      if page != None: #if they don't
         return levelsOpen, levelPos, page, greens, purples, 20 #bring them to the No Lives page

      page = checkTime(timer, givenTime) #same thing but for No Time
      if page != None:
         return levelsOpen, levelPos, page, greens, purples, 20

      #if the player reached the end of the level
      if (player[X], player[Y]) in exitBlocks:
         levelsOpen, page = checkDiamonds(greens, 6, levelPos, levelsOpen, timer) #checks they have enough diamonds to complete the level
         return levelsOpen, levelPos, page, greens, purples, 20

      myClock.tick(60)
      
      display.flip()

   return levelsOpen, levelPos,  "map", greens, purples, 20


def noLives(noLivesFrames, levelPos): #program for displaying "no more lives left" screen
   retry = Rect(235, 518, 155, 66) #button for playing the level agian
   backToHome = Rect(525, 515, 235, 70) #button for bringing user back to map

   running = True
   counter = 0 #counter for animation

   while running:
      for evt in event.get():
         if evt.type == QUIT:
            running = False
         if evt.type == MOUSEBUTTONDOWN:
            mx, my = mouse.get_pos()
            if retry.collidepoint(mx, my): #if user clicked on retry button, play level again
               return levelPos, "lev" + str(levelPos+1) #change page variable to same level again
            
            if backToHome.collidepoint(mx, my): #if user clicked to return to map, quit while loop to return to map
               running = False

      counter += 1 #changing frame slowly

      if counter < 96: #if animation isn't done
         screen.blit(noLivesFrames[int(counter//4)], (0, 0)) #blit the screen at counter
      else:
         screen.blit(noLivesFrames[-1], (0, 0)) #otherwise just keep blitting the last screen

      myClock.tick(60)
           
      display.flip()

   return levelPos, "map" 


def timeOver(noTimeFrames, levelPos): #program for displaying "no more time left" screen
   retry = Rect(150, 500, 155, 60) #retry the level
   backToHome = Rect(385, 495, 235, 70) #back to map

   counter = 0 #counter for the animation

   running = True

   while running:
      for evt in event.get():
         if evt.type == QUIT:
            running = False
         if evt.type == MOUSEBUTTONDOWN:
            mx, my = mouse.get_pos()
            if retry.collidepoint(mx, my): #if retry, page = current level again
               return levelPos, "lev" + str(levelPos+1)
            if backToHome.collidepoint(mx, my): #if back to map, end while loop to get to return statement
               running = False
      
      counter += 1 #changing frame slowly

      if counter < 128: #if animation isn't done
         screen.blit(noTimeFrames[int(counter//4)], (0, 0)) #blit the screen at counter
      else:
         screen.blit(noTimeFrames[-1], (0, 0)) #otherwise just keep blitting the last screen
      
      myClock.tick(60)

      display.flip()

   return levelPos, "map" 


def win(winFrames, purples, greens, neededPurples, font):#program for displaying "level complete" screen
   backToHome = Rect(375, 560, 250, 70) #go back to map

   counter = 0 #counter for animation
   running = True

   while running:
      for evt in event.get():
         if evt.type == QUIT:
            running = False
         if evt.type == MOUSEBUTTONDOWN:
            mx, my = mouse.get_pos()
            if backToHome.collidepoint(mx, my): #if back to home, end while loop to return "map"
               running = False

      counter += 1 #changing frame slowly

      if counter < 36: #if animation isn't done
         screen.blit(winFrames[int(counter//3)], (0, 0)) #blit the screen at counter
      else:
         screen.blit(winFrames[-1], (0, 0)) #otherwise just keep blitting the last screen
         purpleNum = font.render(f"{purples}/{neededPurples}", True, WHITE)
         greenNum = font.render(f"{greens}/{greens}", True, WHITE)
         screen.blit(purpleNum, (110, 125))
         screen.blit(greenNum, (520, 125))
      
      myClock.tick(60)
      
      display.flip()

   return "map"


def noDiamonds(noDiamondsScreen, levelPos): #program for displaying "not enough diamonds" screen
   retry = Rect(770, 415, 125, 65) #to replay the level
   backToHome = Rect(705, 520, 250, 65) #go back to map button

   counter = 0 #counter for animation
   running = True

   while running:
      for evt in event.get():
         if evt.type == QUIT:
            running = False
         if evt.type == MOUSEBUTTONDOWN:
            mx, my = mouse.get_pos()
            if retry.collidepoint(mx, my): #if retry, page = current level again
               return levelPos, "lev" + str(levelPos+1)
            if backToHome.collidepoint(mx, my): #if back to home, end while loop to return "map"
               running = False

      counter += 1 #changing frame slowly

      if counter < 45: #if animation isn't done
         screen.blit(noDiamondsScreen[int(counter//3)], (0, 0)) #blit the screen at counter
      else:
         screen.blit(noDiamondsScreen[-1], (0, 0)) #otherwise just keep blitting the last screen

      myClock.tick(60)

      display.flip()

   return levelPos, "map" 
