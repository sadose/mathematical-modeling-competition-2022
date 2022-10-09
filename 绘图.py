import csv
import matplotlib.pyplot as plt
import numpy as np

colors = {
    "宽城区": "peru",
    "二道区": "orange",
    "朝阳区": "gold",
    "绿园区": "palegreen",
    "南关区": "gray",
    "经开区": "turquoise",
    "长春新区(高新)": "pink",
    "净月区": "fuchsia",
    "汽开区": "yellow"
}

plt.figure(figsize=(19.2, 14.4))


# CSV 转字典
def toDict(filename):
    map = {}
    with open(filename, "r", encoding="utf8") as f:
        reader = csv.reader(f)
        first = True
        for row in reader:
            if first:
                first = False
                continue
            idx = int(row[0])
            map[idx] = []
            for s in row[1:]:
                if s.find('.') != -1:
                    map[idx].append(float(s))
                else:
                    map[idx].append(int(s))
    return map


# 绘制道路数据
node = toDict("data/路口数据.csv")
line = toDict("data/道路数据.csv")
for roadIdx in line.keys():
    [node1, node2, _] = line[roadIdx]
    a = node[node1]
    b = node[node2]
    x = [a[0], b[0]]
    y = [a[1], b[1]]
    plt.plot(x, y, color="aquamarine", linewidth='0.5')

# 绘制小区数据
with open("data/小区数据.csv", "r", encoding="utf8") as f:
    reader = csv.reader(f)
    first = True
    for row in reader:
        if first:
            first = False
            continue
        # if row[7][-1] != ")":
        #     continue
        x = float(row[4])
        y = float(row[5])
        plt.plot(x, y, marker='.', color=colors[row[7]])

# 绘制集散地
with open("output/集散地投影.csv", "r", encoding="utf8") as f:
    reader = csv.reader(f)
    first = True
    for row in reader:
        if first:
            first = False
            continue
        # if row[0][-1] != ")":
        #     continue
        x = float(row[1])
        y = float(row[2])
        plt.plot(x, y, marker='2', color="b")

# 绘制物资来源
with open("data/各区物资来源.csv", "r", encoding="utf8") as f:
    reader = csv.reader(f)
    first = True
    for row in reader:
        if first:
            first = False
            continue
        x = float(row[2])
        y = float(row[3])
        plt.plot(x, y, marker='*', color="r")

plt.savefig('figure.png', dpi=200)
# plt.show()
