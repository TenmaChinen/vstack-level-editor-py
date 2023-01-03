from .button_bistate import ButtonBistate
from .buttons import ButtonDelete
from tkinter import Frame


class ItemLevel(Frame):

    CLICK = 'CLICK'
    DELETE = 'DELETE'

    def __init__(self, master, _id, text='', **kw):
        Frame.__init__(self, master=master, **kw)
        self._id = _id
        self.button_bistate = self.__create_button_bistate(_id=_id, text=text)
        self.btn_delete = self.__create_button_delete()
        self.callback = None

    def __create_button_bistate(self, _id, text):
        button_bistate = ButtonBistate(master=self, _id=_id, text=text, width=0)
        button_bistate.pack(side='left', fill='both', expand=True)
        button_bistate.set_callback(callback=self.__on_bistate_event)
        return button_bistate

    def __create_button_delete(self):
        btn_delete = ButtonDelete(master=self, command=self.__on_click_delete)
        btn_delete.pack(side='left')
        return btn_delete

    def set_callback(self, callback):
        self.callback = callback

    def unselect(self):
        self.button_bistate.set_state(state=ButtonBistate.RELEASED)

    def perform_click(self):
        self.button_bistate.invoke()

    # [ Callbacks ]

    def __on_bistate_event(self, _id):
        if self.callback:
            return self.callback(event=self.CLICK, widget=self)

    def __on_click_delete(self):
        if self.callback:
            self.perform_click()
            if self.callback(event=self.DELETE , widget=self) != False:
                self.destroy()