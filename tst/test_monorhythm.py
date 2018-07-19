import sys
sys.path.append("../src")
from monorhythm import  *
from visumono import *
from time import time
import librosa as lb

#Test

track = "../tracks/solo1.wav"

# time1 = time()
visu1 = VisuMono(file  = track, duration = 10.0)
mono1 = visu1.get_monorhythm()
# time2 = time()
# print "temps load :", (time2-time1)
# mono1.load_onsets()
# time3 = time()
# print "temps onsets :", (time3-time2)

# # #mono1.get_rect(True)
# # print lb.beat.estimate_tempo(mono1.get_onset_envelope())

fs = mono1.get_frame_scale()
oenv = mono1.get_onset_envelope()

pt.plot(fs, oenv)
pt.show()

#mono1.show_track()



# visu1 = VisuMono(file = track)
# monoR = visu1.get_monorhythm()
# oenv = mono1.get_onset_envelope()
# fs = mono1.get_frame_scale()
# pt.plot(fs,oenv)
# pt.show()
# visu1.get_rect_rhythm()

# track = "../tracks/SwingBazar_FlecheDOr/01_BassMic1.wav"

# (signal, sr)=lb.load(track)

# print sr
