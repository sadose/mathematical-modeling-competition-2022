from math import sqrt
import csv


# 计算两点间距离
def distance(a, b):
    return sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


# 全局数据
regions = ["宽城区", "二道区", "朝阳区", "绿园区", "南关区", "经开区", "长春新区(高新)", "净月区", "汽开区"]
data = {}
cache = {}  # 小区到它所属的集散地的映射


# 获取数据
def getData():
    with open("data/各区物资来源.csv", "r", encoding="utf8") as f:
        reader = csv.reader(f)
        first = True
        for row in reader:
            if first:
                first = False
                continue
            name = row[1]
            data[name] = {
                "center": [float(row[2]), float(row[3])],
                "points": [],
                "candidate": [],
                "candidateFlag": [],
                "minx": 100,
                "maxx": 0,
                "miny": 100,
                "maxy": 0
            }
    with open("data/小区数据.csv", "r", encoding="utf8") as f:
        reader = csv.reader(f)
        first = True
        for row in reader:
            if first:
                first = False
                continue
            region = row[7]
            x = float(row[4])
            y = float(row[5])
            if x < data[region]["minx"]:
                data[region]["minx"] = x
            if x > data[region]["maxx"]:
                data[region]["maxx"] = x
            if y < data[region]["miny"]:
                data[region]["miny"] = y
            if y > data[region]["maxy"]:
                data[region]["maxy"] = y
            data[region]["points"].append([int(row[0]),
                                           int(row[3]), x, y])  # [小区序号,人数,坐标]
    for region in regions:
        print(region, data[region]["center"], len(data[region]["points"]))
        print("\t", [data[region]["minx"], data[region]["maxx"]],
              [data[region]["miny"], data[region]["maxy"]])
        data[region]["minx"] = int(data[region]["minx"]) + 1
        data[region]["maxx"] = int(data[region]["maxx"])
        data[region]["miny"] = int(data[region]["miny"]) + 1
        data[region]["maxy"] = int(data[region]["maxy"])
        print("\t", [data[region]["minx"], data[region]["maxx"]],
              [data[region]["miny"], data[region]["maxy"]])
        width = data[region]["maxx"] - data[region]["minx"] + 1
        height = data[region]["maxy"] - data[region]["miny"] + 1
        assert width > 0 and height > 0
        data[region]["candidate"] = [None for i in range(width * height)]
        data[region]["candidateFlag"] = [False for i in range(width * height)]
    print("- Done: 读取数据完成\n")


# 根据候选点序号和区域获得候选点坐标
def getCandidatePoint(idx, region):
    if len(data[region]["candidate"]) and data[region]["candidate"][idx]:
        return data[region]["candidate"][idx]
    width = data[region]["maxx"] - data[region]["minx"] + 1
    height = data[region]["maxy"] - data[region]["miny"] + 1
    xoffset = idx % width
    yoffset = idx // width
    assert xoffset >= 0 and xoffset < width and yoffset >= 0 and yoffset < height
    data[region]["candidate"][idx] = [(data[region]["minx"] + xoffset),
                                      (data[region]["miny"] + yoffset)]
    return data[region]["candidate"][idx]


# 计算单个小区的运输代价
def price(p, region):
    distribution = getCandidatePoint(cache[p[0]], region)
    dis1 = distance(data[region]["center"], distribution)  # 物资来源到集散地的距离
    dis2 = distance(distribution, p[2:])  # 集散地到小区的距离
    return (dis1 + dis2) * p[1]  # 总距离乘以小区人数


# 缓存距离每个小区最近的集散地
def setCache(points, region):
    for p in data[region]["points"]:
        res = -1
        idx = -1
        for pid in points:
            dis = distance(p[2:], getCandidatePoint(pid, region))
            if res == -1 or res > dis:
                res = dis
                idx = pid
        assert res >= 0 and idx >= 0
        cache[p[0]] = idx


# 目标函数
def target(region):
    points = []
    flagArray = data[region]["candidateFlag"]
    for i in range(len(flagArray)):
        if flagArray[i]:
            points.append(i)
    setCache(points, region)
    sumPrice = 0
    for p in data[region]["points"]:
        sumPrice += price(p, region)
    return sumPrice


# 对一个地区进行一轮迭代，返回更新次数
def updateCandidate(region):
    count = 0
    candidateFlag = data[region]["candidateFlag"]
    a = len(candidateFlag) - 1
    while a >= 0:
        if candidateFlag[a]:
            b = 0
            lastRes = target(region)
            lastPos = -1
            while b < len(candidateFlag):
                while b < len(candidateFlag) and candidateFlag[b]:
                    b += 1
                assert candidateFlag[a] and not candidateFlag[b]
                candidateFlag[b] = True
                candidateFlag[a] = False
                res = target(region)
                if res < lastRes:
                    lastRes = res
                    lastPos = b
                candidateFlag[b] = False
                candidateFlag[a] = True
                b += 1
            if lastPos != -1:
                candidateFlag[lastPos] = True
                candidateFlag[a] = False
                count += 1
        a -= 1
    print("本轮更新次数:", count)
    return count


# 初始化地区候选点
def initCandidate():
    counts = {
        "宽城区": 20,  # 306k人数
        "二道区": 27,  # 406k人数
        "朝阳区": 36,  # 548k人数
        "绿园区": 24,  # 373k人数
        "南关区": 30,  # 462k人数
        "经开区": 12,  # 189k人数
        "长春新区(高新)": 22,  # 338k人数
        "净月区": 13,  # 204k人数
        "汽开区": 12  # 193k人数
    }
    for region in regions:
        for i in range(counts[region]):
            data[region]["candidateFlag"][i] = True
    print("- Done: 初始化候选点完成\n")


if __name__ == "__main__":
    getData()
    initCandidate()
    with open("output/集散地.csv", "w", encoding="utf8") as f:
        f.write("地区,x,y\n")
    for region in regions:
        round = 1
        print("- info:", region, "的第", round, "轮迭代，", end="")
        cnt = updateCandidate(region)
        round += 1
        while cnt:
            print("- info:", region, "的第", round, "轮迭代，", end="")
            cnt = updateCandidate(region)
            round += 1
        points = []
        flagArray = data[region]["candidateFlag"]
        for i in range(len(flagArray)):
            if flagArray[i]:
                points.append(i)
        with open("output/集散地.csv", "a", encoding="utf8") as f:
            for pid in points:
                point = getCandidatePoint(pid, region)
                f.write(",".join([region, str(point[0]),
                                  str(point[1])]) + "\n")
        print(points)
        print("- Done:", region, "区域迭代完成")
        print()
