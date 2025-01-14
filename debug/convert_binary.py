# the version of msgpack is 1.1.0 and msgpack-numpy is 0.4.8
import msgpack
import msgpack_numpy as m
import numpy as np


def convert_and_restore_bin():
    arr = np.random.rand(80, 4).astype("float32")

    # convert a numpy array to bytes for storage in mysql table
    bytes = msgpack.packb(arr, default=m.encode)

    # restore the numpy array from bytes
    restored = msgpack.unpackb(bytes, object_hook=m.decode)

    # print true
    print(arr == restored)


def empty_epochs(num_epochs: int, dimension: int) -> np.ndarray:
    return np.array([[-1.0] * dimension] * num_epochs)


arr0 = np.random.rand(50, 4).astype("float32")
arr1 = arr0.tolist() + empty_epochs(30, 4).tolist()

arr2 = np.random.rand(80, 4).astype("float32")
arr3 = arr2.tolist() + empty_epochs(0, 4).tolist()

for elem2, elem3 in zip(arr2, arr3):
    print(elem2 == elem3)
