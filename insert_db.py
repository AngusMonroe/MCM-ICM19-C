import xlrd
import pymysql

file = xlrd.open_workbook('MCM_NFLIS_Data.xlsx')  # 打开Excel文件
sheet = file.sheet_by_index(1)  # 根据sheet页的排序选取sheet
row_number = sheet.nrows  # 获取有数据的最大行数
col_number = sheet.ncols  # 获取有数据的最大列数

print(row_number)
print(col_number)

connect = pymysql.connect("localhost", "root", "jiaxing+", "MCM_ICM19")  # host, user, password, database
cur = connect.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor

for i in range(row_number):
    if i == 0:
        continue
    list = sheet.row_values(i)  # 获取指定行的数据，返回列表，排序自0开始
    print(list)
    # SQL 插入语句
    sql = "INSERT INTO MCM_NFLIS_Data(YYYY, State, COUNTY, FIPS_State, FIPS_County, FIPS_Combined," \
          " SubstanceName, DrugReports, TotalDrugReportsCounty, TotalDrugReportsState) \
           VALUES ('%d', '%s', '%s', '%d', '%d', '%d', '%s', '%d', '%d', '%d' )" % \
           (int(list[0]), list[1], list[2], int(list[3]), int(list[4]), int(list[5]),
            list[6], int(list[7]), int(list[8]), int(list[9]))
    cur.execute(sql)  # 执行sql语句
    connect.commit()   # 提交到数据库执行
connect.close()  # 关闭数据库连接
print('done')
