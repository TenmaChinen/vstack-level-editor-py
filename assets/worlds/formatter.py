import json, os

def format_json_file():
    path = os.path.dirname(__file__)
    file = open(f'{path}/worlds.json', 'r')
    data = json.load(file)
    file.close()

    file = open(f'{path}/worlds_fmt.json', 'w')
    string = json.dumps(data)
    string = string.replace('[{','[\n  {\n    ')
    string = string.replace(', "',',\n    "')
    string = string.replace('}, {', '},\n  {\n    ')
    string = string.replace('[[', '[\n       [') # Matrix Start
    string = string.replace('], [', '],\n       [') # Matrix Between
    string = string.replace(']]}', ']\n    ]\n  }') # Matrix End
    string = string.replace('}]', '}\n]') # JSON End
    file.write(string)
    file.close()

if __name__ == '__main__':
    format_json_file();