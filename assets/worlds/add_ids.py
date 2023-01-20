from string import ascii_uppercase
import json, os, shutil
import random

def save_json(path, data):
    backup_path = f'{path}.bak'
    shutil.copyfile(src=path, dst=backup_path)

    file = open(path, 'w')
    try:
        json.dump(data, file)
        os.remove(backup_path)
        file.close()
    except BaseException as error:
        print('Error :', error)
        file.close()
        os.remove(path)
        os.rename(src=backup_path, dst=path)

def load_json(path):
    file = open(path, 'r')
    data = json.load(file)
    file.close()
    return data


def get_new_id(size):
    # new_id = random.choice(seq=ascii_uppercase)
    return ''.join(random.choices(population=ascii_uppercase, k=size))

def get_world_ids(l_d_worlds):
    return [ d_world.get('id',None) for d_world in l_d_worlds]

l_d_worlds = load_json(path='worlds.json')

# l_world_ids = get_world_ids(l_d_worlds)
l_world_ids = []

for d_world in l_d_worlds:
    # while True:
    #     new_id = get_new_id(size=2)
    #     if new_id not in l_world_ids:
    #         l_world_ids.append(new_id)
    #         d_world['id'] = new_id
    #         break

    # l_lvl_ids = []
    l_levels = d_world['levels']
    for idx in range(len(l_levels)):
        d_level = d_world['levels'][idx]
        _id =d_level.pop('id')
        d_world['levels'][idx] = { 'id':_id, **d_level}
        # else:
            # while True:
            #     new_id = get_new_id(size=1)
            #     if new_id not in l_lvl_ids:
            #         l_lvl_ids.append(new_id)
            #         d_level['id'] = new_id
            #         break

save_json(path='worlds.json', data=l_d_worlds)