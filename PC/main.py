from pyautogui import keyDown, keyUp
import os
import server
from pydub import AudioSegment
from pydub.playback import play
import multiprocessing


def play_sound(filename):
    song = AudioSegment.from_mp3(filename)
    play(song)

class Sound_player():
    def __init__(self):
        if not os.path.isdir('sounds'):
            os.mkdir('sounds')
        self.sound_dict = self.load_sounds() # sound_dict['title'] = 'sounds/title.mp3'
        self.sound_process = None
        self.volume = 0

    def load_sounds(self):
        filenames = os.listdir('sounds')
        sound_dict = {}
        for filename in filenames:
            sound_dict[filename.replace('.mp3', '')] = 'sounds/' + filename
        return sound_dict

    def message_handler(self, conn, addr, msg, send):
        if msg.startswith('REQUEST'):
            #print(self.sound_dict.keys())
            self.sound_dict = self.load_sounds()
            send(conn, addr, list(self.sound_dict.keys()))

        elif msg.startswith('PLAY'):
            msg = msg.replace('PLAY ', '')
            print(msg)
            #self.play_sound(self.sound_dict[msg])
            if self.sound_process == None:
                self.sound_process = multiprocessing.Process(target=self.play_sound, args=(self.sound_dict[msg], self.volume,))
                self.sound_process.start()
                self.sound_process.join()
                self.sound_process = None

        elif msg.startswith('STOP'):
            if not self.sound_process == None:
                self.sound_process.terminate()
                self.sound_process = None

        elif msg.startswith('VOLUME'):
            msg = msg.replace('VOLUME ', '')
            self.volume = float(msg)
            #print(self.volume)


    def play_sound(self, filename, volume):
        song = AudioSegment.from_mp3(filename)
        song += volume
        play(song)


if __name__ == '__main__':

    sp = Sound_player()

    serv = server.Server(sp.message_handler)
    serv.start()

#song = AudioSegment.from_mp3()
#play(song)