from datetime import datetime

from fim_resources import DATASETS, load_data_txt, load_matrix, load_trans_txt

TIME_STAMPS = dict()


def log_ts(func):
    """utility decorator to log runtime

    Args:
        func : function to run
    """

    def wrapper(*args, **kargs):
        start = datetime.now()
        ret = func(*args, **kargs)
        erapsed_time = (datetime.now() - start).total_seconds()

        fn_name = func.__name__
        t, called = TIME_STAMPS.get(fn_name, (0, 0))
        TIME_STAMPS[fn_name] = (t + erapsed_time, called + 1)

        if erapsed_time > 0.1:
            print(f" {fn_name}:\t {erapsed_time:.4f}sec")
        return ret

    return wrapper


# typings
ItemsetsCountsType = list[tuple[frozenset, int]]
ItemsetsType = list[frozenset]
TransactionsType = list[frozenset]


@log_ts
def get_transactions(dataset: str) -> tuple[TransactionsType, list]:
    FUNC_MAP = {
        "data_txt": load_data_txt,
        "matrix": load_matrix,
        "trans_txt": load_trans_txt,
    }
    if DATASETS.get(dataset, None) is None:
        raise ValueError(f"no such dataset {dataset}")

    file_path = DATASETS[dataset]["in_file"]
    func_label = DATASETS[dataset]["format"]
    load_method = FUNC_MAP[func_label]
    params = DATASETS[dataset].get("params", {})  # type: ignore
    tracts, U = load_method(file_path, **params)  # type: ignore
    return tracts, U


@log_ts
def calc_support(itemset: "frozenset", tracts: "TransactionsType") -> int:
    """calculate absolute support

    Args:
        itemset (frozenset)
        tracts (TransactionsType): list of transactions

    Returns:
        int: abs support
    """
    support = 0

    for tract in tracts:
        if itemset.issubset(tract):
            support += 1
    return support


def main():
    tracts, U = get_transactions("plants")
    itemset = ("ri", "va", "ma", "ny")
    itemset = frozenset([U.index(item) for item in itemset])
    support = calc_support(itemset, tracts)
    assert support == 2783
    print(f"{support = }")


if __name__ == "__main__":
    main()
