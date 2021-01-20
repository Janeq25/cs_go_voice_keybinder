from pydub import AudioSegment
from pydub.playback import play
from pyautogui import keyDown, keyUp
import os
import server

class Sound_player():
    def __init__(self):
        if not os.path.isdir('sounds'):
            os.mkdir('sounds')
        self.sound_dict = self.load_sounds() # sound_dict['title'] = 'sounds/title.mp3'

    def load_sounds(self):
        filenames = os.listdir('sounds')
        sound_dict = {}
        for filename in filenames:
            sound_dict[filename.replace('.mp3', '')] = 'sounds/' + filename
        return sound_dict

    def message_handler(self, conn, addr, msg, send):
        if msg.startswith('REQUEST'):
            send(conn, addr, self.sound_dict)
        elif msg.startswith('PLAY'):
            msg = msg.replace('PLAY ', '')
            print(msg)
            if msg in self.sound_dict.keys():
                print('here')
                song = AudioSegment.from_mp3(self.sound_dict[msg])
                keyDown('k')
                play(song)
                keyUp('k')

sp = Sound_player()

serv = server.Server(sp.message_handler)
serv.start()

#song = AudioSegment.from_mp3()
#play(song)