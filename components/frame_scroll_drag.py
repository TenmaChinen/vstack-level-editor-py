from tkinter import Tk, Frame, Canvas, Label, Scrollbar, Button


class FrameScrollDrag(Frame):
    def __init__(self, master, cnf={}, **kw):
        Frame.__init__(self, master, cnf=cnf, **kw)
        self.canvas = self.__create_canvas()
        self.scrollbar = self.__create_scrollbar()
        self.frame = self.__create_frame()
        self.canvas.pack(side='left', fill='both', expand=True)
        self.__setup_listeners()
        self.shadow_item = self.__create_shadow_item()
        
        self.on_swap_items = None
        self.on_item_event = None

        self.selected_item = None

        if 'width' in kw or 'height' in kw:
            self.pack_propagate(False)
            self.grid_propagate(False)
        

    def __create_canvas(self):
        canvas = Canvas(master=self, bg='red')
        canvas.config(highlightthickness=0)
        # canvas.pack_propagate(flag=False)
        return canvas

    def __create_scrollbar(self):
        scrollbar = Scrollbar(self, orient='vertical',command=self.canvas.yview)
        scrollbar.pack(side='right', fill='y')
        return scrollbar

    def __create_frame(self):
        frame = Frame(self.canvas, bg='darkblue')
        frame.cid = self.canvas.create_window((0, 0), window=frame, anchor='nw')
        return frame

    def __setup_listeners(self):
        self.frame.bind('<Configure>', self.__on_frame_scroll_change)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', self.__on_canvas_size_change)
        self.canvas.bind_all('<MouseWheel>', self.__on_scroll_mouse)

    def __repack(self, l_widgets):
        for widget in l_widgets:
            widget.pack_forget()
            widget.pack(side='top', fill='x')
    
    def __create_shadow_item(self):
        shadow_item = Frame(master=self.frame, height=50, bg=self.frame['bg'])
        return shadow_item

    # [ Callbacks ]
    def __on_canvas_size_change(self,event):
        self.canvas.itemconfig(self.frame.cid, width=event.width)

    def __on_frame_scroll_change(self, event):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        l_canvas_bbox = list(self.canvas.bbox('all'))

        if event.height < canvas_height:
            l_canvas_bbox[3] = canvas_height
        
        self.canvas.configure(scrollregion=l_canvas_bbox)

    def __on_scroll_mouse(self, event):
        self.canvas.yview_scroll(- 1 * int(event.delta / 120), 'units')

    def __on_start(self, event, widget):
        widget.start_y = event.y

        l_slaves = self.frame.pack_slaves()
        index = l_slaves.index(widget)
        self.start_index = index

        widget.place(x=0, y=widget.winfo_y(), anchor='nw', relwidth=1)
        widget.lift()

        l_slaves.pop(index)
        l_slaves.insert(index, self.shadow_item)

        self.__repack(l_widgets=l_slaves)


    def __on_moving(self, event, widget):

        y = widget.winfo_y()
        dy = event.y - widget.start_y
        widget.place(x=0, y=y + dy)

        # SHIFT LEFT
        if y <= (self.shadow_item.winfo_y() - self.shadow_item.winfo_height()):

            l_slaves = self.frame.pack_slaves()
            old_index = l_slaves.index(self.shadow_item)
            new_index = old_index - 1

            if new_index >= 0:
                l_slaves.insert(new_index, self.shadow_item)
                l_slaves.pop(old_index + 1)

                self.__repack(l_widgets=l_slaves)

        # SHIFT RIGHT
        elif y >= (self.shadow_item.winfo_y() + self.shadow_item.winfo_height()):

            l_slaves = self.frame.pack_slaves()
            old_index = l_slaves.index(self.shadow_item)
            new_index = old_index + 1
            l_slaves.pop(old_index)
            l_slaves.insert(new_index, self.shadow_item)

            if new_index < len(l_slaves):
                self.__repack(l_widgets=l_slaves)


    def __on_release(self, event, widget):
        l_slaves = self.frame.pack_slaves()
        index = l_slaves.index(self.shadow_item)
        l_slaves.insert(index, widget)
        l_slaves.remove(self.shadow_item)
        self.shadow_item.pack_forget()
        self.__repack(l_widgets=l_slaves)

        if self.start_index != index:
            if self.on_swap_items:
                self.on_swap_items(from_index = self.start_index, to_index = index)

    def __on_item_event(self,event, widget):
        if self.on_item_event:
            is_different = widget != self.selected_item
            if self.selected_item and is_different:
                self.selected_item.unselect()
            self.selected_item = widget
            return self.on_item_event(event=event, _id=widget._id, is_different=is_different)

    # [ Methods ]

    def set_callbacks(self, on_swap_items, on_item_event):
        self.on_swap_items = on_swap_items
        self.on_item_event = on_item_event

    def set_bg(self,bg):
        self.canvas['bg'] = bg
        self.frame['bg'] = bg
        self.shadow_item['bg'] = bg

    def remove_all_children(self):
        for child in self.frame.winfo_children():
            if child != self.shadow_item:
                child.destroy()
        self.selected_item = None

    def get_children(self):
        return self.frame.pack_slaves()

    def get_last_index(self):
        return len(self.get_children()) - 1

    def select_item(self, child_index):
        l_children = self.get_children()
        if l_children:
            child = l_children[child_index]
            child.perform_click()

    def add_item(self,ItemClass, child_idx=None, **kw):
        item = ItemClass(master=self.frame, **kw)
        item.set_callback(self.__on_item_event)
        item.pack(side='top', fill='x')
        
        child = item.winfo_children()[child_idx] if child_idx is not None else item
        child.bind('<Button-1>', lambda e, w=item: self.__on_start(event=e, widget=w))
        child.bind('<B1-Motion>', lambda e, w=item: self.__on_moving(event=e, widget=w))
        child.bind('<ButtonRelease-1>', lambda e, w=item: self.__on_release(event=e, widget=w), add='+')

        return item

    def update_shadow_item(self):
        self.frame.update()
        max_height = max( [ slave.winfo_height() for slave in self.frame.pack_slaves()] )
        self.shadow_item.config(height=max_height)
