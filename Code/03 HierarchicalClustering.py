import pandas as pd
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score


# 读取数据
clinical_data = pd.read_excel('临床表现_Transposed.xlsx')
pathogen_data = pd.read_excel('病因_Transposed.xlsx')
treatment_data = pd.read_excel('治疗方法_Transposed.xlsx')
prescription_data = pd.read_excel('药方_Transposed.xlsx')

# 提取特征和标签
clinical_features = clinical_data.iloc[:, 1:].values
clinical_labels = clinical_data.iloc[:, 0].values
pathogen_features = pathogen_data.iloc[:, 1:].values
pathogen_labels = pathogen_data.iloc[:, 0].values
treatment_features = treatment_data.iloc[:, 1:].values
treatment_labels = treatment_data.iloc[:, 0].values
prescription_features = prescription_data.iloc[:, 1:].values
prescription_labels = prescription_data.iloc[:, 0].values

# 使用层次聚类进行聚类
clinical_linked = linkage(clinical_features, method='ward')
pathogen_linked = linkage(pathogen_features, method='ward')
treatment_linked = linkage(treatment_features, method='ward')
prescription_linked = linkage(prescription_features, method='ward')

from sklearn.metrics import calinski_harabasz_score

# 计算Calinski-Harabasz指数
def calculate_calinski_harabasz_score(features, linked):
    clustering = AgglomerativeClustering(n_clusters=2, linkage='ward')
    labels = clustering.fit_predict(features)
    calinski_harabasz = calinski_harabasz_score(features, labels)
    return calinski_harabasz

# 计算Calinski-Harabasz指数
clinical_calinski_harabasz = calculate_calinski_harabasz_score(clinical_features, clinical_linked)
pathogen_calinski_harabasz = calculate_calinski_harabasz_score(pathogen_features, pathogen_linked)
treatment_calinski_harabasz = calculate_calinski_harabasz_score(treatment_features, treatment_linked)
prescription_calinski_harabasz = calculate_calinski_harabasz_score(prescription_features, prescription_linked)

print("临床表现数据集Calinski-Harabasz指数:", clinical_calinski_harabasz)
print("病因数据集Calinski-Harabasz指数:", pathogen_calinski_harabasz)
print("治疗方法数据集Calinski-Harabasz指数:", treatment_calinski_harabasz)
print("药方数据集Calinski-Harabasz指数:", prescription_calinski_harabasz)

# 绘制树状图
plt.rcParams['font.family'] = 'Arial Unicode MS'
plt.figure(figsize=(15, 6))
dendrogram(clinical_linked, labels=clinical_labels)
plt.title('真菌性皮肤病相关临床表现层次聚类树状图')
plt.xlabel('样本编号')
plt.ylabel('距离')
plt.tight_layout()  # 调整布局以适应文本
plt.savefig('临床表现.png', dpi=600)
plt.close()

plt.figure(figsize=(10, 6))
dendrogram(pathogen_linked, labels=pathogen_labels)
plt.title('真菌性皮肤病相关病因层次聚类树状图')
plt.xlabel('样本编号')
plt.ylabel('距离')
plt.tight_layout()  # 调整布局以适应文本
plt.savefig('病因.png', dpi=600)
plt.close()

plt.figure(figsize=(30, 6))
dendrogram(treatment_linked, labels=treatment_labels)
plt.title('真菌性皮肤病相关治疗方法层次聚类树状图')
plt.xlabel('样本编号')
plt.ylabel('距离')
plt.savefig('治疗方法.png', dpi=800)
plt.close()

plt.figure(figsize=(25, 6))
dendrogram(prescription_linked, labels=prescription_labels)
plt.title('真菌性皮肤病相关药方层次聚类树状图')
plt.xlabel('样本编号')
plt.ylabel('距离')
plt.tight_layout()  # 调整布局以适应文本
plt.savefig('药方.png', dpi=600)
plt.close()