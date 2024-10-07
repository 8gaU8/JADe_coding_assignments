import numpy as np

from CA1.CA1_task1 import TIME_STAMPS, get_transactions, log_ts


@log_ts
def get_unique_items(tracts: list[frozenset]) -> set:
    unique_items = set()
    for tract in tracts:
        unique_items |= tract
    return unique_items


@log_ts
def mk_onehot(tract: frozenset | list, item_map: dict) -> np.ndarray:
    a = np.array([item_map[item] for item in tract])
    one_hot = np.zeros(len(item_map.keys()), dtype=np.int8)
    one_hot[a] = 1
    return one_hot


@log_ts
def get_tracts_mat(tracts: list[frozenset], item_map: dict) -> np.ndarray:
    tracts_mat = np.array(
        [mk_onehot(tract, item_map) for tract in tracts], dtype=np.int8
    )
    return tracts_mat


@log_ts
def calc_support(itemset: np.ndarray, tracts_mat: np.ndarray):
    idx = np.where(itemset == 1)[0]
    item_row = tracts_mat[..., idx]
    item_num = item_row.sum(axis=1)
    return (item_num == idx.shape).sum()


@log_ts
def get_frequent_itemsets(
    itemsets: np.ndarray,
    tracts_mat: np.ndarray,
    min_supp: int,
):
    frequent_itemsets = []
    freq_supp = []
    non_frequent_itemsets = []
    non_freq_supp = []
    for itemset in itemsets:
        supp = calc_support(itemset, tracts_mat)
        if supp >= min_supp:
            frequent_itemsets.append(itemset)
            freq_supp.append(supp)
        else:
            non_frequent_itemsets.append(itemset)
            non_freq_supp.append(supp)
    return (
        (frequent_itemsets, freq_supp),
        (non_frequent_itemsets, non_freq_supp),
    )


@log_ts
def gen_candidates(
    frequent_itemsets: list[np.ndarray], items_ary: np.ndarray
) -> np.ndarray:
    freqs = np.array(frequent_itemsets)
    k = freqs.sum(axis=1).max()
    reps = items_ary.shape[0]
    candiates = np.tile(freqs, reps=(reps, 1))
    reps = freqs.shape[0]
    buddy = items_ary.repeat(reps, axis=0)

    candiates += buddy
    candiates = (candiates > 0).astype(np.int8)
    candiates = np.unique(candiates, axis=0)
    candiates = candiates[candiates.sum(axis=1) > k]
    return candiates


@log_ts
def prune_candidates(
    candidates: np.ndarray,
    pruned: list[np.ndarray],
) -> tuple[np.ndarray, list[np.ndarray]]:

    if len(pruned) == 0:
        return candidates, []

    k = pruned[0].sum()
    prune_indexes = []
    all_index = set(range(candidates.shape[0]))
    for p in pruned:
        prune_index = np.where(((candidates + p) >= k).sum(axis=1) >= k)[0]
        prune_indexes.extend(prune_index)
    prune_indexes = set(prune_indexes)
    cand_indexes = all_index.difference(prune_indexes)
    next_candidates = candidates[list(cand_indexes)]
    next_pruned = candidates[list(prune_indexes)]
    return next_candidates, list(next_pruned)


class SupportCalculator:
    def __init__(self) -> None:
        self.set = False

    @log_ts
    def set_tracts(self, tracts: list[frozenset]) -> None:
        if self.set:
            return
        items = get_unique_items(tracts)
        self.item_map = {e: i for i, e in enumerate(items)}
        tracts_mat = np.array(
            [mk_onehot(tract, self.item_map) for tract in tracts],
            dtype=np.int8,
        )
        self.tracts_mat = tracts_mat
        self.set = True

    @log_ts
    def calc_support_np(self, itemset: frozenset) -> int:
        onehot = mk_onehot(itemset, self.item_map)
        idx = np.where(onehot == 1)[0]
        item_row = self.tracts_mat[..., idx]
        item_num = item_row.sum(axis=1)
        return (item_num == idx.shape).sum()


calc = SupportCalculator()


@log_ts
def main():

    tracts, U = get_transactions("house")
    min_supp = len(tracts) * 0.07

    items = get_unique_items(tracts)
    item_map = {e: i for i, e in enumerate(items)}
    tracts_mat = get_tracts_mat(tracts, item_map)

    frequent_itemsets = []
    frequent_supp = []
    pruned = []

    items_ary = np.array([mk_onehot([item], item_map) for item in items])

    # itemsets = np.array([mk_onehot([item]) for item in items])
    freq, non_freq = get_frequent_itemsets(items_ary, tracts_mat, min_supp)

    frequent_itemsets.extend(freq[0])
    frequent_supp.extend(freq[1])
    pruned.extend(non_freq[0])
    print(len(frequent_itemsets))

    pruned = []
    while len(freq[0]) != 0:
        candidates = gen_candidates(freq[0], items_ary)
        candidates, pruned = prune_candidates(candidates, pruned)

        freq, non_freq = get_frequent_itemsets(
            candidates,
            tracts_mat,
            min_supp,
        )
        if len(freq[0]) == 0:
            break

        frequent_itemsets.extend(freq[0])
        frequent_supp.extend(freq[1])
        pruned.extend(non_freq[0])
        print(len(frequent_itemsets))
    import pickle

    filename = "np-data.pickle"
    with open(filename, "wb") as f:
        pickle.dump(frequent_itemsets, f)
    filename = "np-supp.pickle"
    with open(filename, "wb") as f:
        pickle.dump(frequent_supp, f)


if __name__ == "__main__":
    from pprint import pprint as print

    print(TIME_STAMPS)
    main()
    print(TIME_STAMPS)
