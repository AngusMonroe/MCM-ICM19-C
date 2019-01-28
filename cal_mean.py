
states = ['VA', 'KY', 'OH', 'PA', 'WV']
out_file = open('regression-year/mean.txt', 'w', encoding='utf8')
out_file.write('year,state,o_basic_mean,h_basic_mean,o_neighbor_mean,h_neighbor_mean\n')
for year in range(2010, 2018):
    o_basic, h_basic, o_neighbor, h_neighbor = 0, 0, 0, 0
    for state in states:
        file = open('regression-year/' + str(year) + '/' + str(year) + '-' + state + '.csv', 'r', encoding='utf8')
        lines = file.readlines()
        for line in lines:
            item = line.split(',')
            if item[0] == '':
                continue
            o_basic += float(item[1])
            h_basic += float(item[2])
            o_neighbor += float(item[3])
            h_neighbor += float(item[4])
        num = len(lines)
        out_file.write(str(year) + ',' + state + ',' + str(o_basic/num) + ',' + str(h_basic/num) + ',' + str(o_neighbor/num) + ',' + str(h_neighbor/num) + '\n')
out_file.close()
