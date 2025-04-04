import pygame

import random
import math

import ExtraMath
import OrderedSprites

class Log(pygame.sprite.Sprite):
    def __init__(self, gs, x, y):
        self.gs = gs
        self.x = x
        self.y = y

        self.size = 100

        self.rotationType = random.choice([0, 0, 1])
        if self.rotationType == 0:
            self.speed = random.uniform(0.07, 0.14)
            self.dir = random.choice([1, -1])
            self.rotationSpeed = self.speed * self.dir
        
        if self.rotationType == 1:
            self.amplitude = random.uniform(0.03, 0.06)
            self.frequency = random.uniform(0.0001, 0.0004)
            self.rotationSpeed = math.sin(pygame.time.get_ticks() * self.frequency) * self.amplitude

        self.angle = 0

        self.dead = False

        #load images
        super().__init__()

        topImageNames = ["BrightLogTop.png", "MediumLogTop.png", "DarkLogTop.png"]
        bottomImageNames = ["BrightLogBottom.png", "MediumLogBottom.png", "DarkLogBottom.png"]
        randomLogTypeIndex = random.randint(0, len(topImageNames) - 1)

        self.logTop = OrderedSprites.orderedSpirte(self, self.gs, topImageNames[randomLogTypeIndex], 0, 0, self.size*2, self.size*2, 4)
        self.logBottom = OrderedSprites.orderedSpirte(self, self.gs, bottomImageNames[randomLogTypeIndex], 15, 0, self.size*2, self.size*2, 2)
        self.logTopOutline = OrderedSprites.orderedSpirte(self, self.gs, "LogOutlineBlack.png", 0, 0, self.size*2 + 5, self.size*2 + 5, 1)
        self.logBottomOutline = OrderedSprites.orderedSpirte(self, self.gs, "LogOutlineBlack.png", 15, 0, self.size*2 + 5, self.size*2 + 5, 1)
        self.logShadow = OrderedSprites.orderedSpirte(self, self.gs, "LogShadow.png", 35, 0, self.size*2, self.size*2, 0)

    def updateRotation(self, dTs):
        if self.rotationType == 0:
            self.angle += self.rotationSpeed * dTs
        if self.rotationType == 1:
            self.rotationSpeed = math.sin(pygame.time.get_ticks() * self.frequency) * self.amplitude * dTs
            self.angle += self.rotationSpeed * dTs

    def updateSprites(self):
        self.logTop.update()
        self.logBottom.update()
        self.logTopOutline.update()
        self.logBottomOutline.update()
        self.logShadow.update()

