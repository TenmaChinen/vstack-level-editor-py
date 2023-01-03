from .entry_tristate import EntryTriState
from .buttons import ButtonDelete
from tkinter import Frame


class ItemWorld(Frame):

    LEFT_CLICK = 'LEFT_CLICK'
    RIGHT_CLICK = 'RIGHT_CLICK'
    FOCUS_OUT = 'FOCUS_OUT'
    CHANGED = 'CHANGED'
    CANCEL = 'CANCEL'
    DELETE = 'DELETE'

    def __init__(self, master, _id, text='', **kw):
        self._id = _id
        Frame.__init__(self, master=master, **kw)
        self.entry_tristate = self.__create_entry_tristate(_id,text)
        self.btn_delete = self.__create_button_delete()
        self.callback = None

    def __create_entry_tristate(self, _id, text):
        entry_tristate = EntryTriState(master=self, _id=_id, text=text, width=0)
        entry_tristate.pack(side='left', fill='both', expand=True)
        entry_tristate.set_callback(callback=self.__on_tristate_event)
        return entry_tristate

    def __create_button_delete(self):
        btn_delete = ButtonDelete(master=self, command=self.__on_click_delete)
        btn_delete.pack(side='left')
        return btn_delete

    def set_callback(self, callback):
        self.callback = callback

    def perform_click(self):
        self.entry_tristate.invoke()

    def unselect(self):
        self.entry_tristate.set_state(state=EntryTriState.LABEL)

    # [ Callbacks ]

    def __on_tristate_event(self,event, widget):
        if self.callback:
            return self.callback(event=event, widget=self)

    def __on_click_delete(self):
        if self.callback:
            self.perform_click()
            if self.callback(event=self.DELETE , widget=self) != False:
                self.destroy()