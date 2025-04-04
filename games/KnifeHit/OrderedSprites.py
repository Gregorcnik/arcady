import pygame

import random

class orderedSpirte:
    def __init__(self, parent, gs, fileName, yOffset, xOffset, width, height, zLayer):
        self.gs = gs
        self.gs.orderedSprites.append(self)
        self.parent = parent

        self.fullPath = './Sprites/' + fileName
        self.yOffset = yOffset
        self.xOffset = xOffset
        self.width = width
        self.height = height
        self.zLayer = zLayer

        self.doBlit = True

        self.originalImage = pygame.image.load(self.fullPath).convert_alpha()
        self.originalImage = pygame.transform.scale(self.originalImage, (self.width, self.height))
        self.image = self.originalImage
        self.rect = self.image.get_rect(center=(self.parent.x + self.xOffset, self.parent.y + self.yOffset))

    def update(self):
        self.image = pygame.transform.rotate(self.originalImage, -self.parent.angle)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.parent.x + self.xOffset
        self.rect.centery = self.parent.y + self.yOffset

def blitOrderedSprites(screen, gs):
    gs.orderedSprites.sort(key=lambda x: x.zLayer)

    #blit ordered list of sprites
    for sprite in gs.orderedSprites:
        if sprite.doBlit == True:
            screen.blit(sprite.image, sprite.rect)

class Particle(pygame.sprite.Sprite):
    def __init__(self, gs, x, y, parentImage):
        self.gs = gs
        self.gs.particles.append(self)
        
        self.x = x
        self.y = y
        
        self.vel = (random.uniform(-0.4, 0.4), random.uniform(-0.4, 0.4))
        self.angluralVel = random.uniform(-1, 1)
        self.gravity = 0.015 + random.uniform(-0.005, 0.005)
        self.lifeTime = 120 + random.randint(-60, 60)
        self.startLifeTime = self.lifeTime

        self.parentImage = parentImage

        #get random subsurface from parent image
        self.image = self.parentImage
        self.rect = self.image.get_rect()

    def update(self, screen):
        #update lifetime
        self.lifeTime -= 1
        
        #update velocity and position
        self.vel = (self.vel[0], self.vel[1] + self.gravity)
        self.x += self.vel[0]
        self.y += self.vel[1]

        #update rect
        self.image = pygame.transform.rotate(self.image, self.angluralVel)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y

        #blit image
        self.image.set_alpha(255 * (self.lifeTime / self.startLifeTime))
        screen.blit(self.image, self.rect)

def spawnParticles(gs, x, y, image):
    particle = Particle(gs, x, y, image)