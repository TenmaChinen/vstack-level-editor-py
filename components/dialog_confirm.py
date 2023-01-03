from tkinter import Tk, Frame, Message, Button, StringVar, BooleanVar
from components.frame_header import FrameHeader

d_frame_cnf = dict(bg='#414141', bd=2)
d_lbl_message = dict(fg='white', font=(
    'Calibri', 16, 'bold'), padx=15, pady=20)
d_btn_dialog = dict(fg='white', font=('Calibri', 16, 'bold'),
                    relief='flat', border=0, activeforeground='#DCDCDC')
d_fr_footer_cnf = dict(bg='#313131', bd=1)


class DialogConfirm(Frame):

    ACCEPT = 0
    CANCEL = 1

    def __init__(self, master, **kw):

        Frame.__init__(self, master, cnf=d_frame_cnf, **kw)
        self.fr_header = self.__create_frame_header()
        self.var_message = self.__create_label_message(kw.get('width', 300))
        self.fr_footer = self.__create_frame_footer()
        self.__create_button_cancel()
        self.__create_button_accept()
        self.var_confirmation = BooleanVar(value=False)

        if 'height' in kw:
            self.pack_propagate(False)

    def __create_frame_header(self):
        fr_header = FrameHeader(master=self)
        fr_header.set_callback(on_close=self.__on_close_header)
        fr_header.pack(side='top')
        return fr_header

    def __create_label_message(self, width):
        var_message = StringVar()
        msg_message = Message(
            master=self, textvariable=var_message, cnf=d_lbl_message)
        msg_message.config(bg=self['bg'], padx=20, pady=20, width=width)
        msg_message.pack(side='top', fill='both', expand=True)
        return var_message

    def __create_frame_footer(self):
        fr_footer = Frame(master=self, cnf=d_fr_footer_cnf)
        fr_footer.pack(side='bottom', fill='x')
        return fr_footer

    def __create_button_cancel(self):
        btn_cancel = Button(master=self.fr_footer, text='Cancel', cnf=d_btn_dialog)
        btn_cancel['command'] = self.__on_click_cancel
        btn_cancel.config( bg=self.fr_footer['bg'], activebackground=self.fr_footer['bg'])
        btn_cancel.pack(side='right')

    def __create_button_accept(self):
        btn_accept = Button(master=self.fr_footer, text='Accept', cnf=d_btn_dialog)
        btn_accept['command'] = self.__on_click_accept
        btn_accept.config(bg=self.fr_footer['bg'], activebackground=self.fr_footer['bg'])
        btn_accept.pack(side='right')

    def __set_binds(self):
        self.bind_all('<Escape>', lambda e: self.__on_key_press_escape)


    # Callbacks

    def __on_close_header(self):
        self.var_confirmation.set(value=False)

    def __on_click_cancel(self):
        self.var_confirmation.set(value=False)

    def __on_click_accept(self):
        self.var_confirmation.set(value=True)

    def __on_key_press_escape(self):
        self.var_confirmation.set(value=False)


    # Methods

    def set_title(self, title):
        self.fr_header.set_title(title)

    def set_message(self, message):
        self.var_message.set(message)

    def show(self, message=None):
        if not self.winfo_ismapped():
            self.var_confirmation.set(value=False)
            if message is not None:
                self.var_message.set(message)
            self.place(relx=0.5, rely=0.5, anchor='center')
            self.wait_variable(self.var_confirmation)
            self.hide()
            return self.var_confirmation.get()

    def hide(self):
        self.place_forget()
