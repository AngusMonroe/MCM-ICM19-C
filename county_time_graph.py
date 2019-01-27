import pymysql
import numpy as np
import matplotlib.pyplot as plt

connect = pymysql.connect("localhost", "root", "jiaxing+", "MCM_ICM19")  # host, user, password, database
cur = connect.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
cur.execute('select State from MCM_NFLIS_Data group by State')  # 执行sql语句
connect.commit()  # 提交到数据库执行
states = cur.fetchall()
print(states)

for year in range(2010, 2018):
    y = []
    x_lables = []
    for state in states:
        cur = connect.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
        cur.execute('select COUNTY from ' + state[0] + '_NFLIS_Data group by COUNTY')  # 执行sql语句
        connect.commit()  # 提交到数据库执行
        countys = cur.fetchall()
        data = []
        x_lable = []
        for county in countys:
            cur = connect.cursor()
            sql = 'select TotalDrugReportsCounty from ' + state[0] + '_NFLIS_Data where YYYY = ' + str(year) + ' and COUNTY = \'' + county[0] + '\' group by TotalDrugReportsCounty'
            # print(sql)
            cur.execute(sql)  # 执行sql语句
            connect.commit()  # 提交到数据库执行
            num = cur.fetchall()
            if num:
                data.append(num[0][0])
            x_lable.append(county[0])
        x_lables.append(x_lable)
        y.append(data)

    print(y)
    for y_, state, x_lable in zip(y, states, x_lables):
        plt.clf()
        file = open(str(year) + '/' + str(year) + '-' + state[0] + '.txt', 'w', encoding='utf8')
        for i, line in enumerate(x_lable):
            file.write(str(i) + '\t' + line + '\n')
        file.close()
        print(y_)
        x = np.arange(len(y_))
        plt.bar(x, y_, color='b')
        plt.title(str(year) + '-' + state[0])
        # plt.xticks(x, x_lable)
        plt.savefig('bar_diagram' + str(year) + '/' + str(year) + '-' + state[0])

connect.close()  # 关闭数据库连接
print('done')
