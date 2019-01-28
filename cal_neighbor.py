import xlrd
import math
import json

states = ['VA', 'KY', 'OH', 'PA', 'WV']
neighbor_map = {}
radius = 0.53
sum = 0
num = 0
for state in states:
    file = open('position/' + state + '.txt', 'r', encoding='utf8')
    txt = file.readlines()
    counties = {}
    for county in txt:
        county_info = county[:-1].split(',')
        neighbor = []
        # flag = False
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
# with open("neighbor_map.json", 'w', encoding='utf-8') as json_file:
#     json.dump(neighbor_map, json_file, ensure_ascii=False)
print(float(sum / num))

in_file = xlrd.open_workbook('MCM_NFLIS_Data_pro.xlsx')  # 打开Excel文件
sheet = in_file.sheet_by_index(7)  # 根据sheet页的排序选取sheet
row_number = sheet.nrows  # 获取有数据的最大行数
col_number = sheet.ncols  # 获取有数据的最大列数


def check(a, b):
    if not a:
        a = 0
    if not b:
        b = 0
    return a, b

for year in range(2010, 2018):
    print(year)
    for state in states:
        file = open('regression-year/' + str(year) + '/' + str(year) + '-' + state + '.csv', 'w', encoding='utf8')
        file.write(',o_basic,h_basic,o_neighbor,h_neighbor,aim_o,aim_h\n')
        line_num = 1
        for county, neighbor in neighbor_map[state].items():
            string = ''
            flag = False
            for i in range(row_number):
                if i == 0:
                    continue
                line = sheet.row_values(i)  # 获取指定行的数据，返回列表，排序自0开始
                if year == line[0] and state == line[1] and county == line[2]:
                    line[3], line[4] = check(line[3], line[4])
                    string += str(line_num) + ',' + str(line[3]) + ',' + str(line[4])
                    # file.write(str(line_num) + ',' + str(line[3]) + ',' + str(line[4]))
                    flag = True
                    break
            if not flag:
                continue
            o = 0
            h = 0
            for name in neighbor:
                for i in range(row_number):
                    if i == 0:
                        continue
                    line = sheet.row_values(i)  # 获取指定行的数据，返回列表，排序自0开始
                    if year == line[0] and state == line[1] and name == line[2]:
                        line[3], line[4] = check(line[3], line[4])
                        o += line[4]
                        h += line[3]
                        break
            string += ',' + str(o) + ',' + str(h)
            # file.write(',' + str(o) + ',' + str(h))
            flag = False
            for i in range(row_number):
                if i == 0:
                    continue
                line = sheet.row_values(i)  # 获取指定行的数据，返回列表，排序自0开始
                if year + 1 == line[0] and state == line[1] and county == line[2]:
                    line[3], line[4] = check(line[3], line[4])
                    # file.write(',' + str(line[3]) + ',' + str(line[4]) + '\n')
                    flag = True
                    break
            if not flag:
                continue
            string += ',' + str(line[3]) + ',' + str(line[4]) + '\n'
            line_num += 1
            file.write(string)
        file.close()

# for state in states:
#     print(neighbor_map[state])
#     for county, neighbor in neighbor_map[state].items():
#         file = open('regression/' + state + '/' + state + '-' + county + '.txt', 'w', encoding='utf8')
#         file.write(',o_basic,h_basic,o_neighbor,h_neighbor,aim_o,aim_h\n')
#         for year in range(2010, 2017):
#             for i in range(row_number):
#                 if i == 0:
#                     continue
#                 line = sheet.row_values(i)  # 获取指定行的数据，返回列表，排序自0开始
#                 if year == line[0] and state == line[1] and county == line[2]:
#                     line[3], line[4] = check(line[3], line[4])
#                     file.write(str(year - 2009) + ',' + str(line[3]) + ',' + str(line[4]))
#                     break
#             o = 0
#             h = 0
#             for name in neighbor:
#                 for i in range(row_number):
#                     if i == 0:
#                         continue
#                     line = sheet.row_values(i)  # 获取指定行的数据，返回列表，排序自0开始
#                     if year == line[0] and state == line[1] and name == line[2]:
#                         line[3], line[4] = check(line[3], line[4])
#                         o += line[3]
#                         h += line[4]
#                         break
#             file.write(',' + str(o) + ',' + str(h))
#
#             for i in range(row_number):
#                 if i == 0:
#                     continue
#                 line = sheet.row_values(i)  # 获取指定行的数据，返回列表，排序自0开始
#                 if year + 1 == line[0] and state == line[1] and county == line[2]:
#                     line[3], line[4] = check(line[3], line[4])
#                     file.write(',' + str(line[3]) + ',' + str(line[4]) + '\n')
#                     break
#         file.close()
print('done')
