from tkinter import Button

d_button_cnf = dict(
    bg='#363636', fg='white', font='Calibri 16 bold', bd=1,
    activebackground='#424242', activeforeground='#EEEDED')


class ButtonBase(Button):
    def __init__(self, master, **kw):
        Button.__init__(self, master=master, cnf=d_button_cnf, **kw)

    def disable(self):
        self['state'] = 'disabled'

    def enable(self):
        self['state'] = 'normal'


class ButtonIcon(ButtonBase):
    def __init__(self, master, **kw):
        ButtonBase.__init__(self, master=master, **kw)
        self.config(width=2, padx=5)


class ButtonPlay(ButtonIcon):
    def __init__(self, master, **kw):
        ButtonIcon.__init__(self, master=master, text='▶', **kw)


class ButtonDelete(ButtonIcon):
    def __init__(self, master, **kw):
        ButtonIcon.__init__(self, master=master, text='✖', **kw)


class ButtonEdit(ButtonIcon):
    def __init__(self, master, **kw):
        ButtonIcon.__init__(self, master=master, text='🖊', **kw)


class ButtonConfig(ButtonIcon):
    def __init__(self, master, **kw):
        ButtonIcon.__init__(self, master=master, text='⚙', **kw)


class ButtonOpen(ButtonIcon):
    def __init__(self, master, **kw):
        ButtonIcon.__init__(self, master=master, text='📁', **kw)


class ButtonAdd(ButtonIcon):
    def __init__(self, master, **kw):
        ButtonIcon.__init__(self, master=master, text='➕', **kw)


class ButtonSub(ButtonIcon):
    def __init__(self, master, **kw):
        ButtonIcon.__init__(self, master=master, text='➖', **kw)
