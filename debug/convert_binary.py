# the version of msgpack is 1.1.0 and msgpack-numpy is 0.4.8
import msgpack
import msgpack_numpy as m
import numpy as np

arr = np.random.rand(80, 4).astype("float32")

# convert a numpy array to bytes for storage in mysql table
bytes = msgpack.packb(arr, default=m.encode)

# restore the numpy array from bytes
restored = msgpack.unpackb(bytes, object_hook=m.decode)

# print true
print(arr == restored)
