import json
import xlrd
import xlwt


def check(a, b):
    if not a:
        a = 0
    if not b:
        b = 0
    return a, b

in_file = xlrd.open_workbook('MCM_NFLIS_Data_pro.xlsx')  # 打开Excel文件
out_file = xlwt.Workbook(encoding='utf8')  # 打开Excel文件
worksheet = out_file.add_sheet('res')

states = ['VA', 'KY', 'OH', 'PA', 'WV']

# para = {'VA': {}, 'KY': {}, 'OH': {}, 'PA': {}, 'WV': {}}
# sheet = in_file.sheet_by_index(2)  # 根据sheet页的排序选取sheet
# row_number = sheet.nrows  # 获取有数据的最大行数
# col_number = sheet.ncols  # 获取有数据的最大列数
#
# for i in range(row_number):
#     if i == 0:
#         continue
#     line = sheet.row_values(i)  # 获取指定行的数据，返回列表，排序自0开始
#     para[line[0]].update({str(int(line[1])): line[2:]})
# with open("parameter.json", 'w', encoding='utf-8') as json_file:
#     json.dump(para, json_file, ensure_ascii=False)

with open("neighbor_map.json", 'r', encoding='utf-8') as json_file1:
    neighbor_map = json.load(json_file1)
with open("parameter.json", 'r', encoding='utf-8') as json_file2:
    para = json.load(json_file2)

sheet = in_file.sheet_by_index(8)  # 根据sheet页的排序选取sheet
row_number = sheet.nrows  # 获取有数据的最大行数
col_number = sheet.ncols  # 获取有数据的最大列数
print(row_number)

year = 2021
row = 0
for state in states:
    # file = open('regression-year/' + str(year) + '/' + str(year) + '-' + state + '.csv', 'w', encoding='utf8')
    # file.write(',o_basic,h_basic,o_neighbor,h_neighbor,aim_o,aim_h\n')
    for county, neighbor in neighbor_map[state].items():
        string = ''
        flag = False
        o_b = 0
        h_b = 0
        for i in range(row_number):
            if i == 0:
                continue
            line = sheet.row_values(i)  # 获取指定行的数据，返回列表，排序自0开始
            # line[0] = int(line[0])
            # line[3] = int(line[3])
            # line[4] = int(line[4])
            if year == line[0] and state == line[1] and county == line[2]:
                line[3], line[4] = check(line[3], line[4])
                worksheet.write(row, 0, label=year + 1)
                worksheet.write(row, 1, label=state)
                worksheet.write(row, 2, label=county)
                o_b = line[3]
                h_b = line[4]
                # string += str(line_num) + ',' + str(line[3]) + ',' + str(line[4])
                # file.write(str(line_num) + ',' + str(line[3]) + ',' + str(line[4]))
                flag = True
                break
        if not flag:
            continue
        o_n = 0
        h_n = 0
        for name in neighbor:
            for i in range(row_number):
                if i == 0:
                    continue
                line = sheet.row_values(i)  # 获取指定行的数据，返回列表，排序自0开始
                if year == line[0] and state == line[1] and name == line[2]:
                    line[3], line[4] = check(line[3], line[4])
                    o_n += line[4]
                    h_n += line[3]
                    break
        # string += ',' + str(o) + ',' + str(h)
        # file.write(',' + str(o) + ',' + str(h))
        p = para[state][str(year)]
        y_o = p[0] * o_b + p[1] * h_b + p[2] * o_n + p[3] * h_n + p[4]
        y_h = p[5] * o_b + p[6] * h_b + p[7] * o_n + p[8] * h_n + p[9]
        worksheet.write(row, 3, label=int(y_o))
        worksheet.write(row, 4, label=int(y_h))
        row += 1
    # file.close()
out_file.save('res.xls')
