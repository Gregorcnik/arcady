#by default not on gimvic computers
import pygame
import numpy as np

#extra lib
import math
import random
import time

#project scripts
#import ExtraMath
import OrderedSprites
import GameObjects
import Sound

#------------------------------------------------------------------------------------------------------

#todo - in game settings for volume
musicVolume = 0.6
soundVolume = 0.4

#------------------------------------------------------------------------------------------------------

#window initialization
screenWidth = 400
screenHeight = 800

pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))

#remove window icon and set caption
pygame.display.set_caption('Knife Hit')

transparent_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
transparent_surface = pygame.image.load('./Sprites/Apple.png').convert_alpha()
pygame.display.set_icon(transparent_surface)

#------------------------------------------------------------------------------------------------------

#game management classes and functions and some UI that doesnt realy fit anywhere else
class GameState():
    def __init__(self):
        #initialize everything for all scenes
        self.soundMngr = Sound.SoundManager(musicVolume, soundVolume)

        self.highScore = 0
        self.score = 0

        self.font = pygame.font.Font('./Sprites/SuperMario256.ttf', 40)

        #initialize all objects for one scene

        #initialize transition
        self.transition = gameSceneTransition(self)

        self.orderedSprites = []
        self.knives = []
        self.apples = []

        self.particles = []

        #initialize objects
        self.log = GameObjects.Log(self, 200, 200)

        #spawn apples, get number of available knives
        self.numOfApples = random.randint(2, 5)
        for i in range(self.numOfApples):
            newApple = GameObjects.Apple(self)

        #initialize knife bar
        self.knifeBar = KnifeBar(self, 200, 700, int(self.numOfApples * 1.5))

        #spawn initial knife 
        self.knifeThrowForce = (0, -0.7)
        newKnife = GameObjects.Knife(self, 200, 600)

    def restartScene(self):
        #re initialize all objects for new scene

        #initialize transition
        self.transition = gameSceneTransition(self)

        self.orderedSprites = []
        self.knives = []
        self.apples = []

        self.particles = []

        #initialize objects
        self.log = GameObjects.Log(self, 200, 200)

        #spawn apples, get number of available knives
        self.numOfApples = random.randint(2, 5)
        for i in range(self.numOfApples):
            newApple = GameObjects.Apple(self)

        #initialize knife bar
        self.knifeBar = KnifeBar(self, 200, 700, int(self.numOfApples * 1.5))

        #spawn initial knife 
        self.knifeThrowForce = (0, -0.7)
        newKnife = GameObjects.Knife(self, 200, 600)

    def updateScore(self):
        if self.score > self.highScore:
            self.highScore = self.score

        #blit score text
        highScoreText_top = self.font.render(str(self.highScore), True, (255, 255, 0))
        highScoreText_bottom = self.font.render(str(self.highScore), True, (155, 100, 0))
        highScoreText_shadow = self.font.render(str(self.highScore), True, (0, 0, 0))

        scoreText_top = self.font.render(str(self.score), True, (255, 255, 255))
        scoreText_bottom = self.font.render(str(self.score), True, (155, 155, 155))
        scoreText_shadow = self.font.render(str(self.score), True, (0, 0, 0))

        screen.blit(highScoreText_shadow, (screenWidth - 15 - highScoreText_shadow.get_width(), 30 + screenHeight/2 - highScoreText_shadow.get_width()/2))
        screen.blit(scoreText_shadow, (screenWidth - 15 - scoreText_shadow.get_width(), 30 + screenHeight/2 - scoreText_shadow.get_width()/2 + 45))

        screen.blit(highScoreText_bottom, (screenWidth - 15 - highScoreText_bottom.get_width(), 18 + screenHeight/2 - highScoreText_bottom.get_width()/2))
        screen.blit(scoreText_bottom, (screenWidth - 15 - scoreText_bottom.get_width(), 18 + screenHeight/2 - scoreText_bottom.get_width()/2  + 45))

        screen.blit(highScoreText_top, (screenWidth - 15 - highScoreText_top.get_width(), 15 + screenHeight/2 - highScoreText_top.get_width()/2))
        screen.blit(scoreText_top, (screenWidth - 15 - scoreText_top.get_width(), 15 + screenHeight/2 - scoreText_top.get_width()/2 + 45))

