from tkinter import Tk, Frame, Label, Button, StringVar

d_frame_cnf = dict(bg='#313131', relief='groove')
d_label_title = dict(fg='white', font=('Calibri', 22, 'bold'))
d_btn_close = dict(fg='white', font=('Calibri', 18, 'bold'), relief='flat', border=0, activeforeground='#E3E3E3')

class FrameHeader(Frame):

    def __init__(self, master, title='', **kw):

        Frame.__init__(self, master, cnf=d_frame_cnf, **kw)
        self.pack(fill='x')
        self.lbl_title = self.__create_title(title=title)
        self.__create_button_close()
        self.__set_binds()
        self.callback = None

    def __create_title(self, title):
        lbl_title = Label(master=self, text=title, cnf=d_label_title)
        lbl_title.config(bg=self['bg'])
        lbl_title.pack(side='left', padx=10)
        return lbl_title

    def __create_button_close(self):
      btn_close = Button(master=self,text='✖', cnf=d_btn_close)
      btn_close.config(bg = self['bg'], activebackground= self['bg'])
      btn_close['command'] = self.__on_click_close
      btn_close.pack(side='right')

    def __set_binds(self):
      self.bind_all('<Escape>', self.__on_key_press_close)
        
    def set_callback(self,on_close):
      self.callback = on_close

    def set_title(self,title):
      self.lbl_title['text'] = title

    # Callbacks

    def __on_click_close(self):
      if self.callback:
        self.callback()

    def __on_key_press_close(self,event):
      if self.callback:
        self.callback()      