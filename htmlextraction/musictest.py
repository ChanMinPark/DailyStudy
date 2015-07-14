import pygame

pygame.mixer.init()
song = pygame.mixer.music.load("samsung_song.mp3")
#clock = pygame.time.Clock()
song.play()
while pygame.mixer.music.get_busy() == True:  #True:
    continue    #clock.tick(60)
pygame.mixer.quit()
