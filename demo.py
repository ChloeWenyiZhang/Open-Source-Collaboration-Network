import pandas as pd
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from joblib import Parallel, delayed

# 读取数据
npm_packages_df = pd.read_csv('/OpenSource/npm_data/2024-05-13-16-54-33_EXPORT_CSV_13529018_459_0.csv')
npm_dependencies_df = pd.read_csv('/OpenSource/npm_data/2024-05-13-17-23-22_EXPORT_CSV_13529969_552_0.csv')

# 创建有向图
G = nx.DiGraph()

# 添加节点
def add_node(G, row):
    G.add_node(row['package_id'],
               name=row['name'],
               version=row['version'],
               description=row['description'],
               repository_type=row['repository_type'],
               repository_url=row['repository_url'],
               license=row['license'],
               homepage=row['homepage'],
               time=row['time'])

Parallel(n_jobs=-1)(delayed(add_node)(G, row) for idx, row in npm_packages_df.iterrows())

# 添加边（依赖关系）
def add_edge(G, row):
    G.add_edge(row['package_id'], row['dependency_name'])

Parallel(n_jobs=8)(delayed(add_edge)(G, row) for idx, row in npm_dependencies_df.iterrows())

# 可视化依赖网络
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, k=0.1)
nx.draw(G, pos, with_labels=True, node_size=20, font_size=8, edge_color='gray', alpha=0.7)
plt.savefig('./network_graph.png')
plt.close()

# 分析网络
def analyze_network(G):
    degree_centrality = nx.degree_centrality(G)
    clustering_coefficient = nx.clustering(G.to_undirected())
    average_path_length = nx.average_shortest_path_length(G) if nx.is_weakly_connected(G) else None
    diameter = nx.diameter(G) if nx.is_weakly_connected(G) else None
    return degree_centrality, clustering_coefficient, average_path_length, diameter

degree_centrality, clustering_coefficient, average_path_length, diameter = analyze_network(G)

print("Degree Centrality: ", degree_centrality)
print("Clustering Coefficient: ", clustering_coefficient)
print("Average Path Length: ", average_path_length)
print("Diameter: ", diameter)
