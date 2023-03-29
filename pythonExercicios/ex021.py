"""Faça um programa em Python que abra e reproduza o áudio de um arquivo MP3."""
import pygame
pygame.init()
pygame.mixer.music.load('ex021.mp3')
pygame.mixer.music.play()
pygame.event.wait()
print('\033[1;41mNÃO CONSEGUI FAZER ESSE PROGRAMA FUNCIONAR\033[m')
