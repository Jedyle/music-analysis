import sys
sys.path.append("../src")
from monomelody import *

track = "../tracks/solo1.wav"
mono = MonoMelody(file = track, signal = lb.core.load(track, sr = 44100)[0], duration = 60.0)

#mono.select_note(freq_min = 250, freq_max = 400)

#mono.filter_components(min=4)
#mono.show_components()

#mono.show_activations()

#mono.filter_chroma(min=0.8)
#mono.show_chroma()

mono.filter_chroma()
M = mono.tab_time(mono.tab_notes())
#print M

#print mono.belongs(M, ['C', 'D'])
mono.show_chroma()
