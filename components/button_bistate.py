from tkinter import Button

d_button_cnf = dict(
    bg='#363636', fg='white', font='Calibri 16 bold', bd=1,
    activebackground='#585858', activeforeground='#EEEDED')


class States:
    ACTIVE = 'ACTIVE'
    RELEASED = 'RELEASED'

class Events:
    CLICK = 'CLICK'

d_states = {
    States.ACTIVE : dict(relief='sunken', bg=d_button_cnf['activebackground']),
    States.RELEASED : dict(relief='raised', bg=d_button_cnf['bg'])}


class ButtonBistate(Button, States, Events):

    def __init__(self, master, _id, **kw):
        Button.__init__(self, master=master, cnf=d_button_cnf, **kw)
        self._id = _id
        self.callback = None
        self['command'] = self.__on_click

    def set_callback(self, callback):
        self.callback = callback

    def set_state(self, state):
        self.config( **d_states[state] )

    @property
    def _state(self):
        return States.ACTIVE if self['relief'] == 'sunken' else States.RELEASED

    # [ Callbacks ]

    def __on_click(self):
        if self._state == States.RELEASED:
            if self.callback:
                if self.callback(_id=self._id) == False:
                    return
            self.set_state(state=States.ACTIVE)
            self.focus_force()