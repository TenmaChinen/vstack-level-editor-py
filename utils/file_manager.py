import os, shutil, json

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
