from kivy.app import App
from kivy.uix.widget import Widget

class Form(Widget): pass
class M97(App):
	def build(self):
		return Form()
M97().run()
