import csv

with open('strategy.csv', 'r') as st:
    reader = csv.reader(st)
    data = []
    for c, row in enumerate(reader):
        newData = []
        if c == 0:
            pass
        else:
            for ele in row:
                if ele.isdigit():
                    newData.append(int(ele))
                else:
                    newData.append(str(data))
            
            for d in newData:
                data.append(newData)