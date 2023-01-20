from assets.worlds.formatter import format_json_file
from utils.database_manager import DatabaseManager
import utils.color_filter_manager as cfm
from utils import file_manager
from copy import deepcopy
from PIL import Image

DATA_PATH = 'assets/worlds/worlds.json'


class Model:
    def __init__(self):
        self.d_levels = None
        self.__load_levels()
        self.d_world = self.l_worlds[0]  # DEBUG
        self.d_level = self.d_world['levels'][0]  # DEBUG
        self.__l_red_tiles_img_pil = self.__load_red_tiles_img_pil()
        self.l_tint_tiles_img_pil = deepcopy(self.__l_red_tiles_img_pil)
        self.database_manager = DatabaseManager(l_worlds=self.l_worlds)

    def __load_levels(self):
        self.l_worlds = file_manager.load_json(path=DATA_PATH)

    def __load_red_tiles_img_pil(self):
        file_path = 'assets/tiles'

        l_tiles_img_pil = []
        l_tiles = 'off on wall broken_off broken_on arrow_left arrow_right'.split(' ')
        for idx, file_name in enumerate(l_tiles):

            img_pil = Image.open(f'{file_path}/{file_name}.png')
            l_tiles_img_pil.append(img_pil)
        return l_tiles_img_pil

    def load_world_data(self, world_index):
        if self.l_worlds:
            self.d_world = self.l_worlds[world_index]
            if self.d_world['levels']:
                self.load_level_data(level_index=0)

    def load_level_data(self, level_index):
        if self.d_world['levels']:
            self.d_level = self.d_world['levels'][level_index]

    def save_data(self):
        file_manager.save_json(path=DATA_PATH, data=self.l_worlds)
        format_json_file()

    def update_is_animated_levels(self):
        for d_world in self.l_worlds:
            for d_level in d_world['levels']:
                d_level['isAnimated'] = self.__is_level_animated(d_level['matrix'])

    def update_tinted_tiles_img_pil(self):
        d_color_filter = self.d_world['colorFilter']
        for idx, img_pil in enumerate(self.__l_red_tiles_img_pil):
            if idx == 2: continue
            color_matrix = cfm.create_matrix_identity()
            color_matrix = cfm.adjust_hue(color_matrix=color_matrix, degrees=d_color_filter['hue'])
            color_matrix = cfm.adjust_contrast(color_matrix=color_matrix, value=d_color_filter['contrast'])
            self.l_tint_tiles_img_pil[idx] = img_pil.convert('RGB', matrix=color_matrix)

    def __is_level_animated(self, matrix):
        for row in matrix:
            for tile_id in row:
                if tile_id not in [0, 1, 2]:
                    return True
        return False

    # [ GETTERS ]

    def get_level_matrix(self):
        return self.d_level['matrix']

    def get_level_speeds(self):
        return self.d_level['speeds'][::-1]

    def get_color_filter(self):
        return self.d_world['colorFilter']

    # [ SETTERS ]

    def set_matrix_tile(self, row, col, tile_id):
        self.get_level_matrix()[row][col] = tile_id

    def set_row_speed(self, row, speed):
        last_idx = len(self.d_level['speeds']) - 1
        self.d_level['speeds'][last_idx-row] = speed

    # [ CREATES ]

    def create_world(self, name):
        new_id = self.database_manager.get_new_world_id()
        d_world = dict( id= new_id, name=name, levels=[], colorFilter = dict( hue=0, contrast=0))
        self.l_worlds.append(d_world)

    def create_level(self):
        new_id = self.database_manager.get_new_level_id(self.d_world)
        d_level = dict(
            id=new_id, speeds=[1, 2, 3, 4, 5, 7, 9, 11, 14, 16, 18, 20],
            isAnimated=False, matrix=[[0 for c in range(5)] for r in range(12)])
        self.d_world['levels'].append(d_level)

    def add_row(self):
        top_row = self.d_level['matrix'][0].copy()
        self.d_level['matrix'].insert(0, top_row)
        self.add_speed()

    def sub_row(self):
        self.d_level['matrix'].pop(0)
        self.sub_speed()

    def add_col(self):
        rows = len(self.d_level['matrix'])
        for idx in range(rows):
            self.d_level['matrix'][idx].append(0)

    def sub_col(self):
        rows = len(self.d_level['matrix'])
        for idx in range(rows):
            self.d_level['matrix'][idx].pop(-1)

    def add_speed(self):
        self.d_level['speeds'].append(1)

    def sub_speed(self):
        self.d_level['speeds'].pop(-1)

    # [ DELETES ]

    def delete_world(self, world_index):
        self.l_worlds.pop(world_index)

    def delete_level(self, level_index):
        self.d_world['levels'].pop(level_index)

    # [ EDITS ]

    def edit_world_name(self, world_index, world_name):
        self.l_worlds[world_index]['name'] = world_name

    def edit_color_filter(self, key, value):
        self.d_world['colorFilter'][key] = value
        self.update_tinted_tiles_img_pil()
            
    # [ SWAPS ]

    def swap_worlds(self, from_index, to_index):
        index_1, index_2 = sorted([from_index, to_index])
        d_world_2 = self.l_worlds.pop(index_2)
        d_world_1 = self.l_worlds.pop(index_1)
        self.l_worlds.insert(index_1, d_world_2)
        self.l_worlds.insert(index_2, d_world_1)

    def swap_levels(self, from_index, to_index):
        index_1, index_2 = sorted([from_index, to_index])
        d_level_2 = self.d_world['levels'].pop(index_2)
        d_level_1 = self.d_world['levels'].pop(index_1)
        self.d_world['levels'].insert(index_1, d_level_2)
        self.d_world['levels'].insert(index_2, d_level_1)