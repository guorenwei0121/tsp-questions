#GA.py
#遗传算法求解TSP问题
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import math
import random

matplotlib.rcParams['font.family'] = 'STSong'  # 字体为华文宋体

# 载入数据
site_name = []  #位置名称列表
site_coordinate = []   #位置坐标列表
with open('zuobiao.txt', 'r', encoding='utf-8') as f:   #以读文件模式打开zuobiao.txt
    lines = f.readlines()   #读取文件的所有行，保存在一个列表中，每行作为一个元素
    for line in lines:
        line = line.split('\n')[0]
        line = line.split(' ')
        site_name.append(line[0])   #第一列为位置名称
        site_coordinate.append([float(line[2]), float(line[1])])   #第二三列为横纵坐标
site_coordinate = np.array(site_coordinate)   #使用numpy库把site_coordinate定义为数组

# 两两地点之间的距离矩阵
site_count = len(site_name)   #坐标数等于位置名称列表长度
Distance = np.zeros([site_count, site_count])   #一个总数行总数列的矩阵
for i in range(site_count):
    for j in range(site_count):
        Distance[i][j] = math.sqrt(
            (site_coordinate[i][0] - site_coordinate[j][0]) ** 2 + (site_coordinate[i][1] - site_coordinate[j][1]) ** 2)  #两点之间距离公式

# 种群数
count = 150
# 进化次数
itter_time = 700
# 变异率
mutation_rate = 0.1

# 51个地点与数字对应的字典   地点1：0 .......
site_index_dict = {}
i = 0
for site in site_name:
    site_index_dict[site] = i
    i += 1

# 51个数字与地点对应的字典   0......：地点1
index_site_dict = {}
i = 0
for site in site_name:
    index_site_dict[i] = site
    i += 1


# 获取起点索引及选中城市的索引列表
def get_origin(select_site):
    global site_index_dict
    origin = site_index_dict[select_site[0]]  # 将选择的地点中的第一个设为起点地点
    select_site_index = []
    for site in select_site:
        select_site_index.append(site_index_dict[site])  # 将选择的地点转换为地点对应的序号
    select_site_index.remove(origin)
    return origin, select_site_index


# 一个个体的总距离
def get_total_distance(x, origin):
    distance = 0
    distance += Distance[origin][x[0]]   # 起点到第一个城市的距离
    for i in range(len(x)):
        if i == len(x) - 1:
            distance += Distance[origin][x[i]]    # 最后一个城市返回起点

            break
        else:
            distance += Distance[x[i]][x[i + 1]]     # 城市间距离
    return distance


# 初始化种群
def generate_population(select_site_index):
    population = []
    for i in range(count):
        # 随机生成个体
        x = select_site_index.copy()  #复制
        random.shuffle(x)  # 随机排序
        population.append(x)
    return population   #多个随机顺序（数组）


# 自然选择    轮盘赌算法
def selection(population, origin):
    graded = [[get_total_distance(x, origin), x] for x in population]
    # 计算适应度
    fit_value = []  # 存储每个个体的适应度
    for i in range(len(graded)):
        fit_value.append(1 / graded[i][0] ** 15)
    # 适应度总和
    total_fit = 0
    for i in range(len(fit_value)):
        total_fit += fit_value[i]

    # 计算每个适应度占适应度总和的比例
    newfit_value = []  # 储存每个个体轮盘选择的概率
    for i in range(len(fit_value)):
        newfit_value.append(fit_value[i] / total_fit)

    # 计算累计概率
    t = 0
    for i in range(len(newfit_value)):
        t = t + newfit_value[i]
        newfit_value[i] = t

    # 生成随机数序列用于选择和比较
    ms = []  # 随机数序列
    for i in range(len(population)):
        ms.append(random.random())   #随机生成（0,1）之间的浮点数
    ms.sort()   #就地排序

    # 轮盘赌选择法
    i = 0
    j = 0
    parents = []
    while i < len(population):
        # 选择--累积概率大于随机概率
        if (ms[i] < newfit_value[j]):
            if population[j] not in parents:
                parents.append(population[j])
            i = i + 1
        # 不选择--累积概率小于随机概率
        else:
            j = j + 1

    return parents


# 交叉繁殖
def crossover(parents):
    # 生成子代的个数,以此保证种群稳定
    child_count = count - len(parents)
    # 孩子列表
    children = []
    while len(children) < child_count:
        #选择两个不同的父代
        mother_idx = random.randint(0, len(parents) - 1)
        father_idx = random.randint(0, len(parents) - 1)
        if mother_idx != father_idx:
            mother = parents[mother_idx]
            father = parents[father_idx]

            # 随机选择两个交叉点
            left, right = sorted(random.sample(range(len(mother)), 2))

            def ox_child(p1, p2):
                child = [None] * len(p1)
                # 保留p1的选定片段
                child[left:right] = p1[left:right]
                # 从p2填充剩余基因（保持顺序）
                p2_ptr = 0
                for i in list(range(right, len(p2))) + list(range(0, right)):
                    if p2[i] not in child:
                        while child[p2_ptr] is not None:
                            p2_ptr += 1
                        child[p2_ptr] = p2[i]
                return child

            children.append(ox_child(mother, father))
            children.append(ox_child(father, mother))
    return children

# 变异    基因次序片段交换
def mutation(children):
    for i in range(len(children)):
        if random.random() < mutation_rate:
            child = children[i]
            u = random.randint(0, len(child) - 2)
            v = random.randint(u + 1, len(child) - 1)

            child_x = child[u + 1:v]
            child_x.reverse()
            child = child[0:u + 1] + child_x + child[v:]


# 获取种群中最优解
def get_result(population, origin):
    graded = [[get_total_distance(x, origin), x] for x in population]
    graded = sorted(graded)
    return graded


# 绘制最优路径图
def draw(origin, result_path, distance):
    global site_coordinate, site_name
    # 初始化路径图
    plt.clf()  # 清空当前图形（避免残留）
    plt.title(f"路径图（总距离：{distance:.2f}）")
    plt.scatter(site_coordinate[:, 0], site_coordinate[:, 1], color='gray', label='景点')

    # 标注景点名称
    for i in range(len(site_name)):
        plt.text(site_coordinate[i, 0], site_coordinate[i, 1], site_name[i], fontsize=8, color='black')

    # 绘制路径（起点->路径点->起点）
    path_coords = [site_coordinate[origin]]  # 起点坐标
    for idx in result_path:
        path_coords.append(site_coordinate[idx])
    path_coords.append(site_coordinate[origin])  # 回到起点

    # 定义颜色列表，可根据需要扩展
    colors = ['green', '#FFBD33', '#C7FF33', '#33FF57', '#33FFBD', '#33C7FF', '#3357FF', '#BD33FF']
    num_colors = len(colors)

    # 绘制连线并标注顺序
    for i in range(len(path_coords)-1):
        x1, y1 = path_coords[i]
        x2, y2 = path_coords[i+1]
        # 选择不同的颜色
        color = colors[i % num_colors]
        print(f"段 {i}: 颜色 {color}")  # 添加打印语句
        plt.plot([x1, x2], [y1, y2], 'b-', linewidth=1)  # 路径连线
        plt.text((x1+x2)/2, (y1+y2)/2, str(i), fontsize=9, color='red')  # 标注步骤

    # 突出起点
    plt.scatter(site_coordinate[origin, 0], site_coordinate[origin, 1], s=150, color='red', label='起点')
    plt.legend()
