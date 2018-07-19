import librosa as lb
import numpy as np
import matplotlib.pyplot as pt
#import pygame as pg
from math import *
from constants import *
from pygame.locals import * #constants
from time import time


class MonoRhythm :
    
    def __init__(self, file, signal, offset = 0.0 , duration = None , hop_length=HOP_LENGTH, sr=SAMPLE_RATE):
        ##constructor
        self.load_file(file=file, signal = signal, offset = offset, duration = duration, hop_length = hop_length, sr = sr)

    def load_file(self, file, signal, offset, duration, hop_length, sr) :
        """ loads the main datas of the track : file name, duration, offset, hop_length, the audio time series and a time scale corresponding to the audio time series"""
        self.__file = file #file name
        self.__offset = offset
        self.__hop_length = hop_length
        (self.__signal, self.__sr) = (signal, sr)
        if (duration == None):
            print self.__signal
            self.__duration = lb.get_duration(y = self.__signal, sr = self.__sr, hop_length = self.__hop_length)
        else :
            self.__duration = duration
        self.load_onsets()

    def show_track(self):
        time_scale = [i*1.0/(self.__sr) for i in range(len(self.__signal))] #temporal scale corresonding to the stream of the track
        pt.plot(time_scale, self.__signal)
        pt.show()

    def load_onsets(self):
        """ loads onsets data :
        -  __onset_envelope is an onset envelope computed by librosa
        -  __frame_scale is an array where __frame_scale[i] is the time corresponding to the scale number i (useful to plot the onset envelope)
        -  __onset_frame contains the frame number corresponding to the onset detection (computed by librosa)  """
        self.__onset_envelope = lb.onset.onset_strength(y= self.__signal, sr=self.__sr, hop_length = self.__hop_length)
        self.__frame_scale = [i*1.0*(self.__hop_length)/(self.__sr) for i in range(len(self.__onset_envelope))] #temporal scale corresponding to __onset_envelope
        self.__onset_frames = lb.onset.onset_detect(y= self.__signal, onset_envelope = self.__onset_envelope, sr= self.__sr, hop_length = self.__hop_length)
    
    def get_track(self):
        return (self.__signal, self.__sr)

    def get_onset_envelope(self):
        return self.__onset_envelope

    def get_frame_scale(self):
        return self.__frame_scale

    def get_time_scale(self):           
        return self.__time_scale

    def get_onset_frames(self): 
        return self.__onset_frames

    def get_sample_rate(self):
        return self.__sr

    def get_hop_length(self):
        return self.__hop_length

    def get_frame_interval(self):
        return (self.__hop_length)*1.0/(self.__sr)

    def get_duration(self):
        return self.__duration
