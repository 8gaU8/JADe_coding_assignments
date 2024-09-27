from utils import TEST_TRACTS
from task1 import calc_support
from utils import (
    TEST_TRACTS,
    ItemsetsCountsType,
    ItemsetsType,
    TransactionsType,
)


def get_sorted_items(tracts: TransactionsType) -> list:
    """get items from transactions and sort by support counting

    Args:
        tracts (list[frozenset]): transactions

    Returns:
        list: items which sorted by support counting
    """
    # get unique items
    items = []
    for tract in tracts:
        items.extend(list(tract))
    unique_items = set(items)

    # count support
    counts = []
    for item in unique_items:
        sup = calc_support(set(item), tracts)
        counts.append((item, sup))

    # sort with support and get only items
    sorted_items = sorted(counts, key=lambda i_s: -i_s[1])

    def get_0(i_s):
        return i_s[0]

    items = list(map(get_0, sorted_items))
    return items


def convert_items2itemsets(items: list) -> ItemsetsType:
    itemsets = []
    for item in items:
        itemsets.append(set([item]))
    return itemsets


def gen_candidates(
    frequent_itemsets: ItemsetsType,
    items: list,
) -> ItemsetsType:
    """generate candidates from frequent itemsets and unique frequent items

    Args:
        frequent_itemsets (list[set])
        items (list): frequent singleton items

    Returns:
        list[set]: next candidates of frequent itemsets
    """
    candidates = []
    for fi in frequent_itemsets:
        for item in items:
            if item in fi:
                continue
            candidate = fi.copy()
            candidate.add(item)
            if candidate not in candidates:
                candidates.append(candidate)
    return candidates


def prune_candidates(
    candidates: ItemsetsType,
    prev_pruned_itemsets: ItemsetsType,
) -> tuple[ItemsetsType, ItemsetsType]:
    """Prune itemsets that violate downward closure

    Args:
        candidates (list[set]): return of gen_candidates
        prev_pruned_itemsets (list[set]):
            candidate itemsets which pruned or not frequent

    Returns:
        tuple[list[set], list[set]]: survived itemsets, pruned itemsets
    """
    if len(prev_pruned_itemsets) == 0:
        return candidates, []
    not_pruned = []
    pruned = []
    for cand in candidates:
        violate_flag = False
        for prev_pruned in prev_pruned_itemsets:
            if prev_pruned <= cand:
                violate_flag = True
                break
        if violate_flag:
            pruned.append(cand)
        else:
            not_pruned.append(cand)

    return not_pruned, pruned


def extract_itemsets(itemsets_counts: ItemsetsCountsType) -> ItemsetsType:
    def get_0th(s):
        return s[0]

    return list(map(get_0th, itemsets_counts))


def get_frequent_itemsets(
    not_pruned: ItemsetsType, tracts: TransactionsType, min_supp: int
) -> tuple[ItemsetsCountsType, ItemsetsCountsType]:
    """count support of each itemset that survived from pruning

    Args:
        not_pruned (list[set]): return of prune_candidates[0]
        tracts (list[frozenset]): all transactions of dataset
        min_supp (int)

    Returns:
        list[set]: frequent k-th itemsets, and not frequent ones
    """
    frequent_itemsets = []
    non_frequent_itemsets = []
    for itemset in not_pruned:
        supp = calc_support(itemset, tracts)
        if supp >= min_supp:
            frequent_itemsets.append((itemset, supp))
        else:
            non_frequent_itemsets.append((itemset, supp))
    return frequent_itemsets, non_frequent_itemsets


def main():
    items = get_sorted_items(TEST_TRACTS)
    assert items == ["d", "a", "b", "c"]
    print(f"{items = }")

    frequent_itemsets = []

    items = get_sorted_items(TEST_TRACTS)
    itemsets = convert_items2itemsets(items)

    candidates = gen_candidates(itemsets, items)
    candidates, pruned = prune_candidates(candidates, list())
    fi, non_fi = get_frequent_itemsets(candidates, TEST_TRACTS, 2)
    pruned.extend(non_fi)
    frequent_itemsets.extend(fi)

    candidates = gen_candidates(fi, items)
    candidates, pruned = prune_candidates(candidates, pruned)
    fi, non_fi = get_frequent_itemsets(candidates, TEST_TRACTS, 2)
    pruned.extend(non_fi)
    frequent_itemsets.extend(fi)

    candidates = gen_candidates(fi, items)
    candidates, pruned = prune_candidates(candidates, pruned)
    fi, non_fi = get_frequent_itemsets(candidates, TEST_TRACTS, 2)
    pruned.extend(non_fi)
    frequent_itemsets.extend(fi)
    # ! サポート数を出力する
    print(f"{frequent_itemsets = }")


if __name__ == "__main__":
    main()
