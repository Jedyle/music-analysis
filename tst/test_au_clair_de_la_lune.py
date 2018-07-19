import sys
sys.path.append("../src")
from monomelody import *
from monorhythm import *
from tools import *

signal,sr = lb.core.load("../tracks/long_lune.wav", duration = 26.0)
mono = MonoMelody(file = "../tracks/long_lune.wav", signal = signal, duration = 26.0)


#mono.show_components()
mono.filter_chroma()
mono.show_chroma()

"""mono.filter_chroma()
m = mono.tab_notes()
#print m
#print len(m)
M = mono.tab_time(mono.tab_notes())
print M

#print mono.belongs(M, ['C', 'D'])
#mono.show_chroma()

mono2 =MonoRhythm(file = "./tracks/long_lune.wav", duration = 26.0)
mono2.load_onsets()

onset_frames = mono2.get_onset_frames()
sr = mono2.get_sample_rate()
hl = mono2.get_hop_length()

print frame_to_time(onset_frames, hl, sr)

#print onset_frames



for i in range (0, len(onset_frames)):
    print m[onset_frames[i]+2]
"""
