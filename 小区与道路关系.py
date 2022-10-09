from math import sqrt
import csv


# 点到直线的距离以及分割边
def distance(p, a, b):
    [[x1, y1], [x2, y2], [x3, y3]] = [a, b, p]
    L = abs((y1 - y2) * x3 +
            (x2 - x1) * y3 + x1 * y2 - y1 * x2) / sqrt((y1 - y2)**2 +
                                                       (x1 - x2)**2)
    return L


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


# 计算小区所在道路
# 实际就是计算距离小区最近的道路
def getRoad():
    node = toDict("data/路口数据.csv")
    print("共读取", len(node.keys()), "个路口")
    line = toDict("data/道路数据.csv")
    print("共读取", len(line.keys()), "条道路")
    print("计算中...")
    # fileinput = "data/小区数据.csv" # 小区输入文件
    fileinput = "data/各区物资来源.csv" # 物资来源输入文件
    # fileoutput = "output/小区-道路.csv" # 小区输出文件
    fileoutput = "output/物资来源-道路.csv" # 物资来源输出文件
    with open(fileoutput, "w", encoding="utf8") as f:
        f.write("")
    with open(fileoutput, "a", encoding="utf8") as fr:
        fr.write("点位编号,道路编号,虚拟距离\n")
        with open(fileinput, "r", encoding="utf8") as f:
            reader = csv.reader(f)
            first = True
            for row in reader:
                if first:
                    first = False
                    continue
                idx = int(row[0])
                # p = [float(row[4]), float(row[5])] # 小区
                p = [float(row[2]), float(row[3])] # 物资来源
                road = 1
                a = [0, 0]
                b = [0, 0]
                lastDis = -1
                for roadIdx in line.keys():
                    [node1, node2, _] = line[roadIdx]
                    a = node[node1]
                    b = node[node2]
                    dis = distance(p, a, b)
                    if lastDis == -1 or dis < lastDis:
                        road = roadIdx
                        lastDis = dis
                fr.write(",".join([str(v)
                                   for v in [idx, road, lastDis]]) + "\n")
    print("-- done --")


if __name__ == "__main__":
    getRoad()
