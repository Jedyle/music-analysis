from time import time
from constants import *
from sound import *
from button_set import *
from visumono import *
import pygame as pg

class Track:

    def __init__(self, window, pos, path, channel_id):
        """
        pos: top left corner of the first track bar
        size: (width, height) of a track bar
        """
        self.__name = self.path_to_name(path)
        self.__sound = Sound(path, channel_id)
        self.__button_set = ButtonSet(window, pos)
        self.__sound_path = path
        self.__visumono = None
        self.__visu_mode = VISU_NONE
        self.__timer_ref = 0
        self.__timer = 0

    def path_to_name(self, path):
        """
        return the reduced track name, i.e without full path and extension (.wav)
        if name has no 
        """
        start = path.rfind("/") + 1
        end = path.rfind(".")
        return path[start:end]

    def get_sound_path(self):
        return self.__sound_path

    def get_visumono(self):
        if self.__visumono == None:
            self.__visumono = VisuMono(self.__sound_path)
        return self.__visumono

    def get_sound_timer(self):
        """
        return time in seconds
        """
        if self.get_paused() or self.get_stopped():
            #return last synchronization
            return self.__timer        
        if self.__timer_ref == 0:
            #if sound has not been launched
            return 0
        #refresh timer if sound is playing
        return self.__timer + time() - self.__timer_ref

    ############## draw functions #####################

    def set_visumono(self, mode):
        if mode != VISU_NONE and self.__visumono == None:
            #if visu is not visible, set it to visible
           self.__visumono = VisuMono(self.__sound_path)
        #switch visu mode
        if self.__visu_mode == mode:
            #if the mode is already active, turn it off
            self.__visu_mode = VISU_NONE
        else:
            #else turn it on
            self.__visu_mode = mode


    def draw_track(self, window, pos):
        self.__draw_visumono(window, (pos[0]+TRACK_WIDTH, pos[1]))
        window.draw_rectangle(pos, TRACK_SIZE)
        img_path = IMG_PATH + "volume.png"
        length = min(TRACK_WIDTH * 15 / 100, TRACK_HEIGHT * 9 / 10)#square image
        img_size = (length, length)
        pos_x = pos[0] + (TRACK_WIDTH * 17.5 / 100) - (length / 2)
        pos_y = pos[1] + (TRACK_HEIGHT / 2) - (length / 2)
        vol_img = pg.transform.scale(pg.image.load(img_path).convert(), img_size)
        vol_img.set_colorkey(GREEN)
        window.blit_surface(vol_img, (pos_x, pos_y))
        pos = (pos[0] + TRACK_WIDTH * 35 / 100, pos[1])
        window.blit_text(self.__name, pos)
        buttons = self.__button_set.get_buttons()
        for b in buttons:
            window.draw_button(b)

    def __draw_visumono(self, window, pos):
        if self.__visu_mode == VISU_NONE:
            return
        elif self.__visu_mode == VISU_RTHM:
            surf_list = self.__visumono.get_rect_rhythm()
        elif self.__visu_mode == VISU_MELO:
            surf_list = self.__visumono.get_rect_melody()
        if not self.__visumono == None:
        #if visu must be shown
            s_time = self.get_sound_timer() 
            dx = floor(TRACK_PIXPERSEC * s_time)
            for s in surf_list:
                shifted_pos = pos[0] - dx + s[1]
                if shifted_pos > - PIECE_WIDTH and shifted_pos < SCREEN_WIDTH:
                #only display the piece if it can be seen on the screen
                    window.blit_surface(s[0], (shifted_pos, pos[1]))   
            x = SCREEN_WIDTH - TRACK_WIDTH + LINE_SHIFT
            start_pos = (x / 2, pos[1] - LINE_OVERTRACK)
            end_pos = (x / 2, pos[1] + TRACK_HEIGHT + LINE_OVERTRACK)
            window.draw_line(start_pos, end_pos, WHITE)


    ############## buttons #################
    def get_button_set(self):
        return self.__button_set.get_buttons()

    def set_buttons_pos(self, window, pos):
        self.__button_set.set_buttons_pos(window, pos)

    ############# managing sound #####################
    def set_id(self, channel_id):
        self.__sound.set_id(channel_id)

    def get_paused(self):
        return self.__sound.get_paused()

    def get_stopped(self):
        return self.__sound.get_stopped()

    def pause(self):
        self.__sound.pause()
        if self.__sound.get_paused():
           self.__timer += time() - self.__timer_ref

    def unpause(self):
        self.__sound.unpause()
        if not self.__sound.get_paused():
            self.__timer_ref = time()

    def stop(self):
        self.__sound.stop()
        if self.__sound.get_stopped():
            self.__timer = 0
            self.__timer_ref = 0

    def play(self):
        if not self.__sound.get_played():
            self.__timer_ref = time()
        self.__sound.play()

    def change_volume(self, change):
        self.__sound.change_volume(change)
         
    def mute_track(self):
        mute_button = self.__button_set.get_buttons()[1]
        if not self.__sound.is_muted():
            self.__sound.mute() 
            mute_button.set_button_font_color(MUTE_ON_COLOR)
        else:
            self.__sound.unmute()
            mute_button.set_button_font_color(MUTE_OFF_COLOR)
