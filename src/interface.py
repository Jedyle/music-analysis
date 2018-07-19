from Tkinter import Tk
from tkFileDialog import askopenfilename
import tkMessageBox as mbox
from pygame.locals import * #constants
from window import *
from visumulti import *
from track import *
from time import *
from random import *

class Interface(Window):

    ################### initialisation ########################
    def __init__(self):
        Window.__init__(self)
        self.__track_list = []
        self.__channel_id = 0
        self.__visumulti = None
        self.__visumulti_built = False
        self.__visumulti_mode = VISU_NONE
        self.__loop = True

    ################### file selection ########################
    def choose_file(self):
        """
        Entries: None
        Result: full path name of a chosen file
        Treatment: open a GUI interface to choose a file
        """
        Tk().withdraw() #raw interface
        return askopenfilename()

    def __check_extension(self, path):
        """
        return True only if path match with a .wav file
        """
        extension = path[1+path.rfind(".")::]
        if path != "" and extension == "wav":#if a .wav file has been chosen
            return True
        else:
            if extension != "wav":
                message = "the file must have .wav format"
                mbox.showerror("Error", message)
                
        return False

    def __check_bitsPerSample(self, path):
        wavfile = open(path, "r")
        content = wavfile.read()
        bitspersample = ord(content[34]) + 256*ord(content[35])
        wavfile.close()
        if (bitspersample != 16) :
            message = "file must be 16-bit"
            mbox.showerror("Error", message)
            return False
        return True

    def __check_length(self, path):
        if (len(self.__track_list) != 0):
            if (get_wav_duration(self.__track_list[0].get_sound_path()) != get_wav_duration(path) ):
                message = "imported files must have EXACTLY the same length"
                mbox.showerror("Error", message)
                return False
        return True

    ################### track management #########################
    def add_track(self, path = None):
        """
        if path is not given, a file browser will open and ask for a file
        """
        if path == None:
            path = self.choose_file()
        if not self.__check_extension(path):
            #if name is not a .wav file, quit add_track function
            return
        if not self.__check_bitsPerSample(path):
            return
        if not self.__check_length(path):
            return
        nb_tracks = len(self.__track_list)
        if nb_tracks >= MAX_TRACK:
            message = "maximum number of tracks already reached: " + str(MAX_TRACK)
            mbox.showerror("Error", message)
            return 
        pos = self.__get_pos(nb_tracks)
        self.__track_list.append(Track(self, pos, path, self.__channel_id))
        self.__channel_id += 1
        self.__visumulti_built = False
        self.__visumulti_mode = VISU_NONE


    def delete_track(self, index):
        self.__track_list[index].stop()        
        for t in self.__track_list:
            t.pause()
        track_number = len(self.__track_list)
        for i in range(index, track_number - 1):
            self.__track_list[i] = self.__track_list[i + 1]
            self.__track_list[i].set_id(i)
            self.__track_list[i].set_buttons_pos(self, self.__get_pos(i))
        self.__track_list.pop()
        self.__channel_id -= 1
        if track_number <= 1: 
            #if there are no tracks left, reinit tracks
            self.__track_list = []
        self.__visumulti_built = False
        self.__visumulti_mode = VISU_NONE

    def mute_track(self, index):
        self.__track_list[index].mute_track()

    #################### screen update #########################
    def __get_pos(self, i):
        """
        compute the top left corner coordinates (x, y) of the track bar
        with index 'i'
        """
        x = 0
        y = TRACK_INDENT + (i + 1) * TRACK_HEIGHT * 1.5
        return (x, y)
        
    def update_screen(self):
        self._draw_window(self.get_player_state())
        i = 0
        for t in self.__track_list:
            t.draw_track(self, self.__get_pos(i))
            if self.__visumulti_mode == VISU_MULT:
                self.draw_visumulti()
            i += 1
        pg.display.flip()

    def draw_visumulti(self):
        """
        display a correlation matrix of the loaded tracks
        if tracks are ended, displays a black square
        """        
        shade_list = self.__visumulti.get_shade_list()
        for surf, pos in shade_list:
            self.blit_surface(surf, pos)
        x, y = (0,0)
        tab = self.__visumulti.get_rect_rhythm()
        t = int(floor(self.__track_list[0].get_sound_timer()) * MATRIX_FPS)
        if self.__visumulti.is_visu_ended(t):
            surf = pg.Surface((MATRIX_SIZE, MATRIX_SIZE))
            surf.fill(BLACK)
            self.blit_surface(surf, MATRIX_POS)
        else: 
            for x in range(len(self.__track_list)):
                for y in range(len(self.__track_list)):
                    surf, pos = tab[t][x][y]
                    pos = (pos[0] + MATRIX_POS[0], pos[1] + MATRIX_POS[1])
                    if surf != 0:
                        self.blit_surface(surf, pos)
                    else:
                        print("error: tab[t][x][y] = 0 with (t,x,y) = ", (t, x, y))

    def set_visumono(self, mode):
        for t in self.__track_list:
            t.set_visumono(mode)

    def set_visumulti(self, mode):
        if mode == VISU_MULT:
            if not self.__visumulti_built:
                monoTab = []
                for t in self.__track_list:
                    monoTab.append(t.get_visumono().get_monorhythm())
                self.__visumulti = VisuMulti(monoTab)
                self.__visumulti_built = True
            self.set_visumono(VISU_NONE)
            self.__visumulti_mode = VISU_MULT
        else:
            self.__visumulti_mode = VISU_NONE
        
    
    #################### media player ########################
    def play(self):
        for t in self.__track_list:
            t.play()

    def pause(self):
        for t in self.__track_list:
            if t.get_paused():
                t.unpause()
            else:
                t.pause()

    def stop(self):
        for t in self.__track_list:
            t.stop()
                        
    def get_player_state(self):
        if not self.__track_list or self.__track_list[0].get_stopped():
            #if there is no track, say they are stopped
            return PLAYER_STOPPED
        elif self.__track_list[0].get_paused():
            return PLAYER_PAUSED
        else:
            return PLAYER_PLAYED

    #################### event handling ########################
    def button_handler(self, event):
        #handling window buttons (add file, rhythm picture, ...)
        self.__on_click_action(event, self._buttons[0], self.add_track)
        self.__on_click_action(event, self._buttons[1], self.set_visumono, VISU_RTHM)
        self.__on_click_action(event, self._buttons[2], self.set_visumono, VISU_MELO)
        if self.__visumulti_mode == VISU_NONE and len(self.__track_list) > 0:
            self.__on_click_action(event, self._buttons[3], self.set_visumulti, VISU_MULT)
        else:
            self.__on_click_action(event, self._buttons[3], self.set_visumulti, VISU_NONE)

        #handling track buttons (delete track, change volume, ...)
        i = 0
        while i < len(self.__track_list):
            buttons = self.__track_list[i].get_button_set()
            #mute or unmute   
            self.__on_click_action(event, buttons[1], self.mute_track, i) 
            #increase volume
            self.__on_click_action(event, buttons[2], self.__track_list[i].change_volume, i, 1)            
            #decrease volume
            self.__on_click_action(event, buttons[3], self.__track_list[i].change_volume, i, -1)            
            #delete (must be done at the end, to avoid being out of track_list range)
            self.__on_click_action(event, buttons[0], self.delete_track, i) 
            i += 1


    def __on_click_action(self, event, button, action, index=-1, vol_change=0):
        """
        button: button of which we check the click
        action: function to call (add, delete, ...)
        index: index of the track to modify 
        vol_change: in case action wants to change the volume of a track, 
                    indicates the change to make
        """
        retVal = button.handleEvent(event) 
        if retVal: #if not empty 
            self.draw_button(button)
            for r in retVal:
                if r == 'click':
                    if index != -1:
                        if vol_change != 0:
                            action(vol_change)
                        else:
                            action(index)
                    else:
                        action()

 
    def event_handler(self):
        """
        Entries: None
        Result: False if main loop must end, else True
        Treatment: handle main loop events
        """
        for event in pg.event.get() : 
            #list all received events
            if event.type in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN):
                self.button_handler(event)
            if event.type == MOUSEBUTTONDOWN:
                self._get_player_action(pg.mouse.get_pos(), self.play, self.pause, self.stop, self.get_player_state())
            if event.type == QUIT :
                return False
            if event.type == KEYDOWN :
                if event.key == K_SPACE :
                    self.pause()
                if event.key == K_ESCAPE :
                    self.stop()
                #if event.key == K_RETURN:
                    #self.play()
                if event.key == K_UP :
                    for t in self.__track_list:
                        t.change_volume(1)
                if event.key == K_DOWN :
                    for t in self.__track_list:
                        t.change_volume(-1)
                
        return True

        
