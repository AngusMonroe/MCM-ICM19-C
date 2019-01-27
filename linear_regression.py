import json

neighbor_map = {} #存放读取的数据
with open("neighbor_map.json", 'r', encoding='utf-8') as json_file:
        model = json.load(json_file)

