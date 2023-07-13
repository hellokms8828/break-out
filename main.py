import sys
import math
import random
import pygame
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, Rect, KEYUP
import time
 
class Block:
    def __init__(self, color, rect, speed=0):
        self.color = color
        self.rect = rect
        self.speed = speed
        self.direction = random.randint(-45, 45) + 270
 
    def move(self):
        self.rect.centerx += math.cos(math.radians(self.direction))\
             * self.speed
        self.rect.centery -= math.sin(math.radians(self.direction))\
             * self.speed
 
    def draw(self):
        if self.speed == 0:
            pygame.draw.rect(SURFACE, self.color, self.rect)
        else:
            pygame.draw.ellipse(SURFACE, self.color, self.rect)
 
# Fever Time event
def feverTime():
    global BALLS
    
    # Extend paddle
    PADDLE.rect = Rect(PADDLE.rect.centerx , 700, 150, 20)
    
    # Add two more balls
    for i in range(2):
        BALLS.append(Block((200, 242, 0), Rect(300, 400, 20, 20), 10))
 
    # Set ball speed to 15
    for BALL in BALLS:
        BALL.speed = 15

# Apply ball acceleration. Prevent falling below a certain speed
def ball_acceleration():
    global BALLS, PADDLE
    for BALL in BALLS:
        BALL.speed += 0.1 * (PADDLE.rect.centerx - BALL.rect.centerx)
        if BALL.speed <= 5:
            BALL.speed = 5
 
# When bouncing
def tick():
    global BALLS, BLOCKS, score, isFeverTime, startTime, endTime
 
    # Key input handling
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                if(PADDLE.rect.centerx <= 0):
                    continue
                PADDLE.rect.centerx -= 6
            elif event.key == K_RIGHT:
                if(PADDLE.rect.centerx >= 600):
                    continue
                PADDLE.rect.centerx += 6

        
    for BALL in BALLS:
        if BALL.rect.centery < 1000:
            BALL.move()
 
        # Collision with a block
        prevlen = len(BLOCKS)
        BLOCKS = [x for x in BLOCKS
                if not x.rect.colliderect(BALL.rect)]
        if len(BLOCKS) != prevlen:
            BALL.direction *= -1
            score += 100 # Increase score by 100
 
        # If the score is 1000 and not in Fever Time, enter Fever Time
        if score == 1000 and isFeverTime == False:
            isFeverTime = True
            feverTime()
        # Start counting 10 seconds, and turn off Fever Time after 10 seconds
        elif isFeverTime == True:    
            if startTime == 0.0:
                startTime = time.time()
            elif startTime != 0.0:
                endTime = time.time()
                if endTime - startTime >= 7: # 10 seconds
                    isFeverTime = False
 
        # Collision with the paddle
        if PADDLE.rect.colliderect(BALL.rect):
            BALL.direction = 90 + (PADDLE.rect.centerx - BALL.rect.centerx) \
                / PADDLE.rect.width * 80
            ball_acceleration()
 
        # Collision with the wall
        if BALL.rect.centerx < 0 or BALL.rect.centerx > 600:
            BALL.direction = 180 - BALL.direction
        if BALL.rect.centery < 0:
            BALL.direction = -BALL.direction
            BALL.speed = 15
 
pygame.init()
pygame.key.set_repeat(5, 5)
SURFACE = pygame.display.set_mode((600, 800))
FPSCLOCK = pygame.time.Clock()
BLOCKS = []
PADDLE = Block((242, 242, 0), Rect(300, 700, 100, 20))
BALLS = [Block((242, 242, 0), Rect(300, 400, 20, 20), 10)]
 
isNeedToRestart = False
isFeverTime = False
score = 0
startTime = 0.0
endTime = 0.0
 
# Initialization
def init():
    global SURFACE, FPSCLOCK, BLOCKS, PADDLE, BALLS, isNeedToRestart, isFeverTime, score, startTime, endTime
 
    pygame.init()
    pygame.key.set_repeat(5, 5)
    SURFACE = pygame.display.set_mode((600, 800))
    FPSCLOCK = pygame.time.Clock()
    BLOCKS = []
    PADDLE = Block((242, 242, 0), Rect(300, 700, 100, 20))
    BALLS = [Block((242, 242, 0), Rect(300, 400, 20, 20), 10)]
    isNeedToRestart = False
    isFeverTime = False
    score = 0
    startTime = 0.0
    endTime = 0.0
 
def main():
    global isNeedToRestart, score, isFeverTime, startTime, endTime
 
    myfont = pygame.font.SysFont(None, 80)
    smallfont = pygame.font.SysFont(None, 36)
    scorefont = pygame.font.SysFont(None, 25)
    cleared_message = myfont.render("Cleared!", True, (255, 255, 0))
    game_over_message = myfont.render("Game Over!", True, (255, 255, 0))
    replay_message = smallfont.render("replay (press r)", True, (255, 0, 0))
    fps = 30
    colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0),
              (0, 255, 0), (255, 0, 255), (0, 0, 255)]
 
    # Add blocks
    for ypos, color in enumerate(colors, start=0):
        for xpos in range(0, 5):
            BLOCKS.append(Block(color, Rect(xpos * 100 + 60, ypos * 50 + 40, 80, 30)))
 
    while True:
        tick()
 
        # Draw ball
        SURFACE.fill((0, 0, 0))
        for BALL in BALLS:
            BALL.draw()
        PADDLE.draw()
 
        # Draw blocks
        for block in BLOCKS:
            block.draw()        
 
        # When all blocks are removed, the game is cleared
        if len(BLOCKS) == 0:
            SURFACE.blit(cleared_message, (200, 400))
        
        # Remove balls below the paddle
        for BALL in BALLS:
            if BALL.rect.centery > 800 and len(BLOCKS) > 0:
                BALLS.remove(BALL)
 
        # After Fever Time ends
        if isFeverTime == False and startTime != 0.0 and endTime != 0.0:
            # Remove all balls except one
            for BALL in BALLS:
                if(len(BALLS) == 1):
                    break
                else:
                    BALLS.remove(BALL)
            startTime = 0.0
            endTime = 0.0
            # Restore speed to 10
            PADDLE.rect = Rect(PADDLE.rect.centerx, 700, 100, 20)
            for BALL in BALLS:
                BALL.speed = 10
 
        # When there are no balls left (game over)
        if len(BALLS) == 0:
            SURFACE.blit(game_over_message, (150, 400))
            SURFACE.blit(replay_message, (230, 460))
            isNeedToRestart = True

        # Scoreboard
        score_message = scorefont.render("score : " + str(score), True, (255, 255, 255))
        SURFACE.blit(score_message, (10, 10))
 
        pygame.display.update()
        FPSCLOCK.tick(fps)
 
        # Press R to restart
        while isNeedToRestart:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == pygame.K_r:
                    isNeedToRestart = False
                    break
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    break
 
            if isNeedToRestart == False:
                init()
                main()
                break

if __name__ == '__main__':
    main()
