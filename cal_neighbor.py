import xlrd
import math
import json

in_file = xlrd.open_workbook('MCM_NFLIS_Data_pro.xlsx')  # 打开Excel文件
sheet = in_file.sheet_by_index(2)  # 根据sheet页的排序选取sheet
row_number = sheet.nrows  # 获取有数据的最大行数
col_number = sheet.ncols  # 获取有数据的最大列数

states = ['VA', 'KY', 'OH', 'PA', 'WV']
neighbor_map = {}
radius = 0.53 * 1.5
sum = 0
num = 0
for state in states:
    file = open('position/' + state + '.txt', 'r', encoding='utf8')
    txt = file.readlines()
    counties = {}
    for county in txt:
        county_info = county[:-1].split(',')
        neighbor = []
        for i in txt:
            info = i[:-1].split(',')
            if county_info[0] != info[0] and abs(float(county_info[1]) - float(info[1])) <= radius \
                    and abs(float(county_info[2]) - float(info[2])) <= radius:
                neighbor.append(info[0])
        sum += len(neighbor)
        num += 1
        counties.update({county_info[0]: neighbor})
    neighbor_map.update({state: counties})
    file.close()
with open("neighbor_map1.5.json", 'w', encoding='utf-8') as json_file:
    json.dump(neighbor_map, json_file, ensure_ascii=False)
print(float(sum / num))