class Knife(pygame.sprite.Sprite):
    def __init__(self, gs, x, y):
        self.gs = gs
        self.gs.knives.append(self)

        self.randomDir = random.choice([-1, 1])

        self.x = x - 150 * self.randomDir
        self.y = y
        self.targetX = x
        
        self.vel = (0.9 * self.randomDir, 0)

        #bool to only throw knife once
        self.hasThrown = False

        #vars for after collision, vectolog for position relative to log
        self.hasHit = False
        self.vecToLog = None

        self.dead = False

        #load images
        super().__init__()
        self.angle = 0

        self.knifeSprite = OrderedSprites.orderedSpirte(self, self.gs, "Knife.png", 0, 0, 20, 20 * 3.387, 3)
        self.outlineSprite = OrderedSprites.orderedSpirte(self, self.gs, "KnifeOutlineBlack.png", 0, 0, 24, 24 * 2.887, 1)
        self.shadowSprite = OrderedSprites.orderedSpirte(self, self.gs, "KnifeShadow.png", 35, 0, 20, 20 * 3.387, 0)

    def updateSprites(self):
        self.knifeSprite.update()
        self.outlineSprite.update()
        self.shadowSprite.update()

        #set alpha when not yet positioned
        if self.hasThrown == False:
            alpha = 255 - 255 * (abs((self.x - self.targetX) / 150))
            self.knifeSprite.image.set_alpha(alpha)
            self.outlineSprite.image.set_alpha(alpha)
            self.shadowSprite.image.set_alpha(alpha)
        else:
            self.knifeSprite.image.set_alpha(255)
            self.outlineSprite.image.set_alpha(255)
            self.shadowSprite.image.set_alpha(255)

    def move(self, dTs):
        diff = abs(self.x - self.targetX)
        if diff < 10 and self.hasThrown == False:
            self.x = self.targetX
            self.vel = (0, 0)

        if self.hasHit == False:
            self.x = self.x + self.vel[0] * dTs
            self.y = self.y + self.vel[1] * dTs
        else:
            #rotate by constant log rotaiton
            self.angle += self.gs.log.rotationSpeed * dTs
            self.vecToLog = ExtraMath.rotateVector(self.vecToLog, self.gs.log.rotationSpeed * dTs)

            self.x = self.gs.log.x - self.vecToLog[0]
            self.y = self.gs.log.y - self.vecToLog[1]

    def throw(self, force):
        if self.hasThrown == False:
            self.x = self.targetX
            self.vel = (force[0], force[1])
            self.hasThrown = True

    def collide(self):
        #collide with log
        if self.hasHit == False:
            #get vector to log
            vecToLog = (self.gs.log.x - self.x, self.gs.log.y - self.y)
            distToLog = math.sqrt(vecToLog[0] * vecToLog[0] + vecToLog[1] * vecToLog[1])

            if distToLog < self.gs.log.size + 10:
                self.hasHit = True
                self.gs.soundMngr.playFromSounds(self.gs.soundMngr.knifeHitSfx)
                self.vel = (0, 0)
                self.vecToLog = vecToLog

            #collide with other knives
            for knife in self.gs.knives:
                if knife != self and knife.hasHit == True:
                    vecToKnife = (knife.x - self.x, knife.y - self.y)
                    distToKnife = math.sqrt(vecToKnife[0] * vecToKnife[0] + vecToKnife[1] * vecToKnife[1])
                    if distToKnife < 10:
                        self.dead = True
                        OrderedSprites.spawnParticles(self.gs, self.x, self.y, self.knifeSprite.image)
                        self.gs.soundMngr.playFromSounds(self.gs.soundMngr.knifeBreakSfx)

class Apple(pygame.sprite.Sprite):
    def __init__(self, gs):
        self.gs = gs
        self.gs.apples.append(self)

        #get initial position relative to log
        self.angle = random.randint(0, 360)
        self.vecToLog = ExtraMath.angleToVector(self.angle) * (gs.log.size + 15)
        self.angle -= 90

        self.x = gs.log.x - self.vecToLog[0]
        self.y = gs.log.y - self.vecToLog[1]

        self.dead = False

        #load images
        super().__init__()

        tops = ["Apple.png", "Orange.png", "Banana.png"]
        outlines = ["AppleOutlineBlack.png", "OrangeOutlineBlack.png", "BananaOutlineBlack.png"]
        shadows = ["AppleShadow.png", "OrangeShadow.png", "BananaShadow.png"]
        randomFruitTypeIndex = random.randint(0, len(tops) - 1)

        self.topImage = OrderedSprites.orderedSpirte(self, self.gs, tops[randomFruitTypeIndex], 0, 0, 35, 35, 6)
        self.outline = OrderedSprites.orderedSpirte(self, self.gs, outlines[randomFruitTypeIndex], 0, 0, 40, 40, 5)
        self.shadow = OrderedSprites.orderedSpirte(self, self.gs, shadows[randomFruitTypeIndex], 35, 0, 35, 35, 0)

    def updateSprites(self):
        self.topImage.update()
        self.outline.update()
        self.shadow.update()

    def move(self, dTs):
        #rotate by constant log rotaiton
        self.angle += self.gs.log.rotationSpeed * dTs
        self.vecToLog = ExtraMath.rotateVector(self.vecToLog, self.gs.log.rotationSpeed * dTs)
        self.x = self.gs.log.x - self.vecToLog[0]
        self.y = self.gs.log.y - self.vecToLog[1]

    def collide(self):
        #collide with knives
        for knife in self.gs.knives:
            vecToKnife = (knife.x - self.x, knife.y - self.y)
            distToKnife = math.sqrt(vecToKnife[0] * vecToKnife[0] + vecToKnife[1] * vecToKnife[1])
            if distToKnife < 25:
                self.dead = True
                OrderedSprites.spawnParticles(self.gs, self.x, self.y, self.topImage.image)
                self.gs.soundMngr.playFromSounds(self.gs.soundMngr.fruitSliceSfx)
                self.gs.score += 1
