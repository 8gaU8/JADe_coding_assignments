from utils import TEST_TRACTS, log_ts


@log_ts
def calc_support(itemset: "frozenset", tracts: "list[frozenset]") -> int:
    support = 0

    for tract in tracts:
        if itemset.issubset(tract):
            support += 1
    return support


def main():
    itemset = "abd"
    itemset = frozenset(list(itemset))
    support = calc_support(itemset, TEST_TRACTS)
    assert support == 2
    print(f"{support = }")


if __name__ == "__main__":
    main()
