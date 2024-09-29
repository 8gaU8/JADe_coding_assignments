import pickle
from datetime import datetime

from task1 import TIME_STAMPS, get_transactions
from task2 import apriori


def main():
    tracts, U = get_transactions("plants")
    fi = apriori(tracts, min_supp=3000, zmin=3)
    filename = datetime.now().strftime("normal.pickle")

    with open(filename, "wb") as f:
        pickle.dump(fi, f)
    # show_itemsets(fi)
    return fi


if __name__ == "__main__":
    main()
    print("consumed time of each function")
    for func, (sec, called_nb) in TIME_STAMPS.items():
        print(f"{func}, {sec:3.3f}[sec], {called_nb} times.")
