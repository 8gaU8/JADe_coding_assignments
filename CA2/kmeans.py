import numpy as np
import matplotlib.pyplot as plt


def calc_dist(p1, p2):
    return ((p1 - p2) ** 2).sum() ** 0.5


def calc_centers(dataset, cluster_ids, centers):
    next_centers = np.zeros_like(centers)
    k = centers.shape[0]
    for c_i in range(k):
        data_id = np.where(cluster_ids == c_i)
        m = dataset[data_id].mean(axis=0)
        next_centers[c_i] = m

    return next_centers


def show(dataset, cluster_ids, centers):
    def show_ds(dataset):
        print("|data points|", end="")
        print("|".join([f"{x:.3f}, {y:.3f}" for x, y in list(dataset)]))

    def show_center(ary):
        mapping = map(lambda s: f"{s:.3f}", ary)
        dist_str = ", ".join(mapping)
        return dist_str

    def show_2f(ary):
        mapping = map(lambda s: f"{s:.3f}", ary)
        dist_str = "| ".join(mapping)
        return dist_str

    for c_id, center in enumerate(centers):
        print(f"- C{c_id}: ({show_center(center)})")

    show_ds(dataset)
    for c_id, center in enumerate(centers):
        dists = [calc_dist(p1, center) for p1 in dataset]
        print(f"|distance to C{c_id}|" + show_2f(dists) + "|")

    print("|cluster|", end="")
    if cluster_ids[0] == -1:
        print("|".join(list(map(lambda s: f"not assigned", cluster_ids))) + "|")
    else:
        print("|".join(list(map(lambda s: f"C{s}", cluster_ids))) + "|")


def plot(dataset, cluster_ids, centers):
    plt.figure()
    for c_i, center in enumerate(centers):
        data_ids = np.where(cluster_ids == c_i)
        data = dataset[data_ids]
        x, y = list(data.T)
        plt.scatter(x, y, label=c_i, marker=".")
        x, y = list(center)
        plt.scatter([x], [y], label=f"center of {c_i}", marker="+")

    plt.legend()
    plt.show()
    return data


def assign_cluster(dataset: np.ndarray, centers: np.ndarray) -> np.ndarray:
    k = centers.shape[0]
    dists = np.zeros((dataset.shape[0], k))
    for idx, center in enumerate(centers):
        diff2: np.ndarray = (dataset - center) ** 2
        dist = diff2.sum(axis=1) ** 0.5
        dists[..., idx] = dist

    cluster_ids = dists.argmin(axis=1)
    return cluster_ids


def kmeans(initial_centers, dataset, MAXITER):
    centers = initial_centers
    cluster_ids = (
        np.ones_like(
            assign_cluster(dataset, initial_centers),
        )
        * -1
    )
    step = 0
    while True:
        step += 1
        # plot(dataset, cluster_ids, centers)
        # show(dataset, cluster_ids, centers)

        prev_cluster_ids = cluster_ids.copy()

        cluster_ids = assign_cluster(dataset, centers)
        centers = calc_centers(dataset, cluster_ids, centers)

        if (prev_cluster_ids == cluster_ids).all():
            break
        if step > MAXITER:
            raise TimeoutError(f"Max iter is {MAXITER}")
    return centers, cluster_ids


def main():
    dataset = np.array(
        [
            [0.282, 0.562],
            [0.295, 0.593],
            [0.323, 0.467],
            [0.377, 0.655],
            [0.418, 0.626],
            [0.106, 0.539],
            [0.119, 0.426],
            [0.198, 0.301],
            [0.196, 0.503],
            [0.331, 0.586],
            [0.053, 0.820],
            [0.099, 0.874],
            [0.119, 0.884],
            [0.113, 0.793],
            [0.137, 0.866],
            [0.165, 0.850],
        ]
    )

    initial_centers = np.array(
        [
            [0.230, 0.560],
            [0.150, 0.740],
            [0.120, 0.860],
        ]
    )
    centers, cluster_ids = kmeans(initial_centers, dataset)
    plot(dataset, cluster_ids, centers)
    print(centers)
    print(cluster_ids)


if __name__ == "__main__":

    main()
