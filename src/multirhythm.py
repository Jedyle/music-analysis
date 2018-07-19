from monorhythm import * # suppr ?
from tools import *

class MultiRhythm :
    
    def __init__(self, monoRtab):
        self.__mono_list = monoRtab
        self.__nb_tracks = len(monoRtab)
        if self.check_tracks() == True :
            self.global_onset_envelope()
            self.__estimate_beat_track()
            self.sr = self.__mono_list[0].get_sample_rate()
            self.hop_length = self.__mono_list[0].get_hop_length()
            self.duration = self.__mono_list[0].get_duration()
            #self.estimate_shift(self.__beat)
        else : #tracks not ok
            print "Error : monotracks must have same lengths, sample rates and hop lengths"

    def check_tracks(self):
        duration = self.__mono_list[0].get_duration()
        sr = self.__mono_list[0].get_sample_rate()
        hl = self.__mono_list[0].get_hop_length()
        for mono in self.__mono_list :
            if ((mono.get_duration() != duration) or (mono.get_hop_length() != hl) or (mono.get_sample_rate() != sr)):
                return False
        return True
        
    def global_onset_envelope(self):
        framelen = len(self.__mono_list[0].get_onset_envelope())
        self.__global_oenv = np.zeros(framelen)
        for i in range(framelen):
            summ = 0
            for j in range(self.__nb_tracks):
                summ += self.__mono_list[j].get_onset_envelope()[i]
            self.__global_oenv[i] = summ
                
    def get_global_onset_envelope(self):
        return self.__global_oenv

    def get_mono_list(self):
        return self.__mono_list
        
    def __estimate_beat_track(self):
        """
        Estimate a beat tab representing the tempo of the song. One can imagine several methods to find the rhythm, this one is the easiest, given by librosa
        """
        (self.__tempo,self.__beat) = lb.beat.beat_track(onset_envelope = self.__global_oenv, sr= SAMPLE_RATE, hop_length = HOP_LENGTH)
        
    def get_tempo(self):
        return self.__tempo
            
    def get_beat(self):
        return self.__beat

    def __estimate_shift(self, ref_beat, lim = 8):
        """
        Estimates shift between the __beat tab and the onsets of the mono tracks.
        Fills a shift array which size if nb_track, where for each track i, __shift[i] is an array comparing the onset frames of i and the frames of beat track.
        Example :
            __shift[i][j] = (beat_index, shift, boolean)
            beat_index is the index of the __beat array so that __beat[beat_index] is the closest number of monoi.__onset_frames[j].  shift is the frame shift between __beat[beat_index] and monoi.__onset_frames[j], < 0 if onset_frame[i] is in advance, >0 else. 
        """
        self.__shift = []
        for mono in self.__mono_list :
            onset_frames = mono.get_onset_frames()
            length = len(onset_frames)
            tab = [(0,0,True) for j in range(length)]
            (beat_index, shift) = search(onset_frames[0], ref_beat, 0)
            frame_interval = lb.core.time_to_frames([60.0/self.__tempo])[0] / lim
            tab[0] = (beat_index,shift, (abs(shift) <= frame_interval))
            for i in range (1,length):
                (beat_index, shift) = search(onset_frames[i], ref_beat, beat_index)
                tab[i] = (beat_index,shift, (abs(shift) <= frame_interval))
            self.__shift.append(tab)

    def display_multi(self):
        n = self.__nb_tracks
        pt.figure(1)
        fs = self.__mono_list[0].get_frame_scale()
        for i in range(0,n):
            pt.subplot(n+1, 1, i+1)
            oenv = self.__mono_list[i].get_onset_envelope()
            pt.plot(fs,oenv)
        pt.subplot(n+1,1,n+1)
        pt.plot(fs,self.__global_oenv)
        pt.show()

