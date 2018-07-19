import sys
sys.path.append("../src")
from multirhythm import *

# track = "../tracks/bitter32.wav"

# mono1 = MonoRhythm(file  = track)
# mono1.load_onsets()

# # #mono1.get_rect(True)
# # print lb.beat.estimate_tempo(mono1.get_onset_envelope())

# oenv = mono1.get_onset_envelope()

# (tempo, beats) = lb.beat.beat_track(onset_envelope = oenv)


# beat_time = [0 for i in oenv]
# for t in beats :
#     beat_time[t] = 1

# print tempo
# #print beats
# fs = mono1.get_frame_scale()
# # ob = mono1.get_onset_boolean()

# pt.plot(fs, beat_time)
# pt.plot(fs, oenv)
# pt.show()
# #mono1.show_track()

# track1 = "../tracks/Howlin_Amber_Skye/trim/Drums.wav"
# track2 = "../tracks/Howlin_Amber_Skye/trim/Guitars.wav"
# track3 = "../tracks/Howlin_Amber_Skye/trim/Keyboards.wav"
# track4 = "../tracks/Howlin_Amber_Skye/trim/Effects.wav"
# track5 = "../tracks/Howlin_Amber_Skye/trim/Vocals.wav"
track6 = "../tracks/marseillaise1.wav"
track7 = "../tracks/marseillaise3.wav"


### Test 1 ###
# monoRtab = []

# mono1 = MonoRhythm(file = track1)
# mono1.load_onsets()
# monoRtab.append(mono1)

# mono2 = MonoRhythm(file = track2)
# mono2.load_onsets()
# monoRtab.append(mono2)

# mono3 = MonoRhythm(file = track3)
# mono3.load_onsets()
# monoRtab.append(mono3)

# multiR = MultiRhythm(monoRtab = monoRtab)
# multiR.display_multi()

### Test 2 ###

monoRtab = []

(signal6,sr) = lb.core.load(track6, sr = 44100, duration = 20.0)
(signal7,sr) = lb.core.load(track7, sr = 44100, duration = 20.0)

mono1 = MonoRhythm(file = track6, signal = signal6)
mono1.load_onsets()
monoRtab.append(mono1)

mono3 = MonoRhythm(file = track7, signal = signal7)
mono3.load_onsets()
monoRtab.append(mono3)


multiR = MultiRhythm(monoRtab = monoRtab)x²
#shift = multiR.get_shift()
#oframe1 = mono1.get_onset_frames()
#oframe2 = mono2.get_onset_frames()
print multiR.get_beat()
#print oframe1
#print oframe2
multiR.display_multi()


