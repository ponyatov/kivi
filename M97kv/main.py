from kivy.app import App
from kivy.uix.label import Label

class My(App):
	def build(self):
		return Label(text='Hello')

My().run()