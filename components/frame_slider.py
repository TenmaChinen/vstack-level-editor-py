from tkinter import Frame, Scale, Label, IntVar

d_frame_cnf = dict( bg='#4D4D4D', padx=5, pady=5, relief='raised', bd=1)
d_label_name_cnf = dict( font='Calibri 18 bold', fg='white', relief='flat')
d_label_value_cnf = dict( font='Calibri 16 bold', fg='white', relief='flat')
d_scale_cnf = dict( bd=1, troughcolor='#787878', highlightthickness=0,activebackground='#707070', showvalue=False, length=40)

def ri(v): return int(round(v))

class KeyCode:
    LEFT = 37
    UP = 38
    RIGHT = 39
    DOWN = 40


class FrameSlider(Frame):
    
    class Orientation:
        VERTICAL = 'v'
        HORIZONTAL = 'h'

    def __init__(self, master, _id, name='', range_=(0,10), value=0, orientation=Orientation.HORIZONTAL, wide=30, **kw):
        super().__init__(master=master, cnf=d_frame_cnf, **kw)

        self._id = _id
        self._orientation = orientation
        self.var = self.__create_var(range_=range_, value=value)
        self.__create_name_label(name=name)
        self.__create_value_label(range_=range_)
        self._slider = self.__create_slider(range_=range_, wide=wide)
        self.__set_bindings()

        self.callback = None

    def __create_var(self, range_, value):
        var = IntVar(value=max(range_[0],value))
        self.__trace_tag = var.trace_add(mode='write', callback=self.__on_change_int_var)
        return var

    def __create_name_label(self, name):
        label = Label(master=self, text=name, bg=self['background'], cnf=d_label_name_cnf)
        d_pack = dict( side='bottom', pady=(5,0)) if self._orientation == self.Orientation.VERTICAL else dict(side='left', padx=(0,5))
        label.pack(**d_pack)

    def __create_value_label(self, range_):
        width = len(str(max(range_)))
        label = Label(master=self, textvariable=self.var, bg=self['background'], width=width, cnf=d_label_value_cnf)
        d_pack = dict( side='top', pady=(0,5)) if self._orientation == self.Orientation.VERTICAL else dict(side='right', padx=(5,0))
        label.pack(**d_pack)

    def __create_slider(self, range_, wide):
        from_, to = range_ if (self._orientation ==  self.Orientation.HORIZONTAL) else range_[::-1]
        scale = Scale(master=self, from_=from_, to=to, orient=self._orientation, width=wide, variable=self.var, cnf=d_scale_cnf)
        scale.config(bg=self['background'], )
        side, fill = ('top','y') if self._orientation == self.Orientation.VERTICAL else ('right','x')
        scale.pack(side=side, fill=fill, expand=True)
        return scale

    def __set_bindings(self):
        self._slider.bind('<Button-1>', self.__on_click_left)

    # [ M E T H O D S ]
    
    def set_callback(self,on_change):
        self.callback = on_change

    def set_value(self,value):
        self.var.trace_remove(mode='write', cbname=self.__trace_tag)
        self.var.set(value=value)
        self.__trace_tag = self.var.trace_add(mode='write', callback=self.__on_change_int_var)

    # [ C A L L B A C K S ]

    def __on_change_int_var(self,a,b,c):
        if self.callback:
            self.callback(_id=self._id, value=self.var.get())

    def __on_click_left(self, event):
        self._slider.focus_force()