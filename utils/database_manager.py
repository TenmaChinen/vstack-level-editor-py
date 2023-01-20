from string import ascii_uppercase
from random import choice, choices

class DatabaseManager:

    def __init__(self, l_worlds):
        self.l_worlds = l_worlds


    def get_new_world_id(self):
        l_worlds_id = self.__get_worlds_id()
        while True:
            new_id = ''.join(choices(population=ascii_uppercase, k=2))
            if new_id not in l_worlds_id:
                return new_id

    def get_new_level_id(self,d_world):
        l_levels = d_world['levels']
        l_levels_id = self.__get_world_levels_id(l_levels)
        while True:
            new_id = choice(ascii_uppercase)
            if new_id not in l_levels_id:
                return new_id

    def __get_worlds_id(self):
        return [ d_world['id'] for d_world in self.l_worlds]

    def __get_world_levels_id(self, l_levels):
        return [ d_level['id'] for d_level in l_levels]