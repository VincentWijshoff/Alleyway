import pygame as pg
import random as rndm
import time


def drawWalls(screen):
    global wallSize, screen_width, screen_height
    pg.draw.rect(screen, pg.Color("grey"), pg.Rect((0, 0), (wallSize, screen_height)))
    pg.draw.rect(screen, pg.Color("grey"), pg.Rect((0, 0), (screen_width, wallSize)))
    pg.draw.rect(screen, pg.Color("grey"), pg.Rect((screen_width-wallSize, 0), (wallSize, screen_height)))


def drawBack(screen):
    global screen_height, screen_width
    pg.draw.rect(screen, pg.Color("black"), pg.Rect((0, 0), (screen_width, screen_height)))


class Block:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self, screen):
        pg.draw.rect(screen, pg.Color("blue"), pg.Rect((self.x, self.y), (self.w, self.h)))

class Bal:
    def __init__(self):
        global screen_height, playerY, wallSize, screen_width, player_height, speed
        self.size = player_height
        self.x = int(rndm.uniform(wallSize, screen_width - wallSize - self.size))
        self.y = int(playerY - 10*player_height)
        self.prevx = self.x
        self.prevy = self.y
        self.xvel = speed
        self.yvel = speed

    def touch(self, x, y, w, h):
        if self.x < x + w and self.x + self.size > x and self.y < y + h and self.y + self.size > y:
            if self.y + self.size <= y + 2 or self.y >= y + h - 2:
                self.yvel *= -1
                return True
            if self.x + self.size <= x + 2 or self.x >= x + w - 2:
                self.xvel *= -1
                return True
        return False

    def move(self, screen):
        global screen_width, screen_height, wallSize, player_height, player_width, playerY, playerX, blocks
        self.prevx = self.x
        self.prevy = self.y
        self.x = self.x + self.xvel
        self.y = self.y + self.yvel
        if self.x <= wallSize:
            self.xvel *= -1
        if self.y <= wallSize:
            self.yvel *= -1
        if self.x + self.size >= screen_width - wallSize:
            self.xvel *= -1
        if self.y + self.size >= screen_height:
            self.yvel *= -1
        self.touch(playerX, playerY, player_width, player_height)
        for blok in blocks:
            if self.touch(blok.x, blok.y, blok.w, blok.h):
                blocks.remove(blok)
                break
        for blok in blocks:
            blok.draw(screen)
        self.draw(screen)

    def draw(self, screen):
        pg.draw.rect(screen, pg.Color("black"), pg.Rect((int(self.prevx), int(self.prevy)), (self.size, self.size)))
        pg.draw.rect(screen, pg.Color("white"), pg.Rect((int(self.x), int(self.y)), (self.size, self.size)))


def drawPlayer(x, screen):
    global playerY, player_width, player_height, prev_playerX, screen_width, wallSize, playerX
    pg.draw.rect(screen, pg.Color("black"), pg.Rect((prev_playerX, playerY), (player_width, player_height)))
    if x - wallSize <= 0:
        x = wallSize
    if x + player_width + wallSize >= screen_width:
        x = screen_width - player_width - wallSize
    playerX = x
    pg.draw.rect(screen, pg.Color("white"), pg.Rect((x, playerY), (player_width, player_height)))
    prev_playerX = x


def drawScore(screen):
    global screen_width, screen_height, wallSize, font, blocks
    img = font.render(str(len(blocks)), True, pg.Color("white"))
    screen.blit(img, (20, 20))


def setup():
    global screen_width, screen_height, bal, blocks, player_width, player_height, font
    canv = pg.init()
    screen = pg.display.set_mode([screen_width, screen_height])
    drawBack(screen)
    font = pg.font.SysFont(None, 24)
    pg.display.flip()
    drawPlayer(screen_width // 2, screen)
    drawWalls(screen)
    bal.draw(screen)
    for i in range(20):
        for j in range(6):
            blocks.append(Block(j*player_width + 150, i*player_height + 100, player_width, player_height))
    return screen


def checkWin(screen):
    global blocks, screen_height, screen_width
    if len(blocks) != 0:
        return False
    drawBack(screen)
    f = pg.font.SysFont(None, 70)
    img = f.render('YOU WIN', True, pg.Color("white"))
    screen.blit(img, (screen_width//2 - 100,screen_height//2 - 50))
    pg.display.flip()
    return True


def loop(screen):
    global player_width, bal
    drawBack(screen)
    drawScore(screen)
    drawPlayer(int(bal.x - player_width//2), screen)
    #drawPlayer(pg.mouse.get_pos()[0] - player_width//2, screen)
    bal.move(screen)
    drawWalls(screen)
    if checkWin(screen):
        return True


def main():
    screen = setup()
    while True:
        e = pg.event.poll()
        if e.type == pg.QUIT:
            break
        if loop(screen):
            time.sleep(3)
            break
        pg.display.flip()
    pg.quit()


screen_width = 900
screen_height = 700
player_width = 100
player_height = 10
playerY = screen_height - player_height*5
playerX = 0
prev_playerX = 0
wallSize = 20
blocks = []
speed = 3
bal = Bal()
font = 0
main()