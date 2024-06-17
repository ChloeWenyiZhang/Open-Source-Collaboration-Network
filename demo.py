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

# 构建一个包id到名称的映射字典
package_id_to_name = pd.Series(npm_packages_df.name.values, index=npm_packages_df.package_id).to_dict()

# 创建一个有向图
G = nx.DiGraph()

for package_id, package_name in package_id_to_name.items():
    G.add_node(package_name)

# 添加边（依赖关系）
for index, row in npm_dependencies_df.iterrows():
    package_id = row['package_id']
    dependency_name = row['dependency_name']

    if package_id in package_id_to_name.keys():
        package_name = package_id_to_name[package_id]
        if dependency_name in package_id_to_name.values():
            G.add_edge(package_name, dependency_name)

print("Add edges over.")

# # 可视化依赖网络
# plt.figure(figsize=(12, 12))
# pos = nx.spring_layout(G, k=0.1)
# nx.draw(G, pos, with_labels=True, node_size=1, font_size=8, node_color='lightblue', edge_color='gray', arrows=True, alpha=0.8)
# plt.title('npm Dependency Network')
# plt.savefig('./network.png')
# plt.close()

# 分析网络
degree_centrality = nx.degree_centrality(G)
clustering_coefficient = nx.clustering(G.to_undirected())
average_path_length = nx.average_shortest_path_length(G) if nx.is_weakly_connected(G) else None
diameter = nx.diameter(G) if nx.is_weakly_connected(G) else None

print("Degree Centrality: ", degree_centrality)
print("Clustering Coefficient: ", clustering_coefficient)
print("Average Path Length: ", average_path_length)
print("Diameter: ", diameter)
