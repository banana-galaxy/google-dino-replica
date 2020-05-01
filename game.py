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
        self.states = ["on ground", "jumping", "falling", "on block"]
        self.state = self.states[0]
        self.velocity = 0

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
            self.velocity = 0

    def checkGround(self):
        if self.pos[1] >= self.windowSize[1]-self.blobSize:
            self.state = self.states[0]
    
    def move(self, y):
        obstacle = False
        if y < 0 and self.collision == -1:
            obstacle = True
        if self.collision == 1:
            obstacle = True
        if self.pos[1] >= self.windowSize[1]-self.blobSize:
            self.pos[1] = self.windowSize[1]-self.blobSize
            self.onGround = True
            self.state = self.states[0]
        else:
            self.onGround = False
        if not obstacle:
            if y > 1 and self.onGround:
                self.state = self.states[0]
                pass
            else:
                self.pos[1] += y
                self.velocity = y
            return True
        if obstacle and self.collision == 1:
            if y < 0:
                self.pos[1] += y
                self.velocity = y
                return True
        self.velocity = 0
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
                    self.state = self.states[1]
                else:
                    self.jumping = False
                    self.jumpVel = 20


    def fall(self):
        falling = self.move(self.fallVel)
        if self.fallVel > 20:
            self.fallVel = 20
        if falling:
            self.fallVel += self.fallVel*0.1
            self.state = self.states[2]
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

        #print(collision, Yd)

        if collision:
            if Yd < 35 and Yd >= 0:
                self.collision = 1
                self.fallVel = 1
                self.pos[1] = pos[1]-self.blobSize
                self.jumpCount = 0
                self.state = self.states[3]
                return 1
            else:
                return -1
        else:
            #self.overCount = 0
            self.collision = 0
            return 0
    def reset(self):
        self.pos[1] = self.windowSize[1]-self.blobSize
        self.onGround = True
        self.jumpCount = 0
        self.jumping = False
        self.jumpVel = 25
        self.fallVel = 1
        self.velocity = 0
        self.collision = 0
        self.state = self.states[0]

class Block():
    def __init__(self, windowSize):
        self.windowSize = windowSize
        self.blockSize = windowSize[1]//7
        self.blockImg = pygame.transform.scale(pygame.image.load("leblocksingle.png"), (self.blockSize, self.blockSize))
        number = random.randint(0,2)
        if number == 0:
            self.pos = [windowSize[0], windowSize[1]-((self.blockSize+(self.blockSize/10))*2)]
        else:
            self.pos = [windowSize[0], windowSize[1]-((self.blockSize+(self.blockSize/10))*1)]

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
    jumpCount = 0
    blocks = []
    over = False
    score = 0
    prevScore = 0
    scored_blocks = []
    speed = -5
    time = 500
    debug = False
    superDebug = False

    halfSec = pygame.USEREVENT
    pygame.time.set_timer(halfSec, time)

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
                    if event.key == pygame.K_y:
                        if debug:
                            debug = False
                            superDebug = False
                        else:
                            debug = True
                    if event.key == pygame.K_u:
                        if debug:
                            if superDebug:
                                superDebug = False
                            else:
                                superDebug = True
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                            if over:
                                over = False
                                blocks = []
                                over = False
                                score = 0
                                prevScore = 0
                                speed = -5
                                time = 500
                                pygame.time.set_timer(halfSec, time)
                                scored_blocks = []
                                blob.reset()


    
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
                time -= int(time*0.2)
                pygame.time.set_timer(halfSec, time)
                speed -= 2
                prevScore = score

            # determine closest block to blob
            if len(blocks) >= 1:
                closest = blocks[0]
                for index, block in enumerate(blocks):
                    if index != 0:
                        CDelta = closest.getPos()[0] - blob.getPos()[0]
                        BDelta = block.getPos()[0] - blob.getPos()[0]
                        if CDelta < 0:
                            CDelta = -CDelta
                        if BDelta < 0:
                            BDelta = -BDelta
                        if BDelta < CDelta:
                            closest = block
                # check for collision with closest block
                if blob.check_collision(closest.getPos(), closest.getSize()) == -1:
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
            blob.checkGround()
            #if blob.onGround:
            #    jumpCount = 0

            # remove off screen blocks
            for index, block in enumerate(blocks):
                if block.getPos()[0] <= -block.getSize():
                    del blocks[index]

            # moving blocks
            for block in blocks:
                block.move(speed)
    
        # --- Screen-clearing code
        for x in bg:
            screen.blit(bg_img, (x,0))
    
        # --- Drawing code
        blob.draw(screen)

        if debug:
            # Select the font to use, size, bold, italics
            font = pygame.font.SysFont('Calibri', size[1]//15, True, False)
            # text, anti-aliased, color
            text = font.render(blob.state,True,BLACK)
            screen.blit(text, [blob.pos[0], blob.pos[1]-blob.blobSize/5])

        for block in blocks:
            block.draw(screen)

        if len(blocks) >= 1 and debug:
            # Select the font to use, size, bold, italics
            font = pygame.font.SysFont('Calibri', size[1]//20, True, False)
            # text, anti-aliased, color
            text = font.render(f"Closest",True,BLACK)
            screen.blit(text, [closest.pos[0], closest.pos[1]-closest.getSize()/5])

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
        text = font.render(f"SPEED: {((-speed)-5)//2*10}",True,BLACK)
        screen.blit(text, [size[0]/15, size[1]/15*2])

        # --- blocks amount when debug enabled
        # Select the font to use, size, bold, italics
        font = pygame.font.SysFont('Calibri', size[1]//15, True, False)
        # text, anti-aliased, color
        text = font.render(f"total blocks: {len(blocks)}",True,BLACK)
        if debug:
            screen.blit(text, [size[0]/15, size[1]/15*3])

        # --- blocks speed when super debug enabled
        # text, anti-aliased, color
        text = font.render(f"block speed: {speed}",True,BLACK)
        if superDebug:
            screen.blit(text, [size[0]/15, size[1]/15*4])

        # --- blob speed when super debug enabled
        # text, anti-aliased, color
        text = font.render(f"blob speed: {int(blob.velocity)}",True,BLACK)
        if superDebug:
            screen.blit(text, [size[0]/15, size[1]/15*5])
    
        # --- Update the screen
        pygame.display.flip()
    
        # --- Limit to 60 frames per second
        clock.tick(60)
    
    # Close the window and quit.
    pygame.quit()