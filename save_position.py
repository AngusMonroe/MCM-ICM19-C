import xlrd
import xlwt
import pymysql
import json

file = xlrd.open_workbook('MCM_NFLIS_Data_pro.xlsx')  # 打开Excel文件
sheet = file.sheet_by_index(1)  # 根据sheet页的排序选取sheet
row_number = sheet.nrows  # 获取有数据的最大行数
col_number = sheet.ncols  # 获取有数据的最大列数

print(row_number)
print(col_number)

out_file = xlwt.Workbook(encoding='utf8')  # 打开Excel文件
worksheet = out_file.add_sheet('county_drug')

with open("USCities.json", 'r') as load_f:
    load_dict = json.load(load_f)

states = ['VA', 'KY', 'OH', 'PA', 'WV']
line = 0
for year in range(2010, 2018):
    for state in states:
        # file = open('position/' + state + '.txt', 'w', encoding='utf8')
        county = []
        for i in range(row_number):
            if i == 0:
                if line == 0:
                    worksheet.write(line, 0, label='YYYY')
                    worksheet.write(line, 1, label='State')
                    worksheet.write(line, 2, label='County')
                    worksheet.write(line, 3, label='TotalDrugReportsCounty')
                    worksheet.write(line, 4, label='lat')
                    worksheet.write(line, 5, label='lon')
                    line += 1
                continue
            list = sheet.row_values(i)  # 获取指定行的数据，返回列表，排序自0开始

            if list[0] == year and list[2] not in county and list[1] == state:
                for dict in load_dict:
                    if dict["state"] == state and dict["county"].lower() == list[2].lower():
                        # file.write(list[2] + ',' + str(dict["latitude"]) + ',' + str(dict["longitude"]) + '\n')
                        county.append(list[2])
                        worksheet.write(line, 0, label=list[0])
                        worksheet.write(line, 1, label=list[1])
                        worksheet.write(line, 2, label=list[2])
                        worksheet.write(line, 3, label=list[8])
                        worksheet.write(line, 4, label=dict["latitude"])
                        worksheet.write(line, 5, label=dict["longitude"])
                        line += 1
                        break
        # file.close()
print('done')
out_file.save('MCM_NFLIS_Data_pro1.xls')
