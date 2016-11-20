from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button

class Form(Widget):
    b = Button()
    def __init__(self,**args):
        super(self.__class__,self).__init__(**args)
        self.add_widget(self.b)
    def on_touch_down(self,touch):
        print touch
#         if touch.pos[1]>self.btn.pos[1]:
        self.b.pos = touch.pos
 
class Draw(App):
    def build(self):
        return Form()
Draw().run()