import matplotlib.pyplot as mp
import numpy as np
import madmom
import librosa as lb

y, sr = lb.core.load("../tracks/solo1.wav", offset = 0, duration = 10.0)

oenv = lb.onset.onset_strength(y=y,sr=sr)
onset = lb.onset.onset_detect(y=y, onset_envelope = oenv)

for i in range(len(onset)):
    onset[i]=onset[i]+0.01
print onset
# onset*=512.0/(sr*1.0)

# mp.plot(oenv)
# mp.show()

#hop_length/sr ou 1/sr

print oenv, len(oenv)*512, len(y)

mp.plot(oenv, alpha=0.8)

mp.legend(frameon=True, framealpha=0.75)


lb.display.time_ticks(lb.frames_to_time(np.arange(len(oenv))))
mp.ylabel('Normalized strength')
mp.yticks([])
mp.axis('tight')
mp.tight_layout()
mp.show()
