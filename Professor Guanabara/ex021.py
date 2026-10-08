#Faça um programa em python que abra e reproduza o áudio de um arquivo MP3.

import os
import pygame
pygame.init()
#caminho relativo ao proprio arquivo: o mp3 esta na mesma pasta e assim roda de qualquer lugar
pygame.mixer.music.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ex021.mp3'))
pygame.mixer.music.play()
pygame.event.wait()
