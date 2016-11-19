TITLE = 'CNC M97 Lx calculator'

import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton

class Form(GridLayout):
    K=10
    def on_text(self,inst,val):
        self.calculate()
    def calculate(self):
        try:
            stock = self.K*float(self.length.text)
            chuck = float(self.chuck.text)
            detail = float(self.detail.text)
            cutter = float(self.cutter.text)
            # calc Ln
            res = ((stock-chuck)/(detail+cutter))
            if res<1: raise self
            self.calc.text='L%.1f'%res
        except:
            self.calc.text='<ERROR>'
    def doM(self,inst):
        self.calculate()
    def cm(self):
        self.units.text='Cm'
        self.units.state='down'
        self.K=10
    def mm(self):
        self.units.text='mm'
        self.units.state='normal'
        self.K=1 
    def cmmm(self,inst):
        if self.units.text=='mm': self.cm()
        else: self.mm()
        self.calculate()
        
    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.cols=3
        # calc
        self.add_widget(Label(text='M97'))
        self.add_widget(Label(text='P1000'))
        self.calc = Button(text='',font_size=32)
        self.calc.bind(on_press=self.doM)
        self.add_widget(self.calc)
        # stock
        self.add_widget(Label(text='Length:'))
        self.length = TextInput(text='123',multiline=False,font_size=32,input_type='number')
        self.length.bind(text=self.on_text)
        self.add_widget(self.length)
        self.units = ToggleButton(text='Cm',state='down')
        self.units.bind(on_press=self.cmmm)
        self.add_widget(self.units)
        # detail
        self.add_widget(Label(text='Detail:'))
        self.detail = TextInput(text='45',multiline=False,font_size=32,input_type='number')
        self.detail.bind(text=self.on_text)
        self.add_widget(self.detail)
        self.add_widget(Label(text='mm'))
        # cutter
        self.add_widget(Label(text='Cutter:'))
        self.cutter = TextInput(text='4',multiline=False,input_type='number')
        self.cutter.bind(text=self.on_text)
        self.add_widget(self.cutter)
        self.add_widget(Label(text='mm'))
        # chuck
        self.add_widget(Label(text='Chuck:'))
        self.chuck = TextInput(text='100',multiline=False,input_type='number')
        self.chuck.bind(text=self.on_text)
        self.add_widget(self.chuck)
        self.add_widget(Label(text='mm'))
        # default calc
        self.calculate()

class M97(App):
    def on_pause(self): return True
    def on_resume(self): pass
    def build(self):
        return Form()

M97().run()
