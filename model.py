from PIL import Image
import json
import os

class Model:
    def __init__(self):
        self.d_levels = None
        self.__load_levels()
        self.d_world = self.l_worlds[0] # DEBUG
        self.d_level = self.d_world['levels'][0] # DEBUG
        self.l_tiles_img_pil = self.__load_tiles_img_pil()

    def __load_levels(self):
        self.l_worlds = load_json(path='assets/levels/levels.json')

    def __load_tiles_img_pil(self):
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
        self.d_level = self.d_world['levels'][level_index]

    def save_data(self):
        print('MODEL : SAVE DATA')

    # [ GETTERS ]

    def get_level_matrix(self):
        return self.d_level['matrix']

    def get_level_speeds(self):
        return self.d_level['speeds'][::-1]

    # [ SETTERS ]

    def set_matrix_tile(self,row,col,tile_id):
        self.get_level_matrix()[row][col] = tile_id

    def set_row_speed(self,row,speed):
        last_idx = len(self.d_level['speeds']) - 1
        self.d_level['speeds'][last_idx-row] = speed 

    # [ CREATES ]

    def create_world(self, name):
        d_world = dict( name = name, levels = [] )
        self.l_worlds.append(d_world)

    def create_level(self):
        d_level = dict( speeds= [1,2,3], isAnimated=False, matrix = [[0,0,0],[0,0,0],[0,0,0]] )
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
        # TODO : Update File

    def delete_level(self, level_index):
        self.d_world['levels'].pop(level_index)
        # TODO : Update File

    # [ SWAPS ]

    def swap_worlds(self, from_index, to_index):
        index_1, index_2 = sorted([from_index,to_index])
        d_world_2 = self.l_worlds.pop(index_2)
        d_world_1 = self.l_worlds.pop(index_1)
        self.l_worlds.insert(index_1, d_world_2 )
        self.l_worlds.insert(index_2, d_world_1 )
        # TODO : Update File

    def swap_levels(self, from_index, to_index):
        index_1, index_2 = sorted([from_index,to_index])
        d_level_2 = self.d_world['levels'].pop(index_2)
        d_level_1 = self.d_world['levels'].pop(index_1)
        self.d_world['levels'].insert(index_1, d_level_2 )
        self.d_world['levels'].insert(index_2, d_level_1 )
        # TODO : Save Changes to File


def save_json(path,data):
    file = open(path,'w')
    json.dump(file, path)
    file.close()

def load_json(path):
    file = open(path,'r')
    data = json.load(file)
    file.close()
    return data