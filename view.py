from components.frame_scroll_drag import FrameScrollDrag
from components.dialog_tri_option import DialogTriOption
from components.dialog_confirm import DialogConfirm
from components.input_integer import InputInteger
from components.canvas_tools import CanvasTools
from components.canvas_board import CanvasBoard
from components.item_world import ItemWorld
from components.item_level import ItemLevel
from components.buttons import ButtonBase
from components.labels import LabelTitle
from tkinter import Tk, Frame, Canvas
from components.toast import Toast


class View:
    def __init__(self, title):
        self.controller = None
        self.root = self.__create_root(title)

        self.frame_tools = self.__create_frame_tools()
        self.canvas_tools = self.__create_canvas_tools()
        self.canvas_board = self.__create_canvas_board()
        self.fr_scroll_drag_worlds = self.__create_frame_worlds()
        self.fr_scroll_drag_levels = self.__create_frame_levels()
        self.dialog_confirm = self.__create_dialog_confirm()
        self.dialog_tri_option = self.__create_dialog_tri_option()
        self.toast = self.__create_toast()
        
        self.selected_tool_idx = 0
        self.has_changes = False

    def __create_root(self, title):
        root = Tk()
        # root.geometry('800x600+50+10')
        root.geometry('+200+80')
        root.iconbitmap('assets/icon.ico')
        root.title(title)
        root.config(bg='#393333')
        root.resizable(False, False)
        root.protocol('WM_DELETE_WINDOW', self.__on_root_close)
        root.bind_all('<Control-q>', lambda e: self.__on_root_close())
        root.bind_all('<Control-s>', lambda e: self.__on_key_press_save_shortcut())
        return root

    def set_controller(self, controller):
        self.controller = controller

    def __create_frame_tools(self):
        frame_tools = Frame(master=self.root, bg='#593E3E')
        frame_tools.pack(side='left', fill='y')
        return frame_tools

    def __create_canvas_tools(self):
        canvas_tools = CanvasTools(master=self.frame_tools)
        canvas_tools.pack(side='top', fill='y', expand=True)
        # canvas_tools.pack(side='top', fill='both', expand=True)
        canvas_tools.set_callback(callback=self.__on_select_tool)

        input_integer_rows = InputInteger(master=self.frame_tools, _range=(3,20), text='ROWS')
        input_integer_rows.set_callback(callback=self.__on_input_integer_rows_event)
        input_integer_rows.pack(side='top', fill='x')
        self.input_integer_rows=input_integer_rows

        input_integer_cols = InputInteger(master=self.frame_tools, _range=(3,20), text='COLS')
        input_integer_cols.set_callback(callback=self.__on_input_integer_cols_event)
        input_integer_cols.pack(side='top', fill='x')
        self.input_integer_cols=input_integer_cols

        return canvas_tools

    def __create_canvas_board(self):
        canvas_board = CanvasBoard(master=self.root)
        canvas_board.pack(side='left', fill='y')
        canvas_board.set_callbacks(
            on_click_tile=self.__on_click_board_tile,
            on_row_speed_change=self.__on_row_speed_change)
        return canvas_board

    def __create_frame_worlds(self):
        fr_worlds = Frame(self.root, width=250)
        fr_worlds.pack_propagate(False)
        fr_worlds.pack(side='left', fill='y')

        label_title = LabelTitle(master=fr_worlds, text='WORLDS')
        label_title.pack(side='top', fill='x')

        fr_scroll_drag_worlds = FrameScrollDrag(master=fr_worlds, bg='#632C2C')
        fr_scroll_drag_worlds.set_callbacks(
            on_swap_items=self.__on_item_world_swap,
            on_item_event=self.__on_item_world_event
            )
        fr_scroll_drag_worlds.set_bg(bg='#632C2C')
        fr_scroll_drag_worlds.pack(side='top', fill='y', expand=True)

        btn_add_world = ButtonBase(master=fr_worlds, text='ADD WORLD', command=self.__on_click_add_world)
        btn_add_world.pack(side='top', fill='x')

        return fr_scroll_drag_worlds

    def __create_frame_levels(self):
        fr_levels = Frame(self.root, width=250)
        fr_levels.pack_propagate(False)
        fr_levels.pack(side='left', fill='y')

        label_title = LabelTitle(master=fr_levels, text='LEVELS')
        label_title.pack(side='top', fill='x')

        fr_scroll_drag_levels = FrameScrollDrag(master=fr_levels)
        fr_scroll_drag_levels.set_callbacks(
            on_swap_items=self.__on_item_level_swap,
            on_item_event=self.__on_item_level_event
            )
        fr_scroll_drag_levels.set_bg(bg='#632C2C')
        fr_scroll_drag_levels.pack(side='top', fill='y', expand=True)

        btn_add_level = ButtonBase(master=fr_levels, text='ADD LEVEL', command=self.__on_click_add_level)
        btn_add_level.pack(side='top', fill='x')

        return fr_scroll_drag_levels

    def __create_dialog_confirm(self):
        dialog_confirm = DialogConfirm(master=self.root)
        dialog_confirm.set_title(title='Delete')
        return dialog_confirm

    def __create_dialog_tri_option(self):
        dialog_tri_option = DialogTriOption(master=self.root, width=300)
        dialog_tri_option.set_title(title='Save Changes ?')
        dialog_tri_option.set_message(message='Data hass been modified, save changes?')
        return dialog_tri_option

    def __create_toast(self):
        toast = Toast(master=self.root)
        toast.set_message(message='Saving Data')
        return toast

    # [ Methods ]

    def load_level_on_canvas_board(self, matrix, l_speeds, l_tiles_img_pil):
        self.canvas_board.create_level(matrix, l_tiles_img_pil)
        self.canvas_board.create_speeds(l_speeds)
        self.input_integer_rows.set_value(value=len(matrix))
        self.input_integer_cols.set_value(value=len(matrix[0]))

    def create_world_item(self, idx, name):
        item_world = self.fr_scroll_drag_worlds.add_item(ItemClass=ItemWorld, child_idx=0, _id=idx, text=name)
        self.fr_scroll_drag_worlds.update_shadow_item()

    def create_level_item(self,idx):
        item_level = self.fr_scroll_drag_levels.add_item(ItemClass=ItemLevel, child_idx=0, _id=idx, text=f'Level {idx+1:02d}')
        self.fr_scroll_drag_levels.update_shadow_item()

    def add_world_item(self, name):
        last_index = self.fr_scroll_drag_worlds.get_last_index()
        self.create_world_item(idx=last_index, name=name)

    def add_level_item(self):
        last_index = self.fr_scroll_drag_levels.get_last_index()
        self.create_level_item(idx=last_index)

    def get_selected_tool(self):
        return self.selected_tool

    def clear_world_items(self):
        self.fr_scroll_drag_worlds.remove_all_children()

    def clear_level_items(self):
        self.fr_scroll_drag_levels.remove_all_children()

    def clear_level_matrix(self):
        self.canvas_board.clear_board()

    def select_world_item(self, world_index):
        self.fr_scroll_drag_worlds.select_item(child_index=world_index)

    def select_level_item(self, level_index):
        self.fr_scroll_drag_levels.select_item(child_index=level_index)

    # [ Callbacks ]

    def __on_select_tool(self, img_tag, img_idx):
        self.selected_tool_idx = img_idx
        self.canvas_tools.highlight_tool(img_tag)

    def __on_input_integer_rows_event(self, event):
        if event == InputInteger.ADD:
            self.controller.on_add_row()
        elif event == InputInteger.SUB:
            self.controller.on_sub_row()

        self.has_changes = True

    def __on_input_integer_cols_event(self, event):
        if event == InputInteger.ADD:
            self.controller.on_add_col()
        elif event == InputInteger.SUB:
            self.controller.on_sub_col()

        self.has_changes = True

    def __on_click_board_tile(self, row, col, img_tag):
        self.controller.on_click_board_tile(row=row, col=col, img_tag=img_tag)
        self.has_changes = True

    def __on_row_speed_change(self, value, row):
        self.controller.on_row_speed_change(value=value, row=row)
        self.has_changes = True

    def __on_item_world_event(self, event, _id, is_different):
        if is_different and event != ItemWorld.CHANGED:
            self.controller.on_world_item_click(world_index=_id)

        if event == ItemWorld.DELETE:
            if self.dialog_confirm.show(message=f'Do you want to delete world {_id:02d}'):
                self.controller.on_world_item_delete(world_index=_id)
                self.has_changes = True
            else:
                return False

        elif event == ItemWorld.CHANGED:
            self.controller.on_world_item_edited(world_index=_id)
            self.has_changes = True

    def __on_item_level_event(self, event, _id, is_different):
        if event == ItemLevel.CLICK:
            self.controller.on_level_item_click(level_index=_id)
        elif event == ItemLevel.DELETE:
            self.controller.on_level_item_click(level_index=_id)
            if self.dialog_confirm.show(message=f'Do you want to delete level {_id:02d}'):
                self.controller.on_level_item_delete(level_index=_id)
                self.has_changes = True
                return True
            return False

    # [ SWAPS ]

    def __on_item_world_swap(self, from_index, to_index):
        self.controller.on_swap_world_items(from_index, to_index)
        self.has_changes = True

    def __on_item_level_swap(self, from_index, to_index):
        self.controller.on_swap_level_items(from_index, to_index)
        self.has_changes = True

    # [ ADDS ]

    def __on_click_add_world(self):
        self.controller.on_add_world()
        self.has_changes = True

    def __on_click_add_level(self):
        self.controller.on_add_level()
        self.has_changes = True

    # [ ROOT ]

    def __on_key_press_save_shortcut(self):
        if self.has_changes:
            self.controller.on_save_data()
            self.toast.show()
            self.has_changes = False

    def __on_root_close(self):
        if self.has_changes:
            response = self.dialog_tri_option.show()
            if response == DialogTriOption.YES:
                self.controller.on_save_data()
                self.root.destroy()
            elif response == DialogTriOption.NO:
                self.root.destroy()
            else:
                pass
        else:
            self.root.destroy()
