import pymysql
import numpy as np
import matplotlib.pyplot as plt

connect = pymysql.connect("localhost", "root", "jiaxing+", "MCM_ICM19")  # host, user, password, database
cur = connect.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
cur.execute('select State from MCM_NFLIS_Data group by State')  # 执行sql语句
connect.commit()  # 提交到数据库执行
states = cur.fetchall()
print(states)

index = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]
y = []

for state in states:
    data = []
    for year in index:
        cur = connect.cursor()
        cur.execute('select TotalDrugReportsState from ' + state[0] + '_NFLIS_Data where YYYY = ' + str(year) + ' group by TotalDrugReportsState')  # 执行sql语句
        connect.commit()  # 提交到数据库执行
        num = cur.fetchall()
        data.append(num[0][0])
    y.append(data)

index = np.array(index)
bar_width = 0.15
plt.bar(index - bar_width * 2, y[0], width=0.15, color='y')
plt.bar(index - bar_width, y[1], width=0.15, color='b')
plt.bar(index, y[2], width=0.15, color='r')
plt.bar(index + bar_width, y[3], width=0.15, color='g')
plt.bar(index + bar_width * 2, y[4], width=0.15)
plt.show()

connect.close()  # 关闭数据库连接
print('done')
