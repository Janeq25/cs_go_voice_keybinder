#from pyautogui import keyDown, keyUp
#from pynput.keyboard import Key, Controller
#from pydub import AudioSegment
#from pydub.playback import play
import ctypes
import os
import server
import multiprocessing
#import threading
#from subprocess import Popen
import sys
import music_player

#keyboard = Controller()

SendInput = ctypes.windll.user32.SendInput

K = 0x4B

PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))



class Sound_player():
    def __init__(self):
        if not os.path.isdir('sounds'):
            os.mkdir('sounds')
        self.sound_dict = self.load_sounds() # sound_dict['title'] = 'sounds/title.mp3'
        self.sound_process1 = None
        self.sound_process2 = None
        self.volume = 0


    def load_sounds(self):
        filenames = os.listdir('sounds')
        sound_dict = {}
        for filename in filenames:
            sound_dict[filename.replace('.mp3', '')] = 'sounds/' + filename
        return sound_dict

    def message_handler(self, conn, addr, msg, send):
        print(msg)
        if msg.startswith('REQUEST'):
            #print(self.sound_dict.keys())
            self.sound_dict = self.load_sounds()
            send(conn, addr, list(self.sound_dict.keys()))

        elif msg.startswith('PLAY'):
            msg = msg.replace('PLAY ', '')
            print(msg)
            if self.sound_process2 == None:
                #self.play_sound(self.sound_dict[msg])
                #if self.sound_process1 == None:
                music_player.sound_stop()
                #print('trza zacząć porcess')
                sample_rate, data = music_player.read(self.sound_dict[msg], self.volume, normalized=True)
                #self.sound_process1 = threading.Thread(target=self.play_sound, args=(data, sample_rate, 'VoiceMeeter Aux Input (VB-Audio VoiceMeeter AUX VAIO), Windows DirectSound', ))
                #self.sound_process2 = threading.Thread(target=self.play_sound, args=(data, sample_rate, 'default',))
                self.sound_process1 = multiprocessing.Process(target=music_player.play, args=(data, sample_rate, 'VoiceMeeter Aux Input (VB-Audio VoiceMeeter AUX VAIO), Windows DirectSound',))
                self.sound_process2 = multiprocessing.Process(target=music_player.play, args=(data, sample_rate, 'default',))
                #self.sound_process1 = Popen(['music_player_popen.py', str(self.volume), 'VoiceMeeter Aux Input (VB-Audio VoiceMeeter AUX VAIO), Windows DirectSound'])
                #self.sound_process2 = Popen(['music_player_popen.py', str(self.volume), 'default',])
                #print('proces powstał')
                PressKey(0x25)
                self.sound_process2.start()
                self.sound_process1.start()
                #print('proces ruszył')
                #keyboard.press('k')
                self.sound_process1.join()
                #keyboard.release('k')
                ReleaseKey(0x25)
                self.sound_process1 = None
                self.sound_process2 = None

        elif msg.startswith('STOP'):
            if not self.sound_process2 == None:
                self.sound_process1.terminate()
                self.sound_process2.terminate()
                #music_player.sound_stop()
                self.sound_process1 = None
                self.sound_process2 = None

        elif msg.startswith('VOLUME'):
            msg = msg.replace('VOLUME ', '')
            self.volume = float(msg)
            #print(self.volume)

    #def play_sound(self, filename, volume, speaker):
        #print('jestem w procesie')
        #song = AudioSegment.from_mp3(filename)
        #print('piosenka załadowana')
        #song += volume
        #play(song)
        #print('piosenka zagrana')
        #music_player.play(filename, volume, speaker)







if __name__ == '__main__':
    if sys.platform.startswith('win'):
        # On Windows calling this function is necessary.
        multiprocessing.freeze_support()

    sp = Sound_player()

    serv = server.Server(sp.message_handler)
    serv.start()

#song = AudioSegment.from_mp3()
#play(song)

