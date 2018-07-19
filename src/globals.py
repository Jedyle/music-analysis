import pygame as pg

MAX_TRACK = 6
pg.mixer.pre_init(44100, -16, MAX_TRACK, 2048) #pre-initialize pygame mixer to avoid delay
pg.init() #initializing pygame

############ channel_id ##############
CHANNEL_ID = 0

############ screen size ##############
SCREEN_WIDTH = pg.display.Info().current_w
SCREEN_HEIGHT = pg.display.Info().current_h

############ font constants #############
pg.font.init()
PYGBUTTON_FONT = pg.font.Font('freesansbold.ttf', 14)
TRACK_FONT = pg.font.SysFont("monospace", 20)
