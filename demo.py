import pandas as pd
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from joblib import Parallel, delayed

# 读取数据
npm_packages_df = pd.read_csv('/OpenSource/npm_data/2024-05-13-16-54-33_EXPORT_CSV_13529018_459_0.csv')
npm_dependencies_df = pd.read_csv('/OpenSource/npm_data/2024-05-13-17-23-22_EXPORT_CSV_13529969_552_0.csv')
print(npm_packages_df.shape)
print(npm_dependencies_df.shape)

# 创建一个有向图
G = nx.DiGraph()

# 添加节点
for idx, row in npm_packages_df.iterrows():
    G.add_node(row['packge_id'],
               name=row['name'],
               version=row['version'],
               description=row['description'],
               repository_type=row['repository_type'],
               repository_url=row['repository_url'],
               license=row['license'],
               homepage=row['homepage'],
               time=row['time'])

print("Add nodes over.")

# 添加边（依赖关系）
i = 0
for idx, row in npm_dependencies_df.iterrows():
    G.add_edge(row['packge_id'], row['dependency_name'])
    if i % 10000 == 0:
        print("i")
        i += 1

print("Add edges over.")

# 可视化依赖网络
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, k=0.1)
nx.draw(G, pos, with_labels=True, node_size=20, font_size=8, edge_color='gray', alpha=0.7)
plt.show()

# 分析网络
degree_centrality = nx.degree_centrality(G)
clustering_coefficient = nx.clustering(G.to_undirected())
average_path_length = nx.average_shortest_path_length(G) if nx.is_weakly_connected(G) else None
diameter = nx.diameter(G) if nx.is_weakly_connected(G) else None

print("Degree Centrality: ", degree_centrality)
print("Clustering Coefficient: ", clustering_coefficient)
print("Average Path Length: ", average_path_length)
print("Diameter: ", diameter)
