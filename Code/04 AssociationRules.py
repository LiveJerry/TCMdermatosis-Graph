import pandas as pd
import numpy as np
from apyori import apriori
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# 读取 Excel 文件
data = pd.read_excel('药方_Transposed.xlsx', index_col=0).T

# 转换数据格式为列表
transactions = []
for index, row in data.iterrows():
    transactions.append([col for col in data.columns if row[col] == 1])

# 应用关联规则挖掘
association_rules = apriori(transactions, min_support=0.15, min_confidence=0.5, min_lift=1.0, min_length=2)
association_results = list(association_rules)

# 输出关联规则
for item in association_results:
    # 输出频繁项集
    print("频繁项集: ", item[0])
    # 输出关联规则及其支持度、置信度、提升度
    for rule in item[2]:
        print("关联规则: " + str(rule[0]) + " => " + str(rule[1]))
        print("支持度: " + str(item[1]))
        print("置信度: " + str(rule[2]))
        print("提升度: " + str(rule[3]))
        print("=====================================")

# 创建一个空的DataFrame来存储关联规则
rule_data = []

# 遍历关联规则结果
for item in association_results:
    # 获取前提项和后项
    antecedents = item[2][0][0]
    consequents = item[2][0][1]
    # 获取支持度、置信度和提升度
    support = item[1]
    confidence = item[2][0][2]
    lift = item[2][0][3]
    # 将规则添加到DataFrame中
    rule_data.append({
        '前提项': ', '.join(antecedents),
        '后项': ', '.join(consequents),
        '支持度': support,
        '置信度': confidence,
        '提升度': lift
    })

# 创建DataFrame
rule_df = pd.DataFrame(rule_data)

# 将DataFrame写入Excel文件
rule_df.to_excel('rule.xlsx', index=False)

# 绘制网络图
plt.rcParams['font.sans-serif'] = ['Simhei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False


def plot_rules_net(association_results):
    items = set()  # 创建一个集合来存储所有的药材

    # 遍历关联规则结果
    for item in association_results:
        # 获取前提项和后项
        antecedents = item[2][0][0]
        consequents = item[2][0][1]

        # 将前提项和后项添加到集合中
        items.update(antecedents)
        items.update(consequents)

    # 将集合转换为列表
    items = list(items)

    # 计算药材数量，确定顶点数
    n_items = len(items)

    # 创建一个正n_items边形的顶点坐标
    radius = 5  # 可以调整半径
    angle = np.linspace(0, 2 * np.pi, n_items, endpoint=False)
    x = radius * np.cos(angle)
    y = radius * np.sin(angle)

    # 绘制正多边形和顶点
    fig, ax = plt.subplots(figsize=(10, 10))

    polygon = patches.RegularPolygon((0, 0), n_items, radius=radius, fill=False, edgecolor='k')
    ax.add_patch(polygon)

    def get_label_position(angle):
        label_offset_value = 0.2  # 定义一个变量来存储偏移量

        # 根据角度确定文本标签的对齐方式和位置
        if angle < np.pi / 2:
            ha, va = "center", "bottom"
            offset = np.array([label_offset_value, label_offset_value])
        elif angle < np.pi:
            ha, va = "center", "bottom"
            offset = np.array([-label_offset_value, label_offset_value])
        elif angle < 3 * np.pi / 2:
            ha, va = "center", "top"
            offset = np.array([-label_offset_value, -label_offset_value])
        else:
            ha, va = "center", "top"
            offset = np.array([label_offset_value, -label_offset_value])
        return ha, va, offset

    # 在绘制顶点的循环中调整文本位置
    for (i, j), label, angle in zip(zip(x, y), items, angle):
        ha, va, offset = get_label_position(angle)
        ax.plot(i, j, 'o', markersize=10)
        ax.text(i + offset[0], j + offset[1], label, fontsize=12, ha=ha, va=va)

    # 获取confidence的最小值和最大值
    min_confidence = min([rule[2] for item in association_results for rule in item[2]])
    max_confidence = max([rule[2] for item in association_results for rule in item[2]])
    # 使用colormap - 可以根据需要选择合适的colormap
    # 这里我们使用'Greens'，因为你想要的是颜色越深表示权重越大
    cmap = plt.get_cmap('Greens')

    # 线性映射函数，将confidence值映射到0-1之间，用于colormap
    def get_color(confidence):
        return cmap((confidence - min_confidence) / (max_confidence - min_confidence))

    # 绘制边
    for item in association_results:
        for rule in item[2]:
            antecedents = rule[0]
            consequents = rule[1]
            confidence = rule[2]

            for antecedent in antecedents:
                for consequent in consequents:
                    start_idx = items.index(antecedent)
                    end_idx = items.index(consequent)

                    start_point = (x[start_idx], y[start_idx])
                    end_point = (x[end_idx], y[end_idx])

                    color = get_color(confidence)

                    # 修改箭头的绘制方式，使其从节点边缘出发
                    ax.annotate("",
                                xy=end_point, xytext=start_point,
                                arrowprops=dict(arrowstyle="->", color=color,
                                                shrinkA=5, shrinkB=5,  # shrinkA和shrinkB应该是半径的大小，不是索引
                                                connectionstyle="arc3"),
                                )

    ax.set_xlim([-radius * 1.1, radius * 1.1])
    ax.set_ylim([-radius * 1.1, radius * 1.1])
    ax.axis('off')  # 隐藏坐标轴

    plt.suptitle('前26个最高频次药物的关联规则图', fontsize=20)  # 主标题
    plt.xlabel('颜色深代表置信度高', fontsize=14)  # X轴标签

    save_path = os.path.join('.', '关联规则网络图.jpg')

    plt.savefig(save_path)
    plt.show()


# 调用绘图函数
plot_rules_net(association_results)