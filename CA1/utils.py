from fim_resources import DATASETS, load_data_txt, load_matrix, load_trans_txt


def get_transactions(dataset: str) -> tuple[list, list]:
    # transported from fim_resources:main
    FUNC_MAP = {
        "data_txt": load_data_txt,
        "matrix": load_matrix,
        "tans_txt": load_trans_txt,
    }
    if DATASETS.get(dataset, None) is None:
        raise ValueError(f"no such dataset {dataset}")

    file_path = DATASETS[dataset]["in_file"]
    func_label = DATASETS[dataset]["format"]
    load_method = FUNC_MAP[func_label]
    params = DATASETS[dataset].get("params", {})  # type: ignore
    tracts, U = load_method(file_path, **params)  # type: ignore
    return tracts, U


# small transactions from ex1,2,3
TEST_TRACTS = [
    frozenset(["c", "d"]),
    frozenset(["a"]),
    frozenset(["a", "b", "d"]),
    frozenset(["b", "d"]),
    frozenset(["a", "b", "c", "d"]),
    frozenset(["a", "d"]),
]

# typings
ItemsetsCountsType = list[tuple[set, int]]
ItemsetsType = list[set]
TransactionsType = list[frozenset]
