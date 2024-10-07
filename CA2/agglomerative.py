import numpy as np


def merge_upd(c1: int, c2: int, cluster_ids: list[tuple]):
    next_cluster_ids = cluster_ids.copy()
    c1_id = next_cluster_ids[c1]
    c2_id = next_cluster_ids[c2]
    next_cluster_ids.append((c1_id, c2_id))
    next_cluster_ids.remove(c1_id)
    next_cluster_ids.remove(c2_id)

    return next_cluster_ids


def show_dist_mat(dist_mat: np.ndarray):
    print()
    dm_show = dist_mat.copy()
    dm_show[dm_show == np.inf] = 0
    # header1 = "|" * (dm_show.shape[0] + 2)
    idlist = range(1, dm_show.shape[0] + 1)
    idlist = map(str, idlist)
    header1 = "|".join(idlist)
    header1 = "||" + header1 + "|"

    print(header1)
    header2 = "|:-:" * (dm_show.shape[0] + 1) + "|"
    print(header2)
    for idx, line in enumerate(dm_show):
        line_txt = "|".join([f"{e:.3f}" for e in line])
        line_txt = f"|{idx+1}|" + line_txt + "|"
        print(line_txt)
    print()


def get_min_idx(dist_mat: np.ndarray) -> tuple:
    min_dist = np.min(dist_mat)
    i, j = np.unravel_index(np.argmin(dist_mat), dist_mat.shape)
    return (i, j), min_dist


def complete_linkage(mat):
    return mat.max(axis=1)


def single_linkage(mat):
    return mat.max(axis=1)


def step(dist_mat, cluster_ids, linkage_fn):
    # update cluster_ids
    (c1, c2), min_dist = get_min_idx(dist_mat)
    next_cluster_ids = merge_upd(c1, c2, cluster_ids)

    # calculate lincage
    next_idx_list = set(range(len(dist_mat))) - set([c1, c2])
    next_idx_list = list(next_idx_list)
    dist_merged = linkage_fn(dist_mat[[[c1, c2]]][..., next_idx_list])

    # create new distance matrix
    partial_dist_mat = dist_mat[next_idx_list][..., next_idx_list]
    right_line = np.append(dist_merged, np.inf)[None].T
    next_dist_mat = np.vstack([partial_dist_mat, dist_merged])
    next_dist_mat = np.hstack([next_dist_mat, right_line])
    c1_id = cluster_ids[c1]
    c2_id = cluster_ids[c2]
    return ((c1_id, c2_id), min_dist), next_dist_mat, next_cluster_ids


def cvt_c2t(c1_id):
    ctxt = str(c1_id)
    ctxt = ctxt.replace("(", "{")
    ctxt = ctxt.replace(",)", "}")
    ctxt = ctxt.replace(")", "}")
    return ctxt


def flatten_cluster(c: tuple):
    c_txt = str(c)
    c_txt = c_txt.replace("),", "")
    c_txt = c_txt.replace(")", "")
    c_txt = c_txt.replace("(", "")
    c_txt = c_txt.replace(" ", "").strip()
    return set(map(int, (c_txt.split(",")[:-1])))


def agglomerative(dist_mat: np.ndarray, show=False, linkage="complete"):
    merge_hist = []
    dist_mat = dist_mat.copy()
    dist_mat[dist_mat == 0] = np.inf
    cluster_ids = [tuple([i + 1]) for i in range(len(dist_mat))]
    if show:
        print("## initial step")
        print("- Distance matrix")
        show_dist_mat(dist_mat)

    if linkage == "complete":
        linkage_fn = complete_linkage
    elif linkage == "single":
        linkage_fn = single_linkage
    else:
        raise NotImplementedError(
            f"linkage function {linkage} is" " not implemented yet."
        )

    step_num = 0
    while len(cluster_ids) != 1:
        step_num += 1
        ((c1, c2), min_dist), dist_mat, cluster_ids = step(
            dist_mat, cluster_ids, linkage_fn
        )
        merge_hist.append((c1, c2))
        if show:
            print(f"## step{step_num}")
            print("- Merged clusters:", cvt_c2t(c1), "&", cvt_c2t(c2))
            print("- Distance between merged clusters:", min_dist)
    return cluster_ids, merge_hist


def get_cluster(merge_hist: list[tuple], k=3):
    clusters = []
    for hist in merge_hist[::-1]:
        c1, c2 = hist
        c1 = flatten_cluster(c1)
        c2 = flatten_cluster(c2)
        clusters.append(c1)
        clusters.append(c2)
        for cluster in clusters:
            if c1 < cluster or c2 < cluster:
                clusters.remove(cluster)
        if len(clusters) >= k:
            break
    return clusters


def get_dist_mat(dataset: np.ndarray):
    mM = dataset.shape[0]
    dist_mat = np.zeros((mM, mM))
    for i in range(mM):
        for j in range(mM):
            subd = dataset[i] - dataset[j]
            dist2 = (subd**2).sum()
            dist = dist2**0.5
            dist_mat[i, j] = dist
    return dist_mat


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
    from scipy.spatial import distance

    org_dist_mat = distance.cdist(dataset, dataset, metric="euclidean")
    dist_mat = org_dist_mat.copy()
    cluster_ids, merge_hist = agglomerative(dist_mat, show=False)

    print(get_cluster(merge_hist, 3))


if __name__ == "__main__":
    main()
