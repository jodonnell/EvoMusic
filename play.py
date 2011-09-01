import pygame
pygame.mixer.init()
music = pygame.mixer.Sound('annie.wav')
samples = pygame.sndarray.samples(music)
from random import randint
for yow in range(300000):
    samples[yow][0] += randint(0, 15000)
    samples[yow][1] -= randint(0, 15000)

music.play()

import time
time.sleep(10)
