from task1 import (
    ItemsetsCountsType,
    ItemsetsType,
    TransactionsType,
    calc_support,
    get_transactions,
    log_ts,
)


@log_ts
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
        sup = calc_support(frozenset([item]), tracts)
        counts.append((item, sup))

    # sort with support and get only items
    sorted_items = sorted(counts, key=lambda i_s: -i_s[1])

    def get_0(i_s):
        return i_s[0]

    items = list(map(get_0, sorted_items))
    return items


@log_ts
def convert_items2itemsets(items: list) -> ItemsetsType:
    itemsets = []
    for item in items:
        itemsets.append(set([item]))
    return itemsets


@log_ts
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
    candidates = set()
    for fi in frequent_itemsets:
        for item in items:
            if item in fi:
                continue
            c = list(fi)
            c.append(item)
            candidate_t = tuple(sorted(c))
            if candidate_t not in set(candidates):
                candidates.add(candidate_t)
    candidates = list(map(frozenset, candidates))
    return candidates


@log_ts
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
            if prev_pruned.issubset(cand):
                violate_flag = True
                break
        if violate_flag:
            pruned.append(cand)
        else:
            not_pruned.append(cand)

    return not_pruned, pruned


@log_ts
def extract_itemsets(itemsets_counts: ItemsetsCountsType) -> ItemsetsType:
    return list(map(lambda s: s[0], itemsets_counts))


@log_ts
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


@log_ts
def apriori(tracts: TransactionsType, min_supp: float) -> ItemsetsCountsType:
    if min_supp >= 0 and min_supp < 1:
        min_supp_int = int(min_supp * len(tracts))
    else:
        min_supp_int = int(min_supp)

    step = 0
    print(f"#{step = }")
    frequent_itemsets: ItemsetsCountsType = []
    items = get_sorted_items(tracts)
    itemsets = convert_items2itemsets(items)
    fi, non_fi = get_frequent_itemsets(itemsets, tracts, min_supp_int)
    frequent_itemsets.extend(fi)
    pruned = []

    while len(fi) != 0:
        step += 1
        print(f"#{step = }")
        candidates = gen_candidates(extract_itemsets(fi), items)
        candidates, pruned = prune_candidates(candidates, pruned)
        fi, non_fi = get_frequent_itemsets(candidates, tracts, min_supp_int)
        pruned.extend(extract_itemsets(non_fi))
        frequent_itemsets.extend(fi)

    return frequent_itemsets


def show_itemsets(itemsets_counts: ItemsetsCountsType) -> None:
    sorted_item = []
    for fi, count in itemsets_counts:
        if len(fi) == 1:
            sorted_item.append((list(fi)[0], count))
    count_map = dict(sorted_item)
    for fi, count in itemsets_counts:
        fi = sorted(list(fi), key=lambda s: -count_map[s])
        print(f"itemsets = {fi}, supp = {count}")


def main():
    tracts, U = get_transactions("pizzas")
    frequent_itemsets = apriori(tracts, 2)
    show_itemsets(frequent_itemsets)
    return frequent_itemsets


if __name__ == "__main__":
    main()
