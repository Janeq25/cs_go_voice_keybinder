import threading
#import soundcard as sc
import sounddevice as sd
import pydub
import numpy as np


def read(f, volume, normalized=False):
    """MP3 to numpy array"""
    a = pydub.AudioSegment.from_mp3(f)
    a += volume
    y = np.array(a.get_array_of_samples())
    if a.channels == 2:
        y = y.reshape((-1, 2))
    if normalized:
        return a.frame_rate, np.float32(y) / 2**15
    else:
        return y, a.frame_rate


def play(data, sample_rate, speaker):

    try:
        if speaker == 'default':
            #print(sd.query_devices())
            #sc.default_speaker().play(data, sample_rate, channels=2)
            sd.play(data, sample_rate)
            sd.wait()
        else:
            #sc.get_speaker(speaker).play(data, sample_rate, channels=2)
            default = sd.default.device
            sd.default.device = speaker
            sd.play(data, sample_rate)
            sd.wait()
            sd.default.device = default
        # sc.default_speaker().play(data, sample_rate, channels=2)
    except Exception as e:
        print(e)
        #sc.default_speaker().play(data, sample_rate, channels=2)

def sound_stop():
    sd.stop()



#framerate , data = read('sounds/am gej.mp3',0 , normalized=True)

#t2 = threading.Thread(target=play, args=(data, framerate, 'VoiceMeeter Aux Input (VB-Audio VoiceMeeter AUX VAIO), Windows DirectSound',))
#t1 = threading.Thread(target=play, args=(data, framerate, 'default',))
#t1.start()
#t2.start()


