import numpy as np
import pandas as pd
import folium
import webbrowser
from folium.plugins import HeatMap
import xlrd
# import sys
# sys.setrecursionlimit(10**5)  # set the maximum depth as 10的3次方

in_file = xlrd.open_workbook('MCM_NFLIS_Data_pro.xlsx')  # 打开Excel文件
sheet = in_file.sheet_by_index(1)  # 根据sheet页的排序选取sheet
row_number = sheet.nrows  # 获取有数据的最大行数
col_number = sheet.ncols  # 获取有数据的最大列数


states = ['VA', 'KY', 'OH', 'PA', 'WV']
name = 'Butyryl fentanyl'
for state in states:
    for year in range(2010, 2018):
        n = []
        lat = []
        lon = []
        line = 0
        for i in range(row_number):
            if i == 0:
                continue
            list = sheet.row_values(i)  # 获取指定行的数据，返回列表，排序自0开始
            if list[0] == year and list[1] == state and list[6] == name:
                n.append(list[7])
                pos_file = open('position/' + state + '.txt', 'r', encoding='utf8')
                for record in pos_file.readlines():
                    item = record[:-1].split(',')
                    if item[0] == list[2]:
                        lat.append(float(item[1]))
                        lon.append(float(item[2]))
                        break
                pos_file.close()
                line += 1

        latituade = pd.Series(lat)  # 获取纬度值
        longitude = pd.Series(lon)  # 获取经度值
        num = pd.Series(n)  # 获取TotalDrugReportsCounty
        # print(latituade)
        # print(longitude)
        # print(num)
        # print(line)
        data1 = [[latituade[j], longitude[j], num[j]] for j in range(line)]  # 将数据制作成[lats,lons,weights]的形式
        # print(data1)
        # break
        map_osm = folium.Map(location=[40, -98], zoom_start=5)    # 绘制Map，开始缩放程度是5倍
        HeatMap(data1).add_to(map_osm)  # 将热力图添加到前面建立的map里

        file_path = 'thermodynamic_diagram/3,4-Methylenedioxy U-47700/' + state + '/' + str(year) + '-' + state + ".html"
        map_osm.save(file_path)  # 保存为html文件
    # break

print('done')
