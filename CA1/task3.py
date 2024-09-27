import pickle
from datetime import datetime

from task2 import apriori
from utils import get_transactions, TIME_STAMPS


def main():
    fast = True
    tracts, U = get_transactions("plants")
    # tracts = TEST_TRACTS
    fi = apriori(tracts, 3000)
    if fast:
        filename = datetime.now().strftime("fast.pickle")
    else:
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
