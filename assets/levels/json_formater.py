import json
import re

file = open('levels.json', 'r')
data = json.load(file)
file.close()

file = open('levels_fmt.json', 'w')
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
