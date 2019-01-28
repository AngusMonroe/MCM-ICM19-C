import json
import xlrd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np

out_file = open('regression-year/result_h.csv', 'w', encoding='utf8')
out_file.write('year,State,S_l,H_l,S_o,H_o,epsilon\n')
states = ['VA', 'KY', 'OH', 'PA', 'WV']
for year in range(2010, 2018):
    for state in states:
        try:
            # 通过read_csv来读取我们的目的数据集
            adv_data = pd.read_csv('regression-year/' + str(year) + '/' + str(year) + '-' + state + '.csv', error_bad_lines=False)
            # 清洗不需要的数据
            new_adv_data = adv_data.ix[:, 1:-1]
            # 得到我们所需要的数据集且查看其前几列以及数据形状
            # print('head:', new_adv_data.head(), '\nShape:', new_adv_data.shape)

            # 数据描述
            print(new_adv_data.describe())
            # 缺失值检验
            print(new_adv_data[new_adv_data.isnull() == True].count())

            new_adv_data.boxplot()
            plt.savefig("boxplot.jpg")
            # plt.show()
            # 相关系数矩阵 r(相关系数) = x和y的协方差/(x的标准差*y的标准差) == cov（x,y）/σx*σy
            # 相关系数0~0.3弱相关0.3~0.6中等程度相关0.6~1强相关
            print(new_adv_data.corr())


            sns.pairplot(new_adv_data, x_vars=['o_basic','h_basic','o_neighbor','h_neighbor'], y_vars='aim_o', size=7, aspect=0.8,kind='reg')
            plt.savefig("pairplot.jpg")

            X_train, X_test, Y_train, Y_test = train_test_split(new_adv_data.ix[:, :4], new_adv_data.aim_o, train_size=.80)

            print("原始数据特征:", new_adv_data.ix[:, :3].shape,
                  ",训练数据特征:", X_train.shape,
                  ",测试数据特征:", X_test.shape)

            print("原始数据标签:", new_adv_data.aim_o.shape,
                  ",训练数据标签:", Y_train.shape,
                  ",测试数据标签:", Y_test.shape)

            model = LinearRegression()
            model.fit(X_train, Y_train)

            a = model.intercept_  # 截距

            b = model.coef_  # 回归系数

            print("最佳拟合线:截距", a, ",回归系数：", b)
            ans = str(year) + ',' + state
            for item in b:
                ans += ',' + str(item)
            ans += ',' + str(a) + '\n'
            out_file.write(ans)
        except:
            print(year)
            print(state)
            continue
out_file.close()
