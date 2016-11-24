# -*- coding: utf8 -*-

TITLE = 'CNC M97 Lx calculator'

import re

import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton

from kivy.storage.jsonstore import JsonStore
# from os.path import join
# data_dir = getattr(self, 'user_data_dir') #get a writable path to save the file
# store = JsonStore(join(data_dir, 'user.json'))
db = JsonStore('M97.json')
# db.put('about',about=TITLE)

class NumInput(TextInput):
    re_num = re.compile(r'[0-9.]+')
    def insert_text(self, substring, from_undo=False):
        if self.re_num.match(substring) and len(self.text)<4:
            return super(self.__class__, self).insert_text(substring, from_undo=from_undo)
        else:
            return super(self.__class__, self).insert_text('', from_undo=from_undo)

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
            if (stock>1100): raise self
            res = ((stock-chuck)/(detail+cutter))
            if res<1: raise self
            self.calc.text='L%.1f'%res
            self.calc.background_color=(0,1,0,1)
        except:
            self.calc.text='ОШИБКА'
            self.calc.background_color=(1,0,0,1)
    def doM(self,inst):
        self.calculate()
    def cm(self):
        self.units.text='СМ'
        self.units.state='down'
        self.K=10
    def mm(self):
        self.units.text='мм'
        self.units.state='normal'
        self.K=1 
    def cmmm(self,inst):
        if self.K==1: self.cm()
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
        self.add_widget(Label(text='Заготовка'))
        self.length = NumInput(text='123',multiline=False,font_size=32,input_type='number')
        self.length.bind(text=self.on_text)
        self.add_widget(self.length)
        self.units = ToggleButton(text='СМ',state='down')
        self.units.bind(on_press=self.cmmm)
        self.add_widget(self.units)
        # detail
        self.add_widget(Label(text='Деталь'))
        self.detail = NumInput(text='45',multiline=False,font_size=32,input_type='number')
        self.detail.bind(text=self.on_text)
        self.add_widget(self.detail)
        self.add_widget(Label(text='мм'))
        # cutter
        self.add_widget(Label(text='Отрезной'))
        self.cutter = NumInput(text='4',multiline=False,input_type='number')
        self.cutter.bind(text=self.on_text)
        self.add_widget(self.cutter)
        self.add_widget(Label(text='мм'))
        # chuck
        self.add_widget(Label(text='Патрон'))
        self.chuck = NumInput(text='100',multiline=False,input_type='number')
        self.chuck.bind(text=self.on_text)
        self.add_widget(self.chuck)
        self.add_widget(Label(text='мм'))
        # default calc
        self.calculate()

class M97(App):
    def on_save(self):
        db.put('M97',\
               length=self.form.length.text,\
               K=self.form.K,\
               detail=self.form.detail.text,
               cutter=self.form.cutter.text,
               chuck=self.form.chuck.text\
            )
    def on_load(self):
        # lenth
        try:
            self.form.length.text=db.get('M97')['length']
            self.form.K=db.get('M97')['K']
            self.form.detail.text=db.get('M97')['detail']
            self.form.cutter.text=db.get('M97')['cutter']
            self.form.chuck.text=db.get('M97')['chuck']
        except KeyError:
            self.form.length.text='110'
            self.form.K=10
            self.form.detail.text='77'
            self.form.cutter.text='4'
            self.form.chuck.text='99'
        # set unit button state
        if self.form.K==10: self.form.cm()
        else: self.form.mm()
        # calc
        self.form.calculate()        
    def on_stop(self):
        self.on_save()
        App.on_stop(self)
    def on_pause(self):
        self.on_save()
        return True
    def on_start(self):
        self.on_load()
        App.on_start(self)
    def on_resume(self):
        self.on_load()
    def build(self):
        self.form=Form()
        self.on_load()
        return self.form

M97().run()
