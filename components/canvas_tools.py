from PIL import Image, ImageTk
from tkinter import Canvas
import os

W, H = 180, 200

d_cnf = dict(width=W, highlightthickness=0)

TILE_SIZE = W // 2

class CanvasTools(Canvas):

    def __init__(self, master):
        Canvas.__init__(self, master=master, cnf=d_cnf)
        self['bg'] = master['bg']
        self.l_images = self.__create_image_tools()
        self.__create_highlight()
        self.callback = None
        # self.bind('<Configure>', self.__on_canvas_change)

    def __create_image_tools(self):

        file_path = 'assets/tiles'
        row, col = 0, 0
        l_images = []
        l_tiles = 'off on wall broken_off broken_on arrow_left arrow_right'.split(' ')
        for idx, file_name in enumerate(l_tiles):
            img_pil = Image.open(f'{file_path}/{file_name}.png')
            img_pil = img_pil.resize((TILE_SIZE, TILE_SIZE), Image.ANTIALIAS)
            image_tk = ImageTk.PhotoImage(img_pil)

            pos_x, pos_y = col * TILE_SIZE, row * TILE_SIZE
            img_tag = self.create_image(pos_x, pos_y, image=image_tk, anchor = 'nw')
            self.tag_bind(img_tag, '<Button-1>', lambda event, img_tag=img_tag, img_idx=idx: self.__on_click_tool(img_tag, img_idx))

            col = (col + 1) % 2
            if col == 0:
                row += 1

            l_images.append(image_tk)
        return l_images

    def __create_highlight(self):
        x1,y1,x2,y2 = 0,0,TILE_SIZE,TILE_SIZE
        self.tag_highlight = self.create_rectangle( x1,y1,x2,y2, outline='white', width=2)

    def set_callback(self,callback):
        self.callback = callback

    def highlight_tool(self,img_tag):
        x1,y1 = self.coords(img_tag)
        self.coords(self.tag_highlight,(x1,y1,x1+TILE_SIZE, y1+TILE_SIZE))

    def __on_click_tool(self,img_tag, img_idx):
        if self.callback:
            self.callback(img_tag, img_idx)

    def __on_canvas_change(self,event):
        self.config(width=event.width, height=event.height)