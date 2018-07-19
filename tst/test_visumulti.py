import sys
sys.path.append("../src")
from visumulti import *

track6 = "../tracks/metro80short.wav"
track7 = "../tracks/metro60short.wav"
track8 = "../tracks/metro120short.wav"
track9 = "../tracks/solo1.wav"

def test_visurhythm(tracktab):
    monoRtab = []
    for track in tracktab :
        monoR = MonoRhythm(file = track)
        monoR.load_onsets()
        mono = [monoR, monoR]
        monoRtab.append(mono)
    visumulti = VisuMulti(monoRtab)
    visumulti.test_display_rhythm()

#test_visurhythm([track7, track8])
#test_visurhythm([track7, track8, track6])
#test_visurhythm([track7, track7])
test_visurhythm([track6, track7])
#test_visurhythm([track6, track9]) #erreur car durees diff
