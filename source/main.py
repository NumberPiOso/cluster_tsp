import pandas as pd
import tsp
import plot
import cluster
import matplotlib.pyplot as plt

data = pd.read_csv("../data/tsp.csv")
all_points = data.iloc[:100, :2].values

points_clusters = cluster.group_points_kmeans(all_points, n_clusters=3)
dists_matrix_clusters = [tsp.calc_dist_matrix(c_points) for c_points in points_clusters]
sols_clusters = [
    tsp.opt_tsp_model(dist_matrix) for dist_matrix in dists_matrix_clusters
]
colors = ["b", "g", "y", "p"]
for c_points, c_sol, c_color in zip(points_clusters, sols_clusters, colors):
    plot.plot_solution(c_points, c_sol, c_color)
plt.show()
