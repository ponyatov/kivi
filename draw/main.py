from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Line

class Form(Widget):
    def on_touch_down(self,touch):
        with self.canvas:
            touch.ud["line"] = Line(points=(touch.x,touch.y))
    def on_touch_move(self, touch):
        touch.ud["line"].points += (touch.x,touch.y)
 
class Draw(App):
    def build(self):
        return Form()
Draw().run()