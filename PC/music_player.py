import threading
#import soundcard as sc
import sounddevice as sd
import pydub
import numpy as np


run_flag = True

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
    global run_flag
    run_flag = True

    try:
        if speaker == 'default':
            #print(sd.query_devices())
            #sc.default_speaker().play(data, sample_rate, channels=2)
            sd.play(data, sample_rate)
            #while run_flag:
                #pass
            #sd.stop()
            sd.wait()
        else:
            #sc.get_speaker(speaker).play(data, sample_rate, channels=2)
            sd.play(data, sample_rate, device=speaker)
            #while run_flag:
                #pass
            #sd.stop()
            sd.wait()
        # sc.default_speaker().play(data, sample_rate, channels=2)
    except Exception as e:
        print(e)
        #sc.default_speaker().play(data, sample_rate, channels=2)

def sound_stop():
    global run_flag
    run_flag = False
    print('stopping')
    sd.stop()

if __name__ == '__main__':
    pass
    #if sys.platform.startswith('win'):
        # On Windows calling this function is necessary.
        #multiprocessing.freeze_support()



#framerate , data = read('sounds/am gej.mp3',0 , normalized=True)

#t2 = threading.Thread(target=play, args=(data, framerate, 'VoiceMeeter Aux Input (VB-Audio VoiceMeeter AUX VAIO), Windows DirectSound',))
#t1 = threading.Thread(target=play, args=(data, framerate, 'default',))
#t1.start()
#t2.start()


