from math import *
from constants import *
import librosa as lb

def frame_to_pixels(frame, hop_length, sr):
    return int(ceil((frame*(hop_length*1.0)/sr)*TRACK_PIXPERSEC))

def time_to_frame(time):
    return lb.core.time_to_frames(times = [time], sr = SAMPLE_RATE, hop_length = HOP_LENGTH)[0]

def seconds_to_pixels(time):
    return int(ceil(time*TRACK_PIXPERSEC))

def frame_to_time(frame, hop_length,sr):
    return frame*(hop_length*1.0)/sr

def search(elt, tab, offset):
    """
    Search the closest element to elt in tab
    Parameters :
        elt : element to search
        tab : array for the research
        offset : starting index to search from (the searching in done from tab[offset] to tab[len(tab)-1]
    Returns :
        i = index of the closest elt
        shift = shift (in frames) between elt and tab[i], <0 if elt is in advance, >0 else
    """
    i = offset
    n = len(tab)
    while ((i<n) and (elt > tab[i])):
        i = i + 1
    if (i>=n):
        return (n, elt - tab[n-1])
    elif (i == offset):
        return (offset, elt - tab[offset])
    else :
        interval = (tab[i] - tab[i-1])
        if ((tab[i]-elt) > (interval/2)):
            return (i-1, elt-tab[i-1])
        return (i, elt-tab[i])

def get_wav_duration(path):
    file = open(path, "r")
    content = file.read()
    wave = content[8]+content[9]+content[10]+content[11]
    i = 36
    data = content[i]+content[i+1]+content[i+2]+content[i+3]
    while(data!= "data"):
         i = i+1
         data = content[i]+content[i+1]+content[i+2]+content[i+3]
    subchunk = (ord(content[i+4])+ord(content[i+5])*256+ord(content[i+6])*256*256+ord(content[i+7])*256*256*256)
    channels = ord(content[22])+ord(content[23])*256
    file.close()
    return (subchunk/channels)
