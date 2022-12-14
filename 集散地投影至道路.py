from math import sqrt
import csv


# 点到直线的距离以及分割边
def distance(p, a, b):
    [[x1, y1], [x2, y2], [x3, y3]] = [a, b, p]
    L = abs((y1 - y2) * x3 +
            (x2 - x1) * y3 + x1 * y2 - y1 * x2) / sqrt((y1 - y2)**2 +
                                                       (x1 - x2)**2)
    return L


# 点在直线上的投影
def projection(p, a, b):
    k1 = (a[1] - b[1]) / (a[0] - b[0])
    b1 = a[1] - k1 * a[0]
    k2 = -1 / k1
    b2 = p[1] - k2 * p[0]
    x = (b2 - b1) / (k1 - k2)
    y = k1 * x + b1
    return [x, y]


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
    fileinput = "output/集散地.csv"  # 集散地输入文件
    fileoutput = "output/集散地投影.csv"  # 集散地投影输出文件
    with open(fileoutput, "w", encoding="utf8") as f:
        f.write("地区,x,y,道路编号,虚拟距离\n")
    with open(fileoutput, "a", encoding="utf8") as fr:
        with open(fileinput, "r", encoding="utf8") as f:
            reader = csv.reader(f)
            first = True
            for row in reader:
                if first:
                    first = False
                    continue
                region = row[0]
                p = [float(row[1]), float(row[2])]
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
                [node1, node2, _] = line[road]
                a = node[node1]
                b = node[node2]
                [x, y] = projection(p, a, b)
                fr.write(
                    ",".join([str(v)
                              for v in [region, x, y, road, lastDis]]) + "\n")
    print("-- done --")


if __name__ == "__main__":
    getRoad()
