import pygame as pg
from monorhythm import *
from constants import *
from tools import *
from monomelody import *

from time import time

class VisuMono :
    
    def __init__(self, file, offset = 0 , duration = None , hop_length=HOP_LENGTH, sr=SAMPLE_RATE):
        (self.__signal, self.__sr) = lb.core.load(file, offset = offset, duration = duration, sr=sr)
        self.__file = file
        self.__offset = offset
        self.__duration = duration
        self.__hl = hop_length
        self.__monorhythm = None
        self.__mono_rthm_built = False
        self.__mono_melo_built = False
        self.__rthm_surf_list = []
        self.__melo_surf_list = []
        self.__monomelody = None

    def __load_monomelody(self):
        self.__monomelody = MonoMelody(self.__file, signal = self.__signal, duration = self.__duration, sr = self.__sr)

    def __load_monorhythm(self):
        self.__monorhythm = MonoRhythm(file = self.__file, signal = self.__signal, offset = self.__offset, duration = self.__duration, hop_length = self.__hl, sr = self.__sr) # autres arg si besoin

    def get_monorhythm(self):
        if self.__monorhythm == None:
            self.__load_monorhythm()
        return self.__monorhythm

    def get_rect_rhythm(self):
        #if the rectangle surface containing the visualisation has already 
        #been computed, return it directly
        if not self.__mono_rthm_built:
            if self.__monorhythm == None:
                #verify that monorhythm has been loaded
                self.__load_monorhythm()
            self.__build_rect_rhythm()
            self.__mono_rthm_built = True
        return self.__rthm_surf_list

    def get_rect_melody(self):
        #idem for melody
        if not self.__mono_melo_built:
            if self.__monomelody == None:
                self.__load_monomelody()
                if self.__monorhythm == None:
                    self.__load_monorhythm()
            self.__build_rect_melody()
            self.__mono_melo_built = True
        return self.__melo_surf_list
        
    def __build_rect_rhythm(self):
        """
        Creates a surface list representing the mono track onsets.
        elements of the list are (surf, start_pos) with:
        surf: surface containing a visualisation fragment
        start_pos: position of the fragment start
        """
        width = TRACK_PIXPERSEC * (int(self.__monorhythm.get_duration()) + 1) + LINE_SHIFT + LINE_OFFSET
        nb_pieces = int(floor(width / PIECE_WIDTH))
        sr = self.__monorhythm.get_sample_rate()
        hl = self.__monorhythm.get_hop_length()
        onset_frames = self.__monorhythm.get_onset_frames()

        for i in range (0, nb_pieces):
            self.__rthm_surf_list.append((pg.Surface((PIECE_WIDTH, TRACK_HEIGHT)), PIECE_WIDTH * i))
        if nb_pieces * PIECE_WIDTH != width:
            self.__rthm_surf_list.append((pg.Surface((width - nb_pieces * PIECE_WIDTH, TRACK_HEIGHT)), PIECE_WIDTH * nb_pieces))
            nb_pieces += 1

        #draw the whole surface
        for i in range (0, len(onset_frames)):
            ftp = frame_to_pixels(onset_frames[i], hl, sr) + LINE_SHIFT + LINE_OFFSET
            index = ftp / PIECE_WIDTH
            x = ftp - index * PIECE_WIDTH
            pg.draw.line(self.__rthm_surf_list[index][0], RED, (x, 0), (x, TRACK_HEIGHT))


    def __build_rect_melody(self):
        """
        Creates a surface list representing the mono track notes.
        elements of the list are (surf, start_pos) with:
        surf: surface containing a visualisation fragment
        start_pos: position of the fragment start
        """
        M = self.__monomelody.tab_notes()            
        width = TRACK_PIXPERSEC * (int(self.__monorhythm.get_duration()) + 1) + LINE_SHIFT + LINE_OFFSET
        nb_pieces = int(floor(width / PIECE_WIDTH))
        sr = self.__monorhythm.get_sample_rate()
        hl = self.__monorhythm.get_hop_length()
        onset_frames = self.__monorhythm.get_onset_frames()

        for i in range (0, nb_pieces):
            self.__melo_surf_list.append((pg.Surface((PIECE_WIDTH, TRACK_HEIGHT)), PIECE_WIDTH * i))
        if nb_pieces * PIECE_WIDTH != width:
            self.__melo_surf_list.append((pg.Surface((width - nb_pieces * PIECE_WIDTH, TRACK_HEIGHT)), PIECE_WIDTH * nb_pieces))
            nb_pieces += 1

        #draw the partition lines
        for p in range (0, nb_pieces):
            for i in range (0, 4):
                pg.draw.line(self.__melo_surf_list[p][0], WHITE, (0, TRACK_HEIGHT*1.0*i/4), (PIECE_WIDTH, TRACK_HEIGHT*1.0*i/4))

            pg.draw.line(self.__melo_surf_list[p][0], WHITE, (0, TRACK_HEIGHT-1), (PIECE_WIDTH, TRACK_HEIGHT-1))
            
        #draw the whole surface
        for i in range (0, len(onset_frames)):
            ftp = frame_to_pixels(onset_frames[i], hl, sr) + LINE_SHIFT + LINE_OFFSET
            index = ftp / PIECE_WIDTH
            x = ftp - index * PIECE_WIDTH
    

            pos = onset_frames[i] + 2

            if( M[pos] == 'E'):
                center = 1.0/8
            elif( M[pos] == 'D' or M[pos] == 'D#' ):
                center = 2.0/8
            elif( M[pos] == 'C' or M[pos] == 'C#' ):
                center = 3.0/8
            elif( M[pos] == 'B' ):
                center = 4.0/8
            elif( M[pos] == 'A' or M[pos] == 'A#' ):
                center = 5.0/8
            elif( M[pos] == 'G' or M[pos] == 'G#' ):
                center = 6.0/8
            elif( M[pos] == 'F' or M[pos] == 'F#' ):
                center = 7.0/8
            else:
                center = -1
            
            pg.draw.circle(self.__melo_surf_list[index][0], RED, ( x, int(TRACK_HEIGHT*center)), TRACK_HEIGHT/8 )

            pg.draw.circle(self.__melo_surf_list[index][0], WHITE, ( x, int(TRACK_HEIGHT*center)), TRACK_HEIGHT/8, 1 )
