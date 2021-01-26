import client
import os
import json

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout




def load_ip():
    global c, sound_list
    c = client.Client('192.168.55.110')


    if os.path.isfile('config.json'):
        with open('config.json', 'r') as file:
            config = json.loads(file.read())
        c = client.Client(config['server_ip'])
        file.close()
        print('loaded last ip')
    else:
        with open('config.json', 'w') as file:
            config = json.dumps({'server_ip': '192.168.55.105'})
            file.write(config)
            file.close()
        c = client.Client('192.168.55.110')
        print('created json file')

    try:
        sound_list = c.request('REQUEST')
        c.disconnect()
    except:
        sound_list = []

#    sound_list = []


class no_connection_screen(Screen):

    def on_press_submit(self, server_ip):
        global c, sound_list
        try:
            c = client.Client(server_ip)
            sound_list = c.request('REQUEST')
            sm.current = 'default_screen'
            with open('config.json', 'w') as file:
                file.write(json.dumps({'server_ip': server_ip}))
                file.close()
        except:
            sound_list = []
            sm.current = 'no_connection_screen'

        print(server_ip)

class default_screen(Screen):
    def on_press_stop(self):
        try:
            c.send('STOP')
            c.disconnect()
        except:
            sm.current = 'no_connection_screen'

    def on_press_refresh(self):
        global ds, sound_list
        try:
            sound_list = c.request('REQUEST')
            sm.remove_widget(ds)
            ds = default_screen(name='default_screen')
            sm.add_widget(ds)
            sm.current = 'default_screen'
        except:
            sound_list = []
            sm.current = 'no_connection_screen'

    def on_slider_value_change(self, volume):
        try:
            c.send('VOLUME ' + str(volume))
            c.disconnect()
        except:
            sm.current = 'no_connection_screen'

class Buttons_list(GridLayout):
    def __init__(self, **kwargs):
        if sound_list == []:
            sm.current = 'no_connection_screen'

        super(Buttons_list, self).__init__(**kwargs)
        self.cols = 4
        #box = BoxLayout()
        self.padding = 10
        self.my_buttons = []

        for title in sound_list:
            button = Button(text=title)
            button.font_size = button.width * 0.15
            button.text_size = button.width, None
            button.halign = 'center'
            button.valign = 'middle'
            #button.bind(on_press=lambda x: self.pressed(button.text))
            button.bind(on_press=self.pressed)
            self.my_buttons.append(button)
            self.add_widget(button)
        #self.add_widget(box)







    def pressed(self, instance):
        try:
            #print(instance.text)
            #print('PLATY ' + title)
            c.send('PLAY ' + instance.text)
            c.disconnect()
            return True
        except:
            sm.current = 'no_connection_screen'
            return False



class MyApp(App):
    def build(self):

        global sm, sound_list, ds
        sm = ScreenManager()
        sm.add_widget(no_connection_screen(name='no_connection_screen'))
        ds = default_screen(name='default_screen')
        sm.add_widget(ds)
        if sound_list == []:
            sm.current = 'no_connection_screen'
        else:
            sm.current = 'default_screen'
        return sm

if __name__ == '__main__':
    global c, sound_list
    load_ip()
    MyApp().run()


# cl = client.Client('192.168.55.113')
# print(cl.request('REQUEST'))
# cl.send('PLAY fuckx3')
#
#
# input()