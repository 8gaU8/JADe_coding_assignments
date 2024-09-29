from task1 import (
    ItemsetsCountsType,
    get_transactions,
    calc_support,
    TransactionsType,
    TIME_STAMPS,
    log_ts,
)
from task2 import apriori


@log_ts
def get_confidence(
    itemset_a: frozenset,
    itemset_b: frozenset,
    itemsets_dict: dict[frozenset, int],
    tracts: TransactionsType,
) -> float:
    supp_a = itemsets_dict[itemset_a]

    itemset_ab = itemset_a | itemset_b
    supp_ab = itemsets_dict.get(itemset_ab, None)
    if supp_ab is None:
        supp_ab = calc_support(itemset_ab, tracts)
        itemsets_dict[itemset_ab] = supp_ab
    conf = supp_ab / supp_a

    return conf


@log_ts
def assoc_rules(
    itemsets_counts: ItemsetsCountsType,
    tracts: TransactionsType,
    min_conf: float,
):
    confs = []
    itemsets_dict = dict(itemsets_counts)
    itemsets = list(itemsets_dict.keys())

    for itemset_a in itemsets:
        for itemset_b in itemsets:
            if itemset_b <= itemset_a:
                continue
            conf = get_confidence(
                itemset_a,
                itemset_b,
                itemsets_dict,
                tracts,
            )
            if conf > min_conf:
                confs.append((itemset_a, itemset_b, conf))
    return confs


@log_ts
def main():
    tracts, U = get_transactions("plants")
    min_supp = 4000
    itemsets_counts = apriori(tracts, min_supp)
    min_conf = 0.5
    confs = assoc_rules(itemsets_counts, tracts, min_conf)
    print(
        f"{len(confs)} association rules are found",
        f"({min_supp=}, {min_conf=})",
        f"in {TIME_STAMPS['assoc_rules'][0]} sec."
    )


if __name__ == "__main__":
    main()
    print("consumed time of each function")
    for func, (sec, called_nb) in TIME_STAMPS.items():
        print(f"{func}, {sec:3.3f}[sec], {called_nb} times.")
