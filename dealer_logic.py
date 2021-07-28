import csv

with open('strategy.csv', 'r') as st:
    parsed = csv.reader(st, delimiter=',')
    data = []
    for c, row in enumerate(parsed):
        newData = []
        if c == 0:
            pass
        else:
            for ele in row:
                if ele.isdigit():
                    newData.append(int(ele))
                else:
                    newData.append(str(ele))
            
            for d in newData:
                data.append(newData)