
class Controller:
    def __init__(self,model,view):
        self.model = model
        self.view = view
    
    def init_defaults(self):
        self.draw_world_item_views()
        self.draw_level_item_views()
        self.select_world(world_index=0)

    def draw_world_item_views(self):
        self.view.clear_world_items()
        self.view.clear_level_items()
        self.view.clear_level_matrix()
        for idx, d_world in enumerate(self.model.l_worlds):
            self.view.create_world_item(idx=idx, name=d_world['name'])

    def draw_level_item_views(self):
        self.view.clear_level_items()
        self.view.clear_level_matrix()
        for idx in range(len(self.model.d_world['levels'])):
            self.view.create_level_item(idx=idx)
    
    def draw_level_matrix_view(self):
        matrix = self.model.get_level_matrix()
        l_speeds = self.model.get_level_speeds()
        color_filter = self.model.get_color_filter()
        
        self.view.load_level_on_canvas_board(
            matrix = matrix, l_speeds=l_speeds,
            color_filter=color_filter,
            l_tiles_img_pil = self.model.l_tint_tiles_img_pil)


    def select_world(self, world_index):
        self.view.select_world_item(world_index=world_index)

    def select_level(self,level_index):
        self.view.select_level_item(level_index=level_index)

# [ CALLBACKS ]

    # [ CLICKS ]
    
    def on_click_board_tile(self, row, col, img_tag):
        tile_idx = self.view.selected_tool_idx
        img_pil = self.model.l_tint_tiles_img_pil[tile_idx]
        self.view.canvas_board.change_tile(img_tag,img_pil)
        self.model.set_matrix_tile(row=row, col=col, tile_id=tile_idx)

    def on_row_speed_change(self, value, row):
        self.model.set_row_speed(row=row, speed=value)

    def on_world_item_click(self, world_index):
        self.model.load_world_data(world_index=world_index)
        self.model.update_tinted_tiles_img_pil()
        self.draw_level_item_views()
        self.select_level(level_index=0)

    def on_level_item_click(self, level_index):
        self.model.load_level_data(level_index=level_index)
        self.draw_level_matrix_view()

    # [ ADDS ]

    def on_add_world(self):
        name = 'New World'
        self.model.create_world(name=name)
        self.view.add_world_item(name=name)
        self.view.select_world_item_edit_mode(world_index=-1)

    def on_add_level(self):
        self.model.create_level()
        self.view.add_level_item()
        self.select_level(level_index=-1)

    def on_add_row(self):
        self.model.add_row()
        self.draw_level_matrix_view()

    def on_sub_row(self):
        self.model.sub_row()
        self.draw_level_matrix_view()

    def on_add_col(self):
        self.model.add_col()
        self.draw_level_matrix_view()

    def on_sub_col(self):
        self.model.sub_col()
        self.draw_level_matrix_view()

    # [ DELETES ]

    def on_world_item_delete(self, world_index):
        self.view.clear_world_items()
        self.model.delete_world(world_index=world_index)
        prev_world_index = max(0, world_index-1)
        self.model.load_world_data(world_index=prev_world_index)
        self.draw_world_item_views()
        self.select_world(world_index=prev_world_index)
        # TODO - PENDING

    def on_level_item_delete(self, level_index):
        self.model.delete_level(level_index=level_index)
        prev_level_index = max(0, level_index-1)
        self.model.load_level_data(level_index=prev_level_index)
        self.draw_level_item_views()
        self.select_level(level_index=prev_level_index)

    # [ EDIT ]

    def on_world_item_edited(self, world_index, world_name):
        self.model.edit_world_name(world_index, world_name)

    def on_color_filter_edited(self, key, value):
        self.model.edit_color_filter(key=key, value=value)
        matrix = self.model.get_level_matrix()
        l_tiles_img_pil = self.model.l_tint_tiles_img_pil
        self.view.update_canvas_board_tiles_color(matrix=matrix, l_tiles_img_pil=l_tiles_img_pil)

    # [ SWAPS ]

    def on_swap_world_items(self, from_index, to_index):
        self.model.swap_worlds(from_index=from_index, to_index=to_index)
        self.draw_world_item_views()
        self.select_world(world_index=to_index)

    def on_swap_level_items(self, from_index, to_index):
        self.model.swap_levels(from_index=from_index, to_index=to_index)
        self.draw_level_item_views()
        self.select_level(level_index=to_index)

    # [ SAVE ]

    def on_save_data(self):
        self.model.update_is_animated_levels()
        self.model.save_data()

    # [ OPEN ]

    def on_open_worlds_file(self):
        self.model.open_format_worlds_file()