class gameSceneTransition():
    def __init__(self, gs):
        self.gs = gs
        
        self.a = 255
        self.ta = 0

        self.overlaySurface = pygame.Surface((screenWidth, screenHeight), pygame.SRCALPHA)
        self.overlaySurface.fill((0, 0, 0, self.a))  # RGBA: black with 50% opacity

    def updateOverlay(self):
        #interpolate towards target a
        self.a = self.a + 0.01*(self.ta - self.a) + 0.1

        if self.a > 255:
            self.a = 255
        if self.a < 0:
            self.a = 0

        self.overlaySurface.fill((0, 0, 0, int(self.a)))  # RGBA: black with 50% opacity
        screen.blit(self.overlaySurface, (0, 0))

    def outTransition(self):
        #set target a to black
        self.ta = 255

        #restart scene
        if self.a == self.ta:
            self.gs.restartScene()

class KnifeBar(pygame.sprite.Sprite):
    def __init__(self, gs, x, y, numOfKnives):
        self.gs = gs
        self.x = x
        self.y = y

        self.maxKnives = numOfKnives
        self.knivesLeft = numOfKnives

        self.angle = 160
        self.dead = False

        #create knife slot images
        self.spacing = 20
        self.emptySlotSprites = []
        self.fullSlotSprites = []
        for i in range(self.maxKnives):
            emptySlot = OrderedSprites.orderedSpirte(self, self.gs, "KnifeShadow.png", 15, self.spacing*i - (self.maxKnives * self.spacing) / 2 + self.spacing / 2, 15, 15  * 3.387, 100)
            self.emptySlotSprites.append(emptySlot)

            fullSlot = OrderedSprites.orderedSpirte(self, self.gs, "Knife.png", 0, self.spacing*i - (self.maxKnives * self.spacing) / 2 + self.spacing / 2, 15, 15  * 3.387, 101)
            self.fullSlotSprites.append(fullSlot)

    def updateSprites(self):
        for sprite in self.emptySlotSprites:
            sprite.update()

        for i in range(self.maxKnives):
            self.fullSlotSprites[i].update()
            
            if i >= self.knivesLeft:
                self.fullSlotSprites[i].doBlit = False

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def checkForWin():
    #check if any apples left
    if len(gs.apples) == 0:
        #Win
        gs.transition.outTransition()

    #check if no more knives and all knives have hit the log
    else:
        if gs.knifeBar.knivesLeft <= 0:

            hitKnives = 0
            for knife in gs.knives:
                if knife.hasHit == True:
                    hitKnives += 1

            if hitKnives == len(gs.knives):
                #Lose
                gs.score = 0
                gs.transition.outTransition()

#------------------------------------------------------------------------------------------------------

#initialize vars as game state
gs = GameState()

#get delta time initial ticks
prevT = pygame.time.get_ticks()

running = True
while running:

    #update delta time
    currT = pygame.time.get_ticks()
    dTms = currT - prevT
    dTs = dTms

    # Fill screen
    screen.fill((30, 30, 30))

    # Handle inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

                #throw all not yet thrown knives
                for knife in gs.knives:
                    knife.throw(gs.knifeThrowForce)
                    gs.soundMngr.playFromSounds(gs.soundMngr.knifeThrowSfx)

                #spawn new knife 
                gs.knifeBar.knivesLeft -= 1
                if gs.knifeBar.knivesLeft > 0:
                    newKnife = GameObjects.Knife(gs, 200, 600)

    #update log
    gs.log.updateRotation(dTs)
    gs.log.updateSprites()

    #update knives
    for knife in gs.knives:
        knife.move(dTs)
        knife.collide()
        knife.updateSprites()

    #update apples
    for apple in gs.apples:
        apple.move(dTs)
        apple.collide()
        apple.updateSprites()

    #update knife bar UI
    gs.knifeBar.updateSprites()

    #remove dead objects
    gs.apples = [apple for apple in gs.apples if apple.dead == False]
    gs.knives = [knife for knife in gs.knives if knife.dead == False]
    gs.orderedSprites = [ordrdSprt for ordrdSprt in gs.orderedSprites if ordrdSprt.parent.dead == False]

    #update score
    gs.updateScore()

    #check for win/lose condition, (if statement to allow for close button quiting)
    checkForWin()

    #draw ordered sprites (blit everything other than particles)
    OrderedSprites.blitOrderedSprites(screen, gs)

    #blit particles
    for particle in gs.particles:
        particle.update(screen)
    gs.particles = [particle for particle in gs.particles if particle.lifeTime > 0]

    #update transition animation
    gs.transition.updateOverlay()

    # Update the display
    pygame.display.flip()

    #update delta time
    prevT = currT

# Quit Pygame
pygame.quit()
