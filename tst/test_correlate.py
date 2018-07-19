import sys
sys.path.append("../src")
import librosa as lb
import numpy as np
import matplotlib.pyplot as pt
from math import *
from constants import *
from correlate import *
from monorhythm import *
from tools import *

track = "../tracks/long_lune.wav"
track1 = "../tracks/metro80short.wav"
track2 = "../tracks/solo1trim60.wav"
track3 = "../tracks/metro60short.wav"
track4 = "../tracks/metro120short.wav"

def test_autocorrelation(track):
    mono1 = MonoRhythm(file  = track, signal = lb.core.load(track, sr=44100)[0])
    mono1.load_onsets()
    fs = mono1.get_frame_scale()
    oenv = mono1.get_onset_envelope()
    corr = coeff_correl(oenv, oenv, (0, len(oenv)))
    print corr
    assert (abs(corr-1.0) < 10**(-6))

test_autocorrelation(track)
# test_autocorrelation(track1)
# test_autocorrelation(track2)

def test_correlation(track1, track2, time_interval):
    (starttime, endtime) = time_interval
    mono1 = MonoRhythm(file  = track1, signal = lb.core.load(track1, sr= 44100)[0])
    mono1.load_onsets()

    mono2 = MonoRhythm(file  = track2, signal = lb.core.load(track2, sr=44100)[0])
    mono2.load_onsets()

    (startframe, endframe) = (time_to_frame(starttime), time_to_frame(endtime))
    
    fs = mono1.get_frame_scale()[startframe:endframe]
    oenv1 = mono1.get_onset_envelope()[startframe:endframe]
    oenv2 = mono2.get_onset_envelope()[startframe:endframe]
    
    corr = coeff_correl(oenv1, oenv2, (startframe, endframe))
    print corr

    pt.plot(fs, oenv1)
    pt.plot(fs, oenv2)
    pt.show()

track5 = "../tracks/guillaume2.wav"
track6 = "../tracks/romain2.wav"
track7 = "../tracks/lukaz2.wav"

track8 = "../tracks/marseillaise1.wav"
track9 = "../tracks/marseillaise2.wav"
track10 = "../tracks/marseillaise3.wav"

#test_correlation(track8, track10, (0.0, 5.0))
