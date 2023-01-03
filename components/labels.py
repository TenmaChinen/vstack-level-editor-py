from tkinter import Label

d_label_cnf = dict( bg='#353131', fg='white', font='Calibri 16 bold', bd=2, relief='groove', pady=5)
d_title_cnf = dict( bg='#353131', fg='white', font='Calibri 20 bold', bd=2, relief='groove', pady=5)


class LabelBase(Label):
    def __init__(self, master, **kw):
        Label.__init__(self, master=master, cnf=d_label_cnf, **kw)

class LabelTitle(Label):
    def __init__(self, master, **kw):
        Label.__init__(self, master=master, cnf=d_title_cnf, **kw)

