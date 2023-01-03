from tkinter import Entry, IntVar

d_entry_cnf = dict(
    bg='#808080', fg='white', relief='raised', justify='center',
    font=('Calibri', 22, 'bold'), insertbackground='white',bd=2,
    disabledbackground='#6F6F6F', disabledforeground='white',
    selectbackground='#656565', selectforeground='white')

class States:
    DISABLED = 'DISABLED'
    ENABLED = 'ENABLED'

d_states = {
    States.DISABLED : dict( state='disabled', relief='raised', cursor='arrow'),
    States.ENABLED : dict( state='normal', relief='groove', cursor='xterm')
    }

class ActionType:
    ADD = '1'
    DEL = '0'
    OTHER = '-1'

class EntryInteger(Entry, States):

    def __init__(self, master, _id, value=0, _range=(0, 10), size=22, **kw):
        Entry.__init__(self, master=master, cnf=d_entry_cnf, validate='key', validatecommand=( master._root().register(self.__on_validation), '%P', '%i', '%S', '%d'), **kw)
        self.config(font=f'Calibri {size} bold')
        self._id = _id
        self.int_var = self.__create_variable(value=value, _range=_range)
        self.set_state(state=self.DISABLED)
        self.callback = None

    def __create_variable(self, value, _range):
        self.__min, self.__max = _range
        value = min(max(value, self.__min), self.__max)
        int_var = IntVar(value=value)
        self['textvariable'] = int_var
        return int_var

    @property
    def length(self):
        return len(self.get())

    def set_callback(self, on_change):
        self.callback = on_change

    def set_value(self, value):
        value = max(min(self.__max, value), self.__min)
        self.int_var.set(value=value)

    def set_state(self, state):
        self.config( **d_states[state] )
        if state == States.DISABLED:
            self.unbind('<FocusOut>')
            self.unbind('<Escape>')
            self.unbind('<Return>')
            self.bind('<Button-3>', self.__on_right_click)
        elif state == States.ENABLED:
            self.bind('<FocusOut>', self.__on_focus_out)
            self.bind('<Escape>', self.__on_key_press_escape)
            self.bind('<Return>', self.__on_key_press_enter)
            self.unbind('<Button-3>')
            self.focus_set()
            self.icursor(index=self.length)
            self.select_range(0, self.length)
            self.last_value = self.int_var.get()

    def __callback(self):
        if self.callback:
            if self.int_var.get() != self.last_value:
                self.callback(value=self.int_var.get() , _id=self._id)
    
    # [ CALLBACKS ]

    def __on_focus_out(self, event):
        self.__check_bounds()
        if self.__callback() != False:
            self.set_state(state=States.DISABLED)

    def __on_key_press_enter(self,event):
        self.__check_bounds()
        if self.__callback() != False:
            self.set_state(state=States.DISABLED)

    def __on_key_press_escape(self,event):
        self.int_var.set(value=self.last_value)
        self.set_state(state=States.DISABLED)

    def __on_right_click(self,event):
        self.set_state(state=States.ENABLED)        

    def __on_validation(self, text, idx, str_ins_del, action_type):
        # print(f'Text : {text} | Idx : {idx} | Inserted or Deleted String : {str_ins_del} | Action : {action_type}')

        if action_type == ActionType.DEL:
            return True
        elif action_type == ActionType.ADD:
            if str_ins_del == '':
                return True
            try:
                value = int(str_ins_del)
                return True
            except :
                return False
        elif action_type == ActionType.OTHER:
            return True

    def __check_bounds(self):
        try:
            value = self.int_var.get()
            if value < self.__min:
                self.int_var.set(self.__min)
            elif value > self.__max:
                self.int_var.set(self.__max)
            else:
                self.int_var.set(value)
        except:
            self.int_var.set(value=self.last_value)