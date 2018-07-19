from globals import *
import pygame as pg

############ name constants #############
WINDOW_TITLE = "ETE - EarToEye" 

############ path constants #############
IMG_PATH = "img/"
SOUND_PATH = "track/"

############ display constants ##############
NB_COLORS        = 40
MATRIX_FPS       = 1
CORREL_INTERVAL  = 1
CORREL_THRESHOLD = 0.01

############ size constants #############
BUTTON_SIZE     = (SCREEN_WIDTH / 10, SCREEN_HEIGHT * 4 / 100)
TRACK_INDENT    = SCREEN_WIDTH * 3 / 100
TRACK_WIDTH     = SCREEN_WIDTH * 3 / 10
TRACK_HEIGHT    = 2 * (SCREEN_HEIGHT / 24)
TRACK_SIZE      = (TRACK_WIDTH, TRACK_HEIGHT)
LINE_SHIFT      = (SCREEN_WIDTH - TRACK_WIDTH) / 10
LINE_OVERTRACK  = TRACK_HEIGHT / 10
LINE_OFFSET     = SCREEN_WIDTH / 60
TRACK_PIXPERSEC = SCREEN_WIDTH / 30
PIECE_WIDTH     = SCREEN_WIDTH / 2
# MATRIX_POS      = (TRACK_INDENT + TRACK_WIDTH, TRACK_INDENT)
# MATRIX_SIZE     = min(SCREEN_WIDTH - MATRIX_POS[0],  SCREEN_HEIGHT - MATRIX_POS[1] - TRACK_INDENT)
SHADE_HEIGHT    = TRACK_INDENT / 2
MATRIX_OFFSET = min(SCREEN_WIDTH, SCREEN_HEIGHT)/10
MATRIX_SIZE     = min(SCREEN_WIDTH - TRACK_WIDTH - SHADE_HEIGHT * 2,  SCREEN_HEIGHT - TRACK_INDENT - SHADE_HEIGHT * 2)-MATRIX_OFFSET
#MATRIX_SIZE     = min(SCREEN_WIDTH - TRACK_WIDTH - SHADE_HEIGHT * 2,  (SCREEN_HEIGHT- SHADE_HEIGHT-MATRIX_OFFSET)*NB_COLORS/(NB_COLORS + 2))
MATRIX_POS      = (SCREEN_WIDTH - MATRIX_SIZE, TRACK_INDENT + 2 * SHADE_HEIGHT)
#MATRIX_POS      = (SCREEN_WIDTH - MATRIX_SIZE, SCREEN_HEIGHT - MATRIX_S-MATRIX_OFFSET)

############ limits and enumerations ###########
PLAYER_STOPPED  = 0
PLAYER_PAUSED   = 1
PLAYER_PLAYED   = 2
VISU_NONE       = 0 #no visualisation 
VISU_RTHM       = 1 #rythmic visualisation
VISU_MELO       = 2 #melodic visualisation
VISU_MULT       = 3 #multi-track global rythm visualisation

########### color constants ############
BLACK          = (  0,   0,   0)
WHITE          = (255, 255, 255)
DARKGRAY       = ( 64,  64,  64)
GRAY           = (128, 128, 128)
LIGHTGRAY      = (212, 208, 200)
RED            = (255,   0,   0)
GREEN          = (  0, 255,   0)
MUTE_ON_COLOR  = RED
MUTE_OFF_COLOR = BLACK

########### computing constants #########
SAMPLE_RATE = 44100
HOP_LENGTH = 1024


