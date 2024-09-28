import pickle
from datetime import datetime

from task2 import apriori
from utils import TEST_TRACTS, get_transactions, TIME_STAMPS


def main():
    tracts, U = get_transactions("plants")
    fi = apriori(tracts, min_supp=3000  )
    filename = datetime.now().strftime("normal.pickle")

    with open(filename, "wb") as f:
        pickle.dump(fi, f)
    # show_itemsets(fi)
    return fi


if __name__ == "__main__":
    from pprint import pprint as print

    print(TIME_STAMPS)
    main()
    print(TIME_STAMPS)
