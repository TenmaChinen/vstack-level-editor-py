from .buttons import ButtonAdd, ButtonSub
from tkinter import Frame, IntVar
from .labels import LabelBase


class InputInteger(Frame):

    ADD = 'ADD'
    SUB = 'SUB'

    def __init__(self, master, text='', value=0, _range=(0,10), **kw):
        Frame.__init__(self, master=master, **kw)
        self.var  = self.__create_variable(value=value, _range=_range)
        self.__create_label(text=text)
        self.__create_number()
        self.btn_sub = self.__create_button_sub()
        self.btn_add = self.__create_button_add()
        self.callback = None
        self.__check_state()

    def __create_variable(self,value,_range):
        self.__min, self.__max = _range
        value = min(max(value,self.__min),self.__max)
        var = IntVar(value=value)
        return var

    def __create_label(self, text):
        label = LabelBase(master=self, text=text, width=6)
        label.pack(side='left', fill='both', expand=True)

    def __create_number(self):
        label = LabelBase(master=self, textvariable=self.var, width=3)
        label.pack(side='left', fill='both', expand=True)

    def __create_button_sub(self):
        btn_sub = ButtonSub(master=self, font='Calibri 12 bold', command=self.__on_click_sub)
        btn_sub.pack(side='left', fill='both')
        return btn_sub

    def __create_button_add(self):
        btn_add = ButtonAdd(master=self, font='Calibri 12 bold', command=self.__on_click_add)
        btn_add.pack(side='left', fill='both')
        return btn_add

    def __check_state(self):
        value = self.var.get()
        if value <= self.__min:
            self.btn_sub.disable()
        else:
            self.btn_sub.enable()

        if value >= self.__max:
            self.btn_add.disable()
        else:
            self.btn_add.enable()


    def __increment(self):
        value = min( self.var.get() + 1, self.__max)
        self.var.set( value = value)
        self.__check_state()

    def __decrement(self):
        value = max( self.var.get() -1, self.__min)
        self.var.set( value = value)
        self.__check_state()


    def set_callback(self, callback):
        self.callback = callback

    def set_value(self, value):
        value = max(min(self.__max,value), self.__min)
        self.var.set(value=value)
        self.__check_state()


    # [ Callbacks ]

    def __callback(self, event):
        if self.callback:
            self.callback(event=event)


    def __on_click_sub(self):
        self.__decrement()
        self.__callback(event=self.SUB)

    def __on_click_add(self):
        self.__increment()
        self.__callback(event=self.ADD)

