import xlwt
import xlrd
in_file = xlrd.open_workbook('MCM_NFLIS_Data_pro.xlsx')  # 打开Excel文件
sheet = in_file.sheet_by_index(1)  # 根据sheet页的排序选取sheet
row_number = sheet.nrows  # 获取有数据的最大行数
col_number = sheet.ncols  # 获取有数据的最大列数
out_file = xlwt.Workbook(encoding='utf8')  # 打开Excel文件
worksheet = out_file.add_sheet('county_drug')

states = ['VA', 'KY', 'OH', 'PA', 'WV']
line = 0

for state in states:
    county = []
    for i in range(row_number):
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
        if list[2] not in county and list[1] == state:
            worksheet.write(line, 0, label=list[0])
            worksheet.write(line, 1, label=list[1])
            worksheet.write(line, 2, label=list[2])
            worksheet.write(line, 3, label=list[8])
            worksheet.write(line, 4, label=list[10])
            worksheet.write(line, 5, label=list[11])
            county.append(list[2])
            line += 1

out_file.save('MCM_NFLIS_Data_pro1.xls')
