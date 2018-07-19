import librosa as lb
from numpy import *
import matplotlib.pyplot as plt
from constants import *

from time import time

class MonoMelody :

    def __init__(self, file, signal, duration, sr = SAMPLE_RATE, hop_length = HOP_LENGTH):
        
        """constructor : 
        - feature.chroma_stft is a function of librosa library which compute a chromagram using the song spectrogram
        """
         
        self.__file = file
        self.__y, self.__sr = (signal, sr)
        if (duration == None):
            self.__duration = lb.get_duration(y = self.__y, sr = sr, hop_length = hop_length)
        else :
            self.__duration = duration
        self.__hop_length = hop_length
        S = abs(lb.stft(self.__y, hop_length = self.__hop_length))
        self.__C = lb.feature.chroma_stft(S=S, sr=self.__sr)
        self.filter_chroma()

    def show_chroma(self):
                        
        """print the chromagram of the track:
        - display.specshow is a function of librosa library which useg with 'time' argument for x_axis and 'chroma' argument for y_axis allows to plot the chromagram
        """
        
        lb.display.specshow(self.__C, x_axis='time', y_axis='chroma', hop_length = self.__hop_length)
        plt.title('Chromagram')
        plt.show()

    def filter_chroma(self):
                        
        """for each column, keep the note with the highest coefficient
        Note : this filter is efficient only when a single note is played at the same time.
        """
        
        l, c = shape( self.__C)

        for i in range(0, c):
            max = self.__C[0][i]
            
            for j in range(0, l):
                if( self.__C[j][i] > max ):
                    max = self.__C[j][i]

            for j in range(0, l):
                if( self.__C[j][i] < max ):
                    self.__C[j][i] = 0


    def filter_components(self, min):
                        
        #for each column, keep the frequencies with a coefficient superior to min
        
        l, c = shape( self.__comps )

        for i in range(0, c):
            for j in range(0, l):
                if( self.__comps[j][i] < min ):
                    self.__comps[j][i] = 0

        
    def tab_notes(self):

        """returns the list of the note played. 
        The time between to notes is related to the sample rate
        If no note is played the character is empty
        """


        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        l, c = shape( self.__C )

        tab = ['']*c
        
        for i in range( 0, c):
            for j in range( 0, l):
                if( self.__C[j][i] > 0 ):
                    tab[i] = notes[j]

        char = tab[0]
        if (char != tab[2]):
            char = tab[2]
            tab[0] = tab[2]
        for i in range(0,c-2):
            if (char != tab[i]):
                if(char != tab[i+2]):
                    tab[i] = tab[i+2]
                    char = tab[i+2]
                else:
                    char = tab[i]
          
        return tab


    def tab_time(self,tab):

        """Takes in parameter the list of notes returned by the function tab_notes
        Returns a list of pairs, containing the note and the time when the note begins
        """
                        
        l, c = shape(self.__C)
        #print c
        pas = int(self.__duration) * 1.0 / c
        
        tabTime = []
        
        char = tab[0]
        tabTime.append([char,0.0])

        for i in range(0,len(tab)):
            if (tab[i] != char):
                char = tab[i]
                tabTime.append([char,i*pas])
                
        return tabTime


    def belongs(self, tab_time, notes):
        nb_notes = len(notes)
        l = len(tab_time)

        result = [False]*l
        
        for i in range(0, l):
            for j in range(0, nb_notes):
                if (tab_time[i][0] == notes[j]):
                    result[i] = True

        return result

        
        

        
