import client

from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout


class no_connection_screen(Screen):
    pass

class default_screen(Screen):
    pass



class MyApp():
    global sm
    sm = ScreenManager()
    sm.add_widget(no_connection_screen(name='no_connection_screen'))
    sm.add_widget(default_screen(name='default_screen'))



# cl = client.Client('192.168.55.113')
# print(cl.request('REQUEST'))
# cl.send('PLAY fuckx3')
#
#
# input()