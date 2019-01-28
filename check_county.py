import operator
import xlrd
import math
import json

with open("neighbor_map.json", 'r', encoding='utf-8') as json_file:
    neighbor_map = json.load(json_file)

in_file = xlrd.open_workbook('MCM_NFLIS_Data_pro.xlsx')  # 打开Excel文件
sheet = in_file.sheet_by_index(1)  # 根据sheet页的排序选取sheet
row_number = sheet.nrows  # 获取有数据的最大行数
col_number = sheet.ncols  # 获取有数据的最大列数

out_file = open('regression-year/aim_county1.csv', 'w', encoding='utf8')
out_file.write('state,county\n')
states = ['VA', 'KY', 'OH', 'PA', 'WV']
for state in states:
    print(state)
    for county, neighbors in neighbor_map[state].items():
        print(county)
        flag = True
        for year in range(2010, 2018):
            for neighbor in neighbors:
                aim_num = 0
                for i in range(row_number):
                    if i == 0:
                        continue
                    line = sheet.row_values(i)  # 获取指定行的数据，返回列表，排序自0开始
                    if year == line[0] and state == line[1] and county == line[2]:
                        aim_num = int(line[8])
                for i in range(row_number):
                    if i == 0:
                        continue
                    line = sheet.row_values(i)  # 获取指定行的数据，返回列表，排序自0开始
                    if year == line[0] and state == line[1] and county == neighbor:
                        if aim_num < 2 * int(line[8]):
                            flag = False
                            break
                if not flag:
                    break
            if not flag:
                break
        if flag:
            out_file.write(state + ',' + county + '\n')
out_file.close()
