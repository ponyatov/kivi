TITLE = 'CNC M97 Lx calculator'

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button

class My(App):
    def build(self):
        return Label(text=TITLE)

My().run()
