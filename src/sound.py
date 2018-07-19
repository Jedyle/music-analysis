from constants import *
import pygame as pg

class Sound:

    def __init__(self, path, channel_id):
        self.__id = channel_id
        self.__sound = pg.mixer.Sound(path)
        self.__volume = 1
        self.__sound.set_volume(self.__volume)
        self.__channel = pg.mixer.Channel(self.__id)
        self.__is_muted = False
        self.__played = False
        self.__paused = False
        self.__stopped = True

    def get_stopped(self):
        return self.__stopped

    def get_played(self):
        return self.__played

    def get_paused(self):
        return self.__paused

    def get_id(self):
        return self.__id
    
    def set_id(self, new_id):
        self.stop()
        self.__id = new_id
        self.__channel = pg.mixer.Channel(new_id)

    def mute(self):
        self.__volume = self.__sound.get_volume()
        self.__sound.set_volume(0)
        self.__is_muted = True

    def unmute(self):
        self.__sound.set_volume(self.__volume)
        self.__is_muted = False

    def is_muted(self):
        return self.__is_muted
    
    def change_volume(self, change, step = 0.1):
        """
        Entries: int change with values +1 (increase volume)
                                     or -1 (decrease volume)
                 int step indicating how much the volume is wanted to be changed
        Results: None
        Treatment: set volume to volume + change * step
        """
        if change != 1 and change != -1 :
            print "change expected to be either 1 or -1 (given " + str(change) + ")"
        else :
            self.__volume = self.__sound.get_volume() + change * step
            if self.__volume < 0 :
                self.__volume = 0
            elif self.__volume > 1 :
                self.__volume = 1
            self.__sound.set_volume(self.__volume)
            
    def play(self):
        if not self.__played:
            self.__stopped = False
            self.__channel.play(self.__sound)
            self.__played = True

    def pause(self):
        if self.__played :
            self.__channel.pause()
            self.__paused = True
            self.__played = False

    def unpause(self):
        if self.__paused :
            self.__channel.unpause()
            self.__paused = False
            self.__played = True

    def stop(self):
        if not self.__stopped : 
            self.__channel.stop()
            self.__stopped = True
            self.__paused = False
            self.__played = False
