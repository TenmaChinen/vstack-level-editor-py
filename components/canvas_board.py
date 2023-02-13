from components.entry_integer import EntryInteger
from tkinter import Canvas, Label
from PIL import Image, ImageTk
import os

W, H = 500, 600
d_cnf = dict(bg='#7F4747', width=W, height=H, highlightthickness=0)


class CanvasBoard(Canvas):
    def __init__(self, master):
        Canvas.__init__(self, master=master, cnf=d_cnf)
        self.tile_size = None
        self.d_images_tk = None

        self.__last_row_col = [None, None]

        self.on_click_tile = None
        self.on_speed_change = None

        self.__set_binding()

    def __set_binding(self):
        self.bind('<Button-1>', self.__on_click_left)
        self.bind('<B1-Motion>', self.__on_click_left_motion)

    def create_level(self, matrix, l_tiles_img_pil):

        rows, cols = len(matrix), len(matrix[0])
        l_rows_cols = [[r, c] for r in range(rows) for c in range(cols)]

        x_margin, y_margin = 50, 50
        tile_size_1 = (W - 2 * x_margin ) // ( cols + 1 )
        tile_size_2 = (H - 2 * y_margin) // rows

        if tile_size_1 < tile_size_2:
            tile_size = tile_size_1
            y_margin = (H - tile_size * rows)//2
        else:
            tile_size = tile_size_2
            x_margin = (W - tile_size * ( cols + 1 ) )//2

        self.tile_size = tile_size
        self.x_margin = x_margin
        self.y_margin = y_margin
        self.rows = rows
        self.cols = cols

        d_images_tk = {}
        d_img_row_col = {}

        for row, col in l_rows_cols:
            tile_idx = matrix[row][col]
            img_pil = l_tiles_img_pil[tile_idx]
            img_pil = img_pil.resize((tile_size, tile_size), Image.ANTIALIAS)
            image_tk = ImageTk.PhotoImage(img_pil)

            pos_x = x_margin + col * tile_size
            pos_y = y_margin + row * tile_size

            img_tag = self.create_image(pos_x, pos_y, image=image_tk, anchor='nw')
            d_img_row_col[img_tag] = [row,col]
            d_images_tk[img_tag] = image_tk

        self.d_img_row_col = d_img_row_col
        self.d_images_tk = d_images_tk

    def set_callbacks(self, on_click_tile, on_row_speed_change):
        self.on_click_tile = on_click_tile
        self.on_row_speed_change = on_row_speed_change

    def change_tile(self, img_tag, img_pil):
        img_pil = img_pil.resize(
            (self.tile_size, self.tile_size), Image.ANTIALIAS)
        img_tk = ImageTk.PhotoImage(img_pil)
        self.d_images_tk[img_tag] = img_tk
        self.itemconfig(img_tag, image=img_tk)

    def clear_board(self):
        if self.d_images_tk:
            self.d_images_tk.clear()
        self.clear_speeds()

    def create_speeds(self, l_speeds):
        self.clear_speeds()

        pos_x = self.x_margin + (self.cols * 1) * self.tile_size
        font_size = self.tile_size // 2
        for row, speed in enumerate(l_speeds):
            pos_y = self.y_margin + row * self.tile_size
            entry_integer = EntryInteger(master=self, _id=row, value=int(speed), _range=(1,20) , size=font_size)
            entry_integer.set_callback(on_change=self.__on_row_speed_change)
            entry_integer.place(x=pos_x, y=pos_y, anchor='nw', height=self.tile_size, width=self.tile_size)

    def clear_speeds(self):
        for child in self.place_slaves():
            child.destroy()

    # [ Callbacks ]

    def __on_click_left(self, event):
        if self.on_click_tile:
            img_tag = self.find_closest(x=event.x, y=event.y)[0]
            if img_tag in self.d_img_row_col:
                row, col = self.d_img_row_col[img_tag]
                self.__last_row_col = [row,col]
                self.on_click_tile(row=row, col=col, img_tag=img_tag)

    def __on_click_left_motion(self, event):
        if self.on_click_tile:
            img_tag = self.find_closest(x=event.x, y=event.y)[0]
            if img_tag in self.d_img_row_col:
                row, col = self.d_img_row_col[img_tag]
                if self.__last_row_col != [row,col]:
                    self.__last_row_col = [row,col]
                    self.on_click_tile(row=row, col=col, img_tag=img_tag)

    # def __on_click_tile(self, row, col, img_tag):
    #     if self.on_click_tile:
    #         self.__last_row_col = [row,col]
    #         self.on_click_tile(row=row, col=col, img_tag=img_tag)

    def __on_row_speed_change(self, value, _id):
        if self.on_row_speed_change:
            self.on_row_speed_change(value=value, row=_id)
