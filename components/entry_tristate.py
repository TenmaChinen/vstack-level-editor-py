from tkinter import Tk, Frame, Label, Entry, Button, StringVar

'''
    Selectable as button ( keeps selected step until focus lose )
    Editable Entry by Right Click
    Escape to dismiss editing
    Enter to accept editing
'''

d_entry_tristate = dict(
    bg='#383838', readonlybackground='#353535' ,fg='white', relief='raised', justify='center',
    font=('Calibri', 22, 'bold'), insertbackground='white',bd=2,
    disabledbackground='#353535', disabledforeground='white')

d_states = dict(
    label = dict( state='disabled', relief='raised', cursor='arrow', disabledbackground='#383838'),
    edit  = dict( state='normal', relief='groove', cursor='xterm', bg='#444444'),
    select  = dict( state='disabled', relief='sunken', cursor='arrow', disabledbackground='#585858'))

class EntryTriState(Entry):
    # Events
    LEFT_CLICK = 'LEFT_CLICK'
    RIGHT_CLICK = 'RIGHT_CLICK'
    CANCEL = 'CANCEL'
    CHANGED = 'CHANGED'
    
    # States
    LABEL = 'LABEL'
    EDIT = 'EDIT'
    SELECT = 'SELECT'

    def __init__(self, master, _id, text='' ,**kw):
        self.var = StringVar(value=text)
        Entry.__init__(self, master, textvariable=self.var, cnf=d_entry_tristate, **kw)
        self._id = _id
        self.bind('<Button-3>', self.__on_click_right)
        self.set_state(state=EntryTriState.LABEL)
        self.callback = None
        self.__last_text = None

    def set_callback(self,callback):
        ''' event , state , _id '''
        self.callback = callback

    def set_state(self, state):
        if state == EntryTriState.LABEL:
            self.config( **d_states['label'] )
            self.unbind('<FocusOut>')
            self.unbind('<Escape>')
            self.bind_button_1_release_tag = self.bind('<ButtonRelease-1>', self.__on_click_left, add='+')
        elif state == EntryTriState.EDIT:
            self.config( **d_states['edit'] )
            self.bind('<FocusOut>', self.__on_focus_out)
            self.bind('<Escape>', self.__on_key_press_escape)
            self.bind('<Return>', self.__on_key_press_enter)
            if self.bind_button_1_release_tag is not None:
                self.unbind('<ButtonRelease-1>', funcid=self.bind_button_1_release_tag)
                self.bind_button_1_release_tag = None
        elif state == EntryTriState.SELECT:
            self.config( **d_states['select'] )
            self.unbind('<Escape>')
            if self.bind_button_1_release_tag is not None:
                self.unbind('<ButtonRelease-1>', funcid=self.bind_button_1_release_tag)
                self.bind_button_1_release_tag = None

    def invoke(self):
        self.__on_click_left(event=None)

    def right_click(self):
        self.__on_click_right(event=None)

    def get_text(self):
        return self.var.get()

    @property
    def _state(self):
        if self['state'] == 'normal':
            return EntryTriState.EDIT
        elif self['relief'] == 'raised':
            return EntryTriState.LABEL
        else:
            return EntryTriState.SELECT

    def __has_changed(self):
        return self.var.get() != self.__last_text

    def __callback(self,event):
        if self.callback:
            return self.callback(event=event, widget=self)
        return True

    # [ Callbacks ]

    def __on_focus_out(self,event):
        if self._state == EntryTriState.EDIT:
            if self.__has_changed():
                if self.__callback(event=EntryTriState.CHANGED) == False:
                    return
            self.set_state(state=EntryTriState.SELECT)

    def __on_click_left(self,event):
        if self.__callback(event=EntryTriState.LEFT_CLICK) != False:
            self.set_state(state=EntryTriState.SELECT)
            self.focus_force()

    def __on_click_right(self,event):
        if self._state != EntryTriState.EDIT:
            self.__last_text = self.var.get()
            if self.__callback(event=EntryTriState.RIGHT_CLICK) != False:
                self.set_state(state=EntryTriState.EDIT)
                self.focus_set()
                end_idx = len(self.var.get())
                self.select_range(start=0, end=end_idx)
                self.icursor(index=end_idx)
        elif self._root().focus_get() != self:
            self.focus_set()

    def __on_key_press_escape(self,event):
        if self._state == EntryTriState.EDIT:
            self.var.set(self.__last_text)
            if self.__callback(event=EntryTriState.CANCEL) != False:
                self.set_state(state=EntryTriState.SELECT)

    def __on_key_press_enter(self,event):
        if self._state == EntryTriState.EDIT:
            if self.__has_changed():
                if self.__callback(event=EntryTriState.CHANGED) == False:
                    return
            self.set_state(state=EntryTriState.SELECT)

    def set_edit_mode(self):
        self.__on_click_right(event=None)