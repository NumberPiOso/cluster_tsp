from sklearn.cluster import KMeans


def group_points_kmeans(points, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(points)
    labels = kmeans.labels_
    num_clusters = labels.max() + 1
    return [points[labels == i] for i in range(num_clusters)]
