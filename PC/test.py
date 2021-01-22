from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

class myScreen(Screen):
    def __init__(self, **kwargs):

        self.grid = GridLayout(cols=6)
        self.grid.my_buttons = []
        super(myScreen, self).__init__(**kwargs)
        for x in range(20):
            btt = Button(text=str(x))
            btt.bind(on_press=self.pressed)
            self.grid.my_buttons.append(btt)
            self.grid.add_widget(btt)

        self.add_widget(self.grid)


    def pressed(self, instance):
        print('pressed: ', instance.text)



class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(myScreen(name='no_connection_screen'))
        return sm

if __name__ == '__main__':
    MyApp().run()
