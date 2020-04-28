import pygame, pyautogui, random

class Blob():
    def __init__(self, windowSize):
        self.windowSize = windowSize
        self.blobSize = windowSize[1]//7
        self.run1 = pygame.transform.scale(pygame.image.load("leblob.png"), (self.blobSize, self.blobSize))
        self.run2 = pygame.transform.scale(pygame.image.load("leblobfastomg.png"), (self.blobSize, self.blobSize))
        self.jumping = False
        self.pos = [windowSize[0]//8, windowSize[1]-self.blobSize]
        self.collision = 0
        self.jumpVel = 20
        self.fallVel = 1
        self.blobShow = 1
        self.onGround = True

    def changeDraw(self):
        if self.blobShow:
            self.blobShow = 0
        else:
            self.blobShow = 1

    def draw(self, screen):
        if self.blobShow:
            screen.blit(self.run1, self.pos)
        else:
            screen.blit(self.run2, self.pos)

    def getPos(self):
        return self.pos

    def getSize(self):
        return self.blobSize
    
    def move(self, y):
        obstacle = False
        self.onGround = False
        if y < 0 and self.collision == -1:
            obstacle = True
        if y > 0 and self.collision == 1:
            obstacle = True
        if self.pos[1] > self.windowSize[1]-self.blobSize:
            self.pos[1] = self.windowSize[1]-self.blobSize
            obstacle = True
            self.onGround = True
        if not obstacle:
            self.pos[1] += y
            return True
        return False

    def jump(self):
        if self.jumpVel > 2:
            self.move(-self.jumpVel)
            self.jumpVel -= self.jumpVel/10
        else:
            self.jumping = False
            self.jumpVel = 20

    def fall(self):
        falling = self.move(self.fallVel)
        if falling:
            self.fallVel += self.fallVel*0.1
        else:
            self.fallVel = 1

class Block():
    def __init__(self, windowSize):
        self.windowSize = windowSize
        self.blockSize = windowSize[1]//7
        self.blockImg = pygame.transform.scale(pygame.image.load("leblocksingle.png"), (self.blockSize, self.blockSize))
        self.pos = [windowSize[0], windowSize[1]-(self.blockSize*random.randint(1,2))]

    def getPos(self):
        return self.pos

    def getSize(self):
        return self.blockSize
    
    def move(self, x):
        self.pos[0] += x

    def draw(self, screen):
        screen.blit(self.blockImg, self.pos)

def collision(Pos1, Size1, Pos2, Size2):
    if Pos1[0]+Size1 >= Pos2[0]:
        if Pos1[1]+Size1 > Pos2[1] and Pos1[1] < Pos2[1]+Size2:
            return 0
    elif Pos1[1]+Size1 >= Pos2[1]:
        if Pos1[0]+Size1 > Pos2[0] and Pos1[0] < Pos2[0]+Size2:
            print("on block")
            return 1
    else:
        return 2
            

def game():
    halfScreen = pyautogui.size()[1]//2
    size = (halfScreen, int(halfScreen*0.71))
    blob = Blob(size)
    bg_img = pygame.transform.scale(pygame.image.load("bg.png"), (size[0], size[1]))
    bg = [0, size[0]]
    bg_velocity = 0.5
    WHITE = (255, 255, 255)
    count = 0
    jumpLimit = 2
    jumpCount = 0
    blocks = []

    changeDrawing = pygame.USEREVENT
    pygame.time.set_timer(changeDrawing, 500)
    spawnBlock = pygame.USEREVENT
    pygame.time.set_timer(spawnBlock, 500)

    screen = pygame.display.set_mode(size)
    
    pygame.display.set_caption("My Game")
    
    done = False
    clock = pygame.time.Clock()
    
    # -------- Main Program Loop -----------
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == changeDrawing:
                blob.changeDraw()

            if event.type == spawnBlock:
                luck = random.randint(0, 4)
                if not luck:
                    blocks.append(Block(size))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if not jumpCount >= jumpLimit:
                        jumpCount += 1
                        blob.jumping = True
    
        # --- Game logic should go here

        # collision 
        for block in blocks:
            if collision(blob.getPos(), blob.getSize(), block.getPos(), block.getSize()) == 1:
                blob.collision = 1
            elif collision(blob.getPos(), blob.getSize(), block.getPos(), block.getSize()) == 0:
                print("game over")
            elif collision(blob.getPos(), blob.getSize(), block.getPos(), block.getSize()) == 2:
                blob.collision = 0

        # moving background
        for x in range(len(bg)):
            bg[x] -= bg_velocity
        if bg[0] <= -size[0]:
            bg[0] = 0
            bg[1] = size[0]

        # moving blob, really just jumping and falling
        if not blob.jumping:
            blob.fall()
        else:
            blob.fallVel = 1
            blob.jump()
        if blob.onGround:
            jumpCount = 0

        # moving blocks
        for block in blocks:
            block.move(-5)
    
        # --- Screen-clearing code goes here
        for x in bg:
            screen.blit(bg_img, (x,0))
    
        # --- Drawing code should go here
        blob.draw(screen)
        for block in blocks:
            block.draw(screen)
    
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
    
        # --- Limit to 60 frames per second
        clock.tick(60)
    
    # Close the window and quit.
    pygame.quit()