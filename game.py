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
        self.jumpVel = 25
        self.fallVel = 1
        self.blobShow = 1
        self.onGround = True
        self.jumpCount = 0
        self.falling = False
        self.overCount = 0

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

    def groundUpdate(self):
        if self.pos[1] >= self.windowSize[1]-self.blobSize:
            self.pos[1] = self.windowSize[1]-self.blobSize
            self.onGround = True
            self.jumpCount = 0
    
    def move(self, y):
        obstacle = False
        if y < 0 and self.collision == -1:
            obstacle = True
        if self.collision == 1:
            obstacle = True
        if self.pos[1] >= self.windowSize[1]-self.blobSize:
            self.pos[1] = self.windowSize[1]-self.blobSize
            self.onGround = True
        else:
            self.onGround = False
        if not obstacle:
            if y > 1 and self.onGround:
                pass
            else:
                self.pos[1] += y
            return True
        return False

    def jump(self):
        self.jumpCount += 1
        self.jumping = True
        self.jumpVel = 25

    def jumpCalc(self):
        if self.jumping:
                if self.jumpVel > 2:
                    self.move(-self.jumpVel)
                    self.jumpVel -= self.jumpVel/10
                else:
                    self.jumping = False
                    self.jumpVel = 20


    def fall(self):
        falling = self.move(self.fallVel)
        if self.fallVel > 20:
            self.fallVel = 20
        if falling:
            self.fallVel += self.fallVel*0.1
        else:
            self.fallVel = 1

    def check_collision(self, pos, size):
        collision = False
        Xd = 0
        Yd = 0
        if self.pos[0]+self.blobSize >= pos[0] and self.pos[0] <= pos[0]+size:
            if self.pos[1]+self.blobSize >= pos[1] and self.pos[1] <= pos[1]+size:
                Yd = (self.pos[1]+self.blobSize)-pos[1]
                collision = True

        if collision:
            if Yd and Yd < 35:
                self.collision = 1
                self.fallVel = 1
                self.pos[1] = pos[1]-self.blobSize
                self.jumpCount = 0
                return 1
            else:
                self.overCount += 1
                if self.overCount > 2 and self.collision != 1:
                    return -1
                else:
                    return 0
        else:
            self.collision = 0
            return 0

class Block():
    def __init__(self, windowSize):
        self.windowSize = windowSize
        self.blockSize = windowSize[1]//7
        self.blockImg = pygame.transform.scale(pygame.image.load("leblocksingle.png"), (self.blockSize, self.blockSize))
        self.pos = [windowSize[0], windowSize[1]-((self.blockSize+(self.blockSize/10))*random.randint(1,2))]

    def getPos(self):
        return self.pos

    def getSize(self):
        return self.blockSize
    
    def move(self, x):
        self.pos[0] += x

    def draw(self, screen):
        screen.blit(self.blockImg, self.pos)
            

def game():
    halfScreen = pyautogui.size()[1]//2
    size = (halfScreen, int(halfScreen*0.71))
    blob = Blob(size)
    bg_img = pygame.transform.scale(pygame.image.load("bg.png"), (size[0], size[1]))
    bg = [0, size[0]]
    bg_velocity = 0.5
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    count = 0
    jumpLimit = 2
    jumpCount = 0
    blocks = []
    over = False
    score = 0
    prevScore = 0
    fps = 60
    scored_blocks = []

    halfSec = pygame.USEREVENT
    pygame.time.set_timer(halfSec, 500)

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

            if not over:
                if event.type == halfSec:
                    blob.changeDraw()

                    luck = random.randint(0, 4)
                    if not luck:
                        blocks.append(Block(size))

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        if blob.jumpCount < 1:
                            blob.jump()
    
        # --- Game logic should go here
        if not over:

            # scoring when blob passes block
            for block in blocks:
                if not block in scored_blocks:
                    if blob.getPos()[0] > block.getPos()[0]:
                        score += 10
                        scored_blocks.append(block)
            for index, blocky in enumerate(scored_blocks):
                if not blocky in blocks:
                    del scored_blocks[index]

            # adjusting fps every 100 score
            if score - prevScore == 100:
                fps += 10
                prevScore = score

            #print(blob.jumpCount)
            for block in blocks:
                if blob.check_collision(block.getPos(), block.getSize()) == -1:
                    over = True

            # moving background
            for x in range(len(bg)):
                bg[x] -= bg_velocity
            if bg[0] <= -size[0]:
                bg[0] = 0
                bg[1] = size[0]

            # moving blob, really just jumping and falling
            blob.groundUpdate()
            if not blob.jumping:
                blob.fall()
            else:
                blob.fallVel = 1
                blob.jumpCalc()
            #if blob.onGround:
            #    jumpCount = 0

            # remove off screen blocks
            for index, block in enumerate(blocks):
                if block.getPos()[0] <= -block.getSize():
                    del blocks[index]

            # moving blocks
            for block in blocks:
                block.move(-5)
    
        # --- Screen-clearing code
        for x in bg:
            screen.blit(bg_img, (x,0))
    
        # --- Drawing code
        blob.draw(screen)
        for block in blocks:
            block.draw(screen)

        # --- score
        # Select the font to use, size, bold, italics
        font = pygame.font.SysFont('Calibri', size[1]//10, True, False)
        # text, anti-aliased, color
        text = font.render(f"SCORE: {score}",True,BLACK)
        screen.blit(text, [size[0]/15, size[1]/15])

        # --- speed
        # Select the font to use, size, bold, italics
        font = pygame.font.SysFont('Calibri', size[1]//10, True, False)
        # text, anti-aliased, color
        text = font.render(f"SPEED: {fps-60}",True,BLACK)
        screen.blit(text, [size[0]/15, size[1]/15*2])
    
        # --- Update the screen
        pygame.display.flip()
    
        # --- Limit to 60 frames per second
        clock.tick(60)
    
    # Close the window and quit.
    pygame.quit()