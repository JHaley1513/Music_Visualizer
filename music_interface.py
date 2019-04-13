# J. Haley and A. Liu, 12 Dec 2018
import pygame, sys
from pygame.locals import *
import music_utils as utils

exit = False
song_name = input("Please enter a song name\n> ") #must be an audio file in the same directory as this module.
while not utils.name_valid(song_name):
    if song_name == 'exit':
        exit = True
        break
    else:
        print("Invalid name. It should be case-sensitive with no file extension")
        song_name = input("Please enter a song name\n> ")
if not exit:
    print("\nAlright.")



    DEFAULT_COLOR = (255, 255, 255)
    WINDOWH = WINDOWW = 1000
    pygame.init()
    mainClock = pygame.time.Clock()
    pygame.display.set_caption("Music Visualizer")
    windowSurface = pygame.display.set_mode((WINDOWW, WINDOWH))
    music_extension = 'ogg'
    image_extension = 'bmp'
    snippet_num = 1
    highpass = False

    started = False


    while True:
        if not started:
            song_path = utils.find_path(song_name)
            total_snippets = len(utils.generate_song_and_image_snippets(filename=song_path, extension=music_extension))
            pygame.mixer.music.load(song_name + ' music ' + str(snippet_num) + '.' + music_extension)
            pygame.mixer.music.play()
            started = True

        for event in pygame.event.get():
            if event.type == QUIT:
                utils.remove_files(song_name, music_extension, image_extension)
                pygame.quit()
                sys.exit()

        if started and not pygame.mixer.music.get_busy(): #this means the snippet has finished - go to the next one (if applicable)
            #pygame.mixer.music.stop()
            snippet_num += 1
            if snippet_num > total_snippets:
                utils.remove_files(song_name, music_extension, image_extension)
                pygame.quit()
                sys.exit()
            pygame.mixer.music.load(song_name + ' music ' + str(snippet_num) + '.' + music_extension)
            pygame.mixer.music.play()

        windowSurface.fill(DEFAULT_COLOR)
        background=pygame.image.load(song_name + ' image ' + str(snippet_num) + '.' + image_extension)
        background=pygame.transform.scale(background, (WINDOWW,WINDOWH))
        windowSurface.blit(background,(0,0))

        pygame.display.update()
        mainClock.tick(10)
