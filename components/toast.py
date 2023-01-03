from tkinter import Label

d_toast_cnf = dict( bg='#353131', fg='white', font='Calibri 16 bold', bd=0, relief='flat', pady=5, padx=10)

class Toast(Label):
    def __init__(self, master, **kw):
        Label.__init__(self, master=master, cnf=d_toast_cnf, **kw)
        self.__root = master._root()
        self.__reset()

    def set_message(self,message):
        self.config(text=message, width=len(message))

    def show(self):
        if self.__run == False:
            self.__run = True
            self.__root.after(0,self.__raise_animation)

    def __reset(self):
        self.__pos_y = 1.1
        self.__run = False
    
    def __raise_animation(self):
        self.__pos_y -= 0.01
        self.place(relx=0.5, rely=self.__pos_y, anchor='n')
        if self.__pos_y <= 0.92:
            self.__root.after(2000, self.__down_animation)
        else:
            self.__root.after(15, self.__raise_animation)


    def __down_animation(self):
        self.__pos_y += 0.01
        self.place(relx=0.5, rely=self.__pos_y, anchor='n')
        if self.__pos_y < 1.1:
            self.__root.after(15, self.__down_animation)
        else:
            self.__reset()