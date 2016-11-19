TITLE = 'CNC M97 Lx calculator'

import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton as Button

class Form(GridLayout):
    K=10
    def on_text(self,inst,val):
        self.calculate()
    def calculate(self):
        try:
            stock = self.K*float(self.length.text)
            chuck = float(self.chuck.text)
            detail = float(self.detail.text)
            # calc Ln
            res = ((stock-chuck)/detail)
            if res<1: raise self
            self.calc.text='L%.2f'%res
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
        self.calc = Button(text='')
        self.calc.bind(on_press=self.doM)
        self.add_widget(self.calc)
        # detail
        self.add_widget(Label(text='Detail:'))
        self.detail = TextInput(text='45',multiline=False)
        self.detail.bind(text=self.on_text)
        self.add_widget(self.detail)
        self.add_widget(Label(text='mm'))
        # chuck
        self.add_widget(Label(text='Chuck:'))
        self.chuck = TextInput(text='100',multiline=False)
        self.chuck.bind(text=self.on_text)
        self.add_widget(self.chuck)
        self.add_widget(Label(text='mm'))
        # stock
        self.add_widget(Label(text='Length:'))
        self.length = TextInput(text='123',multiline=False)
        self.length.bind(text=self.on_text)
        self.add_widget(self.length)
        self.units = Button(text='Cm',state='down')
        self.units.bind(on_press=self.cmmm)
        self.add_widget(self.units)
        # default calc
        self.calculate()

class M97(App):
    def on_pause(self): return True
    def on_resume(self): pass
    def build(self):
        return Form()

M97().run()
