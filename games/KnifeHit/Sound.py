#   Main background music track "BackgrounTrack1.mp3" made by Nabeel (Discord: zeuz.0) for the GMTK24 "Built to scale" game jam

import pygame

import random

class SoundManager():
    def __init__(self, musicVolume, soundVolume):
        self.musicVolume = musicVolume
        self.soundVolume = soundVolume

        pygame.mixer.init()

        pygame.mixer.music.load('./Sounds/backgroundTrack1.mp3')
        pygame.mixer.music.set_volume(self.musicVolume)
        pygame.mixer.music.play(-1)

        self.knifeThrow1_sfx = pygame.mixer.Sound('./Sounds/throw1.mp3')
        self.knifeThrow2_sfx = pygame.mixer.Sound('./Sounds/throw2.mp3')
        self.knifeThrowSfx = [self.knifeThrow1_sfx, self.knifeThrow2_sfx]

        self.knifeHit1_sfx = pygame.mixer.Sound('./Sounds/hit1.mp3')
        self.knifeHit2_sfx = pygame.mixer.Sound('./Sounds/hit2.mp3')
        self.knifeHit3_sfx = pygame.mixer.Sound('./Sounds/hit3.mp3')
        self.knifeHit4_sfx = pygame.mixer.Sound('./Sounds/hit4.mp3')
        self.knifeHitSfx = [self.knifeHit1_sfx, self.knifeHit2_sfx, self.knifeHit3_sfx, self.knifeHit4_sfx]

        self.knifeBreak1_sfx = pygame.mixer.Sound('./Sounds/break1.mp3')
        self.knifeBreakSfx = [self.knifeBreak1_sfx]

        self.fruitSlice1_sfx = pygame.mixer.Sound('./Sounds/slice1.mp3')
        self.fruitSlice2_sfx = pygame.mixer.Sound('./Sounds/slice2.mp3')
        self.fruitSlice3_sfx = pygame.mixer.Sound('./Sounds/slice3.mp3')
        self.fruitSliceSfx = [self.fruitSlice1_sfx, self.fruitSlice2_sfx, self.fruitSlice3_sfx]

        self.lose_sfx = pygame.mixer.Sound('./Sounds/lose1.mp3')
        self.loseSfx = [self.lose_sfx]

    def playFromSounds(self, sounds):
        sound = sounds[random.randint(0, len(sounds) - 1)]
        sound.set_volume(self.soundVolume)
        sound.play()