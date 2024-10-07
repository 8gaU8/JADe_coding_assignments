import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.manifold import TSNE

from agglomerative import get_cluster
from clustering_resources import (
    RandomNumGen,
    load_csv,
    normalize_dataset,
    sample_domain,
)
from kmeans import kmeans

MAXITER = 1000


def divide_data(dataset):

    while True:
        try:
            centers = sample_domain(k=2, dataset=dataset)
            centers, cluster_ids = kmeans(centers, dataset, MAXITER)
        except TimeoutError:
            continue
        break
    partial_0 = dataset[np.where(cluster_ids == 0)[0]]
    partial_1 = dataset[np.where(cluster_ids == 1)[0]]
    return partial_0, partial_1


def bisect_step(dataset, d_map, history):
    clusters = []
    if len(dataset) == 1:
        data_id = d_map[tuple(dataset[0])]
        return tuple([data_id])
    p0, p1 = divide_data(dataset)
    c0 = bisect_step(p0, d_map, history)
    c1 = bisect_step(p1, d_map, history)
    clusters.append(c0)
    clusters.append(c1)
    history.append(tuple(clusters))
    return tuple(clusters)


def bisect_kmeans(dataset, k):
    history = []
    dataset_map = {tuple(d): i for i, d in enumerate(dataset)}
    bisect_step(dataset, dataset_map, history)
    clusters = get_cluster(history, k=k)
    return clusters


def plot(clusters, dataset, k):
    indeces = np.zeros(len(dataset), dtype=object)
    for idx, c in enumerate(clusters):
        c = np.array(list(c))
        c -= 1
        indeces[c] = f"C{idx} (n={len(c)})"

    tsne = TSNE(n_components=2, random_state=42)
    result = tsne.fit_transform(dataset)
    plt.figure()  # figsize=(10, 10))
    sns.scatterplot(
        x=result[:, 0],
        y=result[:, 1],
        hue=indeces,
        palette=sns.color_palette("hsv", k),
    )
    plt.show()


def main():

    SEED = 0
    RandomNumGen.set_seed(SEED)
    data_params = {"filename": "Dry_Bean_Dataset_small.csv", "last_column_str": True}
    dataset, head, classes = load_csv(**data_params)

    k = 10
    Dn = normalize_dataset(dataset[:, :-1])
    clusters = bisect_kmeans(Dn, k)
    plot(clusters, Dn, k)


if __name__ == "__main__":

    main()
