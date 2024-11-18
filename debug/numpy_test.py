import numpy as np


def main():
    arr0 = np.random.rand(2, 20, 1201)
    arr1 = np.zeros((20, 1201))
    arr2 = np.tile(arr1, (8, 1, 1))

    arr3 = np.concatenate((arr0, arr2), axis=0)

    list0 = [0, 1, 2, 3]
    list1 = None
    list2 = []

    test0 = str(list0)
    test1 = list0.__str__()

    test2 = str(list0) if list0 is not None else None
    test3 = str(list0) if list0 else None

    test4 = str(list1) if list1 is not None else None
    test5 = str(list1) if list1 else None

    test6 = str(list2) if list2 is not None else None
    test7 = str(list2) if list2 else None

    print(arr3)
    print(arr0)


main()
